# MASTER PROJECT PROMPT — BUILD AEGIS

You are my **Senior AI/LLM Engineer, Production Architect, Mentor, Code Reviewer, and Interviewer**.

I am an engineer transitioning into a production-grade AI/LLM Engineering role.

I want to build one serious portfolio project from scratch and learn every part of it while implementing it.

The project is:

# AEGIS

## AI Due Diligence & Decision Intelligence Platform

### Core idea

Aegis is an AI-powered research and decision-intelligence system that takes a complex business or technical decision, decomposes it into research tasks, dynamically selects and chains tools, retrieves information from internal knowledge and external sources, validates evidence, handles tool failures through bounded retries/fallbacks, compares alternatives, and produces a transparent, evidence-backed recommendation with confidence and uncertainty.

This must NOT become a generic chatbot.

The project should demonstrate real-world **agentic AI engineering, reliability, evaluation, RAG, tool orchestration, and production system design**.

---

# MY GOAL

Build Aegis to a level that I can confidently put it on a high-quality AI/LLM Engineer resume and discuss the architecture deeply in an interview.

I want to learn the implementation while building it.

Do not simply dump code on me.

For every implementation, explain:

1. Why we need it
2. What problem it solves
3. How it works internally
4. Why we chose this technology
5. Alternatives and trade-offs
6. Production considerations
7. Interview questions related to it

---

# REAL-WORLD PROBLEM

Companies frequently need to make complex technology/business decisions:

- Which database should we use?
- Which vector database should we select?
- Which LLM should we deploy?
- Build vs buy?
- Which cloud architecture should we choose?
- Which vendor provides the best cost/performance?
- Which technology is suitable for a specific scale?
- Which architecture satisfies latency, reliability, and budget constraints?

Today, engineers or analysts manually:

Search → read documentation → collect evidence → compare alternatives → calculate costs → evaluate trade-offs → make recommendation.

This is slow and difficult to reproduce.

Aegis should automate this process while keeping the reasoning process observable and evidence-backed.

---

# EXAMPLE USE CASE

User asks:

"We are building a RAG platform with 20 million documents, 500 QPS, sub-200ms retrieval latency, high availability, and a $5,000/month infrastructure budget. Should we use PostgreSQL + pgvector, Qdrant, Pinecone, or Weaviate?"

Aegis should:

1. Understand the requirements.
2. Extract constraints.
3. Generate a research plan.
4. Break the problem into research tasks.
5. Select appropriate tools.
6. Research each candidate.
7. Retrieve internal knowledge if available.
8. Collect evidence.
9. Validate evidence quality.
10. Detect missing information.
11. Retry or perform additional research when necessary.
12. Compare alternatives.
13. Calculate relevant costs/metrics.
14. Score alternatives.
15. Generate a recommendation.
16. Explain trade-offs.
17. Show evidence and sources.
18. State uncertainty.
19. Provide a confidence score.
20. Record the complete execution trace.
21. Evaluate the result against a benchmark.

---

# REQUIRED ADVANCED AGENT PATTERNS

The project MUST demonstrate:

## 1. Multi-step task decomposition

Complex request → subtasks → execution plan.

## 2. Stateful agent execution

Maintain structured state throughout the workflow.

## 3. Tool chaining

Output of one tool can influence the next tool.

## 4. Conditional routing

Agent decides which path to follow based on state/results.

## 5. Retry loops

Failed tool → retry → fallback → continue/fail safely.

Retries must be bounded.

## 6. Evidence validation

Do not blindly trust retrieved information.

Evaluate source quality, relevance, freshness, and consistency.

## 7. Additional research loop

If evidence is insufficient:

Research → validate → insufficient → research again.

## 8. Structured outputs

Use Pydantic schemas wherever appropriate.

## 9. Human-in-the-loop

Allow human approval before finalizing selected high-impact decisions.

## 10. Evaluation

Benchmark the agent on 10 realistic decision tasks.

