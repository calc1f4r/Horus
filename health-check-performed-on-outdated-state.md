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
solodit_id: 48038
audit_firm: OtterSec
contest_link: https://www.naviprotocol.io/
source_link: https://www.naviprotocol.io/
github_link:  github.com/naviprotocol/protocol-core

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
  - Ajay Shankar
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Health Check Performed On Outdated State

### Overview


The bug report discusses an issue with the is_health function in the logic.move code. This function is used to check the health of a user's account, but it relies on outdated information about the user's collateral and loan balances. This can cause inaccuracies, especially during the liquidation process. 

To fix this issue, the developers recommend updating all asset states before conducting the health check. This has been addressed in a recent patch.

### Original Finding Content

## Health Validation Issue in Logic.move

The `is_health` assert in `execute_withdraw` and `execute_borrow` in `logic.move` depends on the user’s collateral and loan balances. However, these balances are not updated with `update_state` during health validation, potentially causing inaccuracies. This issue is particularly impactful during the liquidation process, as outdated collateral asset states may lead to exclusion from liquidation.

## Code Snippet: RUST

```rust
public(friend) fun execute_borrow(clock: &Clock, oracle: &PriceOracle, storage: &mut Storage, asset: u8, user: address, amount: u256) {
    //////////////////////////////////////////////////////////////////
    // Update borrow_index, supply_index, last_timestamp, treasury //
    //////////////////////////////////////////////////////////////////
    update_state(clock, storage, asset);
    /////////////////////////////////////////////////////////////////////
    // Convert balances to actual balances using the latest exchange rates //
    /////////////////////////////////////////////////////////////////////
    increase_borrow_balance(storage, asset, user, amount);
    ///////////////////////////////////////////////////////////
    // Add the asset to the user's list of loan assets //
    ///////////////////////////////////////////////////////////
    if (!is_loan(storage, asset, user)) {
        storage::update_user_loans(storage, asset, user)
    };
    /////////////////////////////////
    // Checking user health factors //
    /////////////////////////////////
    assert!(is_health(oracle, storage, user), LOGIC_USER_UN_HEALTH);
    update_interest_rate(storage, asset);
}
```

## Remediation

Update all asset states invoking `update_state` before performing the health check.

## Patch

Addressed in `c3dbdd3` by updating all asset states prior to conducting the health check.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

