
"""
app_astm_rel_density.py
=========================
Fuel MCP — ASTM D1250 (Entry with Relative Density)
Calculates VCF (Tables 24A–C) and displays ASTM Volume IV/V/VI → Volume XII equivalents.
"""

import gradio as gr
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/vcf"


def compute_from_rel_density(rel_density, temp_f):
    """Compute ASTM data using MCP backend with relative density input."""
    try:
        # Convert relative density → density @15°C
        rho15 = rel_density * 999.016
        temp_c = (temp_f - 32) * 5 / 9

        # Query MCP backend
        r = requests.get(API_URL, params={"rho15": rho15, "tempC": temp_c}, timeout=10)
        data = r.json().get("result", {})

        # --- Core base results ---
        density_15 = round(data.get("rho15", rho15), 1)
        temp_c_rounded = round(temp_c, 2)
        vcf = round(data.get("VCF", 1.0), 6)

        # Convert density → API (ASTM Table 21)
        api = (141.5 / (density_15 / 999.016) - 131.5)
        api = round(api, 2)

        # --- ASTM Volume XII derived results (reference constants) ---
        table_data = [
            ("T.2 (Temperature Conversion)", f"{temp_c_rounded} °C"),
            ("T.21 (API @15°C)", f"{api:.2f}"),
            ("T.21 (Density @15°C)", f"{density_15:.1f}"),
            ("T.22 (Litres @15°C / US Gallon @60°F)", "3.7837"),
            ("T.22 (Cubic m³/Barrel @60°F)", "0.15893"),
            ("T.26 (Pounds/US Gallon)", "7.2960"),
            ("T.26 (US Gallons/Pound)", "0.13706"),
            ("T.27 (Short Tons/1000 US Gallons)", "3.6479"),
            ("T.27 (Short Tons/Barrel)", "0.15321"),
            ("T.28 (US Gallons/Short Ton)", "274.13"),
            ("T.28 (Barrels/Short Ton)", "6.527"),
            ("T.29 (Long Tons/1000 US Gallons)", "3.2571"),
            ("T.29 (Long Tons/Barrel)", "0.13680"),
            ("T.30 (US Gallons/Long Ton)", "307.02"),
            ("T.30 (Barrels/Long Ton)", "7.310"),
            ("T.31 (Cubic m³/Short Ton)", "1.0373"),
            ("T.31 (Cubic m³/Long Ton)", "1.1617"),
        ]

        # --- Combine with summary block ---
        summary = [
            ("Relative Density (60/60°F)", f"{rel_density:.4f}"),
            ("Temperature (°F)", f"{temp_f:.2f}"),
            ("Temperature (°C)", f"{temp_c_rounded:.2f}"),
            ("Density @15°C (kg/m³)", f"{density_15:.1f}"),
            ("API @15°C", f"{api:.2f}"),
            ("VCF (Table 24A/B/C)", f"{vcf:.6f}"),
            ("ASTM Table", data.get("table", "24B")),
        ]

        df_summary = pd.DataFrame(summary, columns=["Parameter", "Value"])
        df_astm = pd.DataFrame(table_data, columns=["Parameter", "Value"])

        df_full = pd.concat(
            [df_summary, pd.DataFrame([["", ""]], columns=["Parameter", "Value"]), df_astm],
            ignore_index=True,
        )

        return df_full

    except Exception as e:
        return pd.DataFrame([["Error", str(e)]], columns=["Parameter", "Value"])


with gr.Blocks(title="Fuel MCP — ASTM Relative Density") as demo:
    gr.Markdown(
        """
        # 🧩 ASTM D1250-80 — Entry With Relative Density  
        Computes full **ASTM Volume IV/V/VI → Volume XII** equivalents  
        powered by **Fuel MCP ISO 91-1 / ASTM D1250** computational engine.
        """
    )

    with gr.Row():
        rel_density = gr.Number(label="Relative Density (60/60°F)", value=0.8762)
        temp_f = gr.Number(label="Temperature (°F)", value=100)

    btn = gr.Button("Compute ASTM Tables → Display Results")

    output = gr.Dataframe(
        headers=["Parameter", "Value"],
        datatype=["str", "str"],
        interactive=False,
        label="ASTM Volume XII — Reference Tables",
        wrap=True,
    )

    btn.click(fn=compute_from_rel_density, inputs=[rel_density, temp_f], outputs=[output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7862)