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
solodit_id: 1021
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/16

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
finders_count: 1
finders:
  - TomFrenchBlockchain
---

## Vulnerability Title

[M-02] Should a Chainlink aggregator become stuck in a stale state then TwapOracle will become irrecoverably broken

### Overview


This bug report is regarding the TwapOracle, which is used to calculate the exchange rate between USDV and VADER. The bug is that if any of the Chainlink aggregators used by the TwapOracle becomes stuck, then the `consult` function will always revert. This means that the TwapOracle will be irrecoverable. The recommended mitigation step is to allow governance to update the aggregator for a pair, ideally with a timelock.

### Original Finding Content

_Submitted by TomFrenchBlockchain_

#### Impact

Inability to call `consult` on the TwapOracle and so calculate the exchange rate between USDV and VADER.

#### Proof of Concept

Should any of the Chainlink aggregators used by the TwapOracle becomes stuck in such a state that the check on L143-146 of `TwapOracle.sol` consistently fails (through a botched upgrade, etc.) then the `consult` function will always revert.

<https://github.com/code-423n4/2021-11-vader/blob/3a43059e33d549f03b021d6b417b7eeba66cf62e/contracts/twap/TwapOracle.sol#L143-L146>

There is no method to update the address of the aggregator to use so the `TwapOracle` will be irrecoverable.

#### Recommended Mitigation Steps

Allow governance to update the aggregator for a pair (ideally with a timelock.)


**[SamSteinGG (Vader) diagreed with severity](https://github.com/code-423n4/2021-11-vader-findings/issues/16#issuecomment-979117099):**
 > The scenario of a Chainlink oracle ceasing function is very unlikely and would cause widespread issues in the DeFi space as a whole.

**[alcueca (judge) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/16#issuecomment-991838030):**
 > I'm going to maintain the severity 2 rating despite the low probability of a Chainlink aggregator being permanently disabled. The risk exists, and in general third-party dependencies should be treated with respect in code and documentation.

**[SamSteinGG (Vader) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/16#issuecomment-999354209):**
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
| Finders | TomFrenchBlockchain |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/16
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`vulnerability`

