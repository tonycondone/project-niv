# Enhancements

## Backend
- Added `/api/upload-csv` for file uploads and ETL run.
- Added `/api/apply-filters` with deterministic row-percentage filtering and updated response (charts, summary, metadata).
- Improved error handling and guarded data access in export and chart generation.

## Frontend
- Added CSV upload UI in `Controls` with hidden file input and `onUpload` handler.
- Added `data-testid` attributes for reliable E2E selectors.
- Jest tests extended for error handling path in `Dashboard`.

## Testing
- Backend pytest suite expanded to cover error cases and transformations, reaching ~86% coverage.
- Playwright E2E expanded with scenarios: load, export, toggle flow, filter, and upload.
- Tooling configured: Jest, ESLint, TypeScript strict checks, Playwright Chromium.

## Build & Quality
- Next.js production build verified.
- Code quality checks: ESLint clean, tsc clean, mypy clean, Black/Flake8 clean.
