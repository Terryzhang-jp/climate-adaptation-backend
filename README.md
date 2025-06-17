# Climate Adaptation Simulation Backend

A FastAPI-based backend service for climate change adaptation scenario simulation and analysis.

## Features

- **Climate Simulation Engine**: Monte Carlo simulation of climate scenarios (2026-2100)
- **Adaptation Strategies**: 7 different climate adaptation strategies simulation
- **Multiple Simulation Modes**: 
  - Monte Carlo Simulation
  - Sequential Decision-Making
  - Prediction Simulation
  - Results Recording
- **Scenario Comparison**: Compare different adaptation strategies
- **User Ranking System**: Track and rank user performance
- **RESTful API**: Complete REST API with OpenAPI documentation

## Quick Start

### Using Docker (Recommended)

```bash
# Build the image
docker build -t climate-adaptation-backend .

# Run the container
docker run -p 8000:8000 climate-adaptation-backend
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key configuration options:
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `CORS_ORIGINS`: Allowed CORS origins
- `FRONTEND_URL`: Frontend application URL
- `DATA_DIR`: Data storage directory

## API Endpoints

### Core Simulation
- `POST /simulate` - Run climate adaptation simulation
- `POST /compare` - Compare multiple scenarios
- `GET /scenarios` - List all scenarios
- `GET /export/{scenario_name}` - Export scenario data

### Ranking & Data
- `GET /ranking` - Get user rankings
- `GET /block_scores` - Get block scores data

### Health & Monitoring
- `GET /health` - Health check
- `GET /ping` - Simple ping endpoint

## Simulation Modes

1. **Monte Carlo Simulation Mode**: Run multiple simulations with uncertainty
2. **Sequential Decision-Making Mode**: Year-by-year decision making
3. **Predict Simulation Mode**: Long-term prediction simulation
4. **Record Results Mode**: Save results for frontend display

## Adaptation Strategies

The system simulates 7 climate adaptation strategies:
1. **Tree Planting** (植林造林)
2. **House Migration** (住宅迁移)
3. **Levee Construction** (堤防建设)
4. **Paddy Dam Construction** (田间水坝)
5. **Capacity Building** (防灾教育)
6. **Transportation Investment** (交通建设)
7. **Agricultural R&D** (农业研发)

## Deployment

### AWS App Runner (Recommended)
1. Push code to GitHub
2. Create App Runner service
3. Connect to GitHub repository
4. Configure environment variables
5. Deploy automatically

### AWS ECS/Fargate
1. Build and push Docker image to ECR
2. Create ECS task definition
3. Create ECS service
4. Configure load balancer and auto-scaling

## Development

### Project Structure
```
app/
├── main.py              # FastAPI application
├── config.py            # Configuration management
├── models/              # Pydantic models
├── services/            # Business logic services
├── api/                 # API route handlers
├── utils/               # Utility functions
└── core/                # Core utilities (logging, exceptions)
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## License

This project maintains compatibility with the original climate adaptation simulation system.
