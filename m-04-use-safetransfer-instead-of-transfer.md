---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42273
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-08-yield
source_link: https://code4rena.com/reports/2021-08-yield
github_link: https://github.com/code-423n4/2021-08-yield-findings/issues/36

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

[M-04] Use `safeTransfer` instead of `transfer`

### Overview


This report is about an issue with the transfer function in a smart contract that manages ERC20 tokens. The issue is that the function may return a false value, indicating a failed transfer, but the calling contract may not be able to detect this failure if it does not check the return value. This is a problem because the ERC20 specification requires callers to handle this false value and not assume that it will never be returned. To fix this issue, it is recommended to use the SafeERC20 library from OpenZeppelin and call the safeTransfer or safeTransferFrom functions instead. This issue has been confirmed and patched by the Yield protocol team.

### Original Finding Content

_Submitted by shw_

Tokens not compliant with the ERC20 specification could return `false` from the `transfer` function call to indicate the transfer fails, while the calling contract would not notice the failure if the return value is not checked. Checking the return value is a requirement, as written in the [EIP-20](https://eips.ethereum.org/EIPS/eip-20) specification:
> Callers MUST handle `false` from `returns (bool success)`. Callers MUST NOT assume that `false` is never returned!

See [ERC20Rewards.sol L175](https://github.com/code-423n4/2021-08-yield/blob/main/contracts/utils/token/ERC20Rewards.sol#L175).

Recommend using the `SafeERC20` library [implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) from OpenZeppelin and calling `safeTransfer` or `safeTransferFrom` when transferring ERC20 tokens.

**[alcueca (Yield) confirmed and patched](https://github.com/code-423n4/2021-08-yield-findings/issues/36#issuecomment-899365631):**
 > [Fix](https://github.com/yieldprotocol/yield-utils-v2/commit/3715140ab7d6fbde593257c7542a661bc9191d8c)



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-yield
- **GitHub**: https://github.com/code-423n4/2021-08-yield-findings/issues/36
- **Contest**: https://code4rena.com/reports/2021-08-yield

### Keywords for Search

`vulnerability`

