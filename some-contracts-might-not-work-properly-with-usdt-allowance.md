---
# Core Classification
protocol: Across Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56764
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Some Contracts Might Not Work Properly with USDT Allowance

### Overview


The `ERC7683OrderDepositorExternal` contract has a bug that causes it to fail when using certain tokens, like USDT. This is because the `safeIncreaseAllowance` function is used, which can only work if the entire allowance is spent in the `depositV3` function call. This bug also affects other contracts that use the `safeIncreaseAllowance` function, like the `ZkStack_Adapter` and `ZkStack_CustomGasToken_Adapter`. To fix this, the `forceApprove` function from the `SafeERC20` library should be used instead. This bug has been resolved in a recent update.

### Original Finding Content

The `ERC7683OrderDepositorExternal` contract implements the `_deposit` function to finalize the creation of an Across V3 deposit. To do so, the function [calls](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683OrderDepositorExternal.sol#L58) the `safeIncreaseAllowance` function on the `inputToken` specified in the order details. This mechanism will work with any token under the assumption that the entire allowance will be spent by the SpokePool in the [`depositV3` function call](https://github.com/across-protocol/contracts/blob/108be77c29a3861c64bdf66209ac6735a6a87090/contracts/erc7683/ERC7683OrderDepositorExternal.sol#L60-L73). The `safeIncreaseAllowance` function is also used in the [`ZkStack_Adapter`](https://github.com/across-protocol/contracts/blob/5a0c67c984d19a3bb843a4cec9bb081734583dd1/contracts/chain-adapters/ZkStack_Adapter.sol#L147) and the [`ZkStack_CustomGasToken_Adapter`](https://github.com/across-protocol/contracts/blob/5a0c67c984d19a3bb843a4cec9bb081734583dd1/contracts/chain-adapters/ZkStack_CustomGasToken_Adapter.sol#L189) contracts, along with some other adapters like the [ZkSync\_Adapter](https://github.com/across-protocol/contracts/blob/5a0c67c984d19a3bb843a4cec9bb081734583dd1/contracts/chain-adapters/ZkSync_Adapter.sol#L241) which are out of scope for this audit.

However, if for any reason, the entire allowance is not used after the approval, any further attempt to `safeIncreaseAllowance` with tokens that prohibit any approval change from non-zero to non-zero values, like USDT, will ultimately fail. As an example of a real impact, the second example of issue [M08](#m08) will likely produce a scenario in which subsequent calls with USDT as the custom gas token will fail, thus blocking the entire `ZkStack_CustomGasToken_Adapter`'s functionality.

Consider using the `forceApprove` [function](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/54b3f14346da01ba0d159114b399197fea8b7cda/contracts/token/ERC20/utils/SafeERC20.sol#L82) of the `SafeERC20` library to be compatible with tokens that revert on approvals from non-zero to non-zero values.

***Update:** Resolved in [pull request #734](https://github.com/across-protocol/contracts/pull/734) at commit [ea59869](https://github.com/across-protocol/contracts/pull/734/commits/ea59869826acbb2ee70b43dd0779288bab3007e7).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

