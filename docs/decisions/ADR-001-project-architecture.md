# ADR-001: Aegis Project Architecture

## Status

Accepted

## Context

Aegis must perform multi-step research and decision-making across external and internal information sources.

The system needs to support:

- stateful execution
- conditional routing
- research loops
- tool failures
- bounded retries
- evidence validation
- human approval
- persistence
- observability
- evaluation

The architecture must remain understandable and maintainable as these capabilities are added.

## Decision

Aegis will use a modular Python architecture with LangGraph as the agent orchestration layer.

The system will separate:

- API
- application services
- agent orchestration
- domain models
- tools
- RAG
- persistence
- infrastructure

PostgreSQL will be used for application persistence and pgvector-based vector retrieval.

Redis will be introduced only where caching, rate limiting, or short-lived state provides a clear benefit.

FastAPI will provide the external REST API.

OpenAI will be the initial LLM provider behind an internal provider abstraction.

Docker Compose will provide the initial local deployment environment.

## Why LangGraph?

Aegis is not a simple linear LLM pipeline.

Its execution can contain:

- conditional branches
- loops
- retries
- human interruptions
- state transitions
- resumable execution

LangGraph provides an explicit state-machine-oriented abstraction for these workflows.

A simpler deterministic workflow may still be implemented as normal Python when graph orchestration is unnecessary.

## Why PostgreSQL + pgvector?

Using PostgreSQL for both application persistence and vector retrieval reduces operational complexity for the initial system.

Aegis is not intended to demonstrate dependence on a particular vector database. In fact, vector-database selection is one of the decision problems the platform should eventually be able to analyze.

## Why Redis?

Redis is not considered mandatory infrastructure.

It will be introduced only when it provides measurable or clearly justified value for:

- caching
- rate limiting
- short-lived execution state

## Why Docker Compose?

The project is initially a modular monolith rather than a microservice architecture.

Docker Compose provides reproducible local infrastructure without introducing Kubernetes-level operational complexity prematurely.

## Consequences

### Positive

- Clear separation of concerns
- Easier testing
- Explicit agent workflow
- Reusable infrastructure components
- Easier observability
- Good foundation for production hardening

### Negative

- More architectural complexity than a simple Python script
- LangGraph introduces framework-specific concepts
- Multiple infrastructure dependencies increase local setup complexity

These costs are accepted because they directly support Aegis's core requirements.

## Alternatives Considered

### Plain Python workflow

Rejected as the primary orchestration approach because the target workflow contains stateful branching, loops, retries, and human intervention.

Still appropriate for simple deterministic components.

### LangChain AgentExecutor

Not selected as the primary workflow abstraction because Aegis requires explicit control over state transitions and workflow structure.

LangChain components may still be used where appropriate.

### Microservices

Rejected initially because the project does not require independent service scaling.

The initial architecture will be a modular monolith.

### Kubernetes

Rejected initially because container orchestration does not solve a current Aegis requirement.

It may be evaluated later if deployment requirements justify it.
