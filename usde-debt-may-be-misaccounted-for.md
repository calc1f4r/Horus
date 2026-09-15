---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60128
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

USDE Debt May Be Misaccounted For

### Overview


The client has reported a bug in the `DefaultPool` and `ActivePool` contracts. The `increaseUSDEDebt()` function always increases the debt by the full amount, while the `decreaseUSDEDebt()` function only decreases the debt by the minimum of the amount or the current debt. This can lead to a surplus of debt in one pool if it increases its debt by more than the other pool decreases its debt. The recommendation is to update the `decreaseUSDEDebt()` function to return the amount it was able to decrease the debt by and pass this value to the `increaseUSDEDebt()` function. 

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> In ActivePool, increaseDebt is the principal amount of the debt, while decreaseDebt is the debt including compound interest. This has no impact on the protocol.

**File(s) affected:**`DefaultPool.sol`, `ActivePool.sol`

**Description:** Both the `DefaultPool` and `ActivePool` track their USDE debt. The function `increaseUSDEDebt()` will always increase the debt by the full `_amount`. The function `decreaseUSDEDebt()` will decrease its debt by the `min(_amount, USDEDebt)` to prevent underflow. These functions are often used to transfer debt from one pool to another. Given the asymmetry between `increaseUSDEDebt()` and `decreaseUSDEDebt()`, it is possible for a pool to increase its debt by a quantity more than the other pool decreased its debt. This would create a surplus of debt where none exists.

**Recommendation:** Update `decreaseUSDEDebt()` to return how much it was able to decrease the debt by. Pass this value to `increaseUSDEDebt()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

