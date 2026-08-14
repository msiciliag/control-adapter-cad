# Adaptador SKÅDIS para soporte de mando

Adaptador impreso que monta el soporte del mando del ventilador/luz sobre un
panel IKEA SKÅDIS, reutilizando los dos tornillos originales del soporte.

```
soporte original -> sus 2 tornillos -> adaptador impreso -> ganchos SKÅDIS
```

## Estructura

```
models/<version>/
  skadis_remote_adapter.step.py   fuente paramétrica build123d (editar aquí)
  skadis_remote_adapter.step      STEP (artefacto primario)
  *.stl / *.3mf / *.glb           mallas
  snapshots/                      vistas renderizadas
  print/                          proyecto Bambu Studio laminado, listo
reference/                        fotos y cotas de la pieza original
```

## Versiones

| Versión | Estado | Cambios |
|---|---|---|
| v0.1 | impresa, pendiente de fit test | Primer prototipo. Placa 46×58×5. 4 ganchos, vástago 4 mm, labio a 45°. 17 cm³, 1 h 09 m. |
| v0.2 | actual | Repisa de anclaje recta de 1.2 mm antes de la rampa (el labio a 45° se descabalgaba al tirar). Vástago 4 → 8 mm. Placa 5 → 6 mm. 17.2 cm³, 1 h 21 m. |

## Regenerar

```bash
V=v0.2
.venv/bin/python models/$V/skadis_remote_adapter.step.py            # auto-chequeo
.venv/bin/python .claude/skills/cad/scripts/gen models/$V/skadis_remote_adapter.step.py --write --force
.venv/bin/python .claude/skills/cad/scripts/export models/$V/skadis_remote_adapter.step.py --stl --3mf --glb
```

## Geometría SKÅDIS usada

Verificada contra la medida física del panel y contra
[franpoli/OpenSCADutil](https://github.com/franpoli/OpenSCADutil/blob/master/libraries/ikea_skadis_pegboard_accessories/ikea_skadis.scad),
la librería de referencia para accesorios SKÅDIS.

- Slot: 5 × 15 mm, vertical, extremos redondeados.
- Paso horizontal entre slots a la **misma altura**: 40 mm.
- Paso vertical dentro de una columna: 40 mm.
- La rejilla tiene columnas intercaladas cada 20 mm bajadas 20 mm; no se usan.
- Grosor del panel: 5.0 mm (estándar IKEA, sin medir).
