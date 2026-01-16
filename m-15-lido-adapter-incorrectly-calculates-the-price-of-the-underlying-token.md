---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2380
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-alchemix-contest
source_link: https://code4rena.com/reports/2022-05-alchemix
github_link: https://github.com/code-423n4/2022-05-alchemix-findings/issues/97

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

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - AuditsAreUS
---

## Vulnerability Title

[M-15] Lido adapter incorrectly calculates the price of the underlying token

### Overview


A bug has been identified in the Lido adapter, which incorrectly calculates the price of WETH in terms of WstETH. This is a severe issue, as it affects the core calculation of the protocol - harvestable amount. The function `IWstETH(token).getStETHByWstETH()` only converts WstETH to stETH, thus `price()` returns the value of WstETH in terms of stETH. To mitigate this, extra steps should be added to `price()` to approximate the rate for converting stETH to ETH, using the same curve pool used to convert stETH to ETH in `unwrap()`.

### Original Finding Content

_Submitted by AuditsAreUS_

The Lido adapter incorrectly calculates the price of WETH in terms of WstETH.

The function returns the price of WstETH in terms of stETH. The underlying token which we desire is WETH.
Since stETH does not have the same value as WETH the output price incorrect.

The impact is severe as all the balance calculations require the price of the yield token converted to underlying. The incorrect price may over or understate the harvestable amount which is a core calculation in the protocol.

### Proof of Concept

The function `IWstETH(token).getStETHByWstETH()` only converts WstETH to stETH. Thus, `price()` returns the value of WstETH in terms of stETH.

```solidity
    function price() external view returns (uint256) {
        return IWstETH(token).getStETHByWstETH(10**SafeERC20.expectDecimals(token));
    }
```

### Recommended Mitigation Steps

Add extra steps to `price()` to approximate the rate for converting stETH to ETH. This can be done using the same curve pool that is used to convert stETH to ETH in `unwrap()`.

**[0xfoobar (Alchemix) disputed and commented](https://github.com/code-423n4/2022-05-alchemix-findings/issues/97#issuecomment-1133989793):**
 
> The design mechanism relies upon stETH reaching eventual 1:1 redeemability for ETH after the merge and shanghai enables withdrawals. This is core to out like-kind collateral/asset model. We will update the stETH token adapter at that time to do direct redemptions instead of Curve swaps. So in the meantime, the protocol accrues discounted assets.

**[0xleastwood (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-alchemix-findings/issues/97#issuecomment-1150012226):**
 > While the sponsor's comments suggest that this will be a non-issue after the merge/shanghai enables withdrawals, I believe there is legitimacy in the fact that the protocol will accrue discounted assets. It does not lead to the loss of assets, but value can be leaked if `WETH` is priced incorrectly. As such, I'm downgrading this to medium severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | AuditsAreUS |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-alchemix
- **GitHub**: https://github.com/code-423n4/2022-05-alchemix-findings/issues/97
- **Contest**: https://code4rena.com/contests/2022-05-alchemix-contest

### Keywords for Search

`vulnerability`

