---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49982
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - i_atiq
---

## Vulnerability Title

Chainlink Keeper Cannot Process All Swap Logs in a Block

### Overview

See description below for full details.

### Original Finding Content

### Summary
`UsdTokenSwapKeeper::checkLog` relies on Chainlink Keepers, which only handle 1 logs every 2 block on Arbitrum. `StabilityBranch::initiateSwap` emits an event (`LogInitiateSwap`) for each swap request. If multiple users request multiple swaps in the same block, some logs will be ignored, leading to unprocessed swaps.

Accroding to chainlink doc-`Chainlink Automation nodes look back over a limited range of the latest blocks and process a limited number of logs per block per upkeep, using a minimum dequeue method to ensure that the latest logs are processed first. After this, the nodes may process additional remaining logs on a best effort basis, but this is not guaranteed` [[doc](https://docs.chain.link/chainlink-automation/overview/service-limits)]

The doc suggest if all logs are needed to be processed, configure a manual trigger as backup. If swap requests are not processed or processed later than the deadline, users have to call `refund` to get back their token. But user will have to pay the base fee to get a refund which becomes unnecessarily costly for users

---

### Impact
- Users pay gas fees for swap requests that may never be processed. Users also have pay base fee to get a refund

---

### Recommendation

Remove base fee when refunding if the protocol cannot 100% guarantee users that their swaps will be executed

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | i_atiq |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

