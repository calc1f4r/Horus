---
# Core Classification
protocol: UniswapX Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32978
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uniswapx-audit
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

Gas Limitation Can Disable Smart Contract Wallets

### Overview


This bug report is about a problem with the `CurrencyLibrary` used in UniswapX, which handles ERC-20 tokens and native currency transfers. The issue is that the native transfers are done with a low-level call that has a hard-coded gas limit of 6900, which can cause problems in the future as gas costs change and when using different side-chains or L2s. This can affect smart contract wallets, fee recipients, and the overall functionality of UniswapX. The solution proposed is to remove the gas limitation to ensure the proper functioning of smart contract wallets. The bug has been resolved in a recent pull request.

### Original Finding Content

The `CurrencyLibrary` is used to handle ERC-20 tokens and native currency transfers in UniswapX. The [native transfer](https://github.com/Uniswap/UniswapX/blob/7c5e359fc476f3e55497a8cd6f405f67af2c1dcf/src/lib/CurrencyLibrary.sol#L51) is performed with a low-level call without calldata and a hard-coded gas limit of 6900. 


Gas limits on calls are considered a bad practice for two main reasons: 


       • Gas costs have changed over time (e.g., as per [EIP-1884](https://eips.ethereum.org/EIPS/eip-1884)).  
       • EVM side-chains and L2s can have different gas costs. This has previously caused funds to           become stuck as transfers run out of gas and revert. 


Both arguments could lead to unreliable functionality over time and across chains. A smart contract wallet can have logic in its `receive` or `fallback` function which exceeds the 6900 gas limit, thereby disabling that wallet to use the service for swaps where the native currency is involved. Furthermore, the protocol injects fees into the orders that are sent to the fee recipient, including ETH. Hence, a fee vault or a multi-sig wallet as a fee recipient can be equally affected by this problem. 


Note that the concern of reentrancy should be tackled at the entry point level, which was not identified as a risk for this scope. Further, for the concern regarding the swapper being able to spend the filler's gas maliciously, please see [M-01](#m1). 


Consider removing the gas limitation to guarantee the functionality of smart contract wallets when engaging with UniswapX. 





***Update:** Resolved in [pull request #189](https://github.com/Uniswap/UniswapX/pull/189) at commit [0cdf97e](https://github.com/Uniswap/UniswapX/commit/0cdf97efb147f22ff2131c949aaa49de48eefae0).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UniswapX Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uniswapx-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

