/**
 * PROJECT NIV - ETL Data Visualization Dashboard
 * TypeScript implementation with SVG support
 */

// Types and Interfaces
interface ETLSummary {
    original_rows: number;
    processed_rows: number;
    columns: number;
}

interface ChartConfig {
    title?: {
        text: string;
    };
    series: any[];
    xaxis?: any;
    yaxis?: any;
    chart?: any;
    [key: string]: any;
}

interface ETLData {
    chart_configs: { [key: string]: ChartConfig };
    flow_data: FlowData;
    summary: ETLSummary;
    metadata: any;
}

interface FlowData {
    nodes: FlowNode[];
    edges: FlowEdge[];
}

interface FlowNode {
    id: string;
    label: string;
    status: 'completed' | 'pending' | 'error';
}

interface FlowEdge {
    from: string;
    to: string;
    label?: string;
}

// Chart Types
type ChartType = 'line' | 'bar' | 'area' | 'pie' | 'scatter';

// Main Dashboard Class
class ETLDashboard {
    private chartInstances: ApexCharts[] = [];
    private etlData: ETLData | null = null;
    private isFlowChartVisible: boolean = false;

    constructor() {
        this.initializeMermaid();
        this.setupEventListeners();
        this.loadETLData();
    }

    /**
     * Initialize Mermaid for flow charts
     */
    private initializeMermaid(): void {
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                startOnLoad: true,
                theme: 'default',
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true
                }
            });
        }
    }

    /**
     * Setup event listeners
     */
    private setupEventListeners(): void {
        document.addEventListener('DOMContentLoaded', () => {
            this.loadETLData();
        });

        window.addEventListener('resize', () => {
            this.resizeCharts();
        });
    }

    /**
     * Load ETL data from the API
     */
    private async loadETLData(): Promise<void> {
        try {
            const response = await fetch('/api/etl-data');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            this.etlData = await response.json();
            this.updateSummary(this.etlData.summary);
            this.generateCharts(this.etlData.chart_configs);
            this.updateFlowChart(this.etlData.flow_data);
            
        } catch (error) {
            console.error('Error loading ETL data:', error);
            this.showError(`Failed to load ETL data: ${error.message}`);
        }
    }

    /**
     * Update summary cards
     */
    private updateSummary(summary: ETLSummary): void {
        const elements = {
            'original-rows': summary.original_rows || 0,
            'processed-rows': summary.processed_rows || 0,
            'columns': summary.columns || 0,
            'charts-count': Object.keys(this.etlData?.chart_configs || {}).length
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value.toString();
            }
        });
    }

    /**
     * Generate all charts
     */
    private generateCharts(chartConfigs: { [key: string]: ChartConfig }): void {
        const container = document.getElementById('charts-container');
        if (!container) return;

        container.innerHTML = '';

        if (!chartConfigs || Object.keys(chartConfigs).length === 0) {
            container.innerHTML = '<div class="error">No chart configurations available</div>';
            return;
        }

        Object.entries(chartConfigs).forEach(([chartType, config]) => {
            this.createChartContainer(chartType, config, container);
        });
    }

    /**
     * Create individual chart container
     */
    private createChartContainer(chartType: string, config: ChartConfig, container: HTMLElement): void {
        const chartDiv = document.createElement('div');
        chartDiv.className = 'chart-container';
        
        const title = config.title?.text || chartType.charAt(0).toUpperCase() + chartType.slice(1);
        chartDiv.innerHTML = `
            <div class="chart-title">${title} Chart</div>
            <div id="chart-${chartType}"></div>
        `;
        
        container.appendChild(chartDiv);
        
        // Create ApexCharts instance
        const chartElement = document.querySelector(`#chart-${chartType}`) as HTMLElement;
        if (chartElement) {
            const chart = new ApexCharts(chartElement, config);
            this.chartInstances.push(chart);
            chart.render();
        }
    }

    /**
     * Update flow chart with SVG support
     */
    private updateFlowChart(flowData: FlowData): void {
        if (!flowData) return;

        const flowChartElement = document.getElementById('flow-chart');
        if (!flowChartElement) return;

        // Generate SVG flow chart
        const svgContent = this.generateSVGFlowChart(flowData);
        flowChartElement.innerHTML = svgContent;
    }

    /**
     * Generate SVG flow chart
     */
    private generateSVGFlowChart(flowData: FlowData): string {
        const width = 800;
        const height = 400;
        const nodeWidth = 120;
        const nodeHeight = 60;
        const padding = 20;

        let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`;
        
        // Define styles
        svg += `
            <defs>
                <style>
                    .node { fill: #667eea; stroke: #5a6fd8; stroke-width: 2; }
                    .node.completed { fill: #4caf50; }
                    .node.pending { fill: #ff9800; }
                    .node.error { fill: #f44336; }
                    .node-text { fill: white; font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; }
                    .edge { stroke: #333; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
                    .edge-label { fill: #666; font-family: Arial, sans-serif; font-size: 10px; text-anchor: middle; }
                </style>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
                </marker>
            </defs>
        `;

        // Calculate node positions
        const nodePositions: { [key: string]: { x: number; y: number } } = {};
        const nodesPerRow = Math.ceil(Math.sqrt(flowData.nodes.length));
        const rowHeight = (height - 2 * padding) / Math.ceil(flowData.nodes.length / nodesPerRow);

        flowData.nodes.forEach((node, index) => {
            const row = Math.floor(index / nodesPerRow);
            const col = index % nodesPerRow;
            const x = padding + col * (nodeWidth + 50);
            const y = padding + row * (nodeHeight + 30);
            nodePositions[node.id] = { x, y };
        });

        // Draw edges first (so they appear behind nodes)
        flowData.edges.forEach(edge => {
            const fromPos = nodePositions[edge.from];
            const toPos = nodePositions[edge.to];
            
            if (fromPos && toPos) {
                const startX = fromPos.x + nodeWidth / 2;
                const startY = fromPos.y + nodeHeight;
                const endX = toPos.x + nodeWidth / 2;
                const endY = toPos.y;
                
                svg += `<line x1="${startX}" y1="${startY}" x2="${endX}" y2="${endY}" class="edge" />`;
                
                // Add edge label if provided
                if (edge.label) {
                    const labelX = (startX + endX) / 2;
                    const labelY = (startY + endY) / 2;
                    svg += `<text x="${labelX}" y="${labelY}" class="edge-label">${edge.label}</text>`;
                }
            }
        });

        // Draw nodes
        flowData.nodes.forEach(node => {
            const pos = nodePositions[node.id];
            if (pos) {
                const statusClass = node.status === 'completed' ? 'completed' : 
                                  node.status === 'error' ? 'error' : 'pending';
                const statusIcon = node.status === 'completed' ? '✅' : 
                                 node.status === 'error' ? '❌' : '⏳';
                
                svg += `
                    <rect x="${pos.x}" y="${pos.y}" width="${nodeWidth}" height="${nodeHeight}" 
                          rx="8" ry="8" class="node ${statusClass}" />
                    <text x="${pos.x + nodeWidth/2}" y="${pos.y + nodeHeight/2 - 5}" class="node-text">
                        ${statusIcon} ${node.label}
                    </text>
                `;
            }
        });

        svg += '</svg>';
        return svg;
    }

    /**
     * Toggle flow chart visibility
     */
    public toggleFlowChart(): void {
        const flowChartContainer = document.getElementById('flow-chart-container');
        if (flowChartContainer) {
            this.isFlowChartVisible = !this.isFlowChartVisible;
            flowChartContainer.classList.toggle('hidden', !this.isFlowChartVisible);
        }
    }

    /**
     * Refresh all charts
     */
    public refreshCharts(): void {
        this.chartInstances.forEach(chart => {
            chart.updateOptions({
                chart: {
                    animations: {
                        enabled: true,
                        easing: 'easeinout',
                        speed: 800
                    }
                }
            });
        });
    }

    /**
     * Export data
     */
    public async exportData(): Promise<void> {
        if (!this.etlData) {
            this.showError('No data available to export');
            return;
        }

        try {
            const response = await fetch('/api/data/export');
            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'etl_data_export.csv';
                link.click();
                URL.revokeObjectURL(url);
            } else {
                throw new Error('Export failed');
            }
        } catch (error) {
            console.error('Export error:', error);
            this.showError('Failed to export data');
        }
    }

    /**
     * Resize all charts
     */
    private resizeCharts(): void {
        this.chartInstances.forEach(chart => {
            chart.resize();
        });
    }

    /**
     * Show error message
     */
    private showError(message: string): void {
        const container = document.getElementById('charts-container');
        if (container) {
            container.innerHTML = `<div class="error">${message}</div>`;
        }
    }

    /**
     * Run ETL process
     */
    public async runETL(csvFile: string, filters?: any, transformations?: string[]): Promise<void> {
        try {
            const response = await fetch('/api/run-etl', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    csv_file: csvFile,
                    filters: filters,
                    transformations: transformations
                })
            });

            if (response.ok) {
                // Reload data after successful ETL
                await this.loadETLData();
            } else {
                throw new Error('ETL process failed');
            }
        } catch (error) {
            console.error('ETL error:', error);
            this.showError('Failed to run ETL process');
        }
    }
}

// Global dashboard instance
let dashboard: ETLDashboard;

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new ETLDashboard();
});

// Global functions for HTML onclick handlers
function refreshCharts(): void {
    dashboard?.refreshCharts();
}

function exportData(): void {
    dashboard?.exportData();
}

function toggleFlowChart(): void {
    dashboard?.toggleFlowChart();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ETLDashboard };
}