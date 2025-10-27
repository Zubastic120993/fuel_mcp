# 🧮 ASTM / ISO Conversion Table Registry Summary

This registry summarizes all available ASTM D1250 / ISO 91-1 correlation tables used for
density, volume, and mass correction within **fuel_mcp**.

Each group below shows the relevant tables, reference links, and purpose notes.

---

## 🗂️ AIR CORRECTION

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table56_Density15C_to_VacuoAirFactor.csv` | `Density_15C_kg_per_L` | Correction_Factor | ASTM D1250-80 Vol XI Table 56 | ISO 91-1 Table 56 | Air/vacuo correction based on density 15 °C. |
| `ASTM_Table57_Density15C_to_AirVacuoFactor.csv` | `Density_15C_kg_per_L` | Correction_Factor | ASTM D1250-80 Vol XI Table 57 | ISO 91-1 Table 57 | Air/vacuo correction based on density 15 °C. |

## 🗂️ DENSITY ↔ MASS

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table54B_Density15C_to_Short_and_Long_Tons_per_CubicMeter.csv` | `Density_15C_kg_per_m3` | Short_Tons_per_CubicMeter, Long_Tons_per_CubicMeter | ASTM D1250-80 Vol XI Table 54B | ISO 91-1 Table 54B | Density 15 °C–based conversion |

