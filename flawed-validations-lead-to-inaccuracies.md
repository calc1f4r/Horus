---
# Core Classification
protocol: Navi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48036
audit_firm: OtterSec
contest_link: https://www.naviprotocol.io/
source_link: https://www.naviprotocol.io/
github_link:  github.com/naviprotocol/protocol-core

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
  - Ajay Shankar
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Flawed Validations Lead To Inaccuracies

### Overview


There is a bug in the code that validates lending operations. Some functions use scaled balances and unscaled amounts together, which can lead to incorrect results. This bug affects the calculation for deposit, withdrawal, and borrowing. To fix this, the validation functions need to be moved to a different location in the code and adjustments need to be made to use unscaled amounts for comparisons. This has been fixed in the latest versions of the code.

### Original Finding Content

## Validator Functions and Inaccuracies in Lending Operations

In `validator.move`, a set of functions validate various actions related to lending operations. These functions validate specific conditions before allowing the execution of the corresponding tasks. However, some of these functions use scaled balances (supply and borrow) in conjunction with unscaled amounts, which may lead to inaccuracies. 

## Specific Issues

1. In `validate_deposit`, the calculation for `estimate_supply` combines a scaled supply balance with an unscaled amount to compare against the `supply_cap_ceiling`.
2. In `invalidate_withdraw`, the condition `supply_balance >= borrow_balance + amount` compares two values scaled using different indexes; this may result in the condition failing if the supply index is relatively small compared to the borrowing index.
3. In `validate_borrow`, the calculation for `current_borrow_ratio` involves scaled borrow and supply balances multiplied by different indexes.

## Remediation

Insert the validation functions in `logic.move` and place them after the `update_state` call; this ensures that the indexes become updated before performing calculations, and the supply and borrow balances become unscaled by multiplying them with their respective indexes.

## Patch

Fixed in `e4557a5` and `d8ec7e7` by relocating validation functions to `logic.move` and making adjustments to utilize unscaled amounts for comparisons during checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Navi |
| Report Date | N/A |
| Finders | Ajay Shankar, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.naviprotocol.io/
- **GitHub**:  github.com/naviprotocol/protocol-core
- **Contest**: https://www.naviprotocol.io/

### Keywords for Search

`vulnerability`

