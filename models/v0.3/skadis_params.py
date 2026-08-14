"""Shared parameters for the v0.3 SKADIS remote-holder adapter.

Two printed parts:
    skadis_remote_adapter.step.py   the plate, hooks + lock windows
    skadis_lock_plug.step.py        the lock plug, printed x2

Coordinate convention (both parts use plate coordinates)
    Origin : centre of the plate's rear (board-facing) face
    X      : plate width,  +X right   (looking at the board from the front)
    Y      : plate height, +Y up
    Z      : depth, +Z rearward (into the pegboard)
    Plate occupies Z in [-PLATE_T, 0]; hooks grow from Z=0 into +Z.

Why v0.3 has a separate lock plug
    A rigid in-and-drop hook can never be lift-proof. Entering the slot needs
    shank + lip <= SLOT_H; resisting lift needs shank + lip > SLOT_H. The two
    are contradictory, so the anti-lift feature has to be a second element.
    The plug fills the lower slot completely, leaving LOCK_LIFT_ALLOWANCE of
    play instead of the 4.2 mm needed to unhook.
"""

from math import sqrt

# --- existing remote holder (measured, approximate) -------------------------
HOLDER_WIDTH = 48.5           # mm, overall
HOLDER_HEIGHT = 67.0          # mm, overall
HOLDER_DEPTH = 19.0           # mm, incl. front retaining clips (reference only)
HOLDER_HOLE_SPACING = 29.5    # mm, centre-to-centre, vertical, on the centreline

# --- SKADIS pegboard --------------------------------------------------------
# Slots at the SAME height are 40 mm apart: the user's 35 mm clear gap plus the
# 5 mm slot, and what franpoli/OpenSCADutil spaces its pegs by. The lattice also
# has intermediate columns dropped 20 mm; they are not used.
SKADIS_SLOT_WIDTH = 5.0            # mm, measured
SKADIS_HORIZONTAL_GAP = 35.0       # mm, measured clear gap between adjacent slots
SKADIS_HORIZONTAL_PITCH = SKADIS_HORIZONTAL_GAP + SKADIS_SLOT_WIDTH  # 40.0
SKADIS_VERTICAL_PITCH = 40.0       # mm, within one column (ASSUMED, not measured)
SKADIS_SLOT_HEIGHT = 15.0          # mm, IKEA standard (ASSUMED, not measured)
SKADIS_BOARD_THICKNESS = 5.0       # mm, IKEA standard (ASSUMED, not measured)

# --- plate ------------------------------------------------------------------
PLATE_W = 47.0            # < HOLDER_WIDTH  -> fully hidden behind the holder
PLATE_H = 58.0            # < HOLDER_HEIGHT -> fully hidden behind the holder
PLATE_T = 6.0             # plate thickness; also sets screw thread engagement
PLATE_CORNER_R = 3.0

PRINT_TOLERANCE = 0.35            # per-side FDM allowance inside a slot
SKADIS_HOOK_CLEARANCE = 2 * PRINT_TOLERANCE
SKADIS_BOARD_CLEARANCE = 0.6      # Z play between plate and board rear face

# --- hooks (top row only; the bottom row carries the lock plugs) ------------
HOOK_WIDTH = SKADIS_SLOT_WIDTH - SKADIS_HOOK_CLEARANCE   # 4.3 mm across the slot
HOOK_HEIGHT = 8.0                 # vertical bearing length inside the slot
HOOK_SHANK_LEN = SKADIS_BOARD_THICKNESS + SKADIS_BOARD_CLEARANCE
HOOK_CATCH = 1.2                  # flat shelf square to the board: the anchor
HOOK_LIP = 3.0                    # 45 deg self-supporting ramp below the shelf
HOOK_ROOT_FILLET = 0.8

# A root fillet flares the hook to HOOK_WIDTH + 2*HOOK_ROOT_FILLET at its base,
# which is wider than the 5 mm slot: it would hold the plate off the board by
# the fillet radius. (v0.1 and v0.2 have exactly this defect.) So each hook
# rises from a shallow relief pocket in the rear face, and the fillet is formed
# down there, below the plane that touches the board.
ROOT_RELIEF_DEPTH = HOOK_ROOT_FILLET + 0.2
ROOT_RELIEF_MARGIN = HOOK_ROOT_FILLET + 0.4

FEATURE_X = SKADIS_HORIZONTAL_PITCH / 2.0   # +/-20 -> two slots at equal height
HOOK_Y = SKADIS_VERTICAL_PITCH / 2.0        # +20 -> the top row

