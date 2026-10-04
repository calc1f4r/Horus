---
# Core Classification
protocol: Yield Ninja
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19125
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-11-01-Yield Ninja.md
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
  - Pashov
---

## Vulnerability Title

[M-01] MEV can sandwich every harvest due to missing slippage tolerance value

### Overview


This bug report outlines a vulnerability in the `NyPtvFantomWftmBooSpookyV2StrategyToUsdc` smart contract. The problem arises when the `_harvestCore` method is called, which calls the `_swapFarmEmissionTokens` method with an argument of 0 for the `amountOutMin` parameter. This argument is used to set the slippage tolerance, and a 0 value essentially means 100% slippage tolerance. This can be exploited in a way that the strategy (so the vault and the users) receive much less value than it should have.

The recommended solution is to make the `harvest` method of the vault callable only by a list of trusted addresses which will send the transaction through a private mempool. Additionally, an on-chain calculation should be used for an `amountOutMin` that is off from the expected `amountOut` by a slippage tolerance percentage. This should protect against MEV sandwich attacks.

### Original Finding Content

**Proof of Concept**

In `NyPtvFantomWftmBooSpookyV2StrategyToUsdc` each time the `_harvestCore` method is called (on each harvest) it will call the `_swapFarmEmissionTokens` method which itself has the following code:

```solidity
IUniswapV2Router02(SPOOKY_ROUTER).swapExactTokensForTokensSupportingFeeOnTransferTokens(
      booBalance,
      0,
      booToUsdcPath,
      address(this),
      block.timestamp
    );
```

The “0” here is the value of the `amountOutMin` argument which is used for slippage tolerance. 0 value here essentially means 100% slippage tolerance. This is a very easy target for MEV and bots to do a flash loan sandwich attack on each of the strategy’s swaps, resulting in very big slippage on each trade.

**Impact**

100% slippage tolerance can be exploited in a way that the strategy (so the vault and the users) receive much less value than it should had. This can be done on every trade if the trade transaction goes through a public mempool.

**Recommendation**

The best solution here is to make the `harvest` method of the vault be callable only by a list of trusted addresses which will send the transaction through a private mempool. This, combined with an on-chain calculation for an `amountOutMin` that is off from the expected `amountOut` by a slippage tolerance percentage (that might be configurable through a setter in the strategy) should be good enough to protect you from MEV sandwich attacks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Yield Ninja |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-11-01-Yield Ninja.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

