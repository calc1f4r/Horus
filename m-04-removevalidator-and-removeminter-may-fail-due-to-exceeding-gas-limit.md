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
solodit_id: 25441
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-frax
source_link: https://code4rena.com/reports/2022-09-frax
github_link: https://github.com/code-423n4/2022-09-frax-findings/issues/12

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

[M-04] removeValidator() and removeMinter() may fail due to exceeding gas limit

### Overview


This bug report is about two functions, `removeValidator()` and `removeMinter()`, found in the code of the Frax protocol. The `removeValidator()` function is used to remove a validator from the array `validators`, and the `removeMinter()` function is used to remove a minter from the array `minters_array`. The issue is that both functions have an unbounded loop that can cause the function call to fail due to exceeding the gas limit if the array gets too large.

The severity of the issue has been debated in the comments. FortisFortuna (Frax) commented that the number of minters will always remain low, so it might not be an issue. 0xean (judge) suggested that the issue should be rated as Medium, as it could impact the functionality of the protocol. Trust (warden) commented that the issue should not be rated as Medium, as the sender can always send enough gas and the validator array gets truncated every time one is popped for use.

### Original Finding Content


<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/OperatorRegistry.sol#L113-L118>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/ERC20/ERC20PermitPermissionedMint.sol#L84-L89>

### Vulnerability Details

#### removeValidator() and removeMinter() may fail due to exceeding gas limit

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/OperatorRegistry.sol#L113-L118>

                for (uint256 i = 0; i < original_validators.length; ++i) {
                    if (i != remove_idx) {
                        validators.push(original_validators[i]);
                    }
                }

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/ERC20/ERC20PermitPermissionedMint.sol#L84-L89>

            for (uint i = 0; i < minters_array.length; i++){ 
                if (minters_array[i] == minter_address) {
                    minters_array[i] = address(0); // This will leave a null in the array and keep the indices the same
                    break;
                }
            }

The `removeValidator()` is used to remove a validator from the array `validators`.

There is an unbounded loop in `removeValidator()` such that if the `validators` array gets sufficiently large, this function call will fail due to exceeding the gas limit.

The same issue exists in the `removeMinter()` function. If `minters_array` gets large, the function call will fail.

**[FortisFortuna (Frax) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/12#issuecomment-1257294786):**
 > Technically correct, but in practice, the number of minters will always remain low. If it becomes an issue, we can designate one minter as a "pre-minter" that has a batch of tokens minted to it beforehand, then auxiliary contracts can connect to that instead of ERC20PermitPermissionedMint.sol instead.

**[0xean (judge) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/12#issuecomment-1278206459):**
 > I think Medium is appropriate here, given this could impact the functionality of the protocol. 

**[Trust (warden) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/12#issuecomment-1279848072):**
 > Wouldn't call this a risk to the functionality of the protocol, because sender can always send enough gas, and validator array gets truncated every time on is popped for use.
 >
> Unbounded for-loops should be handled with care but not sure a realistic impact can be demonstrated here to qualify for Medium.



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

- **Source**: https://code4rena.com/reports/2022-09-frax
- **GitHub**: https://github.com/code-423n4/2022-09-frax-findings/issues/12
- **Contest**: https://code4rena.com/reports/2022-09-frax

### Keywords for Search

`vulnerability`

