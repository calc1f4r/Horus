---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24723
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-paladin
source_link: https://code4rena.com/reports/2022-03-paladin
github_link: https://github.com/code-423n4/2022-03-paladin-findings/issues/54

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

[M-09] Function `cooldown()` is not protected when protocol in emergency mode

### Overview


This bug report is about a function called cooldown() in the HolyPaladinToken.sol contract which is not protected when the protocol is in emergency mode. This is inconsistent with the other major functions defined in the contract which are protected by checking for the emergency flag and reverting.

The impact of this bug is that users can set the cooldown() immediately when the emergency mode is active and plan for unstaking when the emergency mode is lifted and the cooldown period expires. This is not the desirable behaviour expected by the protocol.

The recommended mitigation steps are to add a check for the emergency mode for this function also, by adding the following code: 

```
if(emergency) revert EmergencyBlock();
```

This bug was confirmed, resolved, and commented on by Kogaroshi (Paladin), and changes were made in PaladinFinance/Paladin-Tokenomics#10.

### Original Finding Content

_Submitted by hubble_

[HolyPaladinToken.sol#L228-L235](https://github.com/code-423n4/2022-03-paladin/blob/9c26ec8556298fb1dc3cf71f471aadad3a5c74a0/contracts/HolyPaladinToken.sol#L228-L235)<br>

Function cooldown() is not protected when protocol is in emergency mode.<br>
Its behavior is not consistent with the other major functions defined.

### Impact

While other major functions like stake, unstake, lock, unlock, etc., of this contract is protected by checking for emergency flag and reverting,
this function cooldown() is not checked. The impact of this is that during emergency mode, users can set immediately the cooldown() and plan for unstaking when the emergency mode is lifted and cooldown period expires. This may not be the desirable behaviour expected by the protocol.

### Proof of Concept

Contract Name : HolyPaladinToken.sol
Function cooldown()

### Recommended Mitigation Steps

Add checking for emergency mode for this function also.

    if(emergency) revert EmergencyBlock();

**[Kogaroshi (Paladin) confirmed, resolved, and commented](https://github.com/code-423n4/2022-03-paladin-findings/issues/54#issuecomment-1086726017):**
 > Changes made in: [PaladinFinance/Paladin-Tokenomics#10](https://github.com/PaladinFinance/Paladin-Tokenomics/pull/10).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-paladin
- **GitHub**: https://github.com/code-423n4/2022-03-paladin-findings/issues/54
- **Contest**: https://code4rena.com/reports/2022-03-paladin

### Keywords for Search

`vulnerability`

