/**
 * Fuel MCP Custom Node
 * ---------------------
 * Marine Fuel Correction Processor Node for Flowise
 * Performs ISO 91-1 / ASTM D1250 corrections via local MCP API.
 */

class FuelMCPNode {
    constructor() {
        this.label = 'Fuel MCP';
        this.name = 'FuelMCPNode';
        this.type = 'FuelMCPNode';
        this.category = 'Maritime Engineering';
        this.description = 'Performs marine fuel corrections (ISO 91-1 / ASTM D1250) using local MCP API.';
        this.icon = '⚓';
        this.author = 'Chief Engineer Volodymyr Zub';
        this.version = 1.0;
        this.inputs = [
            {
                label: 'Query',
                name: 'query',
                type: 'string',
                placeholder: 'e.g. calculate VCF for diesel at 25°C',
                optional: false,
            },
            {
                label: 'API URL',
                name: 'api_url',
                type: 'string',
                default: 'http://127.0.0.1:8000/query',
                optional: true,
            },
        ];
        this.outputs = [
            {
                label: 'Result',
                name: 'result',
                type: 'json',
            },
        ];
    }

    // 🚀 Execution logic
    async run(nodeData) {
        const query = nodeData.inputs?.query;
        const apiUrl = nodeData.inputs?.api_url || 'http://127.0.0.1:8000/query';
        const fetch = (await import('node-fetch')).default;

        const url = new URL(apiUrl);
        url.searchParams.append('text', query);

        const res = await fetch(url);
        if (!res.ok) {
            throw new Error(`❌ MCP API returned ${res.status}`);
        }

        const data = await res.json();
        return { result: data };
    }
}

module.exports = { nodeClass: FuelMCPNode };