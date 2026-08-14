"""SKADIS adapter plate for an existing ceiling-fan/light remote holder.

Stack:  remote holder -> its 2 existing screw holes -> THIS plate -> SKADIS board

Coordinate convention
    Origin : centre of the plate's rear (board-facing) face
    X      : plate width,  +X right   (looking at the board from the front)
    Y      : plate height, +Y up
    Z      : depth, +Z rearward (into the pegboard)
    Plate occupies Z in [-PLATE_T, 0]; hooks/pegs grow from Z=0 into +Z.

Print orientation: front face (Z = -PLATE_T) flat on the bed, hooks pointing up.
Every rearward feature is then either vertical or a 45 deg self-supporting ramp,
so the part needs no supports.
"""

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Cylinder,
    Mode,
    Plane,
    Polygon,
    Pos,
    add,
    extrude,
    fillet,
)

# --- existing remote holder (measured, approximate) -------------------------
HOLDER_WIDTH = 48.5           # mm, overall
HOLDER_HEIGHT = 67.0          # mm, overall
HOLDER_DEPTH = 19.0           # mm, incl. front retaining clips (reference only)
HOLDER_HOLE_SPACING = 29.5    # mm, centre-to-centre, vertical, on the centreline

# --- SKADIS pegboard --------------------------------------------------------
SKADIS_SLOT_WIDTH = 5.0            # mm, measured
SKADIS_HORIZONTAL_GAP = 35.0       # mm, measured clear gap between adjacent slots
SKADIS_HORIZONTAL_PITCH = SKADIS_HORIZONTAL_GAP + SKADIS_SLOT_WIDTH  # 40.0, derived
SKADIS_VERTICAL_PITCH = 40.0       # mm, IKEA standard (ASSUMED, not measured)
SKADIS_SLOT_HEIGHT = 15.0          # mm, IKEA standard (ASSUMED, not measured)
SKADIS_BOARD_THICKNESS = 5.0       # mm, IKEA standard (ASSUMED, not measured)

# --- printed adapter --------------------------------------------------------
PLATE_W = 46.0            # < HOLDER_WIDTH  -> fully hidden behind the holder
PLATE_H = 58.0            # < HOLDER_HEIGHT -> fully hidden behind the holder
PLATE_T = 5.0             # plate thickness; also sets screw thread engagement
PLATE_CORNER_R = 3.0

PRINT_TOLERANCE = 0.35            # per-side FDM allowance inside a slot
SKADIS_HOOK_CLEARANCE = 2 * PRINT_TOLERANCE
HOOK_WIDTH = SKADIS_SLOT_WIDTH - SKADIS_HOOK_CLEARANCE   # 4.3 mm across the slot
HOOK_HEIGHT = 4.0                 # vertical size of the shank inside the slot
HOOK_SHANK_LEN = SKADIS_BOARD_THICKNESS + 0.6            # clears the board rear
HOOK_LIP = 3.0                    # 45 deg catch behind the board
HOOK_ROOT_FILLET = 0.8

FEATURE_X = SKADIS_HORIZONTAL_PITCH / 2.0   # +/-20 -> two adjacent slots
FEATURE_Y = SKADIS_VERTICAL_PITCH / 2.0     # +/-20 -> two adjacent rows

# Blind pilot holes: the original screws re-enter from the front, self-tapping
# into the plastic. Screw length must be <= holder boss depth + SCREW_PILOT_DEPTH.
SCREW_PILOT_DIAMETER = 2.9        # suits M3 / 3.5 mm self-tapping screws
SCREW_PILOT_DEPTH = 4.0           # leaves a 1.0 mm wall at the board-facing face
HOLDER_HOLE_DIAMETER = 4.0        # reference only, not modelled (ASSUMED)


def _hook_profile_points():
    """(z, y) polygon of one upper hook, local to its own centre at z=0.

    Straight shank through the board, then a lip that grows downward at 45 deg
    so it prints without support when the plate lies flat on the bed.
    """
    half = HOOK_HEIGHT / 2.0
    return [
        (0.0, -half),
        (HOOK_SHANK_LEN, -half),
        (HOOK_SHANK_LEN + HOOK_LIP, -half - HOOK_LIP),
        (HOOK_SHANK_LEN + HOOK_LIP, half),
        (0.0, half),
    ]


