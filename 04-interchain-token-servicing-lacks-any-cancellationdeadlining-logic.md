---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45379
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-axelar-network
source_link: https://code4rena.com/reports/2024-08-axelar-network
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

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[04] Interchain token servicing lacks any cancellation/deadlining logic

### Overview

See description below for full details.

### Original Finding Content


When a transfer is to be made interchain. The current logic is simple to follow:

- User specifies their transfer to the destination chain from the source chain.
- On the destination chain, the transfer gets processed to the destination address.

For some reason the transfer on the receiving chain might fail, this can be from little issues like gas fees, for e.g.

- An interchain transfer gets requested.
- The amount user pays for gas is not enough to process the transaction, so user is only allowed to retry the messages by specifying a higher amount of gas.

This logic would be flawed in some cases, however. Assume the user is trying to transfer `$30` worth of tokens from Arbitrum to Ethereum to pay for whatever. They specify the destination chain and per their calculation the fee to process the tx on Eth is `$15`. They pay less than `$1` on Arb, gas fees are quite cheap.

After sending their request, the gas fees on ETH hikes up by `~30%`, so their first attempt fails, and now they would need to attach `$20` more for their tx. However with this, the user would rather just cancel on Arb pay another `< $1` fee and have access to their `$30 `worth of tokens, but this isn't possible since the current interchaining logic lacks any cancellation approach.

### Impact

QA, since this can be argued to be a design choice by sponsors; however, integrating a cancellation/deadlining logic would allow the best compatibility for users.

Another window for the deadlining could be attributed to the popular lack of deadline for swaps, this is even if slippage is provided, cause in our case here, assume a user made an assumption to process an interchain transfer of a stablecoin and within the timeframe stablecoin on the destination chain heavily depegs, the user still has no option than to just have his tokens locked on the source chain.

### Recommended Mitigation Steps

Introduce a cancellation/deadlining logic.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-axelar-network
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-08-axelar-network

### Keywords for Search

`vulnerability`

