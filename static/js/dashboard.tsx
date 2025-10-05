/**
 * PROJECT NIV - Data Analysis Dashboard
 * TSX Component with Black, White, and Light Neon Blue Theme
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

interface DashboardState {
    etlData: ETLData | null;
    loading: boolean;
    error: string | null;
    flowChartVisible: boolean;
    selectedChart: string | null;
}

// Color Theme
const THEME = {
    primary: '#00D4FF',      // Light neon blue
    secondary: '#0099CC',    // Darker neon blue
    background: '#0A0A0A',   // Deep black
    surface: '#1A1A1A',      // Dark gray
    surfaceLight: '#2A2A2A', // Lighter gray
    text: '#FFFFFF',         // White
    textSecondary: '#B0B0B0', // Light gray
    accent: '#00FF88',       // Neon green accent
    warning: '#FFB800',      // Neon yellow
    error: '#FF4444',        // Neon red
    border: '#333333',       // Dark border
    gradient: 'linear-gradient(135deg, #00D4FF 0%, #0099CC 100%)',
    shadow: '0 8px 32px rgba(0, 212, 255, 0.1)',
    glow: '0 0 20px rgba(0, 212, 255, 0.3)'
};

// TSX Dashboard Component
class DataAnalysisDashboard {
    private state: DashboardState;
    private chartInstances: ApexCharts[] = [];
    private container: HTMLElement;

    constructor(containerId: string) {
        this.container = document.getElementById(containerId) || document.body;
        this.state = {
            etlData: null,
            loading: true,
            error: null,
            flowChartVisible: false,
            selectedChart: null
        };
        
        this.init();
    }

    private init(): void {
        this.render();
        this.loadETLData();
        this.setupEventListeners();
    }

    private render(): void {
        this.container.innerHTML = this.renderDashboard();
        this.initializeCharts();
    }

    private renderDashboard(): string {
        return `
            <div class="dashboard" style="${this.getDashboardStyles()}">
                ${this.renderHeader()}
                ${this.renderSummaryCards()}
                ${this.renderControls()}
                ${this.renderFlowChart()}
                ${this.renderChartsGrid()}
                ${this.renderLoadingOverlay()}
            </div>
        `;
    }

    private renderHeader(): string {
        return `
            <header class="dashboard-header" style="${this.getHeaderStyles()}">
                <div class="header-content">
                    <div class="logo-section">
                        <div class="logo-icon">📊</div>
                        <div class="logo-text">
                            <h1>PROJECT NIV</h1>
                            <p>Data Analysis Dashboard</p>
                        </div>
                    </div>
                    <div class="header-actions">
                        <div class="status-indicator ${this.state.loading ? 'loading' : 'ready'}">
                            <div class="status-dot"></div>
                            <span>${this.state.loading ? 'Processing...' : 'Ready'}</span>
                        </div>
                    </div>
                </div>
            </header>
        `;
    }

    private renderSummaryCards(): string {
        if (!this.state.etlData) return '';

        const { summary } = this.state.etlData;
        return `
            <section class="summary-section" style="${this.getSummaryStyles()}">
                <div class="summary-card" style="${this.getCardStyles()}">
                    <div class="card-icon">📈</div>
                    <div class="card-content">
                        <h3>Original Data</h3>
                        <div class="card-value">${summary.original_rows.toLocaleString()}</div>
                        <div class="card-label">rows</div>
                    </div>
                </div>
                <div class="summary-card" style="${this.getCardStyles()}">
                    <div class="card-icon">🔄</div>
                    <div class="card-content">
                        <h3>Processed</h3>
                        <div class="card-value">${summary.processed_rows.toLocaleString()}</div>
                        <div class="card-label">rows</div>
                    </div>
                </div>
                <div class="summary-card" style="${this.getCardStyles()}">
                    <div class="card-icon">📋</div>
                    <div class="card-content">
                        <h3>Columns</h3>
                        <div class="card-value">${summary.columns}</div>
                        <div class="card-label">fields</div>
                    </div>
                </div>
                <div class="summary-card" style="${this.getCardStyles()}">
                    <div class="card-icon">📊</div>
                    <div class="card-content">
                        <h3>Charts</h3>
                        <div class="card-value">${Object.keys(this.state.etlData.chart_configs || {}).length}</div>
                        <div class="card-label">visualizations</div>
                    </div>
                </div>
            </section>
        `;
    }

    private renderControls(): string {
        return `
            <section class="controls-section" style="${this.getControlsStyles()}">
                <div class="control-group">
                    <button class="control-btn primary" onclick="dashboard.refreshCharts()" style="${this.getButtonStyles()}">
                        <span class="btn-icon">🔄</span>
                        Refresh Data
                    </button>
                    <button class="control-btn secondary" onclick="dashboard.exportData()" style="${this.getButtonStyles('secondary')}">
                        <span class="btn-icon">📥</span>
                        Export Data
                    </button>
                    <button class="control-btn secondary" onclick="dashboard.toggleFlowChart()" style="${this.getButtonStyles('secondary')}">
                        <span class="btn-icon">🔄</span>
                        Process Flow
                    </button>
                </div>
                <div class="chart-selector">
                    <label>Chart Type:</label>
                    <select onchange="dashboard.selectChart(this.value)" style="${this.getSelectStyles()}">
                        <option value="">All Charts</option>
                        <option value="line">Line Chart</option>
                        <option value="bar">Bar Chart</option>
                        <option value="area">Area Chart</option>
                        <option value="pie">Pie Chart</option>
                    </select>
                </div>
            </section>
        `;
    }

    private renderFlowChart(): string {
        if (!this.state.flowChartVisible || !this.state.etlData) return '';

        return `
            <section class="flow-chart-section" style="${this.getFlowChartStyles()}">
                <div class="section-header">
                    <h2>ETL Process Flow</h2>
                    <button class="close-btn" onclick="dashboard.toggleFlowChart()">×</button>
                </div>
                <div class="flow-chart-container">
                    ${this.generateSVGFlowChart(this.state.etlData.flow_data)}
                </div>
            </section>
        `;
    }

    private renderChartsGrid(): string {
        if (!this.state.etlData) {
            return `
                <section class="charts-section" style="${this.getChartsStyles()}">
                    <div class="no-data">
                        <div class="no-data-icon">📊</div>
                        <h3>No Data Available</h3>
                        <p>Load data to see visualizations</p>
                    </div>
                </section>
            `;
        }

        const charts = Object.entries(this.state.etlData.chart_configs);
        const filteredCharts = this.state.selectedChart 
            ? charts.filter(([type]) => type === this.state.selectedChart)
            : charts;

        return `
            <section class="charts-section" style="${this.getChartsStyles()}">
                <div class="charts-grid">
                    ${filteredCharts.map(([chartType, config]) => `
                        <div class="chart-container" data-chart-type="${chartType}" style="${this.getChartContainerStyles()}">
                            <div class="chart-header">
                                <h3>${config.title?.text || chartType.charAt(0).toUpperCase() + chartType.slice(1)}</h3>
                                <div class="chart-actions">
                                    <button class="chart-btn" onclick="dashboard.fullscreenChart('${chartType}')">⛶</button>
                                </div>
                            </div>
                            <div class="chart-content" id="chart-${chartType}"></div>
                        </div>
                    `).join('')}
                </div>
            </section>
        `;
    }

    private renderLoadingOverlay(): string {
        if (!this.state.loading) return '';

        return `
            <div class="loading-overlay" style="${this.getLoadingStyles()}">
                <div class="loading-spinner">
                    <div class="spinner-ring"></div>
                    <div class="spinner-ring"></div>
                    <div class="spinner-ring"></div>
                </div>
                <p>Processing data...</p>
            </div>
        `;
    }

    // Style Methods
    private getDashboardStyles(): string {
        return `
            background: ${THEME.background};
            color: ${THEME.text};
            min-height: 100vh;
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
            position: relative;
        `;
    }

    private getHeaderStyles(): string {
        return `
            background: ${THEME.surface};
            border-bottom: 1px solid ${THEME.border};
            padding: 20px 30px;
            backdrop-filter: blur(10px);
        `;
    }

    private getSummaryStyles(): string {
        return `
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: ${THEME.surface};
            margin: 20px;
            border-radius: 12px;
            border: 1px solid ${THEME.border};
        `;
    }

    private getCardStyles(): string {
        return `
            background: ${THEME.surfaceLight};
            border: 1px solid ${THEME.border};
            border-radius: 8px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        `;
    }

    private getControlsStyles(): string {
        return `
            padding: 20px 30px;
            background: ${THEME.surface};
            border-bottom: 1px solid ${THEME.border};
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        `;
    }

    private getButtonStyles(type: 'primary' | 'secondary' = 'primary'): string {
        const isPrimary = type === 'primary';
        return `
            background: ${isPrimary ? THEME.gradient : THEME.surfaceLight};
            color: ${THEME.text};
            border: 1px solid ${isPrimary ? THEME.primary : THEME.border};
            border-radius: 6px;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: ${isPrimary ? THEME.shadow : 'none'};
        `;
    }

    private getSelectStyles(): string {
        return `
            background: ${THEME.surfaceLight};
            color: ${THEME.text};
            border: 1px solid ${THEME.border};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        `;
    }

    private getFlowChartStyles(): string {
        return `
            background: ${THEME.surface};
            margin: 20px;
            border-radius: 12px;
            border: 1px solid ${THEME.border};
            overflow: hidden;
        `;
    }

    private getChartsStyles(): string {
        return `
            padding: 30px;
            background: ${THEME.background};
        `;
    }

    private getChartContainerStyles(): string {
        return `
            background: ${THEME.surface};
            border: 1px solid ${THEME.border};
            border-radius: 8px;
            overflow: hidden;
            transition: all 0.3s ease;
        `;
    }

    private getLoadingStyles(): string {
        return `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(10, 10, 10, 0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            backdrop-filter: blur(5px);
        `;
    }

    // Chart Management
    private initializeCharts(): void {
        if (!this.state.etlData) return;

        Object.entries(this.state.etlData.chart_configs).forEach(([chartType, config]) => {
            const element = document.getElementById(`chart-${chartType}`);
            if (element) {
                const chart = new ApexCharts(element, {
                    ...config,
                    chart: {
                        ...config.chart,
                        background: 'transparent',
                        foreColor: THEME.text,
                        toolbar: {
                            show: true,
                            tools: {
                                download: true,
                                selection: true,
                                zoom: true,
                                zoomin: true,
                                zoomout: true,
                                pan: true,
                                reset: true
                            }
                        }
                    },
                    theme: {
                        mode: 'dark',
                        palette: 'palette1'
                    },
                    colors: [THEME.primary, THEME.secondary, THEME.accent, THEME.warning, THEME.error]
                });
                
                this.chartInstances.push(chart);
                chart.render();
            }
        });
    }

    // SVG Flow Chart Generation
    private generateSVGFlowChart(flowData: FlowData): string {
        const width = 800;
        const height = 400;
        const nodeWidth = 140;
        const nodeHeight = 60;
        const padding = 30;

        let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: auto;">`;
        
        // Define styles
        svg += `
            <defs>
                <style>
                    .node { fill: ${THEME.surfaceLight}; stroke: ${THEME.primary}; stroke-width: 2; }
                    .node.completed { fill: ${THEME.accent}; stroke: ${THEME.accent}; }
                    .node.pending { fill: ${THEME.warning}; stroke: ${THEME.warning}; }
                    .node.error { fill: ${THEME.error}; stroke: ${THEME.error}; }
                    .node-text { fill: ${THEME.text}; font-family: Inter, sans-serif; font-size: 12px; text-anchor: middle; font-weight: 500; }
                    .edge { stroke: ${THEME.primary}; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
                    .edge-label { fill: ${THEME.textSecondary}; font-family: Inter, sans-serif; font-size: 10px; text-anchor: middle; }
                </style>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="${THEME.primary}" />
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

        // Draw edges first
        flowData.edges.forEach(edge => {
            const fromPos = nodePositions[edge.from];
            const toPos = nodePositions[edge.to];
            
            if (fromPos && toPos) {
                const startX = fromPos.x + nodeWidth / 2;
                const startY = fromPos.y + nodeHeight;
                const endX = toPos.x + nodeWidth / 2;
                const endY = toPos.y;
                
                svg += `<line x1="${startX}" y1="${startY}" x2="${endX}" y2="${endY}" class="edge" />`;
                
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

    // Public Methods
    public async loadETLData(): Promise<void> {
        this.setState({ loading: true, error: null });
        
        try {
            const response = await fetch('/api/etl-data');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const etlData = await response.json();
            this.setState({ etlData, loading: false });
            this.render();
            this.initializeCharts();
            
        } catch (error) {
            this.setState({ error: error.message, loading: false });
            console.error('Error loading ETL data:', error);
        }
    }

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

    public async exportData(): Promise<void> {
        if (!this.state.etlData) return;

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
            }
        } catch (error) {
            console.error('Export error:', error);
        }
    }

    public toggleFlowChart(): void {
        this.setState({ flowChartVisible: !this.state.flowChartVisible });
        this.render();
    }

    public selectChart(chartType: string): void {
        this.setState({ selectedChart: chartType || null });
        this.render();
        this.initializeCharts();
    }

    public fullscreenChart(chartType: string): void {
        // Implementation for fullscreen chart view
        console.log('Fullscreen chart:', chartType);
    }

    private setState(newState: Partial<DashboardState>): void {
        this.state = { ...this.state, ...newState };
    }

    private setupEventListeners(): void {
        // Add any additional event listeners here
    }
}

// Global dashboard instance
let dashboard: DataAnalysisDashboard;

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new DataAnalysisDashboard('dashboard-container');
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DataAnalysisDashboard };
}