---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32706
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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

Missing Deadline Check for Functions Which Call Uniswap v3 FlashSwap

### Overview


This bug report is about a missing option to set a deadline for certain functions in the Ion Protocol code. These functions are used for flash swapping and can sometimes get stuck in the mempool, causing the transaction to be executed much later than intended. During this time, the price in the Uniswap pool can change, making the swap vulnerable to attacks. The suggestion is to add a deadline check to these functions to prevent this issue. This bug has been resolved in a recent update.

### Original Finding Content

There is no option to set a `deadline` for the [`flashswapLeverage`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/UniswapFlashswapHandler.sol#L82), [`flashswapDeleverage`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/UniswapFlashswapHandler.sol#L127), [`flashLeverageWethAndSwap`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/UniswapFlashloanBalancerSwapHandler.sol#L59) and [`flashDeleverageWethAndSwap`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/UniswapFlashloanBalancerSwapHandler.sol#L115) functions. The transaction can still be stuck in the mempool and be executed a long time after the transaction is initially called. During this time, the price in the Uniswap pool can change. In this case, the slippage parameters can become outdated and the swap will become vulnerable to sandwich attacks.


Consider adding a deadline check to the [`flashswapLeverage`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/UniswapFlashswapHandler.sol#L82), [`flashswapDeleverage`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/UniswapFlashswapHandler.sol#L127), [`flashLeverageWethAndSwap`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/UniswapFlashloanBalancerSwapHandler.sol#L59) and [`flashDeleverageWethAndSwap`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/UniswapFlashloanBalancerSwapHandler.sol#L115) functions.


***Update:** Resolved in [pull request #25](https://github.com/Ion-Protocol/ion-protocol/pull/25).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

