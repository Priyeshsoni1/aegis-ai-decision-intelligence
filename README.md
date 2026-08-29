# Aegis

AI-powered Due Diligence & Decision Intelligence Platform.

## Overview

Aegis is an AI-powered research and decision-intelligence system designed to help engineers and technical teams make complex technology and business decisions.

Instead of producing a simple LLM-generated answer, Aegis decomposes a decision into research tasks, dynamically selects tools, gathers evidence from internal and external sources, validates that evidence, compares alternatives against explicit constraints, and produces an auditable recommendation with confidence and uncertainty.

## Problem

Complex technical decisions often require engineers to manually:

1. Understand requirements
2. Research alternatives
3. Read documentation
4. Collect evidence
5. Compare trade-offs
6. Calculate costs and performance considerations
7. Evaluate risks
8. Produce a recommendation

This process is time-consuming and difficult to reproduce consistently.

## Solution

Aegis automates this workflow through a stateful agentic system.

```text
Decision Request
       |
       v
Requirement Analysis
       |
       v
Research Planning
       |
       v
Dynamic Tool Orchestration
       |
       +------------------+
       |                  |
       v                  v
   Web Search          Internal RAG
       |                  |
       +--------+---------+
                |
                v
       Evidence Collection
                |
                v
       Evidence Validation
                |
          +-----+-----+
          |           |
     Insufficient  Sufficient
          |           |
          v           v
    More Research  Decision
                      |
                      v
             Recommendation
                      |
                      v
           Confidence/Uncertainty
                      |
                      v
               Human Approval
                      |
                      v
                Final Report
```
