---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42347
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-vader
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/20

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Permissioned nature of `TwapOracle` allows owner to manipulate oracle

### Overview


This bug report was submitted by a user named TomFrenchBlockchain. The issue reported is that the USDV:VADER price feed may be frozen or intentionally inaccurate. This can happen because only the owner of the "TwapOracle" contract can update the price feed. If the owner chooses to stop updating the feed for a period of time, the relative prices of VADER and USDC will change. When the owner eventually updates the feed again, the resulting price may not accurately reflect the current exchange rate. This means that the owner can manipulate the price to their advantage. 

The recommended solution is to remove the permissioning from the "TwapOracle" contract, which would allow anyone to update the price feed. This issue has been marked as a duplicate by SamSteinGG and it has been mentioned that the TWAP oracle module has been completely redesigned and is now subject to a new audit.

### Original Finding Content

_Submitted by TomFrenchBlockchain_

#### Impact

Potentially frozen or purposefully inaccurate USDV:VADER price feed.

#### Proof of Concept

<https://github.com/code-423n4/2021-11-vader/blob/3a43059e33d549f03b021d6b417b7eeba66cf62e/contracts/twap/TwapOracle.sol#L322>

Only the owner of `TwapOracle` can call `update` on the oracle. Should the owner desire they could cease calling `update` on the oracle for a period. Over this period the relative prices of VADER and USDC will vary.

After some period `timeElapsed` the owner can call `update` again. A TWAP is a lagging indicator and due to the owner ceasing to update the oracle so `timeElapsed` will be very large, therefore we're averaging over a long period into the past resulting in a value which may not be representative of the current USDV:VADER exchange rate.

The owner can therefore selectively update the oracle so to result in prices which allow them to extract value from the system.

#### Recommended Mitigation Steps

Remove the permissioning from `TwapOracle.update`

**[SamSteinGG (Vader) marked as duplicate](https://github.com/code-423n4/2021-11-vader-findings/issues/20)** 

**[alcueca commented](https://github.com/code-423n4/2021-11-vader-findings/issues/20#issuecomment-991011036):**
 > Duplicate of which other issue, @SamSteinGG?

**[SamSteinGG (Vader) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/20#issuecomment-999353780):**
 > The TWAP oracle module has been completely removed and redesigned from scratch as LBTwap that is subject of the new audit.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/20
- **Contest**: https://code4rena.com/reports/2021-11-vader

### Keywords for Search

`vulnerability`

