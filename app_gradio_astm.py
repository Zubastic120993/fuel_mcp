"""
app_gradio_astm.py
==================
Gradio multi-tab GUI for Fuel MCP / ASTM D1250 converter.
Each tab corresponds to an ASTM desktop panel (API, Density, Rel.Density…)
"""

import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"  # Local MCP API


# ======================================================
# 🧮 API Gravity Entry → Connect to MCP backend
# ======================================================
def calc_api(api, temp_f):
    """
    Convert API gravity (°API) and temperature (°F) → VCF using MCP backend.
    """
    try:
        # --- Convert temperature to °C
        temp_c = (temp_f - 32) * 5 / 9

        # --- Convert API → Density @15°C (kg/m³)
        rho15 = 141.5 / (api + 131.5) * 999.016

        # --- Query your MCP backend /vcf endpoint
        response = requests.get(
            f"{API_URL}/vcf",
            params={"rho15": round(rho15, 2), "tempC": round(temp_c, 2)},
            timeout=10,
        )
        data = response.json()

        # --- Append extra info
        data["input_API"] = api
        data["input_TempF"] = temp_f
        data["converted_TempC"] = round(temp_c, 2)
        data["calculated_rho15"] = round(rho15, 2)

        return data

    except Exception as e:
        return {"error": str(e)}


# ======================================================
# 🚀 Build Gradio Interface
# ======================================================
with gr.Blocks(title="Fuel MCP – ASTM D1250 Tool") as demo:
    gr.Markdown("# 🧩 Fuel MCP — ASTM D1250 Conversion Suite")

    with gr.Tabs():
        # ------------------------------------------------------
        # TAB 1 — API GRAVITY ENTRY
        # ------------------------------------------------------
        with gr.Tab("API Gravity Entry"):
            gr.Markdown("### 🌡️ Enter API Gravity and Temperature (°F)")
            api_input = gr.Number(label="API Gravity (°API)", value=33)
            temp_input = gr.Number(label="Temperature (°F)", value=60)
            output_api = gr.JSON(label="Calculated Results")

            gr.Button("🔹 Compute VCF from API → Density @15°C").click(
            calc_api, inputs=[api_input, temp_input], outputs=output_api
            )

        # ------------------------------------------------------
        # TAB 2 — RELATIVE DENSITY ENTRY
        # ------------------------------------------------------
        with gr.Tab("Relative Density Entry"):
            gr.Markdown("### 🧮 Relative Density + Temperature")
            gr.Markdown("*coming next step*")

        # ------------------------------------------------------
        # TAB 3 — UNIT CONVERSION
        # ------------------------------------------------------
        with gr.Tab("Unit Conversion"):
            gr.Markdown("### ⚖️ ASTM Volume XI – Interrelation of Units")
            gr.Markdown("*coming next step*")

        # ------------------------------------------------------
        # TAB 4 — DENSITY ENTRY
        # ------------------------------------------------------
        with gr.Tab("Density Entry"):
            gr.Markdown("### 🧪 Density + Temperature → VCF Tables 54 A/B/C")
            gr.Markdown("*coming next step*")

        # ------------------------------------------------------
        # TAB 5 — VOLUME & WEIGHT CONVERTER
        # ------------------------------------------------------
        with gr.Tab("Volume & Weight Converter"):
            gr.Markdown("### ⚗️ Volume ↔ Weight (ton / m³ / bbl)")
            gr.Markdown("*coming next step*")

        # ------------------------------------------------------
        # TAB 6 — API & DENSITY CONVERTER
        # ------------------------------------------------------
        with gr.Tab("API & Density Converter"):
            gr.Markdown("### 🔄 API ↔ Density ↔ Relative Density")
            gr.Markdown("*coming next step*")


# ======================================================
# 🧩 Run App
# ======================================================
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)