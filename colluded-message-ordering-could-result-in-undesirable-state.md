---
# Core Classification
protocol: Centrifuge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54427
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/693b6f24-6e47-4194-97b0-356d10dc1df6
source_link: https://cdn.cantina.xyz/reports/cantina_centrifuge_oct2023.pdf
github_link: none

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
finders_count: 2
finders:
  - Liam Eastwood
  - Sujith Somraaj
---

## Vulnerability Title

Colluded message ordering could result in undesirable state 

### Overview

See description below for full details.

### Original Finding Content

## Security Context Overview

## Context
**File:** `Gateway.sol`  
**Line:** 378

## Description
The entire security of Auth in `Root.sol` is heavily dependent on a spell pattern from MakerDAO. There are two ways to add a new ward to root:

1. Through `DelayedAdmin.sol`
2. Through `Gateway.sol`

The `Gateway` contract depends on the cross-chain message bridge Axelar to schedule and cancel newly added adapters.

Imagine `scheduleRely()` is triggered from the Centrifuge chain, which is then quickly canceled on the remote chain by calling `cancelRely()`. However, if these transactions are relayed while the Axelar bridge is down or broken, a problem arises.

After a while, when those two transactions arrive at the EVM chain, the relayers process `cancelRely()` first and then the `scheduleRely()` function. This negates the `cancelRely()` functionality, and if unnoticed, it will add a ward that is canceled on the Centrifuge chain.

**Note:** Axelar provides no order of message ordering/protection, and the message can be executed only once.

## Recommendation
Run off-chain watchers to detect the message ordering impact. These watchers can then initiate a transaction through `DelayedAdmin.sol` to cancel the scheduled transaction. It is advised to add an explicit revert if there are no ward additions scheduled.

## Additional Information
- **Centrifuge:** Fixed in commit `f945184c`.
- **Cantina:** Verified fix. `cancelRely()` will revert if a new ward has not been scheduled.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Centrifuge |
| Report Date | N/A |
| Finders | Liam Eastwood, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_centrifuge_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/693b6f24-6e47-4194-97b0-356d10dc1df6

### Keywords for Search

`vulnerability`

