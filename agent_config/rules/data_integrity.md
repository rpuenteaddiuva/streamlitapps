# Reglas de Integridad de Datos ADS 2025

1. **Inmutabilidad de Fuentes**: 
   - NUNCA sobrescribir `Servicios brindados ADS 2025 (1).xlsx` ni `BBDD.csv`.
   - Todas las salidas deben ser nuevos archivos (e.g., `clean_bbdd.parquet`).
   - Usar `agent_config` para configuraciones.

2. **Idioma**:
   - Comentarios de código: Inglés o Español (consistente).
   - Columnas de datos generadas: `snake_case` (e.g., `tiempo_contacto`).
   - **Reportes y Salidas al Usuario**: ESTRICTAMENTE ESPAÑOL.

3. **Mapeo Geográfico**:
   - `LOCAL` -> Urbano (SLA 45/35 min).
   - `FORANEO` -> Rural/Foráneo (SLA 90/60 min).

4. **Manejo de Errores**:
   - Si > 1% de fechas fallan en conversión, detener y alertar.
   - Tratar "Sin Placa", "Sin Motor" y cadenas vacías como `NaN` para análisis estadístico.
