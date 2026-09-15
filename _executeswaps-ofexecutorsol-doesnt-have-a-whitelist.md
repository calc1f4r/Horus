---
# Core Classification
protocol: LI.FI
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7056
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
  - validation

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

_executeSwaps ofExecutor.sol doesn’t have a whitelist

### Overview


This bug report is about the function _executeSwaps() in two contracts, Executor.sol and SwapperV2.sol. The function in Executor.sol does not have a whitelist, while the function in SwapperV2.sol does. This could be dangerous because it could allow unlimited allowances to be set, which could lead to the stealing of leftover tokens in the Executor contract.

The LiFi team acknowledges the risk but wants to keep the contract open to allow developers to call whatever they wish. The Spearbit team has also acknowledged the risk.

The recommendation is to reuse the code from SwapperV2.sol and add a management interface for the whitelist, like DexManagerFacet.sol. Additionally, it is suggested to create additional functionality for non-dex calls, where whitelists will also be useful.

### Original Finding Content

## Security Report

## Severity: Medium Risk

### Context
- `Executor.sol#L323-L333`
- `SwapperV2.sol#L67-L81`

### Description
The function `_executeSwaps()` of `Executor.sol` doesn’t have a whitelist, whereas `_executeSwaps()` of `SwapperV2.sol` does have a whitelist. Calling arbitrary addresses is dangerous. For example, unlimited allowances can be set to allow stealing of leftover tokens in the Executor contract. Luckily, there wouldn’t normally be allowances set from users to the `Executor.sol`, so the risk is limited.

> **Note:** Also see "Too generic calls in GenericBridgeFacet allow stealing of tokens"

#### Code Snippets
```solidity
contract Executor is IAxelarExecutable, Ownable, ReentrancyGuard, ILiFi {
    function _executeSwaps(... ) ... {
        for (uint256 i = 0; i < _swapData.length; i++) {
            if (_swapData[i].callTo == address(erc20Proxy)) revert UnAuthorized(); // Prevent calling ERC20 Proxy directly !
            LibSwap.SwapData calldata currentSwapData = _swapData[i];
            LibSwap.swap(_lifiData.transactionId, currentSwapData);
        }
    }
}

contract SwapperV2 is ILiFi {
    function _executeSwaps(... ) ... {
        for (uint256 i = 0; i < _swapData.length; i++) {
            LibSwap.SwapData calldata currentSwapData = _swapData[i];
            if (
                !(appStorage.dexAllowlist[currentSwapData.approveTo] &&
                appStorage.dexAllowlist[currentSwapData.callTo] &&
                appStorage.dexFuncSignatureAllowList[bytes32(currentSwapData.callData[:8])])
            ) revert ContractCallNotAllowed();
            LibSwap.swap(_lifiData.transactionId, currentSwapData);
        }
    }
}
```

Based on the comments of the LiFi project, there is also the use case to call more generic contracts, which do not return any token (e.g., NFT buy, carbon offset). It may be better to create new functionality to address these cases.

### Recommendation
- Reuse the code of `SwapperV2.sol`.
- **Note:** Having a whitelist also ensures `erc20Proxy` won’t be called.
- **Note:** This also requires adding a management interface for the whitelist, like `DexManager-Facet.sol`.
- **Note:** Also see the issue "Move whitelist to `LibSwap.swap()`".
- Consider creating additional functionality for non-dex calls; here whitelists will also be useful.

### LiFi Response
The LiFi Team claims that they acknowledge the risk but plan to keep this contract open as it is separate from the main LIFI protocol contract and want to allow developers to call whatever they wish.

### Spearbit Response
Acknowledged.

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

`Validation`

