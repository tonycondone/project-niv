# API Reference

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required. All endpoints are publicly accessible.

## Endpoints

### Health Check

#### GET /api/health
Check system health and status.

**Response:**
```json
{
  "status": "healthy",
  "etl_processor": "ready",
  "data_available": true
}
```

### ETL Data

#### GET /api/etl-data
Get processed ETL data and chart configurations.

**Response:**
```json
{
  "summary": {
    "original_rows": 100,
    "processed_rows": 95,
    "columns": 7
  },
  "chart_configs": {
    "line": { /* ApexCharts config */ },
    "bar": { /* ApexCharts config */ },
    "area": { /* ApexCharts config */ },
    "pie": { /* ApexCharts config */ }
  },
  "flow_data": {
    "nodes": [
      {
        "id": "extract",
        "label": "Extract Data",
        "status": "completed"
      }
    ],
    "edges": [
      {
        "from": "extract",
        "to": "transform"
      }
    ]
  },
  "metadata": { /* Processing metadata */ }
}
```

### Run ETL Process

#### POST /api/run-etl
Execute ETL process on specified data.

**Request Body:**
```json
{
  "csv_file": "sample_detailed.csv",
  "filters": {
    "Sales": {
      "min": 1000,
      "max": 5000
    },
    "Category": ["Electronics", "Hardware"]
  },
  "transformations": ["normalize", "standardize"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "ETL process completed successfully",
  "results": {
    "summary": { /* Data summary */ },
    "chart_configs": { /* Chart configurations */ },
    "output_files": { /* Generated files */ }
  }
}
```

### Chart Configuration

#### GET /api/chart/{chart_type}
Get specific chart configuration.

**Parameters:**
- `chart_type` (string): Type of chart (line, bar, area, pie, scatter)

**Response:**
```json
{
  "chart": {
    "type": "line",
    "height": 350,
    "background": "transparent"
  },
  "series": [
    {
      "name": "Sales",
      "data": [/* Chart data points */]
    }
  ],
  "xaxis": {
    "title": { "text": "Date" }
  },
  "yaxis": {
    "title": { "text": "Sales" }
  }
}
```

### Flow Chart

#### GET /api/flow-chart
Get ETL process flow chart data.

**Response:**
```json
{
  "nodes": [
    {
      "id": "extract",
      "label": "Extract Data",
      "status": "completed"
    },
    {
      "id": "transform",
      "label": "Transform Data",
      "status": "completed"
    },
    {
      "id": "load",
      "label": "Load Data",
      "status": "completed"
    }
  ],
  "edges": [
    {
      "from": "extract",
      "to": "transform"
    },
    {
      "from": "transform",
      "to": "load"
    }
  ]
}
```

### Data Export

#### GET /api/data/export
Export processed data as CSV file.

**Response:**
- Content-Type: `text/csv`
- File download with processed data

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently no rate limiting implemented. Consider implementing for production use.

## CORS

CORS is configured to allow requests from:
- `http://localhost:3000` (Next.js development)
- `http://127.0.0.1:3000` (Next.js development)

## Examples

### Frontend Integration

```typescript
// Get ETL data
const response = await fetch('/api/backend/etl-data');
const data = await response.json();

// Run ETL process
const etlResponse = await fetch('/api/backend/run-etl', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    csv_file: 'data.csv',
    filters: { Sales: { min: 1000 } }
  })
});
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/api/health

# Get ETL data
curl http://localhost:8000/api/etl-data

# Run ETL process
curl -X POST http://localhost:8000/api/run-etl \
  -H "Content-Type: application/json" \
  -d '{"csv_file": "sample.csv"}'
```