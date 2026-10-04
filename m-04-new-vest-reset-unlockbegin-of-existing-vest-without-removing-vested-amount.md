---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: missing-logic

# Attack Vector Details
attack_type: missing-logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1983
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-badger-citadel-contest
source_link: https://code4rena.com/reports/2022-04-badger-citadel
github_link: https://github.com/code-423n4/2022-04-badger-citadel-findings/issues/158

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
  - missing-logic
  - don't_update_state
  - overflow/underflow

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - TrungOre
  - cccz
  - cmichel
  - minhquanym
  - 0xDjango
---

## Vulnerability Title

[M-04] New vest reset `unlockBegin` of existing vest without removing vested amount

### Overview


This bug report is about a vulnerability in the code of the StakedCitadelVester smart contract. When the `vest` function is called by the xCTDL vault, the amount previously locked will be re-locked according to the new vesting timeline. This can lead to an underflow if `vesting[recipient].claimedAmounts` is greater than 0, as the user will need to vest the claimed amount again, which should not be the expected behavior.

The recommended mitigation steps are to reset the `claimedAmounts` on the new vest, as shown in the code snippet provided. This will ensure that the amount claimed is not re-vested, avoiding the underflow.

### Original Finding Content

_Submitted by gzeon, also found by cccz, TrungOre, minhquanym, cmichel, 0xDjango, and rayn_

<https://github.com/code-423n4/2022-04-badger-citadel/blob/18f8c392b6fc303fe95602eba6303725023e53da/src/StakedCitadelVester.sol#L143>

<https://github.com/code-423n4/2022-04-badger-citadel/blob/18f8c392b6fc303fe95602eba6303725023e53da/src/StakedCitadelVester.sol#L109>

### Impact

When `vest` is called by xCTDL vault, the previous amount will re-lock according to the new vesting timeline. While this is as described in L127, `claimableBalance` might revert due to underflow if `vesting[recipient].claimedAmounts` > 0 because the user will need to vest the `claimedAmounts` again which should not be an expected behavior as it is already vested.

### Proof of Concept

<https://github.com/code-423n4/2022-04-badger-citadel/blob/18f8c392b6fc303fe95602eba6303725023e53da/src/StakedCitadelVester.sol#L143>

            vesting[recipient].lockedAmounts =
                vesting[recipient].lockedAmounts +
                _amount;
            vesting[recipient].unlockBegin = _unlockBegin;
            vesting[recipient].unlockEnd = _unlockBegin + vestingDuration;

<https://github.com/code-423n4/2022-04-badger-citadel/blob/18f8c392b6fc303fe95602eba6303725023e53da/src/StakedCitadelVester.sol#L109>

            uint256 locked = vesting[recipient].lockedAmounts;
            uint256 claimed = vesting[recipient].claimedAmounts;
            if (block.timestamp >= vesting[recipient].unlockEnd) {
                return locked - claimed;
            }
            return
                ((locked * (block.timestamp - vesting[recipient].unlockBegin)) /
                    (vesting[recipient].unlockEnd -
                        vesting[recipient].unlockBegin)) - claimed;

### Recommended Mitigation Steps

Reset claimedAmounts on new vest

            vesting[recipient].lockedAmounts =
                vesting[recipient].lockedAmounts - 
                vesting[recipient].claimedAmounts +
                _amount;
            vesting[recipient].claimedAmounts = 0
            vesting[recipient].unlockBegin = _unlockBegin;
            vesting[recipient].unlockEnd = _unlockBegin + vestingDuration;

**[shuklaayush (BadgerDAO) confirmed and commented](https://github.com/code-423n4/2022-04-badger-citadel-findings/issues/158#issuecomment-1110273728):**
 > I think this is valid and was fixed in 
> https://github.com/Citadel-DAO/citadel-contracts/pull/44

**[jack-the-pug (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-04-badger-citadel-findings/issues/158#issuecomment-1140759899):**
 > I'm downgrading this to Medium as there are no funds directly at risk, but a malfunction and leak of value. The user will have to wait for a longer than expected time to claim their vested funds.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | TrungOre, cccz, cmichel, minhquanym, 0xDjango, gzeon, rayn |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-badger-citadel
- **GitHub**: https://github.com/code-423n4/2022-04-badger-citadel-findings/issues/158
- **Contest**: https://code4rena.com/contests/2022-04-badger-citadel-contest

### Keywords for Search

`Missing-Logic, Don't update state, Overflow/Underflow`

