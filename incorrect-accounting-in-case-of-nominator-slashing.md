---
# Core Classification
protocol: Bemo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58848
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/bemo-finance/701f9326-7a77-48b6-a98e-b72c33873cfa/index.html
source_link: https://certificate.quantstamp.com/full/bemo-finance/701f9326-7a77-48b6-a98e-b72c33873cfa/index.html
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
finders_count: 3
finders:
  - Gereon Mendler
  - Julio Aguilar
  - Jonathan Mevs
---

## Vulnerability Title

Incorrect Accounting in Case of Nominator Slashing

### Overview


The client has decided not to fix an issue where the `financial` contract may receive less TON than originally deposited due to slashing events in the `nominator_pool` contract. This can lead to a lack of funds for user withdrawals. The client believes that it is their responsibility to cover any losses from slashing and does not want to make changes to the system that would require them to track the addresses of proxy contracts. The bemo team suggests properly forwarding the discrepancy from `nominator_proxy` to `financial` and reducing `total_ton_supply` accordingly, even though the client plans to cover any losses.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We have decided not to implement a fix for this issue, as slashing is entirely our responsibility. The contract includes a method for receiving rewards from validators. Any contract can send rewards to the system, thereby increasing the TON pool size. We cannot allow any contract to decrease the size of the TON pool. Implementing the proposed fix would require us to account for and verify the addresses of our proxy contracts within the financial contract in such cases. We do not plan to make this change because we prioritize system flexibility, allowing us to work with any proxy contracts without the need to track their addresses. In the future, it is possible to expand beyond the use of only standard nominator_pool contracts for validation-related transactions.

**File(s) affected:**`financial.fc`

**Description:** When withdrawing from the nominator pool, its remaining stake and accrued reward are returned to the `nominator_proxy` contract, where this total is compared to the recorded `deposit_amount`, and the reward portion is calculated and forwarded to the `financial` contract. However, if the stake decreased due to slashing events the `financial` contract may receive fewer TON than originally deposited without reducing the internal `total_ton_supply` accounting. This can eventually lead to a lack of funds for user withdrawals.

**Recommendation:** The bemo team mentioned that they intend to cover the losses due to slashing. However, we still recommend to properly forward the discrepancy from `nominator_proxy` to `financial` and reduce `total_ton_supply` accordingly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Bemo Finance |
| Report Date | N/A |
| Finders | Gereon Mendler, Julio Aguilar, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/bemo-finance/701f9326-7a77-48b6-a98e-b72c33873cfa/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/bemo-finance/701f9326-7a77-48b6-a98e-b72c33873cfa/index.html

### Keywords for Search

`vulnerability`

