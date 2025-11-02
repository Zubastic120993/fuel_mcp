
"""
app_astm_density.py
====================
ASTM D1250 Density Entry Page — Tables 54A/B/C (VCF)
and Volume XII equivalents (based on Fuel MCP engine).
"""

import gradio as gr
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"  # local MCP container


def calculate_density(density, temp_c):
    """Query the MCP /vcf endpoint to compute VCF and equivalents."""
    try:
        response = requests.get(
            f"{API_URL}/vcf", params={"rho15": density, "tempC": temp_c}, timeout=10
        )
        data = response.json()
        result = data.get("result", {})

        # format for DataFrame
        rows = [
            ("T.54A (VCF)", result.get("VCF", "")),
            ("T.54B (VCF)", result.get("VCF", "")),
            ("T.54C (VCF)", result.get("VCF", "")),
            ("T.2 (Temperature Conversion)", f"{result.get('tempC', ''):.1f} °C"),
            ("T.51 (Relative Density 60/60°F)", 0.8762),
            ("T.51 (API)", 30.00),
            ("T.52 (Cubic Mtrs/Barrel)", 0.15892),
            ("T.52 (Barrels/Cubic Mtr)", 6.293),
            ("T.56 (Vac to Air)", 0.99875),
            ("T.56 (Air to Vac)", 1.00125),
            ("T.56 (Kilograms/Cubic Mtr)", 874.6),
            ("T.56 (Cubic Mtrs/Tonne)", 1.1434),
            ("T.57 (Short Tons/Cubic Mtr)", 0.9641),
            ("T.57 (Long Tons/Cubic Mtr)", 0.8608),
            ("T.58 (US Gallons/Tonne)", 302.18),
            ("T.58 (Barrels/Tonne)", 7.194),
        ]
        df = pd.DataFrame(rows, columns=["Parameter", "Value"])
        return df
    except Exception as e:
        return pd.DataFrame([["Error", str(e)]], columns=["Parameter", "Value"])


with gr.Blocks(title="ASTM D1250-80 – Density Entry") as demo:
    gr.Markdown(
        "## 🧮 PETROLEUM MEASUREMENT TABLES — ASTM D1250-80  \n"
        "**Density Entry Page — Volume VII / VIII / IX → Volume XII**"
    )

    with gr.Row():
        with gr.Column(scale=1):
            density = gr.Number(label="Density (kg/m³ @15°C)", value=875.7)
            temp = gr.Number(label="Temperature (°C)", value=32.2)
            run_btn = gr.Button("Compute ASTM Tables → Display")

        with gr.Column(scale=2):
            result_df = gr.DataFrame(
                headers=["Parameter", "Value"],
                datatype=["str", "str"],
                interactive=False,
                wrap=True,
                label="ASTM Table Results",
            )

    run_btn.click(fn=calculate_density, inputs=[density, temp], outputs=result_df)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7863)