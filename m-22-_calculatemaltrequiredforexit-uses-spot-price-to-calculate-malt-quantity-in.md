---
# Core Classification
protocol: Malt Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42387
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-malt
source_link: https://code4rena.com/reports/2021-11-malt
github_link: https://github.com/code-423n4/2021-11-malt-findings/issues/215

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
  - cdp
  - yield
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-22] `_calculateMaltRequiredForExit` Uses Spot Price To Calculate Malt Quantity In `exitEarly`

### Overview


The bug report highlights a vulnerability in the `calculateMaltRequiredForExit` function in the `AuctionEscapeHatch` contract. This function uses Malt's spot price to calculate the amount to return to a user who is exiting the protocol. However, this spot price can be manipulated through a flash loan attack, allowing an attacker to extract funds from the protocol. The report recommends implementing a TWAP oracle to track the price of Malt as a mitigation step. The sponsor of the project has confirmed the issue and a judge commented on the design challenges that need to be addressed. 

### Original Finding Content

_Submitted by leastwood_

`_calculateMaltRequiredForExit` in `AuctionEscapeHatch` currently uses Malt's spot price to calculate the quantity to return to the exiting user. This spot price simply tracks the Uniswap pool's reserves which can easily be manipulated via a flash loan attack to extract funds from the protocol.

#### Proof of Concept

- <https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/AuctionEscapeHatch.sol#L65-L92>
- <https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/AuctionEscapeHatch.sol#L193>
- <https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/DexHandlers/UniswapHandler.sol#L80-L109>
- <https://shouldiusespotpriceasmyoracle.com/>


#### Recommended Mitigation Steps

Consider implementing/integrating a TWAP oracle to track the price of Malt.

**[0xScotch (sponsor) confirmed](https://github.com/code-423n4/2021-11-malt-findings/issues/215)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-11-malt-findings/issues/215#issuecomment-1020710474):**
 > I feel like this issue highlights the design challenge that the sponsor will have to solve, on one hand the protocol is meant to stabilize the price of malt in specific pools (impossible to block / control every pool due to permissionless nature).
> At the same time in order to determine which direction to move the price to, they need to refer to the pricing of the underlying pools (in this case a UniV2Pool, most likely from QuickSwap)
> 
> Personally I understand the finding and think it's valid, however I don't believe there's easy answers as to how the sponsor should address this.
> 
> Whenever there's excess value there will be entities trying to seize it and perhaps through such a harsh environment this protocol can truly find a way to be sustainable.
> 
> That said, I'll mark the finding as valid, but believe this specific issue underlines the challenges that await the sponsor in making the protocol succesful





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-malt
- **GitHub**: https://github.com/code-423n4/2021-11-malt-findings/issues/215
- **Contest**: https://code4rena.com/reports/2021-11-malt

### Keywords for Search

`vulnerability`

