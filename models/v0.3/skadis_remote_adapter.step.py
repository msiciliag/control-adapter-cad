"""SKADIS adapter plate for an existing ceiling-fan/light remote holder. v0.3

Stack:  remote holder -> its 2 existing screw holes -> THIS plate -> SKADIS board

Changes from v0.2
    - The bottom pair of hooks is replaced by two lock windows. After hanging
      the plate on the top hooks you push a lock plug through each window into
      the lower slot; the plug fills the slot, so the plate can no longer be
      lifted the 4.2 mm that unhooks it. See skadis_params for why an anti-lift
      feature cannot be part of a rigid hook.
    - A groove in the front face carries each plug's tail down past the plate's
      bottom edge, so the plugs are fitted and pulled by hand.

Print orientation: front face (Z = -PLATE_T) flat on the bed, hooks pointing up.
No supports: the hooks are vertical, a 45 deg ramp and a 1.2 mm ear, and both
the windows and the groove are vertical-walled cuts.
"""

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Cylinder,
    Locations,
    Mode,
    Plane,
    Polygon,
    Pos,
    SlotOverall,
    add,
    extrude,
    fillet,
)

from skadis_params import (
    FEATURE_X,
    GROOVE_DEPTH,
    GROOVE_TOP_Y,
    HOLDER_HEIGHT,
    HOLDER_HOLE_SPACING,
    HOLDER_WIDTH,
    HOOK_CATCH,
    HOOK_HEIGHT,
    HOOK_LIP,
    HOOK_ROOT_FILLET,
    HOOK_SHANK_LEN,
    HOOK_UNLOCK_LIFT,
    HOOK_WIDTH,
    ROOT_RELIEF_DEPTH,
    ROOT_RELIEF_MARGIN,
    HOOK_Y,
    LOCK_LIFT_ALLOWANCE,
    LOCK_SLOT_CENTRE_Y,
    PLATE_CORNER_R,
    PLATE_H,
    PLATE_T,
    PLATE_W,
    SCREW_PILOT_DEPTH,
    SCREW_PILOT_DIAMETER,
    SKADIS_BOARD_THICKNESS,
    SKADIS_SLOT_HEIGHT,
    SKADIS_SLOT_WIDTH,
    WINDOW_H,
    WINDOW_W,
    hook_profile_points,
)

OVERSHOOT = 1.0   # push cutting tools past the faces they enter and exit