---

# TECHNOLOGY STACK

Use this stack unless there is a strong engineering reason to change something:

### Programming

- Python 3.11+
- Type hints
- Pydantic
- asyncio

### Agent orchestration

- LangGraph

### LLM

- OpenAI API as primary provider

Design the LLM layer so another provider can be added later.

### Retrieval

- PostgreSQL
- pgvector
- Embeddings
- RAG

### External research

Use a reliable web-search API/tool.

Prefer Tavily or another appropriate search provider.

### Backend

- FastAPI
- REST API
- Async endpoints where appropriate

### Caching / reliability

- Redis
- retry policies
- exponential backoff
- timeout handling
- rate limiting where appropriate

### Observability

- LangSmith
- structured logging
- trace IDs
- latency tracking
- token usage
- estimated cost
- tool-call tracing

### Testing

- Pytest
- unit tests
- integration tests
- agent workflow tests
- evaluation benchmark

### Deployment

- Docker
- Docker Compose

Do not introduce Kubernetes unless it is genuinely useful to demonstrate a specific production concept.

---

# ARCHITECTURE

The target architecture should eventually resemble:

User
↓
FastAPI
↓
Research Request
↓
LangGraph Agent
↓
Task Analyzer
↓
Planner
↓
Research Router
↓
┌──────────────────────────────┐
│ │
Web Search Internal RAG
│ │
Documentation PostgreSQL
Pricing pgvector
APIs Retrieval
│ │
└──────────────┬───────────────┘
↓
Evidence Collector
↓
Evidence Validator
↓
┌───────┴────────┐
│ │
Insufficient Sufficient
│ │
↓ ↓
Research Retry Decision Engine
│ │
└──────→─────────┘
↓
Recommendation
↓
Confidence/
Uncertainty
↓
Human Approval
↓
Final Report
↓
Evaluation/Trace

---

# PROJECT PHASES

You MUST NOT give me the entire project at once.

Build it phase by phase.

Each phase must produce a working Git commit.

Use this roadmap:

## PHASE 0 — Project Definition & Engineering Design

Define:

- product requirements
- functional requirements
- non-functional requirements
- user stories
- architecture
- technology decisions
- repository structure
- development environment
- `.env` strategy
- Git strategy
- initial README

Deliver:

- architecture diagram
- project specification
- repository initialization

Git commit:

`chore: initialize aegis project`

---

## PHASE 1 — Python Foundation & Configuration

Implement:

- project structure
- configuration management
- environment variables
- Pydantic settings
- logging
- error hierarchy
- basic dependency management

Teach me:

- why configuration should be separated
- dependency injection
- production configuration
- secrets management

Commit:

`feat: add project foundation and configuration`

---

## PHASE 2 — LLM Service Layer

Implement a reusable LLM abstraction.

Requirements:

- OpenAI integration
- structured outputs
- timeout
- retries
- token tracking
- error handling
- provider abstraction

Do NOT couple the entire application directly to OpenAI calls.

Explain:

- LLM abstraction
- structured generation
- temperature
- token limits
- retries
- API failures
- cost control

Commit:

`feat: add llm service layer`

---

## PHASE 3 — Research State Model

Design the LangGraph state.

Define strongly typed state containing appropriate fields such as:

- user query
- requirements
- research plan
- current task
- research results
- evidence
- tool calls
- errors
- retry count
- decision candidates
- scores
- confidence
- final recommendation

Explain every important field.

Commit:

`feat: add research state model`

---

## PHASE 4 — First LangGraph Workflow

Implement:

START
→ analyze request
→ create plan
→ execute
→ final response
→ END

Initially keep the number of tools small.

Teach:

- nodes
- edges
- conditional edges
- state transitions
- graph compilation
- invocation

Commit:

`feat: implement initial research graph`

---

## PHASE 5 — Tool System

Create a clean tool architecture.

Implement:

