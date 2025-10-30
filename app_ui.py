"""
Fuel MCP UI — ASTM D1250 / ISO 91-1
-----------------------------------
Gradio-based interface for VCF, density, and volume correction.
Connects to the running FastAPI backend on localhost:8000
"""

import gradio as gr
import requests
import json

API_URL = "http://127.0.0.1:8000"  # FastAPI backend

# ------------------------------------------------------
# 📘 Standard reference densities (kg/m³ at 15°C)
# ------------------------------------------------------
STANDARD_DENSITIES = {
    "diesel": 850.0,
    "hfo": 980.0,
    "jet": 800.0,
    "lube": 910.0,
    "gasoline": 740.0,
}

# ------------------------------------------------------
# 🧮 1️⃣  VCF / Density calculation
# ------------------------------------------------------
def compute_vcf(fuel, rho15, tempC, volume_m3):
    """Calls /auto_correct on backend and returns formatted JSON."""
    try:
        params = {
            "fuel": fuel,
            "rho15": rho15 or STANDARD_DENSITIES.get(fuel, 850.0),
            "volume_m3": volume_m3,
            "tempC": tempC,
        }
        r = requests.get(f"{API_URL}/auto_correct", params=params, timeout=30)
        r.raise_for_status()
        return json.dumps(r.json(), indent=2)
    except Exception as e:
        return f"❌ Error: {e}"

# ------------------------------------------------------
# 🧮 2️⃣ API / Gravity Conversion logic
# ------------------------------------------------------
def calc_api(mode, density_input, api_input):
    """Convert between API gravity, specific gravity, and density."""
    try:
        if mode == "From Density":
            sg = density_input / 999.016
            api = 141.5 / sg - 131.5
            return round(sg, 6), round(density_input, 3), round(api, 3)
        elif mode == "From API Gravity":
            sg = 141.5 / (api_input + 131.5)
            density = sg * 999.016
            return round(sg, 6), round(density, 3), round(api_input, 3)
        else:
            return None, None, None
    except Exception as e:
        return f"❌ Error: {e}", None, None

# ------------------------------------------------------
# 🧮 3️⃣ Volume ↔ Mass Conversion logic
# ------------------------------------------------------
def convert_volume_mass(fuel_vm, rho_vm, temp_vm, vol_vm, mass_vm):
    """Uses backend /auto_correct for volume ↔ mass conversions."""
    try:
        params = {
            "fuel": fuel_vm,
            "rho15": rho_vm or STANDARD_DENSITIES.get(fuel_vm, 850.0),
            "tempC": temp_vm,
        }
        if vol_vm:
            params["volume_m3"] = vol_vm
        if mass_vm:
            params["mass_ton"] = mass_vm

        r = requests.get(f"{API_URL}/auto_correct", params=params, timeout=30)
        r.raise_for_status()
        return json.dumps(r.json(), indent=2)
    except Exception as e:
        return f"❌ Error: {e}"

# ------------------------------------------------------
# 🧮 4️⃣ Temperature & Unit Conversion logic
# ------------------------------------------------------
def convert_temp(temp_mode, temp_input):
    """Converts between Celsius and Fahrenheit."""
    try:
        if temp_mode == "°C → °F":
            return round(temp_input * 1.8 + 32, 2)
        else:
            return round((temp_input - 32) / 1.8, 2)
    except Exception as e:
        return f"❌ Error: {e}"

def general_convert(val_unit, from_unit, to_unit):
    """Calls backend /convert for general unit conversions."""
    try:
        params = {"value": val_unit, "from_unit": from_unit, "to_unit": to_unit}
        r = requests.get(f"{API_URL}/convert", params=params, timeout=30)
        r.raise_for_status()
        return json.dumps(r.json(), indent=2)
    except Exception as e:
        return f"❌ Error: {e}"

def safe_convert(val_unit, from_unit, to_unit):
    """Prevents empty unit conversions."""
    if not from_unit or not to_unit:
        return "⚠️ Please provide both 'from' and 'to' units."
    return general_convert(val_unit, from_unit.strip(), to_unit.strip())

