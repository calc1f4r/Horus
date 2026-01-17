---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17901
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Risks related to CurveDAO architecture

### Overview


This bug report discusses the potential risks of integrating CurveDAO with FraxPool.sol, a protocol that tightens the stable FRAX peg and distributes CRV to token holders. The report states that if the kick function in LiquidityGauge is not monitored, users who abuse the system will not be penalized. It is also necessary to ensure that rewards are distributed to users fairly and document the differences between calls to balanceOfAt and totalSupplyAt. The exploit scenario states that Alice, a FRAX user, interacts with code that has been part of the CurveDAO architecture since inception and receives a higher amount of CRV rewards than she is entitled to. The report recommends that Frax Finance should review the findings in the CurveDAO audit to identify the risks associated with them and the mitigations that can be implemented to protect users. In the long term, they should always analyze the risk factors of integrations with third-party protocols and create an incident response plan prior to integration.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** FraxPool.sol  

**Difficulty:** Low  

## Description
CurveAMO_V3 relies heavily on Curve Pools to tighten the stable FRAX peg and to distribute CRV to token holders, granting them voting rights in CurveDAO. The use of CurveDAO could affect the FRAX protocol in a few ways. Frax Finance should be mindful of the following considerations:
- If the kick function in LiquidityGauge is not monitored, users who abuse the system will not be penalized. (See TOB-CURVE-DAO-001.)
- It will be necessary to ensure that rewards are distributed to users fairly.
- The differences between calls to balanceOfAt and totalSupplyAt should be documented. (See TOB-CURVE-DAO-016.)

## Exploit Scenario
Alice, a FRAX user, interacts with code that has been part of the CurveDAO architecture since inception. Because of existing vulnerabilities that favor early users of CurveDAO, she receives a higher amount of CRV rewards than she is entitled to.

## Recommendations
- **Short term:** Review all findings in the CurveDAO audit, identifying the risks associated with them and the mitigations that can be implemented to protect users.
- **Long term:** Always analyze the risk factors of integrations with third-party protocols and create an incident response plan prior to integration.

## References
- CurveDAO Audit

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

