---
# Core Classification
protocol: Brahma Fi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13254
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/05/brahma-fi/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  George Kobakhidze

  - David Oz Kashi
  -  Sergii Kravchenko
---

## Vulnerability Title

The virtual price may not correspond to the actual price in the pool

### Overview


This bug report is about a function in a Curve pool that returns a “virtual price” of the LP token. This price is designed to be resistant to flash-loan attacks and other manipulations. In some cases, however, there may be a significant period when a trade cannot be executed with this price. 

When depositing into Curve, Brahma is doing it in two steps. The first step calculates the user’s share according to the “virtual price”, and the second step deposits funds into the Curve pool. If the deposit price does not correspond to the virtual price, the transaction will revert.

This causes two problems. First, if the chosen slippage parameter is very low, the funds will not be deposited/withdrawn for a long time due to reverts. Second, if the slippage is large enough, the attacker can manipulate the price to steal the slippage. Additionally, because of the two-step deposit, the amount of Vault’s share minted to the users may not correspond to the LP tokens minted during the second step.

### Original Finding Content

#### Description


A Curve pool has a function that returns a “virtual price” of the LP token; this price is resistant to flash-loan attacks and any manipulations in the Curve pool. While this price formula works well in some cases, there may be a significant period when a trade cannot be executed with this price. So the deposit or withdrawal will also be done under another price and will have a different result than the one estimated under the “virtual price”.


When depositing into Curve, Brahma is doing it in 2 steps. First, when depositing the user’s ETH to the Vault, the user’s share is calculated according to the “virtual price”. And then, in a different transaction, the funds are deposited into the Curve pool. These funds only consist of ETH, and if the deposit price does not correspond (with 0.3% slippage) to the virtual price, it will revert.


So we have multiple problems here:


1. If the chosen slippage parameter is very low, the funds will not be deposited/withdrawn for a long time due to reverts.
2. If the slippage is large enough, the attacker can manipulate the price to steal the slippage. Additionally, because of the 2-steps deposit, the amount of Vault’s share minted to the users may not correspond to the LP tokens minted during the second step.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Brahma Fi |
| Report Date | N/A |
| Finders |  George Kobakhidze
, David Oz Kashi,  Sergii Kravchenko |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/05/brahma-fi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

