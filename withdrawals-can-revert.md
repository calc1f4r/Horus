---
# Core Classification
protocol: StakeStone
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59185
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/stake-stone/4b7cbc5e-5595-4ac4-ac36-176f43ee9adf/index.html
source_link: https://certificate.quantstamp.com/full/stake-stone/4b7cbc5e-5595-4ac4-ac36-176f43ee9adf/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Mustafa Hasan
  - Roman Rohleder
  - Ibrahim Abouzied
---

## Vulnerability Title

Withdrawals Can Revert

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> It is a result of the design decision.

**File(s) affected:**`EigenLSTRestaking.sol`, `NativeLendingETHStrategy.sol`, `StoneVault.sol`, `StrategyController.sol`, `SymbioticDepositWstETHStrategy.sol`

**Description:**`StrategyController.forceWithdraw()` makes a call to `Strategy(strategy).instantWithdraw(withAmount)`. This function is expected to withdraw whatever funds possible and not revert (as opposed to `StrategyController._withdrawFromStrategy()` calling `Strategy(_strategy).withdraw(_amount)`).

However, none of the current implementations of `Strategy.instantWithdraw()` correctly gather the requested funds.

*   `NativeLendingETHStrategy.instantWithdraw()`: Leaves potential funds in the LP token.
*   `SymbioticDepositWstETHStrategy.instantWithdraw()`: Is unable to syncronously withdraw additional ETH as it needs to submit withdrawal requests from Lido.
*   `EigenLSTRestaking.instantWithdraw()`: Is unable to syncronously withdraw additional ETH as it needs to submit withdrawal requests from Lido.

All three of these functions will revert if the amount withdrawn exceeds the amount of ETH in the contract. With the current usages, this could prevent some users from being able to call `StoneVault.instantWithdraw()`.

Additionally, it is possible for the implementations of `Strategy.withdraw()` to revert as well. This could result in blocking calls to `StrategyController._rebase()` until the admin makes the ETH available for each of the strategies. This will in turn prevent calls to `StoneVault.rollToNextRound()`.

**Recommendation:** The Stakestone team should assess the intended functionality of the protocol.

1.   If it is important that `instantWithdraw()` withdraws whatever funds possible, the `instantWithdraw()` implementations should be updated to recoup ETH when possible and avoid reverting.
2.   If the current architecture is acceptable, the `instantWithdraw()` functions should be removed to avoid confusion. All of the `instantWithdraw()` implementations are currently identical to their `withdraw()` counterparts. `withdraw()` can be used instead.
3.   If `_rebase()` should always succeed, calculate the `diff.amount` to be within the Strategy's ETH balance.
4.   Consider updating `withdraw()` to trigger actions such as exchanging LP tokens or withdrawing from Symbiotic to avoid requiring admin intervention.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | StakeStone |
| Report Date | N/A |
| Finders | Mustafa Hasan, Roman Rohleder, Ibrahim Abouzied |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/stake-stone/4b7cbc5e-5595-4ac4-ac36-176f43ee9adf/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/stake-stone/4b7cbc5e-5595-4ac4-ac36-176f43ee9adf/index.html

### Keywords for Search

`vulnerability`