## 🗂️ DENSITY ↔ VOLUME

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table53B_Density15C_to_CubicMeters_per_MetricTon.csv` | `Density_15C_kg_per_m3` | Cubic_Meters_per_Tonne | ASTM D1250-80 Vol XI Table 53B | ISO 91-1 Table 53B | Density 15 °C–based conversion |

## 🗂️ API CORRELATION

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table11_API_to_LongTons.csv` | `-` | - | ASTM D1250-80 Vol XI Table 11 | ISO 91-1 Table 11 | Convert API gravity at 60°F to corresponding tons per volume unit. |
| `ASTM_Table15_API_to_MetricTonnes.csv` | `-` | - | ASTM D1250-80 Vol XI Table 15 | ISO 91-1 Table 15 | Convert API gravity at 60°F to corresponding tons per volume unit. |
| `ASTM_Table15_Reverse_MetricTonnes_to_API.csv` | `-` | - | ASTM D1250-80 Vol XI Table 15 | ISO 91-1 Table 15 | Convert API gravity at 60°F to corresponding tons per volume unit. |
| `ASTM_Table18A_APIGravity60F_to_CubicMeters_per_ShortTon_and_LongTon_15C.csv` | `-` | - | ASTM D1250-80 Vol XI Table 18A | ISO 91-1 Table 18A | Convert API gravity at 60°F to corresponding tons per volume unit. |
| `ASTM_Table1_APIGravity60F_to_RelativeDensity60F_and_Density15C.csv` | `-` | - | ASTM D1250-80 Vol XI Table 1 | ISO 91-1 Table 1 | Convert API Gravity 60 °F to Relative Density 60 °F and Density 15 °C. |
| `ASTM_Table1_API_to_CubicMeters.csv` | `-` | - | ASTM D1250-80 Vol XI Table 1 | ISO 91-1 Table 1 | Convert API Gravity 60 °F to cubic meters per barrel at 60 °F to 15 °C. |
| `ASTM_Table2_API_to_Liters.csv` | `-` | - | ASTM D1250-80 Vol XI Table 2 | ISO 91-1 Table 2 | Convert API gravity at 60°F to liters or cubic meters. |
| `ASTM_Table2_RelativeDensity60F_to_APIGravity60F_and_Density15C.csv` | `-` | - | ASTM D1250-80 Vol XI Table 2 | ISO 91-1 Table 2 | Convert Relative Density 60/60 °F to API Gravity 60 °F and Density 15 °C. |
| `ASTM_Table3_Density15C_to_RelativeDensity60F_and_APIGravity60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 3 | ISO 91-1 Table 3 | Convert density at 15 °C to equivalent mass or volume. |
| `ASTM_Table6_APIGravity60F_to_Pounds_per_USGallon_and_USGallons_per_Pound_60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 6 | ISO 91-1 Table 6 | Convert API Gravity 60 °F to pounds per US gallon and vice versa. |
| `ASTM_Table8_API_to_LongTons.csv` | `-` | - | ASTM D1250-80 Vol XI Table 8 | ISO 91-1 Table 8 | Convert API gravity at 60°F to corresponding tons per volume unit. |
| `ASTM_Table9_APIGravity60F_to_USGallons_and_Barrels_per_ShortTon_60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 9 | ISO 91-1 Table 9 | Convert API gravity at 60°F to corresponding tons per volume unit. |
| `ASTM_Table9_API_to_ShortTons.csv` | `-` | - | ASTM D1250-80 Vol XI Table 9 | ISO 91-1 Table 9 | Convert API gravity at 60°F to corresponding tons per volume unit. |

## 🗂️ RELATIVE DENSITY CORRELATION

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table12_RelativeDensity_to_LongTons.csv` | `-` | - | ASTM D1250-80 Vol XI Table 12 | ISO 91-1 Table 12 | Convert relative density 60/60°F to related volumetric or mass properties. |
| `ASTM_Table14_RelativeDensity_to_CubicMeters.csv` | `-` | - | ASTM D1250-80 Vol XI Table 14 | ISO 91-1 Table 14 | Convert relative density 60/60°F to related volumetric or mass properties. |
| `ASTM_Table16B_RelativeDensity_to_USGallons_and_Barrels_per_LongTon_60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 16B | ISO 91-1 Table 16B | Convert relative density 60/60°F to related volumetric or mass properties. |
| `ASTM_Table17_RelativeDensity60F_to_Pounds_per_USGallon_and_USGallons_per_Pound_60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 17 | ISO 91-1 Table 17 | Convert relative density 60/60°F to related volumetric or mass properties. |
| `ASTM_Table25_RelativeDensity_to_Litres_per_USGallon_60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 25 | ISO 91-1 Table 25 | Convert relative density 60/60°F to related volumetric or mass properties. |
| `ASTM_Table35_RelativeDensity60F_to_USGallons_and_Barrels_per_ShortTon_60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 35 | ISO 91-1 Table 35 | Convert relative density 60/60°F to related volumetric or mass properties. |
| `ASTM_Table36_RelativeDensity60F_to_ShortTons_per_1000USGallons_and_per_Barrel_60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 36 | ISO 91-1 Table 36 | Convert relative density 60/60°F to related volumetric or mass properties. |
| `ASTM_Table7_RelativeDensity_to_CubicMeters_per_Barrel_60F.csv` | `-` | - | ASTM D1250-80 Vol XI Table 7 | ISO 91-1 Table 7 | Convert relative density 60/60°F to related volumetric or mass properties. |

## 🗂️ DENSITY CORRELATION

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table16_Density15C_to_MetricTonnes.csv` | `-` | - | ASTM D1250-80 Vol XI Table 16 | ISO 91-1 Table 16 | Convert density at 15 °C to equivalent mass or volume. |
| `ASTM_Table16_Reverse_MetricTonnes_to_Density15C.csv` | `-` | - | ASTM D1250-80 Vol XI Table 16 | ISO 91-1 Table 16 | Convert density at 15 °C to equivalent mass or volume. |
| `ASTM_Table26_Density15C_to_CubicMeters_per_USBarrel_60F_15C.csv` | `-` | - | ASTM D1250-80 Vol XI Table 26 | ISO 91-1 Table 26 | Convert density at 15 °C to equivalent mass or volume. |
| `ASTM_Table27_Density15C_to_USBarrels_per_CubicMeter_15C.csv` | `-` | - | ASTM D1250-80 Vol XI Table 27 | ISO 91-1 Table 27 | Convert density at 15 °C to equivalent mass or volume. |