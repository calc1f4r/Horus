---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24836
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-08-frax
source_link: https://code4rena.com/reports/2022-08-frax
github_link: https://github.com/code-423n4/2022-08-frax-findings/issues/236

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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] FraxlendPair.changeFee() doesn't update interest before changing fee.

### Overview



This bug report is about a function in the FraxlendPairCore.sol code that changes the protocol fee used during interest calculation. However, it does not update interest before changing the fee, which causes the _feesAmount to be calculated incorrectly.

The bug can be demonstrated by looking at the pause() and unpause() functions, which call _addInterest() before any changes. But when using the changeFee() function, it does not update interest, leading to incorrect calculations.

The severity of the bug was discussed, with DrakeEvans (Frax) disagreeing with the severity and commenting that it can be mitigated by calling addInterest() beforehand by the admin or regular user. 0xA5DF (warden) commented that admins might not be aware of the issue, leading to higher interest than intended. GititGoro (judge) maintained the severity as it is a potential leakage.

The recommended mitigation step is to modify the changeFee() function by adding a call to _addInterest() before changing the fee.

### Original Finding Content

_Submitted by auditor0517_

This function is changing the protocol fee that is used during interest calculation [here](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L477-L488).

But it doesn't update interest before changing the fee so the `_feesAmount` will be calculated wrongly.

### Proof of Concept

As we can see during [pause()](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPair.sol#L326) and [unpause()](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPair.sol#L335), `_addInterest()` must be called before any changes.

But with the [changeFee()](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPair.sol#L215), it doesn't update interest and the `_feesAmount` might be calculated wrongly.

*   At time `T1`, [\_currentRateInfo.feeToProtocolRate = F1](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L477).
*   At `T2`, the owner had changed the fee to `F2`.
*   At `T3`, [\_addInterest()](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L409) is called during `deposit()` or other functions.
*   Then [during this calculation](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L477-L488), `F1` should be applied from `T1` to `T2` and `F2` should be applied from `T2` and `T3`. But it uses `F2` from `T1` to `T2`.

### Recommended Mitigation Steps

Recommend modifying `changeFee()` like below.

    function changeFee(uint32 _newFee) external whenNotPaused {
        if (msg.sender != TIME_LOCK_ADDRESS) revert OnlyTimeLock();
        if (_newFee > MAX_PROTOCOL_FEE) {
            revert BadProtocolFee();
        }

        _addInterest(); //+++++++++++++++++++++++++++++++++

        currentRateInfo.feeToProtocolRate = _newFee;
        emit ChangeFee(_newFee);
    }

**[DrakeEvans (Frax) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2022-08-frax-findings/issues/236#issuecomment-1238159753):**
 > Disagree with severity as it can be mitigated by calling `addInterest()` beforehand by admin or regular user.  But we will address it anyway for convenience. We assume admins are not malicious.

**[0xA5DF (warden) commented](https://github.com/code-423n4/2022-08-frax-findings/issues/236#issuecomment-1238249426):**
> Admins might not be malicious, but without knowing about the issue (i.e. if the warden hasn't reported this) they wouldn't call `addInterest()` beforehand, leading to higher interest than intended.

**[gititGoro (judge) commented](https://github.com/code-423n4/2022-08-frax-findings/issues/236#issuecomment-1263082292):**
 > Maintaining severity as it is a potential leakage.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-frax
- **GitHub**: https://github.com/code-423n4/2022-08-frax-findings/issues/236
- **Contest**: https://code4rena.com/reports/2022-08-frax

### Keywords for Search

`vulnerability`

