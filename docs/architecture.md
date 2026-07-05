# Project AEGIS v0.2 Architecture

## Current Purpose
Scan a starter watchlist and rank opportunities through multiple agents.

## Flow
1. Watchlist scanner loads symbols.
2. Market data module fetches recent prices and volume.
3. Agent registry loads available agents.
4. Each agent gives an opinion.
5. CIO converts opinions into a ranked decision.
6. Logger writes each full decision to `logs/decisions.jsonl`.

## Current Agents
- Technical Analyst
- News Analyst
- Insider/Politician Intelligence
- Devil's Advocate
- Risk Manager

## Next Versions
v0.3: Add better dashboard + CSV reports.
v0.4: Add Alpaca read-only account connection.
v0.5: Add public disclosure monitoring.
v1.0: Add guarded live execution.
