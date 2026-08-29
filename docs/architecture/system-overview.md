# Aegis System Architecture

## Overview

Aegis is designed as a stateful agentic decision-intelligence system.

The architecture separates:

- API concerns
- application services
- agent orchestration
- domain models
- tools
- retrieval
- persistence
- infrastructure

## High-Level Architecture

```mermaid
flowchart TD
    U[User] --> API[FastAPI]

    API --> RS[Research Service]

    RS --> LG[LangGraph Agent]

    LG --> RA[Requirement Analyzer]
    RA --> PL[Research Planner]
    PL --> RT[Research Router]

    RT --> TS[Tool System]

    TS --> WS[Web Search]
    TS --> RAG[Internal RAG]
    TS --> CALC[Calculator]

    WS --> EC[Evidence Collector]
    RAG --> EC
    CALC --> EC

    EC --> EV[Evidence Validator]

    EV -->|Insufficient| RT
    EV -->|Sufficient| DE[Decision Engine]

    DE --> REC[Recommendation]

    REC --> CU[Confidence & Uncertainty]

    CU --> HA[Human Approval]

    HA --> FR[Final Report]

    FR --> DB[(PostgreSQL)]

    LG --> LS[LangSmith]

    RS --> REDIS[(Redis)]
```
