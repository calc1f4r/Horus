---
# Core Classification
protocol: Lombard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53235
audit_firm: OtterSec
contest_link: https://www.lombard.finance/
source_link: https://www.lombard.finance/
github_link: https://github.com/lombard-finance/sui-contracts

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Robert Chen
  - Tuyết Dương
---

## Vulnerability Title

Missing Validator Set Integrity Checks

### Overview

See description below for full details.

### Original Finding Content

## Issues in the `assert_and_configure_validator_set` Implementation

The current implementation of `assert_and_configure_validator_set` in **Consortium** lacks critical checks, which may allow invalid validator keys. The function does not check for duplicate validator public keys. Additionally, there is no validation to ensure that the validator keys are correct and that each validator’s public key is exactly 65 bytes long.

## Code Snippet

```rust
move/consortium/sources/consortium.move
fun assert_and_configure_validator_set(
    consortium: &mut Consortium,
    action: u32,
    validators: vector<vector<u8>>,
    weights: vector<u256>,
    weight_threshold: u256,
    epoch: u256,
) {
    assert!(action == consortium.valset_action, EInvalidAction);
    assert!(validators.length() >= MIN_VALIDATOR_SET_SIZE, EInvalidValidatorSetSize);
    assert!(validators.length() <= MAX_VALIDATOR_SET_SIZE, EInvalidValidatorSetSize);
    assert!(weight_threshold > 0, EInvalidThreshold);
    assert!(validators.length() == weights.length(), EInvalidValidatorsAndWeights);
    [...]
}
```

## Remediation

Ensure that each key in the validators list is exactly 65 bytes long.

## Patch

Resolved in commit **f825f07**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Lombard |
| Report Date | N/A |
| Finders | Robert Chen, Tuyết Dương |

### Source Links

- **Source**: https://www.lombard.finance/
- **GitHub**: https://github.com/lombard-finance/sui-contracts
- **Contest**: https://www.lombard.finance/

### Keywords for Search

`vulnerability`

