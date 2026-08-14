"""Fit check for the v0.3 adapter: plate + 2 lock plugs + a section of board.

Not a printed part. This exists so the mate can be looked at: the hooks seated
in the top slots, the plug heads filling the lower slots, and the tabs reaching
out under the plate. Everything is placed at its seated position, so anything
that interferes shows up here.
"""

import importlib.util
from pathlib import Path

from build123d import (
    Align,
    Box,
    BuildPart,
    BuildSketch,
    Locations,
    Mode,
    Plane,
    Pos,
    SlotOverall,
    extrude,
)
from cadgen import srgb
from cadgen.assembly import AssemblyHelper

from skadis_params import (
    FEATURE_X,
    HOOK_SLOT_CENTRE_Y,
    LOCK_SLOT_CENTRE_Y,
    SKADIS_BOARD_THICKNESS,
    SKADIS_SLOT_HEIGHT,
    SKADIS_SLOT_WIDTH,
)

HERE = Path(__file__).resolve().parent
BOARD_W = 104.0
BOARD_H = 96.0


def _load(name):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _board():
    """A section of SKADIS with the four slots this adapter uses."""
    slots = [(sx * FEATURE_X, y)
             for y in (HOOK_SLOT_CENTRE_Y, LOCK_SLOT_CENTRE_Y)
             for sx in (-1.0, 1.0)]
    with BuildPart() as board:
        Box(BOARD_W, BOARD_H, SKADIS_BOARD_THICKNESS,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        with BuildSketch(Plane.XY) as sk:
            with Locations(*slots):
                SlotOverall(SKADIS_SLOT_HEIGHT, SKADIS_SLOT_WIDTH, rotation=90)
        extrude(sk.sketch, amount=SKADIS_BOARD_THICKNESS, mode=Mode.SUBTRACT)
    return board.part


def gen_step():
    plate = _load("skadis_remote_adapter.step.py").gen_step()
    plug = _load("skadis_lock_plug.step.py").gen_step()

    asm = AssemblyHelper("skadis_adapter_fit_check")
    asm.add(_board(), "pegboard_section", color=srgb("#D8DCE2"))
    asm.add(plate, "adapter_plate", color=srgb("#E8E4DC"))
    for side, sx in (("left", -1.0), ("right", 1.0)):
        asm.add(
            plug.moved(Pos(sx * FEATURE_X, LOCK_SLOT_CENTRE_Y, 0)),
            f"lock_plug:{side}",
            color=srgb("#C2410C"),
        )
    return asm.build()


def _clash(a, b):
    """Shared volume between two solids, in mm3. Empty intersections vary in
    type between a null shape and an empty ShapeList, so normalise both."""
    result = a.intersect(b)
    shapes = list(result) if isinstance(result, list) else [result]
    return sum(s.volume
               for shape in shapes if shape is not None
               for s in shape.solids())


def _self_check():
    """The plugs and the plate must not share volume with the board."""
    plate = _load("skadis_remote_adapter.step.py").gen_step()
    plug = _load("skadis_lock_plug.step.py").gen_step()
    board = _board()

    v = _clash(board, plate)
    assert v < 1e-3, f"plate clashes with the board: {v:.3f} mm3"

    for sx in (-1.0, 1.0):
        placed = plug.moved(Pos(sx * FEATURE_X, LOCK_SLOT_CENTRE_Y, 0))
        v = _clash(board, placed)
        assert v < 1e-3, f"plug clashes with the board: {v:.3f} mm3"
        v = _clash(plate, placed)
        assert v < 1e-3, f"plug clashes with the plate: {v:.3f} mm3"

    # and the plug must actually be inside its slot, not floating past it
    inside = board.bounding_box()
    placed = plug.moved(Pos(FEATURE_X, LOCK_SLOT_CENTRE_Y, 0)).bounding_box()
    assert placed.max.Z <= inside.max.Z + 1e-6, "plug pokes out behind the board"
    assert placed.max.Z > SKADIS_BOARD_THICKNESS / 2.0, "plug barely enters the board"

    print(f"ok assembly: no interference; plug reaches Z={placed.max.Z:.2f} "
          f"into a {SKADIS_BOARD_THICKNESS:.1f} mm board")


if __name__ == "__main__":
    _self_check()
