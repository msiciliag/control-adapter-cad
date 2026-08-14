"""Lock plug for the v0.3 SKADIS adapter plate. Print 2.

Pushed from the front through a lock window in the plate and into the lower
SKADIS slot. The head fills the slot, so the plate cannot rise the 4.2 mm that
would unhook it. The tail runs down the plate's front groove and ends in a tab
that sits proud of the holder's bottom edge, so the plugs go in and come out by
hand and you can see at a glance that the plate is locked.

Local coordinates match the plate's, with the origin at the head centre in X/Y
and Z = 0 on the plate's rear (board-facing) face. Fitted position in plate
coordinates is (+/-FEATURE_X, LOCK_SLOT_CENTRE_Y, 0).

Print orientation: lay it on its side, the 4.3 mm width vertical. The L is then
flat on the bed and there is nothing to support.
"""

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Plane,
    Pos,
    SlotOverall,
    add,
    chamfer,
    extrude,
)

from skadis_params import (
    LOCK_ENGAGE,
    LOCK_HEAD_H,
    LOCK_SLOT_CENTRE_Y,
    LOCK_TAB_H,
    LOCK_TAB_T,
    LOCK_TAIL_BOTTOM_Y,
    LOCK_TAIL_T,
    LOCK_TIP_CHAMFER,
    LOCK_W,
    PLATE_H,
    PLATE_T,
    SKADIS_BOARD_THICKNESS,
    SKADIS_SLOT_HEIGHT,
    SKADIS_SLOT_WIDTH,
)

# tail geometry, in this part's local Y (0 = head centre)
TAIL_TOP = -LOCK_HEAD_H / 2.0 + 3.0                       # overlaps into the head
TAIL_BOTTOM = LOCK_TAIL_BOTTOM_Y - LOCK_SLOT_CENTRE_Y     # -19.5
TAB_TOP = TAIL_BOTTOM + LOCK_TAB_H


def gen_step():
    with BuildPart() as plug:
        # 1. head: obround like the slot, through the plate window and into the board
        with BuildSketch(Plane.XY.offset(-PLATE_T)) as head:
            SlotOverall(LOCK_HEAD_H, LOCK_W, rotation=90)
        extrude(head.sketch, amount=PLATE_T + LOCK_ENGAGE)
        # lead-in so it finds the slot without fighting
        chamfer(plug.faces().sort_by(Axis.Z)[-1].edges(), LOCK_TIP_CHAMFER)

        # 2. tail: sits in the plate's front groove, flush with the front face
        with BuildPart(
            Pos(0, (TAIL_TOP + TAIL_BOTTOM) / 2.0, -PLATE_T)
        ) as tail:
            Box(LOCK_W, TAIL_TOP - TAIL_BOTTOM, LOCK_TAIL_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
        add(tail.part)

        # 3. grab tab: below the plate, thicker, in the gap behind the holder
        with BuildPart(
            Pos(0, (TAB_TOP + TAIL_BOTTOM) / 2.0, -PLATE_T)
        ) as tab:
            Box(LOCK_W, TAB_TOP - TAIL_BOTTOM, LOCK_TAB_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
        add(tab.part)

    part = plug.part
    part.label = "skadis_lock_plug_v0_3"
    return part


def _self_check():
    part = gen_step()
    bb = part.bounding_box()
    assert part.is_valid, "invalid solid"
    assert part.volume > 0, "non-positive volume"

    # fits the slot it has to fill
    assert LOCK_W < SKADIS_SLOT_WIDTH, LOCK_W
    assert LOCK_HEAD_H < SKADIS_SLOT_HEIGHT, LOCK_HEAD_H
    assert LOCK_HEAD_H > SKADIS_SLOT_HEIGHT - 1.5, \
        f"head only {LOCK_HEAD_H} mm in a {SKADIS_SLOT_HEIGHT} mm slot: too loose"

    # reaches into the board, without poking out the back of it
    assert LOCK_ENGAGE > SKADIS_BOARD_THICKNESS / 2.0, "not enough engagement"
    assert LOCK_ENGAGE <= SKADIS_BOARD_THICKNESS, "head sticks out behind the board"
    assert abs(bb.max.Z - LOCK_ENGAGE) < 1e-6, (bb.max.Z, LOCK_ENGAGE)

    # nothing may sit proud of the plate's front face: the holder mounts there
    assert abs(bb.min.Z + PLATE_T) < 1e-6, f"plug front at {bb.min.Z}, want {-PLATE_T}"
    assert LOCK_TAIL_T < PLATE_T, "tail deeper than the plate is thick"

    # the tab has to clear the holder's bottom edge to be grabbed
    tab_bottom_plate_y = LOCK_SLOT_CENTRE_Y + bb.min.Y
    assert tab_bottom_plate_y < -PLATE_H / 2.0, "tab does not reach past the plate"
    assert LOCK_TAB_T < PLATE_T, "tab thicker than the gap behind the holder"

    print(f"ok plug: {bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f} mm, "
          f"{part.volume / 1000:.2f} cm3 | head {LOCK_HEAD_H} mm in a "
          f"{SKADIS_SLOT_HEIGHT} mm slot, tab bottom at plate Y "
          f"{tab_bottom_plate_y:.1f}")


if __name__ == "__main__":
    _self_check()
