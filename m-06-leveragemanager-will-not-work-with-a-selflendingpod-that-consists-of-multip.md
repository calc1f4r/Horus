---
# Core Classification
protocol: Peapods_2024-11-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46000
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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

[M-06] `LeverageManager` will not work with a `selfLendingPod` that consists of multiple tokens

### Overview


The report states that there is a bug in the code that affects the use of `selfLendingPod` in leverage positions. This bug has a high impact and a low likelihood of occurring. The code assumes that the `selfLendingPod` only contains one token, and if it contains multiple tokens, the functions will always fail. The recommendation is to either support pods with multiple tokens or check if a `selfLendingPod` contains more than one token when a position is created and revert the operation if so.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When leverage positions use a `selfLendingPod`, it will `bond` and `debond` to convert between the borrowed token and the final paired token.

```solidity
    function _processAndGetPairedTknAndAmt(
        uint256 _positionId,
        address _borrowedTkn,
        uint256 _borrowedAmt,
        address _selfLendingPairPod
    ) internal returns (address _finalPairedTkn, uint256 _finalPairedAmt) {
        _finalPairedTkn = _borrowedTkn;
        _finalPairedAmt = _borrowedAmt;
        address _lendingPair = positionProps[_positionId].lendingPair;
        if (_isPodSelfLending(_positionId)) {
            _finalPairedTkn = _lendingPair;
            IERC20(_borrowedTkn).safeIncreaseAllowance(_lendingPair, _finalPairedAmt);
            _finalPairedAmt = IFraxlendPair(_lendingPair).deposit(_finalPairedAmt, address(this));

            // self lending+podded
            if (_selfLendingPairPod != address(0)) {
                _finalPairedTkn = _selfLendingPairPod;
>>>             IERC20(_lendingPair).safeIncreaseAllowance(_selfLendingPairPod, _finalPairedAmt);
>>>             IDecentralizedIndex(_selfLendingPairPod).bond(_lendingPair, _finalPairedAmt, 0);
                _finalPairedAmt = IERC20(_selfLendingPairPod).balanceOf(address(this));
            }
        }
    }
```

```solidity
    function _debondFromSelfLendingPod(address _pod, uint256 _amount) internal returns (uint256 _amtOut) {
        IDecentralizedIndex.IndexAssetInfo[] memory _podAssets = IDecentralizedIndex(_pod).getAllAssets();
        address[] memory _tokens = new address[](1);
        uint8[] memory _percentages = new uint8[](1);
        _tokens[0] = _podAssets[0].token;
        _percentages[0] = 100;
>>>     IDecentralizedIndex(_pod).debond(_amount, _tokens, _percentages);
        _amtOut = IERC20(_tokens[0]).balanceOf(address(this));
    }
```

```solidity
    function _spTknToAspTkn(address _spTKN, uint256 _pairedRemainingAmt, LeverageFlashProps memory _props)
        internal
        returns (uint256 _newAspTkns)
    {
        // uint256 _aspTknCollateralBal =
        // _spTknToAspTkn(IDecentralizedIndex(_pod).lpStakingPool(), _pairedLeftover, _props);
        address _aspTkn = _getAspTkn(_props.positionId);
        uint256 _stakingBal = IERC20(_spTKN).balanceOf(address(this));
        IERC20(_spTKN).safeIncreaseAllowance(_aspTkn, _stakingBal);
        _newAspTkns = IERC4626(_aspTkn).deposit(_stakingBal, address(this));

        // for self lending pods redeem any extra paired LP asset back into main asset
        if (_isPodSelfLending(_props.positionId) && _pairedRemainingAmt > 0) {
            if (positionProps[_props.positionId].selfLendingPod != address(0)) {
                address[] memory _noop1;
                uint8[] memory _noop2;
>>>             IDecentralizedIndex(positionProps[_props.positionId].selfLendingPod).debond(
                    _pairedRemainingAmt, _noop1, _noop2
                );
                _pairedRemainingAmt = IERC20(positionProps[_props.positionId].lendingPair).balanceOf(address(this));
            }
            IFraxlendPair(positionProps[_props.positionId].lendingPair).redeem(
                _pairedRemainingAmt, address(this), address(this)
            );
        }
    }
```

However, it can be observed that it assumes the `selfLendingPod` only consists of `lendingPair`, if it consists of multiple tokens, the functions will always revert.

## Recommendations

Consider supporting pods with multiple tokens, or check when positions are created, if a `selfLendingPod` consists of more than one token, revert the operation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Peapods_2024-11-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

