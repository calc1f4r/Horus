---
# Core Classification
protocol: Archi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60914
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
source_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Mustafa Hasan
  - Zeeshan Meghji
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

Loans Can Quickly Become Under-Collateralized in Volatile Market Conditions

### Overview


The report discusses a bug in the health calculation of a protocol, which can lead to bad debt accumulation. The bug has been fixed by requiring a liquidation incentive and allowing liquidation when the leftover collateral is less than 30% of the original collateral. The affected file is CreditCaller.sol. It is recommended to run market simulations and use liquidation bots to mitigate the risk of under-collateralized positions.

### Original Finding Content

**Update**
A change has been applied to the health calculation, such that liquidation is only possible if the leftover collateral in GLP after paying back the loan is less than `10%` of the of original collateral in GLP after repaying the loan. When considering the scenario of `10x` leverage, this means that liquidation is only possible when the leftover collateral in GLP is less than or equal to `1%` of the borrowed tokens in GLP. This means there is a very narrow window for liquidation before the protocol starts to accumulate bad debt. For additional information on this issue refer to ARC-38.

![Image 82: Alert icon](blob:http://localhost/542c9b08ab7b8ff1c3683eefe75dc1a0)

**Update**
The team has fixed the issue by:

1.   Requiring a liquidation incentive which is a fixed percentage of the collateral upon initially opening the position.
2.   Liquidation can now be activated if the leftover collateral in GLP after paying back the loan is `30%` or less than the original collateral in GLP. The `30%` number can be increased to `50%`. We recommend deploying with a maximum number `50%` when the protocol first launches for safety.

**File(s) affected:**`credit/CreditCaller.sol`

**Description:** Given the support of up to 10x leveraged positions, it is possible that volatile market conditions make a loan under-collateralized if liquidation does not occur in time. In such events, the protocol would be operating at a loss. This issue is further exacerbated by the lack of liquidation incentives (ARC-3) and the inability to liquidate defaulted loans (ARC-11).

**Recommendation:** Run market simulations to see whether adequate time to liquidate a position is possible at 10x leverage. Mitigate the odds of an under-collateralized position through liquidation bots.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Archi Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Zeeshan Meghji, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html

### Keywords for Search

`vulnerability`

