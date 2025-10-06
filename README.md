# PROJECT NIV

**Professional Data Analysis & Visualization Platform**

A modern full-stack application for ETL processing and data visualization built with Next.js and Python.

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://typescriptlang.org)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red)](https://fastapi.tiangolo.com)

## Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.12+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tonycondone/project-niv.git
   cd project-niv
   ```

2. **Install dependencies**
   ```bash
   # Frontend
   npm install
   
   # Backend
   pip install -r backend/requirements.txt
   ```

3. **Start the application**
   ```bash
   # Development (both frontend and backend)
   npm run full:dev
   
   # Or start separately:
   # Frontend: npm run dev
   # Backend: npm run backend
   ```

4. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Features

### Data Processing
- **ETL Pipeline** - Extract, transform, and load CSV data
- **Advanced Filtering** - Range, value, and custom filters
- **Data Transformations** - Normalization, standardization, log transforms
- **Multiple Formats** - Excel, JSON, CSV export

### Visualization
- **Interactive Charts** - Line, bar, area, pie, scatter plots
- **Real-time Updates** - Live data processing and visualization
- **Process Flow** - Visual ETL pipeline representation
- **Responsive Design** - Works on desktop, tablet, and mobile

### Dashboard
- **Professional Interface** - Modern black and neon blue theme
- **Summary Cards** - Key metrics at a glance
- **Interactive Controls** - Refresh, export, and filter data
- **Error Handling** - Graceful error states and recovery

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health check |
| `/api/etl-data` | GET | Get processed data and charts |
| `/api/run-etl` | POST | Execute ETL process |
| `/api/chart/{type}` | GET | Get specific chart configuration |
| `/api/data/export` | GET | Export processed data |

## Project Structure

```
project-niv/
├── src/                    # Next.js frontend
│   ├── app/               # Pages and layouts
│   ├── components/        # React components
│   └── lib/               # Utility functions
├── backend/               # Python FastAPI backend
│   ├── main.py           # FastAPI application
│   └── requirements.txt  # Python dependencies
├── data/                 # Sample data files
└── docs/                 # Documentation
```

## Development

### Frontend Development
```bash
npm run dev          # Start Next.js development server
npm run build        # Build for production
npm run type-check   # TypeScript type checking
npm run lint         # ESLint checking
```

### Backend Development
```bash
npm run backend      # Start FastAPI development server
npm run install:backend  # Install Python dependencies
```

### Full Stack Development
```bash
npm run full:dev     # Start both frontend and backend
npm run full:build   # Build both frontend and backend
```

## Technology Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **TailwindCSS** - Utility-first CSS framework
- **Recharts** - Data visualization
- **ShadCN UI** - Modern UI components

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **OpenPyXL** - Excel file handling

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/tonycondone/project-niv/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tonycondone/project-niv/discussions)

---

**Made with ❤️ by [Tony Condone](https://github.com/tonycondone)**