# ------------------------------------------------------
# 🧩  Build UI
# ------------------------------------------------------
with gr.Blocks(title="Fuel MCP — ASTM D1250 / ISO 91-1") as demo:
    gr.Markdown("## 🛢️ Petroleum Measurement Tables — ASTM D1250 / ISO 91-1")

    # ======================================================
    # 1️⃣ VCF / Density Tab
    # ======================================================
    with gr.Tab("VCF / Density"):
        gr.Markdown("### Table 54A–54D — VCF and Density Correction")

        with gr.Row():
            fuel = gr.Dropdown(
                list(STANDARD_DENSITIES.keys()),
                label="Fuel type (suggests standard ρ₁₅, editable)",
                value="diesel",
            )
            rho15 = gr.Number(
                label="Density @15 °C (kg/m³)",
                value=STANDARD_DENSITIES["diesel"],
                interactive=True,
            )
            tempC = gr.Number(label="Observed Temperature (°C)", value=25)
            volume_m3 = gr.Number(label="Observed Volume (m³)", value=1000)

        # 🔁 Auto-update density suggestion but keep editable
        def suggest_density(selected_fuel):
            suggested = STANDARD_DENSITIES.get(selected_fuel, 850.0)
            return gr.update(value=suggested, interactive=True)

        fuel.change(fn=suggest_density, inputs=fuel, outputs=rho15)

        result = gr.Textbox(label="Result (JSON output)", lines=16)
        btn = gr.Button("Compute VCF and Volume @15 °C")
        btn.click(compute_vcf, [fuel, rho15, tempC, volume_m3], result)

    # ======================================================
    # 2️⃣ API / Gravity Conversion Tab
    # ======================================================
    with gr.Tab("API / Gravity Conversion"):
        gr.Markdown("### ASTM D1250 — Table 21 (API / Density / Specific Gravity)")

        with gr.Row():
            mode = gr.Radio(["From Density", "From API Gravity"], label="Select mode", value="From Density")
        with gr.Row():
            density_input = gr.Number(label="Density @15°C (kg/m³)", value=850)
            api_input = gr.Number(label="API Gravity (°API)", value=35.0)
            sg_output = gr.Number(label="Specific Gravity (SG @60°F/60°F)", interactive=False)
            density_output = gr.Number(label="Calculated Density (kg/m³)", interactive=False)
            api_output = gr.Number(label="Calculated API Gravity", interactive=False)

        calc_btn = gr.Button("Compute API / Density")
        calc_btn.click(calc_api, [mode, density_input, api_input],
                       [sg_output, density_output, api_output])

    # ======================================================
    # 3️⃣ Volume ↔ Mass Conversion Tab
    # ======================================================
    with gr.Tab("Volume ↔ Mass Conversion"):
        gr.Markdown("### ASTM D1250 — Table 22 (Volume–Mass Corrections)")

        with gr.Row():
            fuel_vm = gr.Dropdown(list(STANDARD_DENSITIES.keys()),
                                  label="Fuel type (suggests standard ρ₁₅, editable)",
                                  value="diesel")
            rho_vm = gr.Number(label="Density @15 °C (kg/m³)",
                               value=STANDARD_DENSITIES["diesel"], interactive=True)
            temp_vm = gr.Number(label="Observed Temperature (°C)", value=25)

        def suggest_density_vm(selected_fuel):
            return gr.update(value=STANDARD_DENSITIES.get(selected_fuel, 850.0), interactive=True)

        fuel_vm.change(fn=suggest_density_vm, inputs=fuel_vm, outputs=rho_vm)

        with gr.Row():
            vol_vm = gr.Number(label="Observed Volume (m³)", value=1000)
            mass_vm = gr.Number(label="Mass (t)", value=None)

        result_vm = gr.Textbox(label="Result (JSON output)", lines=14)
        btn_vm = gr.Button("Compute Volume ↔ Mass Correction")
        btn_vm.click(convert_volume_mass, [fuel_vm, rho_vm, temp_vm, vol_vm, mass_vm], result_vm)

    # ======================================================
    # 4️⃣ Temperature & Unit Converter Tab
    # ======================================================
    with gr.Tab("Temperature & Unit Converter"):
        gr.Markdown("### ASTM D1250 — Table 1 & 2 (Temperature and Unit Conversions)")

        gr.Markdown("#### 🌡️ Temperature Conversion")
        with gr.Row():
            temp_mode = gr.Radio(["°C → °F", "°F → °C"], label="Select conversion", value="°C → °F")
            temp_input = gr.Number(label="Temperature value", value=25.0)
            temp_result = gr.Number(label="Converted value", interactive=False)
        gr.Button("Convert Temperature").click(convert_temp, [temp_mode, temp_input], temp_result)

        gr.Markdown("#### ⚙️ General Unit Conversion (Volume, Mass, Pressure, etc.)")
        with gr.Row():
            val_unit = gr.Number(label="Value", value=1.0)
            from_unit = gr.Textbox(label="From unit", placeholder="e.g., barrel, litre, m3, ton, bar", value="barrel")
            to_unit = gr.Textbox(label="To unit", placeholder="e.g., litre, usg, kg, Pa", value="litre")
        conv_result = gr.Textbox(label="Result (JSON output)", lines=3)
        gr.Button("Convert Units").click(safe_convert, [val_unit, from_unit, to_unit], conv_result)

    # ======================================================
    # Footer info
    # ======================================================
    gr.Markdown("### ℹ️ Connected to local FastAPI backend at `http://127.0.0.1:8000`")

# ------------------------------------------------------
# 🚀  Run local UI
# ------------------------------------------------------
if __name__ == "__main__":
    demo.launch()