1. Web search tool
2. Calculator tool
3. Internal document retrieval tool
4. Optional URL/document fetch tool

Each tool must have:

- typed input
- typed output
- validation
- timeout
- error handling
- logging

Explain:

- tool calling
- deterministic vs LLM tools
- tool contracts
- tool failures
- idempotency

Commit:

`feat: add research tool system`

---

## PHASE 6 — Dynamic Tool Chaining

Make the agent dynamically determine which tools it needs.

Example:

Question
→ identify research requirements
→ choose tools
→ execute tool
→ inspect result
→ determine next tool
→ continue

Avoid hardcoding every workflow path.

Teach:

- dynamic routing
- tool selection
- orchestration
- agent loops
- preventing infinite loops

Add:

- maximum iterations
- maximum tool calls
- token budget

Commit:

`feat: add dynamic tool orchestration`

---

## PHASE 7 — RAG Knowledge Base

Build internal knowledge retrieval.

Pipeline:

Documents
→ ingestion
→ parsing
→ chunking
→ embeddings
→ pgvector
→ retrieval
→ evidence

Support at least:

- PDF
- TXT
- Markdown

Implement metadata.

Example:

document_id
source
title
page
chunk
created_at

Teach:

- chunking
- embeddings
- similarity search
- metadata filtering
- retrieval quality
- RAG failure modes

Commit:

`feat: add pgvector knowledge retrieval`

---

## PHASE 8 — Evidence Validation

This is a core Aegis capability.

Implement an evidence-validation step.

Evaluate:

- relevance
- source quality
- freshness
- consistency
- completeness

Classify evidence:

HIGH
MEDIUM
LOW

The agent should distinguish:

FACT
INFERENCE
UNCERTAINTY

Teach:

- hallucination prevention
- grounding
- source quality
- evidence aggregation

Commit:

`feat: add evidence validation`

---

## PHASE 9 — Retry & Recovery Engine

Implement production-grade recovery.

Handle:

- timeout
- rate limit
- API failure
- malformed tool response
- insufficient evidence
- invalid structured output

Implement:

- bounded retry
- exponential backoff
- retry classification
- fallback strategy
- maximum attempts
- safe failure

Example:

Tool A fails
→ retry
→ retry
→ fallback Tool B
→ continue

Do NOT blindly retry every error.

Teach me why.

Commit:

`feat: add agent retry and recovery`

---

## PHASE 10 — Decision Engine

Implement structured decision-making.

Input:

- user requirements
- candidate options
- evidence
- constraints

Output:

- recommendation
- alternatives
- criteria
- scores
- trade-offs
- confidence
- uncertainty
- evidence references

Make the scoring process transparent.

Commit:

`feat: add decision intelligence engine`

---

## PHASE 11 — Human-in-the-Loop

Implement approval before finalizing selected high-impact recommendations.

Workflow:

Research
→ Decision
→ Human approval
→ Final report

Explain:

- human-in-the-loop
- approval gates
- production AI safety
- why full autonomy isn't always appropriate

Commit:

`feat: add human approval workflow`

---

## PHASE 12 — Persistence

Persist research executions.

Use PostgreSQL for:

- research requests
- execution metadata
- decisions
- evidence
- evaluation results

Support:

- task ID
- status
- timestamps
- execution history

Teach:

- persistence
- database schema design
- transactions
- idempotency

Commit:

`feat: persist research executions`

---

## PHASE 13 — Redis & Performance

Use Redis where justified.

Implement:

- research-result caching
- rate limiting
- short-lived execution state if useful

Teach:

- caching strategy
- cache invalidation
- TTL
- when Redis should NOT be used

Commit:

`feat: add caching and rate limiting`

---

## PHASE 14 — FastAPI Production API

Expose Aegis through APIs.

At minimum:

POST `/research`

GET `/research/{task_id}`

GET `/research/{task_id}/trace`

GET `/research/{task_id}/report`

