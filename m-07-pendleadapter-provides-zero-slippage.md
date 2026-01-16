---
# Core Classification
protocol: AdapterFinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58090
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
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

[M-07] `PendleAdapter` provides zero slippage

### Overview


The report states that when a vault triggers `_adapter_deposit` and delegates the call to `PendleAdapter.deposit`, it will deposit the given `_asset_amount` into the Pendle market. However, there is a bug where the minimum out return value is set to 0 and there is no check for slippage, which can lead to a sandwich attack. The report recommends adding a minimum accepted return value to prevent this issue.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When the vault triggers `_adapter_deposit` and delegates the call to `PendleAdapter.deposit`, it will deposit the provided `_asset_amount` into the configured Pendle market.

```python
@external
@nonpayable
def deposit(asset_amount: uint256, pregen_info: Bytes[4096]=empty(Bytes[4096])):
    # ....

    #mint if minting price is better, then sell the YT.
    if pg.mint_returns > pg.spot_returns:
        #Mint PY
        inp: TokenInput = empty(TokenInput)
        inp.tokenIn = asset
        inp.netTokenIn = asset_amount
        inp.tokenMintSy = asset

        netPyOut: uint256 = 0
        netSyInterm: uint256 = 0
        ERC20(asset).approve(pendleRouter, asset_amount)
        #Mint PY+PT using asset
        netPyOut, netSyInterm = PendleRouter(pendleRouter).mintPyFromToken(
            self,
            yt_token,
>>>         0,
            inp
        )

        #Swap any YT gained to PT
        ERC20(yt_token).approve(pendleRouter, netPyOut)

        PendleRouter(pendleRouter).swapExactYtForPt(
            self,
            pendleMarket,
            netPyOut,
>>>         0,
            pg.approx_params_swapExactYtForPt
        )

    else:
        #swapExactTokenForPt
        inp: TokenInput = empty(TokenInput)
        inp.tokenIn = asset
        inp.netTokenIn = asset_amount
        inp.tokenMintSy = asset

        limit: LimitOrderData = empty(LimitOrderData)
        ERC20(asset).approve(pendleRouter, asset_amount)
        PendleRouter(pendleRouter).swapExactTokenForPt(
            self,
            pendleMarket,
>>>         0,
            pg.approx_params_swapExactTokenForPt,
            inp,
            limit
        )
        #NOTE: Not doing any checks and balances, minPtOut=0 is intentional.
        #It's up to the vault to revert if it does not like what it sees.
```

It can be observed that the minimum out return value from all operations is set to 0, and it is noted that not providing slippage is intentional and will be left to the vault to check the slippage. However, inside `_balanceAdapters`, after `_adapter_deposit` is called, there is no slippage check to ensure that the minted/swapped token amount is within the expected range. A sandwich attack can be executed when `_balanceAdapters` is called to extract value from the operation.

## Recommendations

Consider adding a minimum accepted return value inside `_balanceAdapters` and `_adapter_deposit` inside the vault.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AdapterFinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

