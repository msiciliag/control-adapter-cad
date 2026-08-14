# Adaptador SKÅDIS para soporte de mando

Adaptador impreso que monta el soporte del mando del ventilador/luz sobre un
panel IKEA SKÅDIS, reutilizando los dos tornillos originales del soporte.

```
soporte original -> sus 2 tornillos -> adaptador impreso -> ganchos SKÅDIS
```

## Estructura

```
models/<version>/
  skadis_params.py                todos los parámetros (v0.3+; editar aquí)
  skadis_remote_adapter.step.py   la placa
  skadis_lock_plug.step.py        el tapón de bloqueo, imprimir x2 (v0.3+)
  assembly_check.step.py          placa + tapones + panel, solo verificación
  *.step / *.stl / *.3mf / *.glb  artefactos
  snapshots/                      vistas renderizadas
  print/                          proyecto Bambu Studio laminado, listo
reference/                        fotos y cotas de la pieza original
```

## Montaje (v0.3)

1. Cuelga la placa en la fila de slots de arriba y déjala caer hasta el tope.
2. Mete un tapón por cada ventana, empujando de frente hasta que el tirador
   quede plano en la ranura. Ahora la placa no puede subir.
3. Atornilla el soporte del mando a la placa con dos tornillos de ≤ 8 mm.

Para descolgarlo del panel: quitar los dos tornillos, sacar los tapones tirando
del tirador, levantar la placa. Con el soporte puesto los tapones no salen —
su trasera bloquea el recorrido, que es justo lo que impide que se suelte solo.

## Versiones

| Versión | Estado | Cambios |
|---|---|---|
| v0.1 | impresa, pendiente de fit test | Primer prototipo. Placa 46×58×5. 4 ganchos, vástago 4 mm, labio a 45°. 17 cm³, 1 h 09 m. |
| v0.2 | superada | Repisa de anclaje recta de 1.2 mm antes de la rampa (el labio a 45° se descabalgaba al tirar). Vástago 4 → 8 mm. Placa 5 → 6 mm. 17.2 cm³, 1 h 21 m. |
| v0.3 | actual | Se sacaba tirando del mando hacia arriba. Dos piezas: la fila de ganchos de abajo pasa a ser dos ventanas con **tapón de bloqueo**, que rellena el slot y deja la subida en 0.9 mm en vez de 4.2. Corrige además dos errores de v0.1/v0.2. 16.6 cm³, 1 h 35 m. |

### Errores de v0.1/v0.2 corregidos en v0.3

1. **El redondeo de raíz separaba la placa del panel.** Un fillet de 0.8 mm ensancha
   el gancho a 5.9 mm en la base, y el slot tiene 5 mm: la placa quedaba apoyada
   0.8 mm por delante del panel. v0.3 hunde cada gancho en un rebaje de alivio para
   que el fillet quede por debajo del plano de contacto.
2. **Los extremos de los slots son semicirculares (r = 2.5).** Un gancho recto de
   4.3 mm de ancho no llega al fondo del slot: se apoya 1.22 mm más arriba. Sin
   tenerlo en cuenta, la ventana del tapón quedaba desalineada más que su holgura.

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
