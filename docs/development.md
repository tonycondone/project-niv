# Development Guide

## Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.12+ ([Download](https://python.org/))
- **Git** ([Download](https://git-scm.com/))
- **npm** or **yarn** package manager

## Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tonycondone/project-niv.git
   cd project-niv
   ```

2. **Install dependencies**
   ```bash
   # Frontend dependencies
   npm install
   
   # Backend dependencies
   pip install -r backend/requirements.txt
   ```

3. **Start development servers**
   ```bash
   # Start both frontend and backend
   npm run full:dev
   
   # Or start separately:
   # Frontend: npm run dev
   # Backend: npm run backend
   ```

4. **Open in browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Project Structure

```
project-niv/
├── src/                    # Next.js frontend
│   ├── app/               # App Router pages
│   │   ├── layout.tsx     # Root layout
│   │   ├── page.tsx       # Home page
│   │   └── globals.css    # Global styles
│   ├── components/        # React components
│   │   ├── dashboard/     # Dashboard components
│   │   ├── layout/        # Layout components
│   │   └── ui/           # Reusable UI components
│   ├── store/            # Zustand state management
│   │   └── etl-store.ts  # ETL data store
│   ├── api/              # API integration
│   │   └── etl.ts        # ETL API client
│   └── lib/              # Utility functions
│       └── utils.ts      # Common utilities
├── backend/               # Python FastAPI backend
│   ├── main.py           # FastAPI application
│   └── requirements.txt  # Python dependencies
├── data/                 # Sample data files
├── docs/                 # Documentation
└── package.json          # Node.js dependencies
```

## Development Commands

### Frontend Development
```bash
npm run dev          # Start Next.js development server
npm run build        # Build for production
npm run start        # Start production server
npm run type-check   # TypeScript type checking
npm run lint         # ESLint checking
```

### Backend Development
```bash
npm run backend      # Start FastAPI development server
npm run backend:prod # Start production server
npm run install:backend  # Install Python dependencies
```

### Full Stack Development
```bash
npm run full:dev     # Start both frontend and backend
npm run full:build   # Build both frontend and backend
```

## Code Style

### TypeScript/React
- Use TypeScript strict mode
- Follow React best practices
- Use functional components with hooks
- Implement proper error boundaries
- Use meaningful variable and function names

### Python
- Follow PEP 8 style guide
- Use type hints for all functions
- Implement proper error handling
- Use docstrings for all functions
- Follow FastAPI best practices

## Adding New Features

### Frontend Components
1. Create component in `src/components/`
2. Add TypeScript interfaces
3. Implement proper error handling
4. Add to storybook if applicable
5. Write tests

### Backend Endpoints
1. Add endpoint in `backend/main.py`
2. Implement proper validation
3. Add error handling
4. Update API documentation
5. Write tests

### State Management
1. Add new state to `src/store/etl-store.ts`
2. Implement actions and reducers
3. Update components to use new state
4. Test state changes

## Testing

### Frontend Testing
```bash
# Run tests (when implemented)
npm test

# Type checking
npm run type-check

# Linting
npm run lint
```

### Backend Testing
```bash
# Run Python tests (when implemented)
cd backend
python -m pytest

# Type checking
python -m mypy main.py
```

## Debugging

### Frontend Debugging
- Use React Developer Tools
- Check browser console for errors
- Use Next.js built-in debugging
- Check network tab for API calls

### Backend Debugging
- Use FastAPI automatic documentation at `/docs`
- Check server logs for errors
- Use Python debugger (pdb)
- Test endpoints with curl or Postman

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```env
DATA_DIR=./data
OUTPUT_DIR=./reports
DEBUG=true
```

## Common Issues

### Port Already in Use
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### Python Dependencies
```bash
# Reinstall Python dependencies
pip install -r backend/requirements.txt --force-reinstall
```

### Node Modules Issues
```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Zustand Documentation](https://github.com/pmndrs/zustand)