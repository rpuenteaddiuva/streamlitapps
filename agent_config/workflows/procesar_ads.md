---
description: Pipeline Maestro ADS 2025
---

# Pipeline Maestro ADS 2025

1. **Limpieza**
   Invocar `agent_config/workflows/01_limpieza.md`.
   Comando: `python codigos/ads_utils.py --action clean`

2. **Análisis**
   Invocar `agent_config/workflows/02_analisis.md`.
   Comando: `python codigos/ads_utils.py --action analyze`

3. **Conclusión**
   Invocar `agent_config/workflows/03_conclusion.md`.
