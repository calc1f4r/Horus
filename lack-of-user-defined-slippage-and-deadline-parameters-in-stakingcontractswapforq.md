---
# Core Classification
protocol: Benqi Ignite
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44261
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
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
finders_count: 2
finders:
  - Immeas
  - Giovanni Di Siena
---

## Vulnerability Title

Lack of user-defined slippage and deadline parameters in `StakingContract::swapForQI` may result in unfavorable `QI` token swaps

### Overview

See description below for full details.

### Original Finding Content

**Description:** When a user interacts with `StakingContract` to provision a hosted node, they can choose between two methods:[`StakingContract::stakeWithAVAX`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L457-L511) or [`StakingContract::stakeWithERC20`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L513-L577). If the staked token is not `QI`, `StakingContract::swapForQI` is invoked to swap the staked token for `QI` via Trader Joe. Once created, the validator node is then [registered](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L441-448) with [`Ignite`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L353-L400), using `QI`, via `StakingContract::registerNode`.

Within the swap to `QI`, `amountOutMin` is [calculated](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L844) using Chainlink price data and a slippage parameter defined by the protocol:

```solidity
// Get the best price quote
uint256 slippageFactor = 100 - slippage; // Convert slippage percentage to factor
uint256 amountOutMin = (expectedQiAmount * slippageFactor) / 100; // Apply slippage
```

If the actual amount of `QI` received is below this `amountOutMin`, the transaction will [revert](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L897-L900); however, users are restricted by the protocol-defined slippage, which may not reflect their preferences if they desire a smaller slippage tolerance to ensure they receive a more favorable swap execution.

Additionally, the swap [deadline](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L863) specified as `block.timestamp` in `StakingContract::swapForQI` provides no protection as deadline validation will pass whenever the transaction is included in a block:

```solidity
uint256 deadline = block.timestamp;
```

This could expose users to unfavorable price fluctuations and again offers no option for users to provide their own deadline parameter.

**Impact:** Users may receive fewer `QI` tokens than expected due to the fixed slippage tolerance set by the protocol, potentially resulting in unfavorable swap outcomes.

**Recommended Mitigation:** Consider allowing users to provide a `minAmountOut` slippage parameter and a `deadline` parameter for the swap operation. The user-specified `minAmountOut` should override the protocol's slippage-adjusted amount if larger.

**BENQI:** Acknowledged, there is already a slippage check inside `StakingContract::swapForQI` based on the Chainlink pricing.

**Cyfrin:** Acknowledged.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Benqi Ignite |
| Report Date | N/A |
| Finders | Immeas, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

