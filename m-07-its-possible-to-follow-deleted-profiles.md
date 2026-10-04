---
# Core Classification
protocol: Aave Lens
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42472
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-02-aave-lens
source_link: https://code4rena.com/reports/2022-02-aave-lens
github_link: https://github.com/code-423n4/2022-02-aave-lens-findings/issues/70

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
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] It's possible to follow deleted profiles

### Overview


This bug report discusses an issue in the code for Aave Lens, specifically in the InteractionLogic.sol file. The code is supposed to check if a profile exists before allowing someone to follow it, but there is a problem where a deleted profile can still be followed if a new profile with the same handle is created. This can lead to confusion and unintended actions. The report recommends a change to the code to fix this issue, which has been confirmed and resolved by the Aave Lens team. The judge also commented on the report, acknowledging the find.

### Original Finding Content

_Submitted by danb_

[InteractionLogic.sol#L49](https://github.com/code-423n4/2022-02-aave-lens/blob/main/contracts/libraries/InteractionLogic.sol#L49)<br>

When someone tries to follow a profile, it checks if the handle exists, and if it doesn't, it reverts because the profile is deleted.
The problem is that there might be a new profile with the same handle as the deleted one, allowing following deleted profiles.

### Proof of Concept

Alice creates a profile with the handle "alice." The profile id is 1.<br>
She deleted the profile.<br>
She opens a new profile with the handle "alice". The new profile id is 2.<br>
Bob tries to follow the deleted profile (id is 1).<br>
The check<br>

    if (_profileIdByHandleHash[keccak256(bytes(handle))] == 0)
    	revert Errors.TokenDoesNotExist();

doesn't revert because there exists a profile with the handle "alice".<br>
Therefore Bob followed a deleted profile when he meant to follow the new profile.

### Recommended Mitigation Steps

Change to:

    if (_profileIdByHandleHash[keccak256(bytes(handle))] != profileIds[i])
    	revert Errors.TokenDoesNotExist();

**[Zer0dot (Aave Lens) confirmed and commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/70#issuecomment-1072661676):**
 > Will be changed to use the new `exists()` terminology. Valid!

**[Zer0dot (Aave Lens) commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/70#issuecomment-1072741927):**
 > Correction, we won't be using `exists()` to prevent extra calls, adding this comment!

**[Zer0dot (Aave Lens) resolved and commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/70#issuecomment-1072745226):**
 > Resolved in [aave/lens-protocol#69](https://github.com/aave/lens-protocol/pull/69).

**[0xleastwood (judge) commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/70#issuecomment-1117941336):**
 > Nice find!



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Aave Lens |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-aave-lens
- **GitHub**: https://github.com/code-423n4/2022-02-aave-lens-findings/issues/70
- **Contest**: https://code4rena.com/reports/2022-02-aave-lens

### Keywords for Search

`vulnerability`

