# Multi-Agent Financial Analysis System

A modular, extensible multi-agent framework for advanced financial intelligence. The system ingests heterogeneous market data, performs structured analysis through coordinated AI agents, and generates comprehensive and actionable insights.

## Key Features

### Multi-Agent Architecture
The system implements a hierarchical workflow with **eight specialised agents** to promote transparent, reproducible reasoning:

- **Base Agent** — System bootstrap and entry point
- **Coordinator** — Orchestrates workflow and agent sequencing
- **Senior Researcher** — Performs deep contextual research using macroeconomic data and news
- **Analyst** — Conducts quantitative analysis and data processing
- **Decision Maker** — Synthesises research and analytical outputs into recommendations
- **Evaluator** — Validates logical consistency, coherence, and confidence scoring
- **Optimiser** — Refines reasoning chains for efficiency and accuracy
- **Writer** — Produces structured, human-readable reports

Workflow: Coordination → Parallel Research & Analysis → Decision Synthesis → Evaluation → Optimization (conditional) → Report Generation

### Data Sources & Processing
- **News Sources**: CNBC, Reuters, The Guardian (via NewsAPI integration)
- **Structured Data**: CSV datasets, macroeconomic time series (FRED), equity data (yfinance)
- **High-Performance Processing**: **Polars** for superior speed and memory efficiency over Pandas
- **Storage**:
  - `financial_data.db` — Cleaned financial and news data
  - `agent_memory.db` — Persistent agent context and intermediate reasoning

### Integrated Tools
- **Economic Tool** — Time-series macroeconomic data from Federal Reserve Economic Data (FRED)
- **News Tool** — Fetching, storage, and retrieval of financial news via NewsAPI (recent, historical, and database queries)
- **Stock Tool** — Equity prices and metadata via yfinance

### Technical Architecture
Built for maintainability, scalability, and extensibility using established design patterns:

- **SQLAlchemy ORM** — Full object-relational mapping with defined models
- **DTOs** (Data Transfer Objects) — Type-safe data exchange between components
- **DAOs** (Data Access Objects) — Abstracted database operations
- **Adapters** — Source-specific normalisation (CSV, news APIs)
- **Services** — Encapsulated business logic (e.g., NewsService)
- **Model-Agnostic Design** — Default local inference with **GPT4All** (low resource usage); easily configurable for OpenAI, Anthropic, Grok, or other providers
- **Tool Integration** — Agents equipped with a function calling for real-time data retrieval

### Flow Chart

<img width="1548" height="870" alt="image" src="https://github.com/user-attachments/assets/d0df02f5-1fe0-490c-94cc-3534f43086c8" />

### Extensibility
Designed for seamless extension:

#### Adding New Agents
- Inherit from base agent interface in `agents/`
- Define role-specific prompts and tools
- Register in the Coordinator workflow

#### New Data Sources
- Normalise to standardised DTOs
- Register in the appropriate service

#### New Tools
- Add standalone functions/classes in `tools/`
- Register and assign to relevant agents

#### LLM Flexibility
- Switch providers via configuration only
- Supports streaming, function calling, and per-agent parameters

#### Database Scaling
- ORM models are easily extensible
- Agent memory persistence supports migration to PostgreSQL, vector stores, etc.

## License
MIT License — free to use, modify, and distribute.

**Note**: This system is intended for research, analysis, and experimentation. Outputs are informational only and do not constitute financial advice.

Contributions welcome — new agents, tools, adapters, or integrations encouraged. Please see contribution guidelines for details.
