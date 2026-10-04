---
# Core Classification
protocol: Bucket Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48016
audit_firm: OtterSec
contest_link: https://bucketprotocol.io/
source_link: https://bucketprotocol.io/
github_link: https://github.com/Bucket-Protocol/v1-core

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Improper Conversion

### Overview


The report is about a bug in the bottle module of the protocol, which calculates the collateral amount returned for a given debt amount. The code in question is written in RUST and is used to determine the collateral amount when repaying a loan. However, the bug occurs when the debt amount is equal to or greater than the Bottle debt. In this case, the collateral amount is calculated as 1.1 times the debt amount, but the calculation does not take into account the decimals of the collateral token, resulting in an incorrect value for the collateral amount. The suggested solution is to adjust the calculation based on the decimals of the collateral token. The bug has been fixed in the latest version of the code.

### Original Finding Content

## `record_repay_capped` Function in the Bottle Module

The `record_repay_capped` function calculates the collateral amount returned for a given debt amount.

## Function Signature

```rust
public(friend) fun record_repay_capped<T>(
    bottle: &mut Bottle, 
    repay_amount: u64,
    oracle: &BucketOracle, 
    clock: &Clock
): (bool, u64) {
```

## Logic Description

1. **Check if Debt Amount is Greater than or Equal to Bottle Debt:**
    ```rust
    if (repay_amount >= bottle.buck_amount) {
    ```

    - Retrieve price and denominator:
    ```rust
    let (price, denominator) = bucket_oracle::get_price<T>(oracle, clock);
    ```
    
    - Calculate collateral returned (maximum of 110% of the debt):
    ```rust
    let return_sui_amount = mul_factor(repay_amount * 110 / 100, denominator, price);
    ```
    
    - Update the bottle's collateral and debt:
    ```rust
    bottle.collateral_amount = bottle.collateral_amount - return_sui_amount;
    bottle.buck_amount = 0;
    ```
    
    - Return statement:
    ```rust
    (true, return_sui_amount)
    ```

2. **If Debt Amount is Less Than Bottle Debt:**
    ```rust
    } else {
    ```
    
    - Calculate collateral returned based on the debt amount:
    ```rust
    let return_sui_amount = mul_factor(bottle.collateral_amount, repay_amount, bottle.buck_amount);
    ```
    
    - Update the bottle's collateral and debt:
    ```rust
    bottle.collateral_amount = bottle.collateral_amount - return_sui_amount;
    bottle.buck_amount = bottle.buck_amount - repay_amount;
    ```
    
    - Return statement:
    ```rust
    (false, return_sui_amount)
    ```

## Problem Description

If the debt amount (`repay_amount`) is greater than or equal to the bottle debt, the collateral returned is calculated as 1.1 times the debt amount. However, the conversion of the debt amount to the collateral amount is not adjusted based on the decimals of the collateral token, leading to an improper value for the collateral amount (`return_sui_amount`).

## Remediation

Correctly convert the amount based on the decimals of the collateral token.

## Patch

Fixed in commit `2b68221` by correctly calculating `return_sui_amount`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Bucket Protocol |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://bucketprotocol.io/
- **GitHub**: https://github.com/Bucket-Protocol/v1-core
- **Contest**: https://bucketprotocol.io/

### Keywords for Search

`vulnerability`

