---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: swap

# Attack Vector Details
attack_type: swap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7060
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
  - swap

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

Pulling tokens by LibSwap.swap() is counterintuitive

### Overview


A bug was discovered in LibSwap.sol, SwapperV2.sol, Swapper.sol, and Executor.sol that could put users at risk. The bug was found in the function LibSwap.swap(), which pulls in tokens from msg.sender when needed. If someone were to try to swap multiple tokens, such as 100 USDC to 100 DAI and then 100 DAI to 100 USDT, and the first swap gave back less tokens, the LibSwap.swap() would pull in extra tokens from msg.sender. This could lead to an attacker being able to sweep multiple tokens from the user, cleaning out their entire wallet. 

In Executor.sol, the tokens are already deposited, so the "pull" functionality is not needed and can even result in additional issues. In Executor.sol, it tries to "pull" tokens from "msg.sender" itself, which could break some non-standard ERC20 implementations. 

To fix this bug, it is recommended that in Swapper.sol and SwapperV2.sol, LibAsset.depositAsset() should be used before doing _executeSwaps() or _executeAndCheckSwaps(). This will also prevent accidentally sending native tokens with ERC20 tokens, and will also make sure _executeSwaps of Executor.sol doesn't pull any tokens. Alternatively, the names can be changed to something like LibSwap.pullTokensAndSwap(), _pullTokensAndExecuteSwaps(), and _pullTokensAndExecuteAndCheckSwaps. Additionally, consider adding an emit of toDeposit. 

The bug has been fixed with PR #94 & PR #96 and verified by Spearbit.

### Original Finding Content

## Vulnerability Report

### Severity
**Medium Risk**

### Context
- `LibSwap.sol#L30-L68`
- `SwapperV2.sol#L67-L81`
- `Swapper.sol#L65-L78`
- `Executor.sol#L323-L333`

### Description
The function `LibSwap.swap()` pulls in tokens via `transferFromERC20()` from `msg.sender` when needed. When put in a loop, through `_executeSwaps()`, it can pull in multiple different tokens. It also doesn’t detect accidentally sending native tokens along with ERC20 tokens. This approach is counterintuitive and leads to risks.

Suppose someone wants to swap 100 USDC to 100 DAI and then 100 DAI to 100 USDT. If the first swap somehow gives back fewer tokens (for example, 90 DAI), then `LibSwap.swap()` pulls in 10 extra DAI from `msg.sender`. **Note**: This requires the `msg.sender` to have given multiple allowances to the LiFi Diamond.

Another risk is that an attacker could trick a user into signing a transaction for the LiFi protocol. Within one transaction, it can sweep multiple tokens from the user, potentially clearing out the entire wallet. **Note**: This also requires the `msg.sender` to have given multiple allowances to the LiFi Diamond.

In `Executor.sol`, the tokens are already deposited, so the "pull" functionality is not needed and can even result in additional issues. In `Executor.sol`, it tries to "pull" tokens from `msg.sender` itself. In the best-case scenario of ERC20 implementations (like OpenZeppelin and Solmate), this has no effect. However, some non-standard ERC20 implementations might break.

```solidity
contract SwapperV2 is ILiFi {
    function _executeSwaps(...) ... {
        ...
        for (uint256 i = 0; i < _swapData.length; i++) {
            ...
            LibSwap.swap(_lifiData.transactionId, currentSwapData);
        }
    }
}
```
```solidity
library LibSwap {
    function swap(...) ... {
        ...
        uint256 initialSendingAssetBalance = LibAsset.getOwnBalance(fromAssetId);
        ...
        uint256 toDeposit = initialSendingAssetBalance < fromAmount ? fromAmount - initialSendingAssetBalance : 0; , !
        ...
        if (toDeposit != 0) {
            LibAsset.transferFromERC20(fromAssetId, msg.sender, address(this), toDeposit);
        }
    }
}
```

### Recommendation
In `Swapper.sol` / `SwapperV2.sol`: Use `LibAsset.depositAsset()` before doing `_executeSwaps()` / `_executeAndCheckSwaps()`. This will also prevent accidentally sending native tokens along with ERC20 tokens (as `LibAsset.depositAsset()` checks `msg.value`).

Change the `swap()` function to something similar to this:

```solidity
library LibSwap {
    function swap(...) ... {
        ...
        - uint256 toDeposit = initialSendingAssetBalance < fromAmount ? fromAmount - initialSendingAssetBalance : 0; , !
        + if (initialSendingAssetBalance < fromAmount) revert NotEnoughFunds();
        ...
        - if (toDeposit != 0) {
        - LibAsset.transferFromERC20(fromAssetId, msg.sender, address(this), toDeposit);
        - }
    }
}
```

This will also ensure that `_executeSwaps` of `Executor.sol` doesn’t pull any tokens.

Alternatively, at least change the names as follows:
- `LibSwap.swap()` ==> `LibSwap.pullTokensAndSwap()`
- `_executeSwaps()` ==> `_pullTokensAndExecuteSwaps()` (3 locations)
- `_executeAndCheckSwaps` ==> `_pullTokensAndExecuteAndCheckSwaps` (3 locations)

And consider adding an emit for `toDeposit`.

LiFi: Fixed with PR #94 & PR #96.  
Spearbit: Verified.

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

`Swap`

