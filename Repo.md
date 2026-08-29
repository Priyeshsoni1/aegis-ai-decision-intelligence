aegis/
│
├── app/
│ ├── api/
│ │ ├── routes/
│ │ └── schemas/
│ │
│ ├── agent/
│ │ ├── graph.py
│ │ ├── state.py
│ │ ├── nodes/
│ │ └── routing/
│ │
│ ├── domain/
│ │ ├── models/
│ │ ├── enums/
│ │ └── exceptions/
│ │
│ ├── services/
│ │ ├── research.py
│ │ ├── decision.py
│ │ └── evidence.py
│ │
│ ├── tools/
│ │ ├── base.py
│ │ ├── search.py
│ │ ├── calculator.py
│ │ ├── retrieval.py
│ │ └── registry.py
│ │
│ ├── llm/
│ │ ├── base.py
│ │ ├── openai.py
│ │ └── models.py
│ │
│ ├── rag/
│ │ ├── ingestion.py
│ │ ├── chunking.py
│ │ ├── embeddings.py
│ │ └── retrieval.py
│ │
│ ├── persistence/
│ │ ├── models/
│ │ ├── repositories/
│ │ └── database.py
│ │
│ ├── infrastructure/
│ │ ├── redis.py
│ │ ├── search.py
│ │ └── observability.py
│ │
│ ├── config.py
│ ├── logging.py
│ └── main.py
│
├── tests/
│ ├── unit/
│ ├── integration/
│ └── agent/
│
├── evals/
│ ├── datasets/
│ ├── runners/
│ └── reports/
│
├── docs/
│ ├── architecture/
│ ├── decisions/
│ └── benchmark/
│
├── scripts/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
