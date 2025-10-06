# System Architecture

## Overview

PROJECT NIV is a modern full-stack data analysis platform built with Next.js 14 and FastAPI, featuring a professional TypeScript/TSX frontend and a robust Python backend.

## Technology Stack

### Frontend (Next.js 14)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript 5.0+
- **Styling**: TailwindCSS with custom design system
- **UI Components**: ShadCN UI components
- **State Management**: Zustand for global state
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React

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
│ • State Mgmt    │    │ • Data Process  │    │ • Reports       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Data Flow

1. **Data Input** - CSV files uploaded or selected
2. **ETL Processing** - Extract, transform, and load data
3. **API Communication** - Frontend requests data via REST API
4. **Visualization** - Charts and dashboards render data
5. **Export** - Processed data exported in multiple formats

## API Architecture

### RESTful Endpoints
- `GET /api/health` - System health check
- `GET /api/etl-data` - Get processed data and charts
- `POST /api/run-etl` - Execute ETL process
- `GET /api/chart/{type}` - Get specific chart configuration
- `GET /api/data/export` - Export processed data

### Data Models
- **ETLData** - Processed data with metadata
- **ChartConfig** - Chart configuration objects
- **FlowData** - Process flow visualization data

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
- Microservices architecture
- Container orchestration