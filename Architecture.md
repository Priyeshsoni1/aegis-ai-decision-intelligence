                         ┌──────────────────┐
                         │      Client      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │   API Layer      │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │     Research Service    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       LangGraph         │
                    │     Agent Runtime       │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
        Requirement          Planner            Router
         Analyzer
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │    Tool Registry    │
                      └──────────┬──────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
        Web Search          Internal RAG        Calculator
             │                   │
             ▼                   ▼
        External Web       PostgreSQL
                              +
                           pgvector
             │                   │
             └──────────┬────────┘
                        ▼
                Evidence Collector
                        │
                        ▼
                Evidence Validator
                        │
                  ┌─────┴─────┐
                  │           │
             insufficient   sufficient
                  │           │
                  ▼           ▼
             More Research  Decision Engine
                  │           │
                  └─────┬─────┘
                        ▼
                 Recommendation
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        Confidence            Uncertainty
              │                   │
              └─────────┬─────────┘
                        ▼
                  Human Approval
                        │
                        ▼
                   Final Report
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        PostgreSQL             LangSmith
        Persistence            Observability
             │
             ▼
           Redis
     Cache / Rate Limit
