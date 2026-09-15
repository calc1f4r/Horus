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
solodit_id: 60907
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
source_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
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

No Incentive or Penalty for Liquidation

### Overview


The team has implemented a new feature that rewards liquidators with 10% of leftover collateral after a borrower's loan is paid back. However, if there is little or no leftover collateral, there is not enough incentive for liquidators to act. This puts the protocol at risk if the liquidation bots fail. The team has fixed this issue by setting aside a fixed portion of the collateral as a liquidation fee when a position is opened. It is recommended to use a reasonable percentage of the collateral to incentivize liquidators and penalize borrowers. This is important for maintaining the protocol's solvency and preventing bad debt. The affected file is `credit/CreditCaller.sol`.

### Original Finding Content

**Update**
The team has implemented a liquidation mechanism that rewards the liquidator with 10% of the leftover collateral after the borrower's loan has been paid back. However, if the leftover collateral is low or zero, then there will be very little incentive to liquidate. We note that the Archi team will be running their own liquidation bots, which they believe to be effective, but if these bots fail, the protocol will be exposed to additional risk. For more detail on this issue refer to ARC-47.

![Image 65: Alert icon](blob:http://localhost/542c9b08ab7b8ff1c3683eefe75dc1a0)

**Update**
The team has fixed the issue by setting aside a fixed portion of the collateral as the liquidation fee when the position is opened. We recommend that the team uses a reasonable percentage of the collateral to sufficiently incentive liquidations.

**File(s) affected:**`credit/CreditCaller.sol`

**Description:** Effective liquidation mechanisms are critical for lending protocols to maintain their solvency and prevent bad debt. Currently, the protocol provides no incentive for liquidating an unhealthy position. All of the remaining collateral is returned to the borrower.

**Recommendation:** Implement incentives for liquidators and penalties for borrowers being liquidated. One method is to award a part of the borrower's collateral to the liquidator.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

