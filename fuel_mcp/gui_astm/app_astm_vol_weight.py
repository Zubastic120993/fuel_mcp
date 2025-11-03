"""
app_astm_vol_weight.py
======================
ASTM Volume & Weight Converter (Gradio version)
Excel-style interface for marine fuel conversions using Fuel MCP engine.
"""

import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"  # local MCP API


# =====================================================
# 🔹 Conversion Handler (via MCP backend)
# =====================================================
def convert_units(table, temp_unit, rho15, temp_obs, from_unit, to_unit, value):
    try:
        # Normalize temperature
        if temp_unit == "°F":
            tempC = (temp_obs - 32) * 5 / 9
        else:
            tempC = temp_obs

        # Call official VCF calculation
        resp = requests.get(
            f"{API_URL}/vcf", params={"rho15": rho15, "tempC": tempC}, timeout=10
        )
        data = resp.json().get("result", {})
        vcf = data.get("VCF", 1.0)

        # Standardized conversions (ASTM / MCP scale)
        unit_map = {
            "BBLS @Temp.": 0.158987,
            "BBLS @60°F": 0.158987,
            "M3 @Temp.": 1.0,
            "M3 @15°C": 1.0,
            "Long Tons": 1.01605,
            "Short Tons": 0.907185,
            "Metric Tonnes (Air)": 1.0,
            "Metric Tonnes (Vac)": 1.00125,
            "US Gallons @60°F": 0.00378541,
        }

        from_factor = unit_map.get(from_unit, 1.0)
        to_factor = unit_map.get(to_unit, 1.0)

        # Convert value into cubic meters as base reference
        base_m3 = value * from_factor

        # Adjust by VCF
        std_m3 = base_m3 * vcf

        # Convert to target unit
        converted_value = std_m3 / to_factor

        # Prepare output
        result = {
            "ASTM Table": table,
            "Density @15°C (kg/m³)": round(rho15, 3),
            "Observed Temp (°C)": round(tempC, 2),
            "VCF": round(vcf, 6),
            "From Unit": from_unit,
            "To Unit": to_unit,
            "Input Value": value,
            "Output Value": round(converted_value, 3),
        }

        return result

    except Exception as e:
        return {"Error": str(e)}


# =====================================================
# 🔹 Gradio GUI (ASTM-style)
# =====================================================
with gr.Blocks(title="ASTM Volume & Weight Converter") as demo:
    gr.Markdown(
        """
        ## ⚖️ ASTM D1250 — Volume & Weight Converter  
        *Excel-style interface powered by Fuel MCP ISO 91-1 computational engine*
        """
    )

    with gr.Row():
        table = gr.Dropdown(["54A", "54B", "54C"], label="ASTM Table", value="54B")
        temp_unit = gr.Radio(["°C", "°F"], label="Temperature Unit", value="°C")

    with gr.Row():
        rho15 = gr.Number(label="Density @15°C (kg/m³)", value=796.7)
        temp_obs = gr.Number(label="Observed Temperature", value=22.6)

    with gr.Row():
        from_unit = gr.Dropdown(
            [
                "BBLS @Temp.",
                "BBLS @60°F",
                "M3 @Temp.",
                "M3 @15°C",
                "Long Tons",
                "Short Tons",
                "Metric Tonnes (Air)",
                "Metric Tonnes (Vac)",
                "US Gallons @60°F",
            ],
            label="From Unit",
            value="M3 @15°C",
        )
        to_unit = gr.Dropdown(
            [
                "BBLS @Temp.",
                "BBLS @60°F",
                "M3 @Temp.",
                "M3 @15°C",
                "Long Tons",
                "Short Tons",
                "Metric Tonnes (Air)",
                "Metric Tonnes (Vac)",
                "US Gallons @60°F",
            ],
            label="To Unit",
            value="US Gallons @60°F",
        )

    with gr.Row():
        value = gr.Number(label="Value to Convert", value=2941)
        output = gr.Dataframe(
            headers=["Parameter", "Value"],
            label="Calculated ASTM Conversion Result",
            wrap=True,
        )

    def wrapper(table, temp_unit, rho15, temp_obs, from_unit, to_unit, value):
        result = convert_units(
            table, temp_unit, rho15, temp_obs, from_unit, to_unit, value
        )
        if "Error" in result:
            return [["Error", result["Error"]]]
        return [[k, v] for k, v in result.items()]

    gr.Button("Compute ASTM Conversion → Display").click(
        wrapper,
        inputs=[table, temp_unit, rho15, temp_obs, from_unit, to_unit, value],
        outputs=output,
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7864)