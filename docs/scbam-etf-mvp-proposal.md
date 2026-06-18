# SCBAM ETF Tactical Allocation MVP Proposal

## Executive Summary

This proposal defines a practical MVP for applying the TradingAgents framework to ETF research and tactical asset allocation. The MVP is intended as a decision-support research tool for SCBAM's Quant Investment team, not an autonomous trading system. The first proof of concept will focus on a small ETF universe, produce monthly overweight/underweight recommendations, and generate investment committee briefing materials with a human-in-the-loop review trail.

The target annual budget is THB 1.2 million, or approximately THB 100,000 per month, covering model/API usage, market data, infrastructure, engineering, and coding-agent support.

## Business Context

The sponsor is a fund manager in SCBAM's Quant Investment team, managing Thai and global equity portfolios with approximately THB 1 billion AUM. The investment need is a faster, more explainable ETF research workflow that can combine market data, macro context, risk signals, and LLM-generated investment narratives into a repeatable monthly process.

The MVP should support investment committee discussion by producing transparent recommendations, not black-box trades.

## MVP Scope

The full ETF universe of interest is:

`IVV`, `IEUR`, `EWJ`, `MCHI`, `EWY`, `INDA`, `THD`, `BND`, `VNQ`, `IAU`, `PDBC`

For speed and cost control, the POC universe will be limited to:

`IVV`, `IEUR`, `INDA`, `IAU`, `THD`

The MVP will generate:

- ETF ranking across the POC universe
- Tactical overweight/underweight signals
- Suggested monthly allocation weights
- Investment committee briefing reports in Markdown
- CSV/Excel allocation tables
- Human review notes and audit trail

## Investment Horizon and Benchmark

The strategy horizon is monthly rebalancing. Recommendations should be framed as one-month tactical tilts, with supporting medium-term context where relevant.

The benchmark allocation is:

| Asset | Weight |
| --- | ---: |
| ACWI proxy | 65% |
| BND | 20% |
| IAU | 15% |

For the MVP, IVV and IEUR can be used as developed-market equity proxies, while INDA and THD represent regional equity tilts and IAU represents gold exposure. A later phase should add BND and the remaining ETFs to align the production universe more directly with the benchmark.

## Model and API Configuration

The POC should use OpenRouter for LLM access.

Preferred model:

```text
deepseek/deepseek-v4-flash
```

Preferred provider order:

```text
Baidu Qianfan, Wafer
```

For this model, OpenRouter currently exposes these endpoint slugs:

```text
baidu/fp8, wafer/fp4
```

The local POC environment should configure this through `.env` and environment variables rather than hard-coding model settings. The API key must not be committed to git, pasted into reports, or included in committee materials. This repository's `.gitignore` excludes `.env`.

Local `.env` configuration:

```bash
TRADINGAGENTS_LLM_PROVIDER=openrouter
TRADINGAGENTS_DEEP_THINK_LLM=deepseek/deepseek-v4-flash
TRADINGAGENTS_QUICK_THINK_LLM=deepseek/deepseek-v4-flash
OPENROUTER_API_KEY=...
TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
TRADINGAGENTS_MAX_RISK_ROUNDS=1
TRADINGAGENTS_OPENROUTER_PROVIDER_ORDER=baidu/fp8,wafer/fp4
TRADINGAGENTS_OPENROUTER_ALLOW_FALLBACKS=false
TRADINGAGENTS_OPENROUTER_REQUIRE_PARAMETERS=true
TRADINGAGENTS_OPENROUTER_DATA_COLLECTION=deny
TRADINGAGENTS_OPENROUTER_MAX_PROMPT_PRICE=0.10
TRADINGAGENTS_OPENROUTER_MAX_COMPLETION_PRICE=0.20
TRADINGAGENTS_OPENROUTER_SESSION_ID=scbam-etf-mvp
```

For early testing, use conservative debate depth and a small ETF universe to control cost and latency. Disabling OpenRouter fallbacks is intentional for the POC: if Baidu and Wafer are unavailable or exceed the price cap, the run should fail rather than silently route to a more expensive provider.

