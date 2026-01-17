---
# Core Classification
protocol: Opyn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18222
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Opyn.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Opyn.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Gustavo Grieco
  - Jaime Iglesias
  - Devashish Tomar
---

## Vulnerability Title

Front-running a withdrawal operation can cause it to revert

### Overview

See description below for full details.

### Original Finding Content

## Description

An attacker can front-run the withdraw function in the CrabStrategy contract to force the transaction to fail. The CrabStrategy defines the following withdraw function:

```solidity
function withdraw(uint256 _crabAmount, uint256 _wSqueethAmount) external payable nonReentrant {
    uint256 ethToWithdraw = _withdraw(msg.sender, _crabAmount, _wSqueethAmount, false);
    // send back ETH collateral
    payable(msg.sender).sendValue(ethToWithdraw);
    emit Withdraw(msg.sender, _crabAmount, _wSqueethAmount, ethToWithdraw);
}
```

**Figure 8.1:** The withdraw function in the CrabStrategy contract

The operation calculates the amount of collateral that can be withdrawn based on the amount of shares the user wants to burn. Furthermore, if the strategy holds any debt, the strategy requires that a proportionate amount of power perpetuals be burned to keep the collateral ratio within the threshold; this amount has to be calculated by the user before performing the withdrawal.

```solidity
function _withdraw(
    address _from,
    uint256 _crabAmount,
    uint256 _wSqueethAmount,
    bool _isFlashWithdraw
) internal returns (uint256) {
    (uint256 strategyDebt, uint256 strategyCollateral) = _syncStrategyState();
    uint256 strategyShare = _calcCrabRatio(_crabAmount, totalSupply());
    uint256 ethToWithdraw = _calcEthToWithdraw(strategyShare, strategyCollateral);
    if (strategyDebt > 0) require(_wSqueethAmount.wdiv(strategyDebt) == strategyShare, "invalid ratio");
    ...
}
```

**Figure 8.2:** The _withdraw function in the CrabStrategy contract

This last invariant introduces the front-running vulnerability. The user needs to calculate beforehand the amount of power perpetuals and strategy tokens they have to burn for the strategy’s current debt; however, any transaction that precedes the withdrawal could change the strategy’s current debt, making the withdrawal operation fail.

## Exploit Scenario

Alice is a user of the Crab strategy and wants to withdraw some of her funds. She calls withdraw, defining a number of strategy tokens and power perpetuals to burn with her withdrawal. Eve sees Alice’s unconfirmed transaction and front-runs it with another transaction that causes the CrabStrategy debt to decrease. This reduction in debt causes the `require(_wSqueethAmount.wdiv(strategyDebt) == strategyShare)` invariant to fail, since Alice had already defined a number of power perpetuals to burn.

## Recommendations

- Short term: Refactor the code so that, given a number of power perpetuals and strategy tokens, it calculates the maximum amount of collateral that can be withdrawn for the current debt without breaking the invariant.
- Long term: Review all system invariants and use Echidna to test them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Opyn |
| Report Date | N/A |
| Finders | Gustavo Grieco, Jaime Iglesias, Devashish Tomar |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Opyn.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Opyn.pdf

### Keywords for Search

`vulnerability`

