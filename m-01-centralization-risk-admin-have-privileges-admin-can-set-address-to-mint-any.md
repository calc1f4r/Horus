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
solodit_id: 25438
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-frax
source_link: https://code4rena.com/reports/2022-09-frax
github_link: https://github.com/code-423n4/2022-09-frax-findings/issues/107

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

[M-01] Centralization risk: admin have privileges: admin can set address to mint any amount of frxETH, can set any address as validator, and change important state in frxETHMinter and withdraw fund from frcETHMinter

### Overview


This bug report is about the permission structure of FortisFortuna (Frax), a decentralized finance protocol. The admin has privileges to set address to mint any amount of frxETH, can set any address as validator, and change important state in frxETHMinter and withdraw fund from frcETHMinter. The admin can add or remove validator from OperatorRegistry.sol, set minter address or remove minter address in frxETH.sol, mint or burn any amount of frxETH token, set ETE deduction ratio, and withdraw any amount of ETH or ERC20 token in frcETHMinter.sol.

The bug report states that without significant redesign, it is not possible to avoid the admin being able to rug pull the protocol. As a result, the recommendation is to set all admin functions behind either a timelocked DAO or at least a timelocked multisig contract. The FortisFortuna (Frax) team is aware of the permission structure and mentioned that the owner will most likely be a large multisig. The bug report has been used as the canonical issue for all "malicious owner" type reports and it is important for end users to understand the highlighted issues in the report.

### Original Finding Content


<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/ERC20/ERC20PermitPermissionedMint.sol#L41>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/ERC20/ERC20PermitPermissionedMint.sol#L53>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/ERC20/ERC20PermitPermissionedMint.sol#L65>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/ERC20/ERC20PermitPermissionedMint.sol#L76>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/ERC20/ERC20PermitPermissionedMint.sol#L94>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/frxETHMinter.sol#L159>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/frxETHMinter.sol#L166>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/frxETHMinter.sol#L177>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/frxETHMinter.sol#L184>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/frxETHMinter.sol#L191>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/frxETHMinter.sol#L199>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/OperatorRegistry.sol#L53>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/OperatorRegistry.sol#L61>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/OperatorRegistry.sol#L69>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/OperatorRegistry.sol#L82>

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/OperatorRegistry.sol#L93>

### Impact

Admin have privileges: admin can set address to mint any amount of frxETH, can set any address as validator, and change important state in frxETHMinter and withdraw fund from frcETHMinter.

Note the modifier below, either the timelock governance contract or the contract owner can access to all the high privilege function.

        modifier onlyByOwnGov() {
            require(msg.sender == timelock_address || msg.sender == owner, "Not owner or timelock");
            _;
        }

There are numerous methods that the admin could apply to rug pull the protocol and take all user funds.

The admin can

    add or remove validator from OperatorRegistry.sol

    set minter address or remove minter address in frxETH.sol

    minter set by admin can mint or burn any amount of frxETH token.

    set ETE deduction ratio, withdraw any amount of ETH or ERC20 token in frcETHMinter.sol

### Tools Used

Foundry

### Recommended Mitigation Steps

Without significant redesign it is not possible to avoid the admin being able to rug pull the protocol.

As a result the recommendation is to set all admin functions behind either a timelocked DAO or at least a timelocked multisig contract.

**[FortisFortuna (Frax) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/107#issuecomment-1257281609):**
 > We are well aware of the permission structure. The owner will most likely be a large multisig. We mentioned the Frax Multisig in the scope too.

**[0xean (judge) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/107#issuecomment-1276220502):**
 > Going to use this issue as the canonical issue for all "malicious owner" type reports.  The protocol does have some serious "trust" in the administrator and the highlighted issues are important for end users to understand and should be part of the report. 



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
- **GitHub**: https://github.com/code-423n4/2022-09-frax-findings/issues/107
- **Contest**: https://code4rena.com/reports/2022-09-frax

### Keywords for Search

`vulnerability`

