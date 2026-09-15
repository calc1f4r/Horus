---
# Core Classification
protocol: LI.FI
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7058
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
github_link: none

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
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jonah1005
  - DefSec
  - Gerard Persoon
---

## Vulnerability Title

Processing of initial balances

### Overview


This bug report is about the LiFi code bases which contains two similar source files - Swapper.sol and SwapperV2.sol. The difference between the two is the processing of msg.value for native tokens. An exploit example is provided to explain the issue. It states that when a call is done with msg.value equal to 1 ETH, and the _swapData[0].fromAmount is 0.5 ETH, the implementation of SwapperV2.sol sends the previously available native token to the msg.sender. This leads to an incorrect initial balance calculation. The report also suggests two options to fix the issue - either consider the tokens left in the LiFi Diamond and Executor and make a correction with msg.value, or remove fetchBalances() and comparable code in other functions as the initial balances are not relevant. The issue has been fixed with PR #94 and verified.

### Original Finding Content

## Severity
**Medium Risk**

## Context
- Swapper.sol#L22-L38
- Swapper.sol#L83-L96
- SwapperV2.sol#L22-L39
- SwapperV2.sol#L86-L93
- Executor.sol#L143-L149
- Executor.sol#L191-L199
- Executor.sol#L242-L249
- Executor.sol#L338-L345
- XChainExecFacet.sol#L30-L38

## Description
The LiFi code bases contain two similar source files: **Swapper.sol** and **SwapperV2.sol**. One of the differences is the processing of `msg.value` for native tokens, see pieces of code below. The implementation of **SwapperV2.sol** sends previously available native tokens to the `msg.sender`.

### Exploit Example
Assume that:
- The LiFi Diamond contract contains **0.1 ETH**.
- A call is done with `msg.value == 1 ETH`.
- `_swapData[0].fromAmount == 0.5 ETH`, which is the amount to be swapped.

**Option 1 - Swapper.sol**:
```
initialBalances == 1.1 ETH - 1 ETH == 0.1 ETH
```

**Option 2 - SwapperV2.sol**:
```
initialBalances == 1.1 ETH
```

After the swap:
- `getOwnBalance() is 1.1 - 0.5 == 0.6 ETH`.

**Option 1 - Swapper.sol**:
```
returns 0.6 - 0.1 = 0.5 ETH
```

**Option 2 - SwapperV2.sol**:
```
returns 0.6 ETH (so includes the previously present ETH).
```

**Note:** The implementations of `noLeftovers()` are also different in **Swapper.sol** and **SwapperV2.sol**. This issue is related to "Pulling tokens by `LibSwap.swap()` is counterintuitive", because the ERC20 tokens are pulled in via `LibSwap.swap()`, whereas the `msg.value` is directly added to the balance. 

As there normally shouldn’t be any tokens in the LiFi Diamond contract, the risk is limited.

```solidity
contract Swapper is ILiFi {
    function _fetchBalances(...) ... {
        ...
        for (uint256 i = 0; i < length; i++) {
            address asset = _swapData[i].receivingAssetId;
            uint256 balance = LibAsset.getOwnBalance(asset);
            if (LibAsset.isNativeAsset(asset)) {
                balances[i] = balance - msg.value;
            } else {
                balances[i] = balance;
            }
        }
        return balances;
    }
}
```

```solidity
contract SwapperV2 is ILiFi {
    function _fetchBalances(...) ... {
        ...
        for (uint256 i = 0; i < length; i++) {
            balances[i] = LibAsset.getOwnBalance(_swapData[i].receivingAssetId);
        }
        ...
    }
}
```

### Comparable Functions
The following functions do a comparable processing of `msg.value` for the initial balance:
- `swapAndCompleteBridgeTokensViaStargate()` of **Executor.sol**
- `swapAndCompleteBridgeTokens()` of **Executor.sol**
- `swapAndExecute()` of **Executor.sol**
- `swapAndCompleteBridgeTokens()` of **XChainExecFacet**

```solidity
if (!LibAsset.isNativeAsset(transferredAssetId)) {
    ...
} else {
    startingBalance = LibAsset.getOwnBalance(transferredAssetId) - msg.value;
}
```

However, in **Executor.sol**, the function `swapAndCompleteBridgeTokensViaStargate()` isn’t optimal for ERC20 tokens because ERC20 tokens are already deposited in the contract before calling this function.

```solidity
function swapAndCompleteBridgeTokensViaStargate(... ) ... {
    ...
    if (!LibAsset.isNativeAsset(transferredAssetId)) {
        startingBalance = LibAsset.getOwnBalance(transferredAssetId); // doesn't correct for initial balance
    } else {
        ...
    }
}
```

### Assumptions
Assume:
- **0.1 ETH** was in the contract.
- **1 ETH** was added by the bridge.
- **0.5 ETH** is swapped.

Then the starting balance is calculated to be:
```
0.1 ETH + 1 ETH == 1.1 ETH
```
So no funds are returned to the receiver as the end balance is:
```
1.1 ETH - 0.5 ETH == 0.6 ETH
```
This is smaller than **1.1 ETH**. Whereas it should have been:
```
(1.1 ETH - 0.5 ETH) - 0.1 ETH == 0.5 ETH.
```

## Recommendation
- First implement the suggestions of "Pulling tokens by `LibSwap.swap()` is counterintuitive".
- Consider implementing the suggestions of "Consider using wrapped native token".
- Also consider whether any tokens left in the LiFi Diamond and the Executor should be taken into account:
  - If they are: use the correction with `msg.value` everywhere in function `swapAndCompleteBridgeTokensViaStargate()` of **Executor.sol** code, and make a correction of the initial balance with the received tokens.
  - If not: then the initial balances are not relevant and `fetchBalances()` and the comparable code in other functions can be removed.
- Also see "Processing of end balances".
- Also see "Integrate all variants of `_executeAndCheckSwaps()`".

**LiFi:** Fixed with PR #94.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

