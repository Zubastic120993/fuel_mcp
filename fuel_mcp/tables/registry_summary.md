# 🧮 ASTM / ISO Conversion Table Registry Summary

This registry summarizes all available ASTM D1250 / ISO 91-1 correlation tables used for
density, volume, and mass correction within **fuel_mcp**.

Each group below shows the relevant tables, reference links, and purpose notes.

---

## 🗂️ UNCATEGORIZED

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table11_API_to_LongTons.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table12_RelativeDensity_to_LongTons.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table14_RelativeDensity_to_CubicMeters.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table15_API_to_MetricTonnes.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table15_Reverse_MetricTonnes_to_API .csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table16B_RelativeDensity_to_USGallons_and_Barrels_per_LongTon_60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table16_Density15C_to_MetricTonnes.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table16_Reverse_MetricTonnes_to_Density15C.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table17_RelativeDensity60F_to_Pounds_per_USGallon_and_USGallons_per_Pound_60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table18A_APIGravity60F_to_CubicMeters_per_ShortTon_and_LongTon_15C.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table1_APIGravity60F_to_RelativeDensity60F_and_Density15C.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table1_API_to_CubicMeters.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table25_RelativeDensity_to_Litres_per_USGallon_60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table26_Density15C_to_CubicMeters_per_USBarrel_60F_15C.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table27_Density15C_to_USBarrels_per_CubicMeter_15C.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table2_API_to_Liters.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table2_RelativeDensity60F_to_APIGravity60F_and_Density15C.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table35_RelativeDensity60F_to_USGallons_and_Barrels_per_ShortTon_60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table36_RelativeDensity60F_to_ShortTons_per_1000USGallons_and_per_Barrel_60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table3_Density15C_to_RelativeDensity60F_and_APIGravity60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table6_APIGravity60F_to_Pounds_per_USGallon_and_USGallons_per_Pound_60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table7_RelativeDensity_to_CubicMeters_per_Barrel_60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table8_API_to_LongTons.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table9_APIGravity60F_to_USGallons_and_Barrels_per_ShortTon_60F.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |
| `ASTM_Table9_API_to_ShortTons.csv` | `` | - | - | - | Table metadata placeholder — to be completed later. |

---

## 🗂️ AIR CORRECTION

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table56_Density15C_to_VacuoAirFactor.csv` | `Density_15C_kg_per_L` | Correction_Factor | ASTM D1250-80 Vol XI Table 56 | ISO 91-1 Table 56 | Air/vacuo correction based on density 15 °C. |
| `ASTM_Table57_Density15C_to_AirVacuoFactor.csv` | `Density_15C_kg_per_L` | Correction_Factor | ASTM D1250-80 Vol XI Table 57 | ISO 91-1 Table 57 | Air/vacuo correction based on density 15 °C. |

---

## 🗂️ DENSITY ↔ MASS

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table54B_Density15C_to_Short_and_Long_Tons_per_CubicMeter.csv` | `Density_15C_kg_per_m3` | Short_Tons_per_CubicMeter, Long_Tons_per_CubicMeter | ASTM D1250-80 Vol XI Table 54B | ISO 91-1 Table 54B | Density 15 °C–based conversion |

---

## 🗂️ DENSITY ↔ VOLUME

| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |
|:------|:----------------|:---------|:----------|:--------|:---------|
| `ASTM_Table53B_Density15C_to_CubicMeters_per_MetricTon.csv` | `Density_15C_kg_per_m3` | Cubic_Meters_per_Tonne | ASTM D1250-80 Vol XI Table 53B | ISO 91-1 Table 53B | Density 15 °C–based conversion |

---

