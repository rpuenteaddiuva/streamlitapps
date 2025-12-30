# Workflow: Limpieza de Datos ADS 2025

Este flujo de trabajo se encarga de ingerir, normalizar y limpiar los datos crudos.

1. **Carga de Datos**
   - Ejecutar script para cargar `Servicios brindados ADS 2025 (1).xlsx`, hoja `BBDD`.
   - Inspeccionar columnas y normalizar a `snake_case`.

2. **Validación de Integridad**
   - Identificar nulos en `tiempo_asignacion`, `tiempo_contacto`.
   - Generar reporte preliminar de calidad.

3. **Transformación**
   - Unificar fechas y horas en objetos `datetime`.
   - Convertir `tiempo_asignacion` a minutos (float).
   - Filtrar cancelaciones para el dataset operativo.

4. **Persistencia**
   - Guardar `clean_bbdd.parquet`.
   - Guardar `data_quality_report.md`.

## Ejecución
```bash
python codigos/ads_utils.py --action clean --input "Servicios brindados ADS 2025 (1).xlsx"
```
