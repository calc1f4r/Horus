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
solodit_id: 1016
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/253

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - TomFrenchBlockchain
  - pauliax
---

## Vulnerability Title

[H-31] Unused slippage params

### Overview


This bug report deals with an issue related to the function addLiquidity in VaderRouter (both V1 and V2). The problem is that the function does not use slippage parameters which makes it vulnerable to sandwich attacks and MEV (Miner Extractable Value). This means that the system can be manipulated by mempool snipers. To fix this issue, it is recommended to pay attention to the slippage to reduce the possibility of manipulation attacks.

### Original Finding Content

_Submitted by pauliax, also found by TomFrenchBlockchain_

#### Impact

Unused slippage params.
function `addLiquidity` in VaderRouter (both V1 and V2) do not use slippage parameters:

```solidity
 uint256, // amountAMin = unused
 uint256, // amountBMin = unused
```

making it susceptible to sandwich attacks / MEV.
For a more detailed explanation, see: <https://github.com/code-423n4/2021-09-bvecvx-findings/issues/57>

#### Recommended Mitigation Steps

Consider paying some attention to the slippage to reduce possible manipulation attacks from mempool snipers.

**[SamSteinGG (Vader) disputed](https://github.com/code-423n4/2021-11-vader-findings/issues/253#issuecomment-979186152):**
 > Slippage checks are impossible in the Thorchain CLP model.

**[alcueca (judge) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/253#issuecomment-991471469):**
 > Taking as main over #1 as it is a more general issue, but refer to #1 for a more detailed description and justification for the severity rating.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | TomFrenchBlockchain, pauliax |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/253
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`vulnerability`

