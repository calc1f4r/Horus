---
# Core Classification
protocol: Triall
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56032
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-09-Triall.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

No deposit token validation

### Overview


The report suggests that there is a potential bug in the Vesting.sol contract. The contract does not have any validation for deposit tokens, which could leave it vulnerable to a combination of reentrancy and fake token attacks. To prevent this, the report recommends using the SafeERC20 library for transfer operations and implementing the ReentrancyGuard for affected methods. It also suggests moving storage changes before the transfer/transferFrom operation. These changes will help to ensure the security of the contract and prevent potential attacks.

### Original Finding Content

**Description**

Vesting.sol
Since the contract does not have any validation for deposit tokens, consider the usage of
SafeERC20 library for transfers of deposit token and ReentrancyGuard in order to prevent
reentrancy+fake token attack combination.
Potentially affected methods:
Vesting.withdrawFunds()
Vesting.deposite()

**Recommendation**:

Use SafeERC20 library for deposit token transfer() and transferFrom()
move storage changes before the transfer/transferFrom operation
use ReentrancyGuard for affected methods

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Triall |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-09-Triall.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

