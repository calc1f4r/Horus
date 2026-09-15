---
# Core Classification
protocol: Sharwafinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36481
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Risk of unaccounted asset removal

### Overview


This bug report discusses a problem with a list called `MarginAccount.availableErc20` in a code file called `MarginAccount.sol`. This list is important for certain functions and removing a token from it can cause issues with the account's value and liquidation process. This can result in users being liquidated using only some of their tokens to cover debts, potentially causing the Insurance Pool to cover the rest. The report recommends preventing the removal of tokens from this list to avoid unexpected problems.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

The `MarginAccount.availableErc20` list is crucial for functions like `MarginAccount::preparationTokensParams`, which helps in valuing the account, and `MarginAccount::liquidate`. Removing a token from the `availableErc20` list can lead to users being liquidated using only the remaining active tokens to cover debts:

```solidity
File: MarginAccount.sol
217:     function liquidate(uint marginAccountID, address baseToken, address marginAccountOwner) external onlyRole(MARGIN_TRADING_ROLE) {
218:         IModularSwapRouter.ERC20PositionInfo[] memory erc20Params = new IModularSwapRouter.ERC20PositionInfo[](availableErc20.length);
219:         IModularSwapRouter.ERC721PositionInfo[] memory erc721Params = new IModularSwapRouter.ERC721PositionInfo[](availableErc721.length);
220:
221:         for(uint i; i < availableErc20.length; i++) {
222:             uint erc20Balance = erc20ByContract[marginAccountID][availableErc20[i]];
223:             erc20Params[i] = IModularSwapRouter.ERC20PositionInfo(availableErc20[i], baseToken, erc20Balance);
224:             erc20ByContract[marginAccountID][availableErc20[i]] -= erc20Balance;
225:         }
226:
227:         for(uint i; i < availableErc721.length; i++) {
228:             uint[] memory erc721TokensByContract = erc721ByContract[marginAccountID][availableErc721[i]];
229:             erc721Params[i] = IModularSwapRouter.ERC721PositionInfo(availableErc721[i], baseToken, marginAccountOwner, erc721TokensByContract);
230:             delete erc721ByContract[marginAccountID][availableErc721[i]];
231:         }
232:
233:         uint amountOutInUSDC = modularSwapRouter.liquidate(erc20Params,erc721Params);
234:
235:         erc20ByContract[marginAccountID][baseToken] += amountOutInUSDC;
236:
237:         _clearDebtsWithPools(marginAccountID, baseToken);
238:     }
```

When a token is deactivated and thus removed from `availableErc20`, it is not utilized in the debt settlement process during liquidation. This oversight leads to the `InsurancePool` potentially covering any shortfalls:

```solidity
File: MarginAccount.sol
282:      */
283:     function _clearDebtsWithPools(uint marginAccountID, address baseToken) private {
...
293:                     IERC20(availableTokenToLiquidityPool[i]).transferFrom(insurancePool, address(this), poolDebt-amountOut);
...
301:     }
```

**Recommendations**

It is advisable to prevent the removal of tokens from the `MarginAccount.availableErc20` list within the `MarginAccount::setAvailableErc20` function. Ensuring that all tokens originally considered as assets remain accountable throughout the lifecycle of the account can prevent unexpected burdens on the Insurance Pool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sharwafinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

