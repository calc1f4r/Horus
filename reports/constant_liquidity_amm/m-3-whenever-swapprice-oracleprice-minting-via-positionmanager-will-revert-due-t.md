---
# Core Classification
protocol: Smilee Finance
chain: everychain
category: uncategorized
vulnerability_type: denial-of-service

# Attack Vector Details
attack_type: denial-of-service
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30626
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/180
source_link: none
github_link: https://github.com/sherlock-audit/2024-02-smilee-finance-judging/issues/32

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
  - denial-of-service

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - panprog
  - cawfree
  - juan
---

## Vulnerability Title

M-3: Whenever swapPrice > oraclePrice, minting via PositionManager will revert, due to not enough funds being obtained from user.

### Overview


This bug report discusses an issue with the Smilee Finance protocol, specifically with the `PositionManager::mint()` function. The issue was found by three individuals and reported on GitHub. The vulnerability allows for a denial of service to users when the swap price is greater than the oracle price. This is due to a difference in the way the `obtainedPremium` is calculated and the actual premium needed. The impact of this bug is that minting positions via the PositionManager will revert, disrupting core protocol functionality. The code snippet and tool used for this report were a manual review. The recommendation is to consider using the premium from `swapPrice` when calculating `obtainedPremium`. The bug has been fixed and signed off by the Lead Senior Watson.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-02-smilee-finance-judging/issues/32 

## Found by 
cawfree, juan, panprog
## Summary
In [`PositionManager::mint()`](https://github.com/sherlock-audit/2024-02-smilee-finance/blob/3241f1bf0c8e951a41dd2e51997f64ef3ec017bd/smilee-v2-contracts/src/periphery/PositionManager.sol#L91-L178), `obtainedPremium` is calculated in a different way to the actual premium needed, and this will lead to a revert, denying service to users.

## Vulnerability Detail
In [`PositionManager::mint()`](https://github.com/sherlock-audit/2024-02-smilee-finance/blob/3241f1bf0c8e951a41dd2e51997f64ef3ec017bd/smilee-v2-contracts/src/periphery/PositionManager.sol#L91-L178), the PM gets `obtainedPremium` from `DVP::premium()`:
```solidity
(obtainedPremium, ) = dvp.premium(params.strike, params.notionalUp, params.notionalDown);
```

Then the actual premium used when minting by the DVP is obtained via the following [code](https://github.com/sherlock-audit/2024-02-smilee-finance/blob/3241f1bf0c8e951a41dd2e51997f64ef3ec017bd/smilee-v2-contracts/src/DVP.sol#L152-L155):
<details>
<summary>Determining option premium</summary>

```js
    uint256 swapPrice = _deltaHedgePosition(strike, amount, true);
    uint256 premiumOrac = _getMarketValue(strike, amount, true, IPriceOracle(_getPriceOracle()).getPrice(sideToken, baseToken));
    uint256 premiumSwap = _getMarketValue(strike, amount, true, swapPrice);
    premium_ = premiumSwap > premiumOrac ? premiumSwap : premiumOrac;
```
</details>

From the code above, we can see that the actual premium uses the greater of the two price options. However, [`DVP::premium()`](https://github.com/sherlock-audit/2024-02-smilee-finance/blob/3241f1bf0c8e951a41dd2e51997f64ef3ec017bd/smilee-v2-contracts/src/IG.sol#L94-L113) only uses the oracle price to determine the `obtainedPremium`.

This leads to the opportunity for `premiumSwap > premiumOrac`, so in the PositionManager, `obtainedPremium` is less than the actual premium required to mint the position in the DVP contract.

Thus, when the DVP contract tries to collect the premium from the PositionManager, it will revert due to insufficient balance in the PositionManager:
```solidity
IERC20Metadata(baseToken).safeTransferFrom(msg.sender, vault, premium_ + vaultFee);
```

## Impact
Whenever `swapPrice > oraclePrice`, minting positions via the PositionManager will revert. This is a denial of service to users and this disruption of core protocol functionality can last extended periods of time.

## Code Snippet
https://github.com/sherlock-audit/2024-02-smilee-finance/blob/3241f1bf0c8e951a41dd2e51997f64ef3ec017bd/smilee-v2-contracts/src/DVP.sol#L152-L155

## Tool used
Manual Review

## Recommendation
When calculating `obtainedPremium`, consider also using the premium from `swapPrice` if it is greater than the premium calculated from `oraclePrice`.



## Discussion

**sherlock-admin2**

2 comment(s) were left on this issue during the judging contest.

**panprog** commented:
> valid high, dup of #42

**takarez** commented:
>  valid, the calculation should consider the swapPrice; medium(1)



**metadato-eth**

MEDIUM
DoS but 1) no fund at risk, 2) overcome easily by changing the position manager, 3) immediately identifiable by internal testing before official release

**sherlock-admin4**

The protocol team fixed this issue in PR/commit https://github.com/dverso/smilee-v2-contracts/commit/84174d20544970309c862a2bf35ccfa3046d6bd9.

**panprog**

Fix review; Fixed

**sherlock-admin4**

The Lead Senior Watson signed off on the fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Smilee Finance |
| Report Date | N/A |
| Finders | panprog, cawfree, juan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-02-smilee-finance-judging/issues/32
- **Contest**: https://app.sherlock.xyz/audits/contests/180

### Keywords for Search

`Denial-Of-Service`