def gen_step():
    with BuildPart() as adapter:
        # 1. base plate, rear face on Z = 0
        Box(PLATE_W, PLATE_H, PLATE_T,
            align=(Align.CENTER, Align.CENTER, Align.MAX))
        fillet(adapter.edges().filter_by(Axis.Z), PLATE_CORNER_R)

        # 2. relief pockets in the rear face, so the root fillets sit below the
        #    plane that touches the board instead of propping the plate off it
        for sx in (-1.0, 1.0):
            with BuildPart(
                Pos(sx * FEATURE_X, HOOK_Y, 0), mode=Mode.SUBTRACT,
            ) as relief:
                Box(HOOK_WIDTH + 2 * ROOT_RELIEF_MARGIN,
                    HOOK_HEIGHT + 2 * ROOT_RELIEF_MARGIN,
                    ROOT_RELIEF_DEPTH,
                    align=(Align.CENTER, Align.CENTER, Align.MAX))
            add(relief.part, mode=Mode.SUBTRACT)

        # 3. two SKADIS hooks in the top row, sketched in YZ and extruded along X
        for sx in (-1.0, 1.0):
            hook_plane = Plane.YZ.offset(sx * (FEATURE_X - HOOK_WIDTH / 2.0))
            with BuildSketch(hook_plane) as sk:
                # Plane.YZ local axes: local x -> world Y, local y -> world Z
                Polygon(*[(y + HOOK_Y, z) for z, y in hook_profile_points()],
                        align=None)
            extrude(sk.sketch, amount=sx * HOOK_WIDTH)

        # 4. fillet the hook roots, down on the pocket floor
        roots = [
            e for e in adapter.edges()
            if abs(e.center().Z + ROOT_RELIEF_DEPTH) < 1e-6
            and abs(abs(e.center().X) - FEATURE_X) < HOOK_WIDTH / 2.0 + 0.1
            and abs(e.center().Y - HOOK_Y) < HOOK_HEIGHT / 2.0 + 0.1
        ]
        assert len(roots) == 8, f"expected 8 hook root edges, found {len(roots)}"
        fillet(roots, HOOK_ROOT_FILLET)

        # 5. lock windows: obround like the slot behind them, straight through
        with BuildSketch(Plane.XY.offset(-PLATE_T - OVERSHOOT)) as windows:
            with Locations(*[(sx * FEATURE_X, LOCK_SLOT_CENTRE_Y)
                             for sx in (-1.0, 1.0)]):
                SlotOverall(WINDOW_H, WINDOW_W, rotation=90)
        extrude(windows.sketch, amount=PLATE_T + 2 * OVERSHOOT,
                mode=Mode.SUBTRACT)

        # 6. front-face groove: carries each plug's tail out under the plate
        groove_top = GROOVE_TOP_Y
        groove_bottom = -PLATE_H / 2.0 - OVERSHOOT
        for sx in (-1.0, 1.0):
            with BuildPart(
                Pos(sx * FEATURE_X, (groove_top + groove_bottom) / 2.0, -PLATE_T),
                mode=Mode.SUBTRACT,
            ) as groove:
                Box(WINDOW_W, groove_top - groove_bottom, GROOVE_DEPTH + OVERSHOOT,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
            add(groove.part, mode=Mode.SUBTRACT)

        # 7. blind pilot holes, open at the front (holder) face
        for sign in (1.0, -1.0):
            with BuildPart(
                Pos(0, sign * HOLDER_HOLE_SPACING / 2.0, -PLATE_T),
                mode=Mode.SUBTRACT,
            ) as pilot:
                Cylinder(SCREW_PILOT_DIAMETER / 2.0, SCREW_PILOT_DEPTH,
                         align=(Align.CENTER, Align.CENTER, Align.MIN))
            add(pilot.part, mode=Mode.SUBTRACT)

    part = adapter.part
    part.label = "skadis_remote_holder_adapter_v0_3"
    return part


def _self_check():
    part = gen_step()
    bb = part.bounding_box()
    assert part.is_valid, "invalid solid"
    assert part.volume > 0, "non-positive volume"

    # hidden behind the holder from the front
    assert bb.size.X <= HOLDER_WIDTH + 1e-6, bb.size.X
    assert bb.size.Y <= HOLDER_HEIGHT + 1e-6, bb.size.Y

    expected_depth = PLATE_T + HOOK_SHANK_LEN + HOOK_LIP
    assert abs(bb.size.Z - expected_depth) < 1e-6, (bb.size.Z, expected_depth)
    assert HOOK_SHANK_LEN > SKADIS_BOARD_THICKNESS, "hook does not clear the board"

    # hooks fit a slot and stay inside the plate outline
    assert HOOK_WIDTH < SKADIS_SLOT_WIDTH, HOOK_WIDTH
    assert 2 * FEATURE_X + HOOK_WIDTH <= PLATE_W + 1e-6, "hooks overhang the plate"
    envelope = HOOK_HEIGHT + HOOK_CATCH + HOOK_LIP
    assert SKADIS_SLOT_HEIGHT - envelope > 0.5, f"hook will not enter ({envelope})"

    # the whole point of v0.3: the lock removes the lift that unhooks the plate
    assert LOCK_LIFT_ALLOWANCE < HOOK_CATCH, (
        f"lock leaves {LOCK_LIFT_ALLOWANCE:.2f} mm of lift; must stay under the "
        f"{HOOK_CATCH} mm catch shelf so it never stops bearing "
        f"(and far under the {HOOK_UNLOCK_LIFT} mm that unhooks it)")

    # the lock window really is a hole through the plate, at the lower slot
    window_faces = [
        f for f in part.faces()
        if abs(abs(f.center().X) - FEATURE_X) < WINDOW_W
        and abs(f.center().Y - LOCK_SLOT_CENTRE_Y) < WINDOW_H
    ]
    assert window_faces, "no geometry found at the lock window"
    assert WINDOW_W < SKADIS_SLOT_WIDTH, "window wider than the slot behind it"
    assert WINDOW_H < SKADIS_SLOT_HEIGHT, "window taller than the slot behind it"

    # window and groove must not run into a hook root or a pilot hole
    assert LOCK_SLOT_CENTRE_Y + WINDOW_H / 2.0 < HOOK_Y - HOOK_HEIGHT / 2.0, \
        "lock window overlaps the hook row"
    assert FEATURE_X - WINDOW_W / 2.0 > SCREW_PILOT_DIAMETER / 2.0, \
        "lock window overlaps a pilot hole"
    assert SCREW_PILOT_DEPTH < PLATE_T, "pilot hole breaks through the rear face"

    print(f"ok plate: {bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f} mm, "
          f"{part.volume / 1000:.2f} cm3 | lift with lock fitted "
          f"{LOCK_LIFT_ALLOWANCE:.1f} mm vs {HOOK_UNLOCK_LIFT:.1f} mm to unhook")


if __name__ == "__main__":
    _self_check()
