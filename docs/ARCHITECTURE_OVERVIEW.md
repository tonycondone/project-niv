# Architecture Overview

## System Architecture

PROJECT NIV is a modern full-stack data analysis platform built with Next.js 14 and FastAPI, featuring a professional TypeScript/TSX frontend and a robust Python backend. The system is designed as a **data analysis tool** focused on ETL processing and visualization.

## Technology Stack

### Frontend (Next.js 14)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript 5.0+
- **Styling**: TailwindCSS with custom design system
- **UI Components**: ShadCN UI components
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React
- **State Management**: React hooks (no complex state management needed for analysis tool)

### Backend (FastAPI)
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.12+
- **Data Processing**: Pandas, NumPy
- **File Handling**: OpenPyXL for Excel files
- **Server**: Uvicorn ASGI server
- **Validation**: Pydantic for data validation

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Data Layer    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (CSV Files)   │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • ETL Engine    │    │ • Sample Data   │
│ • Charts        │    │ • API Endpoints │    │ • User Data     │
│ • Simple State  │    │ • Data Process  │    │ • Reports       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Data Flow

1. **Data Input** - CSV files uploaded or selected from sample data
2. **ETL Processing** - Extract, transform, and load data using Pandas
3. **API Communication** - Frontend requests data via REST API
4. **Visualization** - Charts and dashboards render data using Recharts
5. **Export** - Processed data exported in multiple formats

## API Architecture

### RESTful Endpoints
- `GET /api/health` - System health check
- `GET /api/etl-data` - Get processed data and chart configurations
- `POST /api/run-etl` - Execute ETL process
- `GET /api/chart/{type}` - Get specific chart configuration
- `GET /api/flow-chart` - Process flow visualization data
- `GET /api/data/export` - Export processed data

### Data Models
- **ETLData** - Processed data with metadata
- **ChartConfig** - Chart configuration objects
- **FlowData** - Process flow visualization data

## Key Design Decisions

### Why Remove Zustand?
- **Analysis Tool Focus**: Simple state management sufficient for data processing
- **Reduced Complexity**: No need for complex global state management
- **Performance**: Lighter bundle size for better performance
- **Simplicity**: Easier to understand and maintain for data analysts

### Why Next.js + FastAPI?
- **Next.js**: Modern React framework with excellent TypeScript support
- **FastAPI**: Best-in-class Python web framework with automatic documentation
- **Separation of Concerns**: Clear frontend/backend separation
- **Type Safety**: Full TypeScript implementation for reliability

## Component Architecture

### Frontend Components
```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/             # React components
│   ├── dashboard/         # Dashboard components
│   │   ├── dashboard.tsx  # Main dashboard
│   │   ├── summary-cards.tsx
│   │   ├── charts-grid.tsx
│   │   ├── controls.tsx
│   │   ├── flow-chart.tsx
│   │   └── loading-spinner.tsx
│   ├── layout/            # Layout components
│   │   ├── header.tsx
│   │   └── sidebar.tsx
│   └── ui/                # Reusable UI components
│       ├── button.tsx
│       ├── card.tsx
│       └── badge.tsx
├── lib/                   # Utility functions
│   └── utils.ts
└── api/                   # API integration (future)
```

### Backend Structure
```
backend/
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
└── (future modules)      # Additional backend modules
```

## Security

### Frontend Security
- Input validation and sanitization
- XSS protection via React
- CSRF protection via SameSite cookies

### Backend Security
- Input validation with Pydantic
- CORS configuration for allowed origins
- Error message sanitization

## Performance

### Frontend Optimizations
- Next.js automatic code splitting
- Image optimization
- Static generation where possible
- Lazy loading of components
- No unnecessary state management overhead

### Backend Optimizations
- Pandas vectorized operations
- Memory-efficient data processing
- Chunked processing for large datasets
- Caching of processed results

## Scalability

### Horizontal Scaling
- Frontend can be deployed to CDN
- Backend can be containerized and scaled
- Database integration ready for future

### Future Enhancements
- Real-time WebSocket updates
- Database integration
- Advanced analytics
- Machine learning integration

## Development Workflow

### Local Development
```bash
# Frontend development
npm run dev

# Backend development
npm run backend

# Full stack development
npm run full:dev
```

### Production Build
```bash
# Build frontend
npm run build

# Install backend dependencies
npm run install:backend

# Start production servers
npm run start
npm run backend:prod
```

## Interpreted Logic from Original System

### Preserved ETL Processing
- **Data Extraction**: CSV file reading with encoding detection
- **Data Transformation**: Normalization, standardization, log transforms
- **Data Filtering**: Range filters, value filters, custom conditions
- **Data Loading**: Export to multiple formats (Excel, JSON, CSV)

### Preserved Visualization
- **Chart Generation**: Interactive charts for data analysis
- **Process Flow**: Visual ETL pipeline representation
- **Real-time Updates**: Live data processing and visualization
- **Export Capabilities**: Download charts and processed data

### Modernized Architecture
- **Type Safety**: Full TypeScript implementation
- **Modern UI**: Professional dashboard with TailwindCSS
- **API-First**: RESTful API for all operations
- **Component-Based**: Reusable React components
- **Performance**: Optimized for data analysis workflows

This architecture provides a solid foundation for a professional data analysis tool while maintaining the core ETL processing capabilities from the original system.