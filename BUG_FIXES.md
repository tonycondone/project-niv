# Bug Fixes Summary

- Fixed `backend/requirements.txt` typo (removed `pytouch`).
- Added `requirements-dev.txt` and installed testing/linting tools.
- Added timestamp and improved response fields in `/api/health` and `/api/etl-data`.
- Implemented flexible sample-data autoloading across endpoints.
- Enhanced `/api/data/export` to support `format` param and return 400 on unsupported formats; improved exception handling.
- Added validation in `/api/upload-csv` to reject empty/invalid CSV uploads.
- Resolved pathing so backend uses project `data` directory consistently.
- Fixed TypeScript errors by adding `@types/react` and updating `layout.tsx` types.
- Excluded Playwright `e2e/` from Jest via `jest.config.js` to avoid conflicts.
- Cleaned Flake8 issues and long lines; added typing for `etl_metadata`.
