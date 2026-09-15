---
# Core Classification
protocol: SSV.network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60299
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ssv-network/6682a4e0-872e-4cec-8b8d-4cd489a20b66/index.html
source_link: https://certificate.quantstamp.com/full/ssv-network/6682a4e0-872e-4cec-8b8d-4cd489a20b66/index.html
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
  - Cameron Biniamow
  - Jennifer Wu
  - Roman Rohleder
  - Rabib Islam
---

## Vulnerability Title

Cluster Owner Can Withdraw Into Liquidation

### Overview


The report is about a bug in the `withdraw()` function of the `SSVNetwork.sol` file. This function allows the cluster owner to withdraw funds from the cluster balance, but the liquidation check is done before the withdrawal amount is subtracted from the balance. This means that a cluster owner could withdraw funds that would make the cluster eligible for liquidation. To prevent this, it is recommended to perform the liquidation check after the withdrawal amount is subtracted from the balance. This will reduce the risk of unintended consequences or vulnerabilities in the code. 

### Original Finding Content

**Update**
The client fixed the issue in commit `9c9206f` by validating the cluster for liquidation after deducting the amount from the cluster balance.

**File(s) affected:**`SSVNetwork.sol`

**Description:** The `withdraw()` function allows the cluster owner to withdraw funds from the cluster balance. The withdrawal is successful as long as there is sufficient balance and the cluster is not liquidatable. The `cluster.isLiquidatable()` function checks whether the cluster is eligible for liquidation based on operator fees, the current network fee, the minimum blocks before the liquidation, and the minimum liquidation collateral. The liquidation check is done before the `amount` is subtracted from the cluster `balance`. This means that it is possible for a cluster owner to withdraw funds that would cause the cluster to become liquidatable.

**Exploit Scenario:**

1.   Alice is the owner of the cluster.
2.   Alice noticed that her cluster balance is eligible for liquidation soon.
3.   Alice wants to withdraw her entire balance. 
4.   Alice withdraws the entire cluster balance to zero using `withdraw()`.
5.   It is not possible to liquidate Alice's cluster since the cluster balance is zero.

**Recommendation:** To prevent the possibility of withdrawing into liquidation, it is recommended to perform the liquidation check after the withdrawal amount is subtracted from the cluster balance in the `withdraw()` function. This ensures that the cluster owner cannot withdraw funds that could cause the cluster to become liquidatable, and reduces the risk of unintended consequences or vulnerabilities in the code.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | SSV.network |
| Report Date | N/A |
| Finders | Cameron Biniamow, Jennifer Wu, Roman Rohleder, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ssv-network/6682a4e0-872e-4cec-8b8d-4cd489a20b66/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ssv-network/6682a4e0-872e-4cec-8b8d-4cd489a20b66/index.html

### Keywords for Search

`vulnerability`