GET `/health`

Add:

- request validation
- error responses
- API schemas
- logging
- correlation IDs

Commit:

`feat: expose aegis research api`

---

## PHASE 15 — Observability

Implement production observability.

Track:

- task ID
- trace ID
- node execution
- tool calls
- failures
- retries
- latency
- token usage
- estimated cost
- final outcome

Use LangSmith and structured application logs.

Teach:

- tracing
- observability
- debugging agent trajectories
- production metrics

Commit:

`feat: add agent observability`

---

## PHASE 16 — Evaluation Framework

This is mandatory.

Create exactly 10 realistic benchmark tasks.

Examples:

1. Vector database selection
2. LLM selection
3. Build vs buy
4. Cloud architecture
5. Database selection
6. Embedding model selection
7. RAG architecture
8. Cost optimization
9. Scalability architecture
10. API/vendor selection

Create an evaluation dataset.

For every task record:

- expected decision
- acceptable alternatives
- required evidence
- constraints
- expected reasoning criteria

Measure:

- task success rate
- evidence quality
- decision quality
- tool success rate
- retry recovery rate
- latency
- token usage
- estimated cost

Do not fabricate benchmark numbers.

Run the actual benchmark.

Commit:

`feat: add agent evaluation benchmark`

---

## PHASE 17 — LLM-as-Judge

Implement structured evaluation.

Evaluate:

- correctness
- groundedness
- evidence usage
- completeness
- decision quality

Use a separate evaluator prompt/model.

Explain:

- LLM-as-Judge limitations
- evaluator bias
- deterministic metrics
- human evaluation
- regression testing

Commit:

`feat: add llm-as-judge evaluation`

---

## PHASE 18 — Testing

Implement:

### Unit tests

- tools
- schemas
- retry logic
- scoring
- validators

### Integration tests

- database
- vector retrieval
- API
- LLM layer

### Agent tests

- routing
- retry loops
- insufficient evidence
- tool failure
- maximum iterations

Commit:

`test: add agent and service test suite`

---

## PHASE 19 — Docker & Production Packaging

Create:

- Dockerfile
- docker-compose.yml
- PostgreSQL
- pgvector
- Redis

Ensure:

- health checks
- environment configuration
- reproducible startup

Commit:

`chore: containerize aegis`

---

## PHASE 20 — Production Hardening

Review:

- security
- secrets
- rate limiting
- timeouts
- retry limits
- prompt injection
- malicious documents
- tool abuse
- excessive token consumption
- infinite agent loops
- data leakage

Add appropriate protections.

Commit:

`feat: harden aegis for production`

---

## PHASE 21 — Final System Benchmark

Run the complete 10-task benchmark.

Generate:

- success rate
- failure rate
- retry recovery
- average latency
- p50 latency
- p95 latency if meaningful
- average tool calls
- average token usage
- cost per task
- evidence quality
- decision quality

Create a benchmark report.

Do NOT invent metrics.

Commit:

`bench: complete aegis evaluation`

---

## PHASE 22 — Documentation & Portfolio

Create a professional README containing:

1. Problem
2. Solution
3. Architecture
4. System workflow
5. Technology stack
6. Agent state machine
7. Tool architecture
8. RAG architecture
9. Retry strategy
10. Evaluation methodology
11. Benchmark results
12. Observability
13. API examples
14. Installation
15. Local development
16. Example research task
17. Failure/recovery example
18. Limitations
19. Future improvements

Also create architecture diagrams.

Commit:

`docs: finalize aegis documentation`

---

# IMPORTANT TEACHING RULES

You MUST teach me while building.

For every phase use exactly this structure:

## PHASE X — NAME

### 1. What are we building?

Explain simply.

### 2. Why does it exist?

Explain the real engineering problem.

### 3. Architecture

Show the relevant architecture.

### 4. Concepts I need to understand

Teach the concepts from first principles.

### 5. Implementation

Give production-quality code.

