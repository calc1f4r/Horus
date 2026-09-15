---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33489
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/395

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 23
finders:
  - mussucal
  - 0xAadi
  - kennedy1030
  - p0wd3r
  - Tendency
---

## Vulnerability Title

[H-02] Incorrect calculation of queued withdrawals can deflate TVL and increase ezETH mint rate

### Overview


Bug report summary:

The function `OperatorDelegator.getTokenBalanceFromStrategy()` is used to calculate the protocol TVL, but it has a bug that causes it to incorrectly check for the queued amount of `address(this)` instead of `address(token)`. This results in the TVL being lower than it should be and can unfairly favor certain users who mint ezETH during a withdrawal process. The bug has been confirmed and mitigated by the Renzo team. 

### Original Finding Content


The function [`OperatorDelegator.getTokenBalanceFromStrategy()`](https://github.com/code-423n4/2024-04-renzo/blob/519e518f2d8dec9acf6482b84a181e403070d22d/contracts/Delegation/OperatorDelegator.sol#L327) is used by the [`RestakeManager`](https://github.com/code-423n4/2024-04-renzo/blob/519e518f2d8dec9acf6482b84a181e403070d22d/contracts/RestakeManager.sol) to calculate the protocol TVL, which in turn is used to calculate the amount of ezETH to mint against a given value in collateral tokens.

This function, however, incorrectly checks for the queued amount of `address(this)` instead of `address(token)`; therefore, consistently failing to consider collaterals in the withdrawal process for calculation:

```Solidity
File: OperatorDelegator.sol
326:     /// @dev Gets the underlying token amount from the amount of shares + queued withdrawal shares
327:     function getTokenBalanceFromStrategy(IERC20 token) external view returns (uint256) {
328:         return
329:             queuedShares[address(this)] == 0
330:                 ? tokenStrategyMapping[token].userUnderlyingView(address(this))
331:                 : tokenStrategyMapping[token].userUnderlyingView(address(this)) +
332:                     tokenStrategyMapping[token].sharesToUnderlyingView(
333:                         queuedShares[address(token)]
334:                     );
335:     }
```

Within this code, `queuedShares[address(this)]` will always return `0`; therefore, missing the opportunity to count the contribution of `queuedShares[address(token)]`.

### Impact

Any amount of collateral in the `OperatorDelegator` withdrawal process will not be counted for TVL calculation. This causes the TVL to be low, so more ezETH will be minted for the same amount of collateral, unfairly favoring people who mint ezETH during an `OperatorDelegator` withdrawal, penalizing holders, and those who initiate a `RestakeManager` withdraw.

### Proof of Concept

The following PoC in Foundry shows how the issue can lead to a decrease in TVL. The PoC can be run in Foundry by using the setup and mock infra provided [here](<https://gist.github.com/3docSec/a4bc6254f709a6218907a3de370ae84e>).

```Solidity
pragma solidity ^0.8.19;

import "contracts/Errors/Errors.sol";
import "./Setup.sol";

contract H2 is Setup {

    function testH2() public {
        // we'll only be using stETH with unitary price for simplicity
        stEthPriceOracle.setAnswer(1e18);

        // and we start with 0 TVL
        (, , uint tvl) = restakeManager.calculateTVLs();
        assertEq(0, tvl);

        // now we have Alice depositing some stETH
        address alice = address(1234567890);
        stETH.mint(alice, 100e18);
        vm.startPrank(alice);
        stETH.approve(address(restakeManager), 100e18);
        restakeManager.deposit(IERC20(address(stETH)), 100e18);

        // ✅ TVL and balance are as expected
        (, , tvl) = restakeManager.calculateTVLs();
        assertEq(100e18, tvl);
        assertEq(100e18, ezETH.balanceOf(alice));

        // Now some liquidity enters the withdraw sequence
        vm.startPrank(OWNER);

        IERC20[] memory tokens = new IERC20[](1);
        uint256[] memory tokenAmounts = new uint256[](1);

        tokens[0] = IERC20(address(stETH));
        tokenAmounts[0] = 50e18;

        operatorDelegator1.queueWithdrawals(tokens, tokenAmounts);

        // 🚨 The collateral queued for withdrawal does not show up in TVL,
        // so the mint rate is altered
        (, , tvl) = restakeManager.calculateTVLs();
        assertEq(50e18, tvl);
    }
}
```

### Tools Used

Foundry

### Recommended Mitigation Steps

Consider changing the address used for the mapping lookup:

```diff
    /// @dev Gets the underlying token amount from the amount of shares + queued withdrawal shares
    function getTokenBalanceFromStrategy(IERC20 token) external view returns (uint256) {
        return
-           queuedShares[address(this)] == 0
+           queuedShares[address(token)] == 0
                ? tokenStrategyMapping[token].userUnderlyingView(address(this))
                : tokenStrategyMapping[token].userUnderlyingView(address(this)) +
                    tokenStrategyMapping[token].sharesToUnderlyingView(
                        queuedShares[address(token)]
                    );
    }
```

**[jatinj615 (Renzo) confirmed](https://github.com/code-423n4/2024-04-renzo-findings/issues/395#event-12916027310)**

**[Renzo mitigated](https://github.com/code-423n4/2024-06-renzo-mitigation?tab=readme-ov-file#scope)**

**Status:** Mitigation confirmed. Full details in reports from [0xCiphky](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/9), [grearlake](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/51), [Fassi\_Security](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/41), [Bauchibred](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/18), and [LessDupes](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/3).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | mussucal, 0xAadi, kennedy1030, p0wd3r, Tendency, SBSecurity, fyamf, aman, 0xnightfall, KupiaSec, NentoR, 0xhacksmithh, 0rpse, adam-idarrha, jokr, zigtur, araj, FastChecker, baz1ka, bigtone, 0xCiphky, maxim371, LessDupes |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/395
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

