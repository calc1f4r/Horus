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
solodit_id: 36475
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-04] Users could avoid liquidation by providing a large number of position NFTs

### Overview


This bug report describes a problem where users can provide an unlimited number of position NFTs to their margin account, which can cause issues during liquidation. This can be exploited by users to avoid liquidation by causing an out-of-gas error. The report recommends restricting the maximum number of NFTs that can be added to a margin account to prevent this issue.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** High

**Description**

Users could provide an arbitrary number of position NFTs to their margin account using the `provideERC721` function, each new token would be pushed to an array associated with their margin account ID (line 178):

```solidity
File: MarginAccount.sol
176:     function provideERC721(uint marginAccountID, address txSender, address token, uint collateralTokenID, address baseToken) external onlyRole(MARGIN_TRADING_ROLE) {
177:         require(isAvailableErc721[token], "Token you are attempting to deposit is not available for deposit");
178:         erc721ByContract[marginAccountID][token].push(collateralTokenID);
179:         IERC721(token).transferFrom(txSender, address(this), collateralTokenID);
180:         IERC721(token).approve(modularSwapRouter.getModuleAddress(token, baseToken), collateralTokenID);
181:     }
```

During liquidation array of the user's NFTs would be used in the router to execute liquidation on each NFT (line 131):

```solidity
File: ModularSwapRouter.sol
110:     function liquidate(ERC20PositionInfo[] memory erc20Params, ERC721PositionInfo[] memory erc721Params)
111:         external
112:         onlyRole(MARGIN_ACCOUNT_ROLE)
113:         returns(uint amountOut)
114:     {
115:         address marginTradingBaseToken = marginTrading.BASE_TOKEN();
116:         for (uint i; i < erc20Params.length; i++) {
117:             address moduleAddress = tokenInToTokenOutToExchange[erc20Params[i].tokenIn][erc20Params[i].tokenOut];
118:             if (
119:                 erc20Params[i].tokenIn == marginTradingBaseToken &&
120:                 erc20Params[i].tokenOut == marginTradingBaseToken
121:             ) {
122:                 amountOut += erc20Params[i].value;
123:             } else if (moduleAddress != address(0)) {
124:                 amountOut += IPositionManagerERC20(moduleAddress).liquidate(erc20Params[i].value);
125:             }
126:         }
127:
128:         for (uint i; i < erc721Params.length; i++) {
129:             address moduleAddress = tokenInToTokenOutToExchange[erc721Params[i].tokenIn][erc721Params[i].tokenOut];
130:             if (moduleAddress != address(0)) {
131:                 amountOut += IPositionManagerERC721(moduleAddress).liquidate(erc721Params[i].value, erc721Params[i].holder);
132:             }
133:         }
134:     }
```

This gives users a way to avoid liquidations by proving a large number of position NFTs that would cause an out-of-gas error each time when liquidation is called on their margin account.

**Recommendations**

Consider restricting max number of position NFTs per one margin account that would prevent out-of-gas during liquidation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

