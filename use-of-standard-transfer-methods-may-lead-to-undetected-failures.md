---
# Core Classification
protocol: BitFluxFi - Stable AMM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50865
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/coredao/bitfluxfi-stable-amm
source_link: https://www.halborn.com/audits/coredao/bitfluxfi-stable-amm
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Use of standard transfer methods may lead to undetected failures

### Overview


The report describes a bug in the **Router** contract that could lead to undetected transaction failures and unexpected behavior. This is because the contract uses `transfer` and `transferFrom` methods for token transfers, which do not handle cases where tokens do not return a value or return **false** upon failure. This could result in failed transfers without reverts. The affected functions are `convert`, `addLiquidity`, `removeLiquidity`, and `removeBaseLiquidityOneToken`. The recommended solution is to replace these methods with `safeTransfer` and `safeTransferFrom` from OpenZeppelin's SafeERC20 library. The BitFlux team has accepted this risk and stated that they already use the SafeERC20 library in other parts of the contract. They only use `transfer` and `transferFrom` for well-known tokens that adhere strictly to the ERC-20 standard. 

### Original Finding Content

##### Description

The functions `convert`, `addLiquidity`, `removeLiquidity`, and `removeBaseLiquidityOneToken` in the **Router** contract use `transfer` and `transferFrom` methods for token transfers. Unlike `safeTransfer` and `safeTransferFrom` from OpenZeppelin's SafeERC20 library, the standard `transfer` and `transferFrom` methods do not handle cases where tokens do not return a value or return **false** upon failure. This could lead to undetected transaction failures and unexpected behavior if tokens do not adhere strictly to the ERC-20 standard, potentially resulting in failed transfers without reverts. The affected functions are the following:

* `Router.convert`
* `Router.addLiquidity`
* `Router.removeLiquidity`
* `Router.removeBaseLiquidityOneToken`

##### BVSS

[AO:A/AC:L/AX:M/R:N/S:U/C:N/A:N/I:N/D:H/Y:N (5.0)](/bvss?q=AO:A/AC:L/AX:M/R:N/S:U/C:N/A:N/I:N/D:H/Y:N)

##### Recommendation

Replace all instances of `transfer` and `transferFrom` with `safeTransfer` and `safeTransferFrom` from OpenZeppelin's SafeERC20 library. This ensures that all token transfers are properly checked and revert in case of failure, improving the security and reliability of the contract.

##### Remediation

**RISK ACCEPTED**: The **BitFlux team** accepted this risk of this finding and stated the following:

*Router contract already utilizes OpenZeppelin's SafeERC20 library in several parts of the contract. For example, functions such as* ***swapFromBase****,* ***swapToBase****, and* ***removeLiquidity*** *already use* ***safeTransferFrom*** *and* ***safeTransfer*** *to ensure secure token transfers. This is to make sure that transfers either succeed or revert, preventing issues with tokens that do not return a boolean on success.*

*There are specific cases where functions make direct calls to* ***transfer*** *and* ***transferFrom****. These are mainly used when interacting with well-known tokens, such as LPs, which strictly follows ERC-20**standards.*

##### References

contracts/stable-amm/Router.sol#L31, L46, L102, L116, L154

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | BitFluxFi - Stable AMM |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/coredao/bitfluxfi-stable-amm
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/coredao/bitfluxfi-stable-amm

### Keywords for Search

`vulnerability`

