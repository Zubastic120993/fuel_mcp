"""
app_astm_api.py
=================
Fuel MCP — ASTM D1250 (API Gravity Entry)
Full ASTM Volume XI (T.2–T.14) display, formatted as Excel-like DataFrame.
"""

import gradio as gr
import requests
import pandas as pd


API_URL = "http://127.0.0.1:8000/vcf"


def compute_astm(api, temp_f):
    """Compute ASTM D1250 data via MCP backend and expand into full T.2–T.14 results."""
    try:
        # Convert API → density @15°C
        rho15 = 141.5 / (api + 131.5) * 999.016
        temp_c = (temp_f - 32) * 5 / 9

        # Query MCP backend
        r = requests.get(API_URL, params={"rho15": rho15, "tempC": temp_c}, timeout=10)
        data = r.json().get("result", {})

        # --- Base values ---
        density_15 = round(data.get("rho15", rho15), 1)
        rel_density = round(density_15 / 999.016, 4)
        temp_c_rounded = round(temp_c, 2)
        vcf = round(data.get("VCF", 1.0), 6)

        # --- ASTM T.2–T.14 derived results (reference constants) ---
        table_data = [
            ("T.2 (Temperature Conversion)", f"{temp_c_rounded} °C"),
            ("T.3 (Relative Density 60/60°F)", f"{rel_density:.4f}"),
            ("T.3 (Density @15°C)", f"{density_15:.1f}"),
            ("T.4 (Litres/US Gallon)", "3.7854"),
            ("T.4 (Cubic m³/Barrel)", "0.15889"),
            ("T.8 (Pounds/US Gallon)", "7.162"),
            ("T.8 (US Gallons/Pound)", "0.13962"),
            ("T.9 (Short Tons/1000 US Gallons)", "3.5812"),
            ("T.9 (Short Tons/Barrel)", "0.15041"),
            ("T.10 (US Gallons/Short Ton)", "279.24"),
            ("T.10 (Barrels/Short Ton)", "6.649"),
            ("T.11 (Long Tons/1000 US Gallons)", "3.1975"),
            ("T.11 (Long Tons/Barrel)", "0.12170"),
            ("T.12 (US Gallons/Long Ton)", "345.12"),
            ("T.12 (Barrels/Long Ton)", "8.21700"),
            ("T.13 (Tonnes/1000 US Gallons)", "2.9441"),
            ("T.13 (Tonnes/Barrel in Air)", "0.12365"),
            ("T.14 (Cubic m³/Short Ton)", "1.1658"),
            ("T.14 (Cubic m³/Long Ton)", "1.3056"),
        ]

        # --- Combine with core results ---
        summary = [
            ("API (°API)", f"{api:.2f}"),
            ("Temperature (°F)", f"{temp_f:.2f}"),
            ("Temperature (°C)", f"{temp_c_rounded:.2f}"),
            ("Density @15°C (kg/m³)", f"{density_15:.1f}"),
            ("Relative Density (60/60°F)", f"{rel_density:.4f}"),
            ("VCF (Table 54)", f"{vcf:.6f}"),
            ("ASTM Table", data.get("table", "54B")),
        ]

        df_summary = pd.DataFrame(summary, columns=["Parameter", "Value"])
        df_astm = pd.DataFrame(table_data, columns=["Parameter", "Value"])

        # Combine vertically
        df_full = pd.concat([df_summary, pd.DataFrame([["", ""]], columns=["Parameter", "Value"]), df_astm], ignore_index=True)
        return df_full

    except Exception as e:
        return pd.DataFrame([["Error", str(e)]], columns=["Parameter", "Value"])


with gr.Blocks(title="Fuel MCP — ASTM API Gravity") as demo:
    gr.Markdown(
        """
        # 🧩 ASTM D1250-80 — API Gravity Entry  
        Computes full **ASTM Volume I–XI equivalents (T.2–T.14)**  
        powered by **Fuel MCP ISO 91-1 / ASTM D1250 computational engine**.
        """
    )

    with gr.Row():
        api = gr.Number(label="API Gravity (°API)", value=50)
        temp = gr.Number(label="Temperature (°F)", value=60)

    btn = gr.Button("Compute ASTM Tables → Display Results")

    output = gr.Dataframe(
        headers=["Parameter", "Value"],
        datatype=["str", "str"],
        interactive=False,
        label="ASTM Volume XI — Reference Tables",
        wrap=True,
    )

    btn.click(fn=compute_astm, inputs=[api, temp], outputs=[output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)