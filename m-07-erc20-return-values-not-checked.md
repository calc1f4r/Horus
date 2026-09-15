---
# Core Classification
protocol: Amun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6529
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-amun-contest
source_link: https://code4rena.com/reports/2021-12-amun
github_link: https://github.com/code-423n4/2021-12-amun-findings/issues/192

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - JMukesh
  - cmichel
  - WatchPug
  - p4st13r4
  - defsec
---

## Vulnerability Title

[M-07] ERC20 return values not checked

### Overview


This bug report is about a vulnerability in the `ERC20.transfer()` and `ERC20.transferFrom()` functions. These functions return a boolean value indicating success, but some tokens do not revert if the transfer fails but instead return `false`. This means that tokens that don't actually perform the transfer and return `false` are still counted as a correct transfer and the tokens remain in the `SingleNativeTokenExitV2` contract and could potentially be stolen by someone else.

The recommended mitigation step is to use OpenZeppelin’s `SafeERC20` versions with the `safeTransfer` and `safeTransferFrom` functions that handle the return value check as well as non-standard-compliant tokens. This will help to ensure that tokens are not left in the `SingleNativeTokenExitV2` contract and are instead transferred to the intended recipient.

### Original Finding Content


_Submitted by cmichel, also found by defsec, JMukesh, p4st13r4, and WatchPug_

The `ERC20.transfer()` and `ERC20.transferFrom()` functions return a boolean value indicating success. This parameter needs to be checked for success.
Some tokens do **not** revert if the transfer failed but return `false` instead.

See:

- `SingleNativeTokenExitV2.exit`'s `outputToken.transfer(msg.sender, outputTokenBalance);`
- `PieFactoryContract.bakePie`'s `pie.transfer(msg.sender, _initialSupply);`

#### Impact

Tokens that don't actually perform the transfer and return `false` are still counted as a correct transfer and the tokens remain in the `SingleNativeTokenExitV2` contract and could potentially be stolen by someone else.

#### Recommended Mitigation Steps

We recommend using [OpenZeppelin’s `SafeERC20`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.1/contracts/token/ERC20/utils/SafeERC20.sol#L74) versions with the `safeTransfer` and `safeTransferFrom` functions that handle the return value check as well as non-standard-compliant tokens.

**[0xleastwood (Judge) commented](https://github.com/code-423n4/2021-12-amun-findings/issues/192#issuecomment-1019041118):**

> Nice find! I think this is valid considering the extent basket tokens are used. It is more than likely that non-standard tokens will be utilised.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Amun |
| Report Date | N/A |
| Finders | JMukesh, cmichel, WatchPug, p4st13r4, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-amun
- **GitHub**: https://github.com/code-423n4/2021-12-amun-findings/issues/192
- **Contest**: https://code4rena.com/contests/2021-12-amun-contest

### Keywords for Search

`vulnerability`

