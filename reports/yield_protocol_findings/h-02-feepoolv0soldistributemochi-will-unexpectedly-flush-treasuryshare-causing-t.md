---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 923
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/114

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
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[H-02] FeePoolV0.sol#distributeMochi() will unexpectedly flush treasuryShare, causing the protocol fee cannot be properly accounted for and collected

### Overview


A bug has been discovered in the code for the WatchPug project. The `distributeMochi()` function will call `_buyMochi()` to convert `mochiShare` to Mochi token and call `_shareMochi()` to send Mochi to vMochi Vault and veCRV Holders. However, it will also reset the `treasuryShare` to `0` which is unexpected. This means the protocol fee cannot be properly accounted for and collected.

Anyone can call `distributeMochi()` and reset `treasuryShare` to `0`, and then call `updateReserve()` to allocate part of the wrongfuly resetted `treasuryShare` to `mochiShare` and call `distributeMochi()`. Repeating these steps will cause the `treasuryShare` to be consumed to near zero, which profits the vMochi Vault holders and veCRV Holders, while the protocol suffers the loss of funds.

The recommendation is to change the code to the code provided in the report. This will ensure that the `treasuryShare` is not reset to `0` and the protocol fee can be properly accounted for and collected.

### Original Finding Content

## Handle

WatchPug


## Vulnerability details

`distributeMochi()` will call `_buyMochi()` to convert `mochiShare` to Mochi token and call `_shareMochi()` to send Mochi to vMochi Vault and veCRV Holders. It wont touch the `treasuryShare`.

However, in the current implementation, `treasuryShare` will be reset to `0`. This is unexpected and will cause the protocol fee can not be properly accounted for and collected.

https://github.com/code-423n4/2021-10-mochi/blob/8458209a52565875d8b2cefcb611c477cefb9253/projects/mochi-core/contracts/feePool/FeePoolV0.sol#L79-L95

```solidity=79
function _shareMochi() internal {
    IMochi mochi = engine.mochi();
    uint256 mochiBalance = mochi.balanceOf(address(this));
    // send Mochi to vMochi Vault
    mochi.transfer(
        address(engine.vMochi()),
        (mochiBalance * vMochiRatio) / 1e18
    );
    // send Mochi to veCRV Holders
    mochi.transfer(
        crvVoterRewardPool,
        (mochiBalance * (1e18 - vMochiRatio)) / 1e18
    );
    // flush mochiShare
    mochiShare = 0;
    treasuryShare = 0;
}
```

### Impact

Anyone can call `distributeMochi()` and reset `treasuryShare` to `0`, and then call `updateReserve()` to allocate part of the wrongfuly resetted `treasuryShare` to `mochiShare` and call `distributeMochi()`.

Repeat the steps above and the `treasuryShare` will be consumed to near zero, profits the vMochi Vault holders and veCRV Holders. The protocol suffers the loss of funds.

### Recommendation

Change to:

```solidity=64
function _buyMochi() internal {
    IUSDM usdm = engine.usdm();
    address[] memory path = new address[](2);
    path[0] = address(usdm);
    path[1] = address(engine.mochi());
    usdm.approve(address(uniswapRouter), mochiShare);
    uniswapRouter.swapExactTokensForTokens(
        mochiShare,
        1,
        path,
        address(this),
        type(uint256).max
    );
    // flush mochiShare
    mochiShare = 0;
}

function _shareMochi() internal {
    IMochi mochi = engine.mochi();
    uint256 mochiBalance = mochi.balanceOf(address(this));
    // send Mochi to vMochi Vault
    mochi.transfer(
        address(engine.vMochi()),
        (mochiBalance * vMochiRatio) / 1e18
    );
    // send Mochi to veCRV Holders
    mochi.transfer(
        crvVoterRewardPool,
        (mochiBalance * (1e18 - vMochiRatio)) / 1e18
    );
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/114
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

