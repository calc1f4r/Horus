---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21418
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Xiaoming90
  - 0xNazgul
  - Jonatas Martins
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

ALLOWED_CALLER can steal all rewards from AutoCompounder using a fake factory in the route.

### Overview


This bug report is about AutoCompounder.sol, which allows addresses with ALLOWED_CALLER role to trigger swapTokenToVELOAndCompound. This function sells the specified tokens to VELO. The issue is that since the Velo router supports multiple factories, an attacker can deploy a fake factory with a backdoor, and route the swaps through the backdoor factory to steal all reward tokens in the AutoCompounder contract.

The Velodrome team recommended to check the factory in the routes against the registry to see if it is approved. Additionally, it is important to pay more attention to permission management, as the ALLOWED_CALLER can still steal the rewards. The fix for this issue is to ensure that any interaction with the router is done with a PoolFactory approved by the registry. The change to the registry is that once a PoolFactory is approved, it will always appear as a registered PoolFactory. Spearbit verified the fix.

### Original Finding Content

## Security Analysis

## Severity
**Medium Risk**

## Context
**Location:** AutoCompounder.sol#L187

## Description
The `AutoCompounder` contract allows addresses with the `ALLOWED_CALLER` role to trigger the `swapTokenToVELOAndCompound` function, which sells the specified tokens for VELO. However, since the Velo router supports multiple factories, there is a potential risk: an attacker could deploy a fake factory with a backdoor. By routing the swaps through this backdoor factory, the attacker may steal all reward tokens from the AutoCompounder contract.

## Recommendation
As suggested by the Velodrome team, we should restrict the allowed factories in the routing process. One viable solution is to check the factory in the routes against an approved registry. 

In addition to this fix, it’s crucial to acknowledge the inherent risks and focus on improving permission management. The `ALLOWED_CALLER` role can potentially steal rewards at any time. There is also a noted risk related to "Lack of slippage control during compounding," where an attacker may exploit the system by sandwiching trades to steal tokens. This issue reflects a broader limitation within DeFi systems, which currently lacks easy mechanisms to mitigate such risks without the use of an oracle.

## Velodrome Response
The code was fixed in commit `24e50b`. Initially, the fix was implemented, but it was determined that a greater risk for users arises from the possibility of calling the router from a frontend that can pass in any arbitrary factory. This presents a risk, especially if a website is compromised and interacts with the router using a fake factory.

With commit `24e50b`, we now ensure that any interaction with the router is conducted using a `PoolFactory` approved by our registry. Additionally, changes were made to the registry to ensure that once a `PoolFactory` is approved, it will always appear as a registered `PoolFactory`.

## Verification
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Xiaoming90, 0xNazgul, Jonatas Martins, 0xLeastwood, Jonah1005, Alex the Entreprenerd |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

