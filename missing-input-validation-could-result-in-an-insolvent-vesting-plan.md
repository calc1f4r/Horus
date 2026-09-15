---
# Core Classification
protocol: Merkle Trade Move
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51681
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/taurus-labs/merkle-trade-move
source_link: https://www.halborn.com/audits/taurus-labs/merkle-trade-move
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Missing input validation could result in an insolvent vesting plan

### Overview

See description below for full details.

### Original Finding Content

##### Description

During the creation of a vesting plan, the `create` function, which can be called by anyone, currently lacks validation for the accuracy of the following arguments: `_start_at_sec`, `_end_at_sec`, `_initial_amount` and `_total_amount`.

This oversight presents integrity issues, potentially leading to the following scenarios:

* Creation of a vesting plan allowing the user to claim more than the total amount if the provided initial amount exceeds the total amount.
* Creation of a vesting plan with a start time in the past or one that has already expired.
* Creation of a vesting plan with `start_at_sec` equaling `end_at_sec`, resulting in a division by zero error when calling `get_claimable` and related functions (such as `cancel` and `claim`).
* Creation of a vesting plan where 'start\_at\_sec' is greater than `end_at_sec`, causing an underflow error when calling `get_claimable` and related functions with the current timestamp exceeding the vesting plan's start time.

Code Location
-------------

The `create` function does not validate the user-provided arguments:

```
public fun create(
        _user_address: address,
        _start_at_sec: u64,
        _end_at_sec: u64,
        _initial_amount: u64,
        _total_amount: u64,
        _claimable_fa_store_claim_cap: claimable_fa_store::ClaimCapability
    ): (VestingPlan, ClaimCapability, AdminCapability)
    acquires VestingConfig {
        let config = borrow_global_mut<VestingConfig>(@merkle);
        let uid = config.next_uid;
        let vesting_plan = VestingPlan {
            uid,
            user: _user_address,
            start_at_sec: _start_at_sec,
            end_at_sec: _end_at_sec,
            initial_amount: _initial_amount,
            total_amount: _total_amount,
            claimed_amount: 0,
            paused: false,
            claimable_fa_store_claim_cap: _claimable_fa_store_claim_cap
        };
        config.next_uid = config.next_uid + 1;
        (vesting_plan, ClaimCapability { uid }, AdminCapability { uid })
    }
```

##### BVSS

[AO:A/AC:L/AX:L/R:P/S:U/C:N/A:M/I:M/D:N/Y:N (3.1)](/bvss?q=AO:A/AC:L/AX:L/R:P/S:U/C:N/A:M/I:M/D:N/Y:N)

##### Recommendation

Consider validating user-provided inputs by ensuring the following criteria:

* The initial amount is less than the total amount.
* The current timestamp is before the start time, and the end time is between the start time and a valid upper limit.

Remediation Plan
----------------

**SOLVED:** The **Taurus Labs team** implemented the recommended checks.

##### Remediation Hash

<https://github.com/tauruslabs/merkle-contract/commit/e368a744c4e03e9bfd7ac517a96e1f746d9474e1>

##### References

[tauruslabs/merkle-contract/merkle-token/sources/vesting.move#L53](https://github.com/tauruslabs/merkle-contract/blob/8b9d5bb6a65adfd62654daaba4061287714b2594/merkle-token/sources/vesting.move#L53)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Merkle Trade Move |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/taurus-labs/merkle-trade-move
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/taurus-labs/merkle-trade-move

### Keywords for Search

`vulnerability`