Initial live API testing should start with one ETF, then expand to the five-ETF POC universe after cost, latency, and output quality are acceptable.

OpenRouter prompt caching for DeepSeek is automatic, but cache hit rates depend on stable prompts and stable routing. The `TRADINGAGENTS_OPENROUTER_SESSION_ID` setting should be kept fixed during a POC run to improve sticky routing behavior.

## Data Sources

The MVP should prioritize free but credible data sources:

- Yahoo Finance via `yfinance` for ETF prices, volume, returns, and basic fund data
- FRED for macro indicators such as rates, inflation, growth, and labor data
- Public ETF issuer pages for validation of expense ratios, holdings, and index exposure where needed
- Public market/news sources available through the existing TradingAgents dataflow layer

All generated recommendations must cite the underlying data inputs at a high level and flag missing or stale data explicitly.

## Proposed Workflow

1. Run monthly ETF data collection for the POC universe.
2. Generate market, macro, technical, and fundamental-style ETF summaries.
3. Rank ETFs by return momentum, volatility, drawdown, macro support, and diversification role.
4. Produce overweight/underweight signals relative to the benchmark allocation.
5. Generate a proposed allocation table with clear constraints and rationale.
6. Save Markdown briefing report and CSV/Excel allocation output.
7. Require fund manager review before any recommendation is used in committee materials.

## MVP Outputs

The Markdown report should include:

- Executive recommendation
- ETF ranking table
- Proposed allocation table
- Key overweight and underweight rationales
- Market and macro regime summary
- Risk dashboard summary
- Backtest summary
- Human review section
- Compliance disclaimer

The CSV/Excel output should include:

- Ticker
- ETF name
- Current benchmark weight
- Proposed weight
- Active weight
- Signal: Overweight, Neutral, or Underweight
- Ranking score
- Key rationale
- Reviewer status

## Backtest and Risk Dashboard

The POC should include a simple monthly rebalance backtest over an agreed historical window, subject to data availability. Initial metrics should include:

- Total return and annualized return
- Volatility
- Sharpe ratio
- Maximum drawdown
- Hit rate versus benchmark
- Turnover estimate
- Active weight history

The risk dashboard should show allocation concentration, equity/gold exposure, regional exposure, drawdown, volatility, and benchmark-relative performance.

## Success Criteria

The POC is successful if it demonstrates:

- Faster monthly ETF research workflow
- Explainable recommendations suitable for committee review
- Reproducible ranking and allocation output
- Backtest evidence versus the benchmark allocation
- Human-in-the-loop audit trail
- Lower research preparation cost
- Clear path from MVP to production governance

## Governance and Compliance

The system must be positioned as decision support only. It must not place trades, rebalance portfolios automatically, or bypass fund manager judgment. All outputs should include a disclaimer stating that recommendations require human review and approval before use.

The audit trail should record input data date, model name, prompt/config version, generated recommendation, reviewer name, reviewer decision, and final committee-ready output.

API keys and model credentials should be treated as production secrets even during POC. Access should be limited to approved project contributors, and keys should be rotated if exposed outside the controlled development environment.

## Budget Framing

Target annual budget: THB 1.2 million.

Indicative monthly allocation:

| Category | Monthly Budget |
| --- | ---: |
| Model/API usage | THB 20,000 |
| Market data and validation sources | THB 20,000 |
| Infrastructure and storage | THB 10,000 |
| Engineering and maintenance | THB 30,000 |
| Coding-agent support | THB 15,000 |
| Contingency | THB 5,000 |

The POC should track actual model calls, token usage, runtime, and report generation cost so the production budget can be refined before approval.

## Recommended Delivery Plan

Phase 1 should deliver the POC for `IVV`, `IEUR`, `INDA`, `IAU`, and `THD`: data pipeline, ranking model, allocation output, Markdown report, and backtest summary.

Phase 2 should add the full ETF universe, richer risk dashboard, Excel export, and improved benchmark mapping.

Phase 3 should prepare production governance: access control, scheduled runs, versioned reports, model monitoring, and committee workflow integration.
