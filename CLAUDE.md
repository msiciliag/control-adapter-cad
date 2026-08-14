# SKÅDIS remote holder adapter

Design a small 3D-printable adapter that lets me mount the **existing ceiling-fan/light remote holder shown in the attached photos** onto my IKEA SKÅDIS pegboard.

Use the installed **text-to-cad / CAD skills** and create a parametric, editable model.

## Existing remote holder measurements

Approximate physical measurements:

- Width: **48.5 mm**
- Height: **67 mm**
- Total depth: **19 mm**, including the two front retaining clips
- Vertical distance between mounting-hole centres: **29–30 mm**
- Two mounting holes are vertically aligned on the centreline

Use the attached photos to understand the actual geometry.

## Measured SKÅDIS dimensions

I also physically measured the SKÅDIS panel:

- Horizontal distance **between the nearest edges of two adjacent slots: ~35 mm**
- Maximum slot width: **~5 mm**
- Slots are vertical and elongated, as visible in the reference photos

These are approximate manual measurements.

**Important:** 35 mm is the clear distance from the inner/nearest edge of one slot to the nearest edge of the adjacent slot. It is **not a centre-to-centre measurement**.

Given approximately 5 mm slot width, this suggests roughly **40 mm centre-to-centre horizontal pitch**, but treat the direct physical measurements above as the source data.

Use sensible FDM clearance for the hooks rather than designing them at exactly 5.0 mm.

If another SKÅDIS dimension is critical and cannot be established reliably, ask me to measure it.

## Desired solution

Do **not** redesign or modify the original holder.

Create a separate adapter:

**original holder → existing 2 screw holes → printed adapter → SKÅDIS hooks**

The adapter should:

- sit behind the existing holder;
- reuse its two mounting holes;
- be mostly hidden from the front;
- include proper SKÅDIS-compatible hooks on the rear;
- use preferably **two adjacent SKÅDIS slots** for stability;
- resist rotation and wobble when inserting/removing the remote;
- sit close to the SKÅDIS board;
- be removable;
- preferably print as one part;
- preferably require no supports.

## CAD requirements

Use parametric `build123d` / STEP-first CAD according to the installed text-to-cad skill.

Keep important dimensions editable, for example:

```python
HOLDER_WIDTH = 48.5
HOLDER_HEIGHT = 67.0
HOLDER_DEPTH = 19.0
HOLDER_HOLE_SPACING = 29.5

SKADIS_SLOT_WIDTH = 5.0
SKADIS_HORIZONTAL_GAP = 35.0
SKADIS_HORIZONTAL_PITCH = 40.0  # derived approx.

HOLDER_HOLE_DIAMETER = ...
ADAPTER_THICKNESS = ...
SKADIS_HOOK_CLEARANCE = ...
PRINT_TOLERANCE = ...
```

Measurements marked as approximate should remain easy to adjust after a test print.

Do not guess a fit-critical dimension if it cannot be inferred safely. Ask me for it if necessary.

Add fillets around hook roots and avoid fragile thin sections.

Target printer: **Bambu Lab A1 mini**, FDM.

## Deliverables

Generate and validate:

- editable parametric source;
- STEP;
- STL;
- 3MF if supported;
- front, rear, side and isometric snapshots.

Inspect the resulting geometry before finishing.

Tell me:

- final dimensions used;
- assumptions made;
- recommended print orientation;
- whether supports are required;
- recommended material/settings;
- which dimensions should be verified before the first test print.

The objective is a **simple first prototype that can be quickly adjusted after a physical fit test**, rather than unnecessarily overengineering the adapter.