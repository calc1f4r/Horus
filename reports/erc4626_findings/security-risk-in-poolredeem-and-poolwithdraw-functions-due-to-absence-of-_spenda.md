---
# Core Classification
protocol: Nemeos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59586
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
source_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
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
finders_count: 3
finders:
  - Sebastian Banescu
  - Faycal Lalidji
  - Guillermo Escobero
---

## Vulnerability Title

Security Risk in `Pool.redeem()` and `Pool.withdraw()` Functions Due to Absence of `_spendAllowance()` in `Pool._withdraw()` Logic

### Overview


A recent update has fixed a bug in the `Pool.sol` contract where the `redeem()` and `withdraw()` functions allowed for withdrawals on behalf of another user. This could potentially lead to security risks, such as attackers being able to withdraw assets from other users and manipulate the daily interest rate of the `Pool`. This vulnerability was caused by the absence of a feature called `_spendAllowance()` in the `withdraw()` function, which is used to verify and limit spending by users. To address this issue, it is recommended to disallow withdrawals on behalf of third-party user addresses to prevent unauthorized access and manipulation of funds.

### Original Finding Content

**Update**
Fixed in `b59662850f943169452f2295f70a14329e21c0e1`. Now `_withdraw()` verifies caller allowance of vault shares.

**File(s) affected:**`Pool.sol`

**Description:** The `Pool.redeem()` and `Pool.withdraw()` functions in the contract allow for withdrawals on behalf of another user, creating a potential security risk under certain conditions:

*   The affected user is a contract unable to manage withdrawn funds effectively.
*   This flaw could let attackers withdraw assets from other users, enhancing their own ROI returns.
*   It enables manipulation of the `Pool`'s daily interest rate, as withdrawals prompt an update to this rate.

The absence of the `_spendAllowance()` logic in `Pool.withdraw()`, a feature originally included in the `ERC4626Upgradeable` contract, is the fundamental cause of this vulnerability. This mechanism is essential for verifying and upholding the spending limits designated by users, thus blocking unauthorized withdrawals.

**Recommendation:** To address this security concern, the recommendation is to disallow withdrawals on behalf of third-party user addresses. This change would prevent unauthorized access and manipulation of funds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nemeos |
| Report Date | N/A |
| Finders | Sebastian Banescu, Faycal Lalidji, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html

### Keywords for Search

`vulnerability`