def gen_step():
    with BuildPart() as adapter:
        # 1. base plate, rear face on Z = 0
        Box(PLATE_W, PLATE_H, PLATE_T,
            align=(Align.CENTER, Align.CENTER, Align.MAX))
        fillet(adapter.edges().filter_by(Axis.Z), PLATE_CORNER_R)

        # 2. four identical SKADIS hooks, one per slot intersection.
        #    Sketched in the YZ plane and extruded along X. All four lips point
        #    down, so the part is inserted flat and dropped to lock all at once.
        for sx in (-1.0, 1.0):
            hook_plane = Plane.YZ.offset(sx * (FEATURE_X - HOOK_WIDTH / 2.0))
            for sy in (-1.0, 1.0):
                with BuildSketch(hook_plane) as sk:
                    # Plane.YZ local axes: local x -> world Y, local y -> world Z
                    Polygon(*[(y + sy * FEATURE_Y, z)
                              for z, y in _hook_profile_points()], align=None)
                extrude(sk.sketch, amount=sx * HOOK_WIDTH)

        # 3. fillet the hook roots where they meet the plate
        roots = [
            e for e in adapter.edges()
            if abs(e.center().Z) < 1e-6
            and abs(abs(e.center().X) - FEATURE_X) < HOOK_WIDTH
            and abs(abs(e.center().Y) - FEATURE_Y) < HOOK_HEIGHT
        ]
        fillet(roots, HOOK_ROOT_FILLET)

        # 4. blind pilot holes, open at the front (holder) face
        for sign in (1.0, -1.0):
            with BuildPart(
                Pos(0, sign * HOLDER_HOLE_SPACING / 2.0, -PLATE_T),
                mode=Mode.SUBTRACT,
            ) as pilot:
                Cylinder(SCREW_PILOT_DIAMETER / 2.0, SCREW_PILOT_DEPTH,
                         align=(Align.CENTER, Align.CENTER, Align.MIN))
            add(pilot.part, mode=Mode.SUBTRACT)

    part = adapter.part
    part.label = "skadis_remote_holder_adapter"
    return part


def _self_check():
    """Smallest checks that fail if the geometry intent breaks."""
    part = gen_step()
    bb = part.bounding_box()
    assert part.is_valid, "invalid solid"
    assert part.volume > 0, "non-positive volume"

    # hidden behind the holder from the front
    assert bb.size.X <= HOLDER_WIDTH + 1e-6, bb.size.X
    assert bb.size.Y <= HOLDER_HEIGHT + 1e-6, bb.size.Y

    # hooks reach past the board rear face, and only just
    expected_depth = PLATE_T + HOOK_SHANK_LEN + HOOK_LIP
    assert abs(bb.size.Z - expected_depth) < 1e-6, (bb.size.Z, expected_depth)
    assert HOOK_SHANK_LEN > SKADIS_BOARD_THICKNESS, "hook does not clear the board"

    # hooks fit a slot with clearance, and stay inside the plate outline
    assert HOOK_WIDTH < SKADIS_SLOT_WIDTH, HOOK_WIDTH
    assert 2 * FEATURE_X + HOOK_WIDTH <= PLATE_W + 1e-6, "hooks overhang the plate"
    assert HOOK_HEIGHT + HOOK_LIP < SKADIS_SLOT_HEIGHT, "hook will not enter a slot"

    # insert flat with hooks centred in their slots, then drop to lock:
    max_drop = (SKADIS_SLOT_HEIGHT - HOOK_HEIGHT) / 2.0
    drop_to_engage = SKADIS_SLOT_HEIGHT / 2.0 - (HOOK_HEIGHT / 2.0 + HOOK_LIP)
    engagement = max_drop - max(drop_to_engage, 0.0)
    assert engagement > 1.0, f"lip engagement only {engagement:.2f} mm"

    # pilot holes stay blind
    assert SCREW_PILOT_DEPTH < PLATE_T, "pilot hole breaks through the rear face"

    print(f"ok: {bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f} mm, "
          f"{part.volume / 1000:.2f} cm3, "
          f"drop {max_drop:.1f} mm, lip engagement {engagement:.1f} mm")


if __name__ == "__main__":
    _self_check()
