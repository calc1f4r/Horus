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
solodit_id: 24725
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-paladin
source_link: https://code4rena.com/reports/2022-03-paladin
github_link: https://github.com/code-423n4/2022-03-paladin-findings/issues/64

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

[M-11] Emergency mode enable/disable issue

### Overview


This bug report discusses a potential issue with the emergency mode of the HolyPaladinToken contract. Enabling emergency mode should be a one-way process that sets the contract in emergency mode, and it should not be possible to revert this process. If it is, then the owner of the contract is in a privileged position and could trigger emergency mode, perform emergency withdrawal operations without any restrictions, and then disable emergency mode. The recommended mitigation step is to remove the "bool trigger" parameter from the triggerEmergencyWithdraw function and set the emergency to true after the function is successfully executed. Kogaroshi (Paladin) acknowledged this issue and commented that the current emergency system will not be updated. During deployment, the admin of the contract will be set to be the Paladin DAO multisig, and the Governance will decide on admin decision for this contract. This layer of the multisig is meant to prevent any potential abuse of the emergency system.

### Original Finding Content

_Submitted by reassor_

Enabling emergency mode should be one way process that sets contract(s) in emergency mode. It should be not possible to revert that process, otherwise it puts owner of the contract(s) in very privileged position. Owner can trigger emergency mode, perform emergency withdrawal operations without any restrictions and then disable emergency mode.

### Proof of Concept

[HolyPaladinToken.sol#L1425](https://github.com/code-423n4/2022-03-paladin/blob/9c26ec8556298fb1dc3cf71f471aadad3a5c74a0/contracts/HolyPaladinToken.sol#L1425)

### Recommended Mitigation Steps

It is recommended to remove `bool trigger` parameter from `triggerEmergencyWithdraw` function and set `emergency` to `true` after successfully executing function.

**[Kogaroshi (Paladin) acknowledged and commented](https://github.com/code-423n4/2022-03-paladin-findings/issues/64#issuecomment-1086848734):**
 > This Issue is acknowledged. The current emergency system will not be updated.<br>
> During deployment, the admin of the contract will be set to be the Paladin DAO multisig, and the Governance will decide on admin decision for this contract. Yet we don't want the emergency system to totally kill the contract, but to allow users to exit if there is an issue that can be remediated.
> 
> As much as any version of this contract that will be deployed as a single signer being admin of this system could present the risk of the presented scenario, in our case we use the layer that is the multisig to prevent this type of abuse.



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
- **GitHub**: https://github.com/code-423n4/2022-03-paladin-findings/issues/64
- **Contest**: https://code4rena.com/reports/2022-03-paladin

### Keywords for Search

`vulnerability`