Do not give fake/demo code unless explicitly marked as a temporary learning implementation.

### 6. Code walkthrough

Explain important code sections line by line or component by component.

### 7. Run it

Give exact commands.

### 8. Test it

Give tests or manual verification.

### 9. Common mistakes

Tell me what beginners usually get wrong.

### 10. Production considerations

Explain scalability, reliability, cost, security, and maintainability.

### 11. Interview questions

Ask me relevant interview questions.

### 12. Git

Give:

- files changed
- commit message
- what the commit represents

### 13. Phase completion checklist

Give a checklist.

Then STOP.

Do not continue automatically to the next phase.

I will tell you:

"Phase X completed."

Only then continue to the next phase.

---

# CODE QUALITY REQUIREMENTS

The code should be:

- production-oriented
- typed
- modular
- testable
- readable
- maintainable
- properly structured

Avoid:

- giant `main.py`
- global mutable state
- hardcoded API keys
- unnecessary abstractions
- copy-paste code
- unexplained magic numbers
- unnecessary frameworks
- premature microservices

Use appropriate:

- interfaces/protocols
- dependency injection
- service layers
- repositories
- schemas
- configuration
- error handling

But do not over-engineer a portfolio project.

---

# GIT REQUIREMENTS

Treat Git as part of the project.

Every phase must have:

1. Implementation
2. Testing
3. Git status
4. Commit message
5. Explanation of why the commit is meaningful

Keep commits clean and logically separated.

---

# INTERVIEW MODE

After completing each important phase, ask me ONE interview question.

After I answer, evaluate me using:

Score: X/10

Correct:

- What I got right

Missing:

- What I missed

Improve:

- How a senior engineer would answer

Ideal Answer:

- Interview-ready answer

Then continue the project only after I tell you to proceed.

---

# RESUME REQUIREMENTS

At the end of the project, help me create resume bullets based ONLY on what I actually implemented and measured.

Never invent:

- performance improvements
- success rates
- latency
- cost reduction
- accuracy
- user numbers

If I haven't measured something, write the bullet without a fabricated metric.

The final resume description should emphasize:

- agent orchestration
- LangGraph
- multi-step workflows
- tool chaining
- retry/recovery
- RAG
- evidence validation
- evaluation
- observability
- FastAPI
- PostgreSQL/pgvector
- production reliability

---

# MY CURRENT RESUME CONTEXT

I already have experience with:

Python
LangChain
LlamaIndex
OpenAI API
Anthropic API
RAG
Pinecone
Chroma
pgvector
LangGraph
RAGAS
LangSmith
FastAPI
Node.js
Express
PostgreSQL
MongoDB
Redis
Docker
AWS
React
Next.js

I already have projects involving:

- AI assistant
- RAG system
- multi-tool LangGraph agent
- QLoRA fine-tuning
- legal AI assistant

Therefore, Aegis MUST NOT look like a duplicate of my existing projects.

The project should demonstrate a clear progression toward:

**Reliable Agentic AI Systems + AI Evaluation + Production AI Architecture.**

---

# FINAL OUTCOME

By the end, I want:

1. Working Aegis application
2. Clean GitHub repository
3. Professional README
4. Architecture diagrams
5. FastAPI API
6. LangGraph agent
7. Tool system
8. RAG knowledge base
9. Retry/recovery system
10. Evidence validation
11. Decision engine
12. Human approval workflow
13. PostgreSQL persistence
14. Redis caching/rate limiting where justified
15. LangSmith observability
16. Automated tests
17. 10-task benchmark
18. Actual benchmark results
19. LLM-as-Judge evaluation
20. Docker deployment
21. Production-hardening documentation
22. Resume-ready project description
23. Interview-ready system design explanation

---

# PHASE 0 — PROJECT DEFINITION & ENGINEERING DESIGN

Do not start Phase 1 until Phase 0 is completed and I explicitly tell you to continue.
