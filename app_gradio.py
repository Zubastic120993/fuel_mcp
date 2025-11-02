"""
app_gradio.py — Fuel MCP Gradio GUI (v1.1.1)
--------------------------------------------
Web-based UI for the Fuel MCP API.
Mimics ASTM D1250 calculator layout in browser form.
"""

import requests
import gradio as gr

API_BASE = "http://127.0.0.1:8000"


def query_mcp(fuel, table, density, temp, from_unit, to_unit, value):
    """
    Calls MCP API and formats output nicely.
    """
    try:
        # Build a natural-language query dynamically
        text = f"convert {value} {fuel} from {from_unit} to {to_unit} @ {temp}C"
        url = f"{API_BASE}/query?text={text}"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}


with gr.Blocks(title="Fuel MCP — ASTM Converter") as demo:
    gr.Markdown("# 🧩 Fuel MCP — ASTM D1250 Conversion Panel")
    gr.Markdown("### Interactive ASTM-style converter for density, volume, and mass corrections")

    with gr.Row():
        with gr.Column():
            fuel = gr.Dropdown(
                ["diesel", "hfo", "mgo", "lpg", "lng", "methanol"],
                label="Fuel Type",
                value="diesel"
            )
            table = gr.Dropdown(["54A", "54B", "54C"], label="ASTM Table", value="54B")
            density = gr.Number(label="Density @15°C (kg/m³)", value=850)
            temp = gr.Number(label="Observed Temp (°C)", value=25)
            from_unit = gr.Dropdown(
                ["m³ @ Temp", "m³ @15°C", "tons", "litres", "barrels"],
                label="From Unit",
                value="m³ @ Temp"
            )
            to_unit = gr.Dropdown(
                ["m³ @15°C", "tons", "litres", "barrels"],
                label="To Unit",
                value="tons"
            )
            value = gr.Number(label="Value to Convert", value=1000)
            convert_btn = gr.Button("🚀 Calculate")

        with gr.Column():
            gr.Markdown("### Result Output")
            api_response = gr.JSON(label="API Response")

    convert_btn.click(
        fn=query_mcp,
        inputs=[fuel, table, density, temp, from_unit, to_unit, value],
        outputs=[api_response]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)