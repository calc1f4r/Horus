---
# Core Classification
protocol: Hifi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59638
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
source_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
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
finders_count: 3
finders:
  - Zeeshan Meghji
  - Roman Rohleder
  - Souhail Mssassi
---

## Vulnerability Title

Potential Re-Entrancy/Checks-Effects-Interactions Pattern Violations

### Overview


This report discusses an issue with the code in several contracts, including HifiProxyTarget and HifiPool. The issue is that the code does not follow the "Checks-Effects-Interactions" pattern, which is a best practice for preventing unwanted side effects from external contracts. This means that the code performs external contract calls before modifying state variables, which could potentially lead to unexpected behavior. The report recommends restructuring the code or adding reentrancy guards to address this issue.

### Original Finding Content

**Update**
From the team :

```
1. HifiProxyTarget is completely stateless (doesn't have any internal state).
2. Every time underlying.safeTransferFrom() or collateral.safeTransferFrom() is called to transfer tokens from the user's EOA to the proxy target, it is in order to use those tokens in a subsequent subcall. It’s not possible to use those tokens in the proxy before they're transferred to it.
3. The only other contract affected by this other than HifiProxyTarget is HifiPool.
But there is still no internal state being modified after the underlying.safeTransferFrom
interaction.
```

**File(s) affected:**`packages/protocol/contracts/core/fintroller/Fintroller.sol`, `packages/protocol/contracts/oracles/ChainlinkOperator.sol`, `packages/proxy-target/contracts/HifiProxyTarget.sol`, `packages/amm/contracts/HifiPool.sol`

**Description:** As a best practice and to prevent unwanted external contract side effects, it is advised to adhere to the ["Checks-Effects-Interactions"-pattern](https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html), even in the presence of [reentrancy guards](https://docs.openzeppelin.com/contracts/4.x/api/[](https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html)security#ReentrancyGuard).

Following instances were observed where said pattern was violated:

*   `HifiProxyTarget.addLiquidity()`: Performs external contract calls (`underlying.safeTransferFrom()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.borrowHTokenAndAddLiquidity()`: Performs external contract calls (`underlying.safeTransferFrom()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.buyHToken()`: Performs external contract calls (`underlying.safeTransferFrom()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.buyHTokenAndAddLiquidity()`: Performs external contract calls (`underlying.safeTransferFrom()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.buyHTokenAndRepayBorrow()`: Performs external contract calls (`underlying.safeTransferFrom()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.depositCollateral()`: Performs external contract calls (`collateral.safeTransferFrom()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.depositUnderlyingAndMintHTokenAndAddLiquidity()`: Performs external contract calls (`underlying.safeTransferFrom()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.removeLiquidity()`: Performs external contract calls (`hifiPool.underlying().safeTransfer()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.removeLiquidityAndRedeem()`: Performs external contract calls (`hToken.underlying().safeTransfer()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.removeLiquidityAndSellHToken()`: Performs external contract calls (`hifiPool.underlying().safeTransfer()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.sellUnderlyingAndRepayBorrow()`: Performs external contract calls (`underlying.transferFrom()`), before modifying state variables in following sub-calls.
*   `HifiProxyTarget.depositUnderlyingInternal()`: Performs external contract calls (`underlying.safeTransferFrom()`), before modifying state variables in following sub-calls.
*   `HifiPool.sellUnderlying()`: Performs external contract calls (`underlying.safeTransferFrom()`), before modifying state variables in following sub-calls.

**Recommendation:** Consider re-structuring the code, such that it no longer violates the "Checks-Effects-Interactions"-pattern and/or add [reentrancy guards](https://docs.openzeppelin.com/contracts/4.x/api/security#ReentrancyGuard) at corresponding calling locations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hifi Finance |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Roman Rohleder, Souhail Mssassi |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html

### Keywords for Search

`vulnerability`