# Seated position. The slot ends are semicircular (r = 2.5), so a square-ended
# hook 4.3 mm wide does NOT reach the extreme bottom of the slot: its two
# bottom corners land on the radius HOOK_SEAT_RISE above it. Getting this wrong
# misplaces the lock window by over a millimetre, which is more than its
# clearance, so it is computed rather than assumed.
SLOT_END_R = SKADIS_SLOT_WIDTH / 2.0
HOOK_SEAT_RISE = SLOT_END_R - sqrt(SLOT_END_R ** 2 - (HOOK_WIDTH / 2.0) ** 2)

HOOK_SLOT_BOTTOM_Y = HOOK_Y - HOOK_HEIGHT / 2.0 - HOOK_SEAT_RISE
HOOK_SLOT_CENTRE_Y = HOOK_SLOT_BOTTOM_Y + SKADIS_SLOT_HEIGHT / 2.0
LOCK_SLOT_CENTRE_Y = HOOK_SLOT_CENTRE_Y - SKADIS_VERTICAL_PITCH

# Lift needed to unhook = how far the lip has to clear the slot bottom.
HOOK_UNLOCK_LIFT = HOOK_CATCH + HOOK_LIP                           # 4.2

# --- lock plug --------------------------------------------------------------
# The head is obround like the slot itself, so it beds into the rounded ends
# instead of stopping on them the way a square hook does.
LOCK_W = HOOK_WIDTH                       # 4.3, same slot fit as a hook
LOCK_CLEARANCE_Y = 0.3                    # per end, inside the 15 mm slot
LOCK_HEAD_H = SKADIS_SLOT_HEIGHT - 2 * LOCK_CLEARANCE_Y            # 14.4
LOCK_ENGAGE = 4.5                         # how far the head enters the board
LOCK_TIP_CHAMFER = 0.6

# Sideways fit can be generous; the vertical fit is what caps the lift, so it
# is the tight one. Both are per-axis totals, window minus plug.
LOCK_FIT_W = 0.5
LOCK_FIT_H = 0.3
WINDOW_W = LOCK_W + LOCK_FIT_W            # 4.8
WINDOW_H = LOCK_HEAD_H + LOCK_FIT_H       # 14.7

LOCK_TAIL_T = 2.0                         # strap in the plate's front groove
LOCK_TAIL_BOTTOM_Y = -36.0                # plate coords; holder bottom is -33.5
LOCK_TAB_T = 3.5                          # thicker grab tab, clear of the plate
LOCK_TAB_H = 4.0
GROOVE_DEPTH = LOCK_TAIL_T + 0.3
# The groove has to start above where the window's obround end narrows, or the
# square tail fouls the rounded corners on its way out.
GROOVE_TOP_Y = LOCK_SLOT_CENTRE_Y - WINDOW_H / 2.0 + WINDOW_W

# With the plug fitted the plate can only rise by the head's play in the slot
# plus its play in the window. Kept under HOOK_CATCH so even at full lift the
# hook's square catch shelf is still bearing on the board.
LOCK_LIFT_ALLOWANCE = (SKADIS_SLOT_HEIGHT - LOCK_HEAD_H) + LOCK_FIT_H   # 0.9

# --- screws -----------------------------------------------------------------
SCREW_PILOT_DIAMETER = 2.9        # suits M3 / 3.5 mm self-tapping screws
SCREW_PILOT_DEPTH = 5.0           # leaves a 1.0 mm wall at the board-facing face
HOLDER_HOLE_DIAMETER = 4.0        # reference only, not modelled (ASSUMED)


def hook_profile_points(base_z=-ROOT_RELIEF_DEPTH):
    """(z, y) polygon of one hook, local to its own centre in Y.

    Starts at the relief pocket floor, runs a shank out through the board, then
    a flat shelf square to the board (HOOK_CATCH) that takes the pull-out load
    without camming, then a 45 deg ramp so it still prints without support.
    Z is measured from the plate's rear face, so HOOK_SHANK_LEN stays the
    protrusion past the board-touching plane whatever the pocket depth is.
    """
    half = HOOK_HEIGHT / 2.0
    return [
        (base_z, -half),
        (HOOK_SHANK_LEN, -half),
        (HOOK_SHANK_LEN, -half - HOOK_CATCH),
        (HOOK_SHANK_LEN + HOOK_LIP, -half - HOOK_CATCH - HOOK_LIP),
        (HOOK_SHANK_LEN + HOOK_LIP, half),
        (base_z, half),
    ]
