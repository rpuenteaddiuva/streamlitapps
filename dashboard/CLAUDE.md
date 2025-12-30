# ADS Dashboard - Project Documentation

## Overview

This Streamlit dashboard visualizes service quality metrics for ADS (Asistencia y Diagnóstico de Servicios). It processes data from an Excel file containing service records.

## Data Source

- **File**: `datos/Servicios brindados ADS 2025 (1).xlsx`
- **Sheet**: `BBDD` (main data)
- **Records**: ~10,000 services from January-October 2025

## Key Columns

| Column | Description |
|--------|-------------|
| `status_del_servicio` | Service status: Concluido, Cancelado al momento, Cancelado posterior, En proceso |
| `origen_del_servicio` | LOCAL or FORANEO |
| `tipo_de_servicio` | Service type (Auxilio Vial, Remolque, Legal, etc.) |
| `duracion_minutos` | Service duration in minutes |
| `fec_contacto`, `hrs_contacto` | Contact datetime (split) |
| `fec_asignacion`, `hrs_asignacion` | Assignment datetime (split) |
| `nps_calificacion_cliente` | NPS score (1-5 or 0-10 scale) |

## Metric Calculations

### 1. SLA (Service Level Agreement)
```
SLA = (Services Meeting Threshold / Total Valid Services) × 100
```

**Thresholds:**
- **Vial Local**: 45 minutes
- **Vial Foráneo**: 90 minutes
- **Legal Local**: 35 minutes
- **Legal Foráneo**: 60 minutes

**Exclusions applied:**
- `servicios_programados = "No"`
- Status: Cancelado, Fallida, Anulado
- Keywords in motivo: "Cita", "Agendada", "Programada"

### 2. NS (Nivel de Servicio / Completion Rate)
```
NS = (Concluidos / Total Válidos) × 100
```

**Total Válidos excludes:**
- Cancelado al momento
- Cancelado posterior
- Anulado, Abortado, Duplicado, Prueba

### 3. Abandono (Abandonment Rate)
```
Abandono = (Cancelados / Total Bruto) × 100
```
Uses total raw count (not filtered) as denominator.

### 4. Coordinación (Assignment Time)
```
Time = Contact Datetime - Assignment Datetime
Coordinación = (Services ≤ 10 min / Total Valid) × 100
```

**Note**: Only positive diffs are counted (assignment should occur before contact).

### 5. NPS (Net Promoter Score)
```
NPS = %Promoters - %Detractors
```

**Scale 0-10:**
- Promoters: 9-10
- Passives: 7-8
- Detractors: 0-6

**Scale 1-5:**
- Promoters: 5
- Passives: 4
- Detractors: 1-3

## Dashboard Sections

1. **Resumen Ejecutivo**: KPI cards, status distribution, SLA by category
2. **Histórico Coordinación**: Monthly trends, service types
3. **Detalle Auxilio Vial**: Filtered view for roadside assistance
4. **Detalle Remolque (Grúa)**: Filtered view for towing services
5. **Tipo de Plan**: Distribution by insurance plan
6. **Líneas de Servicio**: Service type breakdown
7. **Demanda Geográfica**: By province and city
8. **Satisfacción & NPS**: NPS gauge and distribution
9. **Indicadores Mensuales**: Monthly KPI table with SLAs
10. **Metodología**: Calculation formulas and data sources

## Styling

- **Theme**: Dark mode (CSS variables in `load_css()`)
- **Charts**: Plotly with `plotly_dark` template
- **Colors**: 
  - Primary: `#1f8ef1` (blue)
  - Success: `#2ecc71` (green)
  - Warning: `#f39c12` (orange)
  - Danger: `#e74c3c` (red)

## Files

- `app.py`: Main dashboard application
- `modules/metrics.py`: KPI calculation functions
- `modules/data_loader.py`: Data loading utilities
