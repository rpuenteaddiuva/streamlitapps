# Workflow: Análisis de SLAs y NPS

Este flujo consume `clean_bbdd.parquet` y aplica la lógica de negocio.

1. **Cálculo de Variables de Tiempo**
   - Calcular `duracion_min` = `tiempo_contacto` - `tiempo_asignacion`.
   - Manejar casos negativos o anómalos.

2. **Evaluación de SLA**
   - **Vial Local**: <= 45 min.
   - **Vial Foráneo**: <= 90 min.
   - **Legal Local**: <= 35 min.
   - **Legal Foráneo**: <= 60 min.
   - Generar columna `cumple_sla` (Binario).

3. **Cálculo de NPS**
   - Calcular NPS por Broker y Mes.
   - Formula: (Promotores - Detractores) / Total * 100.

4. **Validación Cruzada**
   - Comparar Globales con `TIEMPO` (Hoja Excel si disponible o archivo).
   - Generar alerta si discrepancia > 5%.

## Ejecución
```bash
python codigos/ads_utils.py --action analyze
```
