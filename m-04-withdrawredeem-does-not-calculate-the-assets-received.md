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
solodit_id: 45998
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

[M-04] `withdraw/redeem` does not calculate the assets received

### Overview


The report discusses a bug in a code that calculates and transfers assets to users. The bug occurs when rewards are processed after the calculation, resulting in users not receiving the correct amount of assets. The severity and likelihood of the bug are medium, and the recommendation is to trigger rewards processing before the calculation to ensure users receive the correct amount of assets.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

`AutoCompoundingPodLp.withdraw/redeem` first calculates the `assets/shares` to be received or burned, then triggers `_withdraw` to burn the shares and transfer the calculated assets to the users. However, the calculated assets or burned shares for the users do not account for processed rewards, as these are triggered later within the `_withdraw` operation.

```solidity
    function withdraw(uint256 _assets, address _receiver, address _owner) external override returns (uint256 _shares) {
>>>     _shares = convertToShares(_assets);
        _withdraw(_assets, _shares, _msgSender(), _owner, _receiver);
    }
```

```solidity
    function redeem(uint256 _shares, address _receiver, address _owner) external override returns (uint256 _assets) {
>>>     _assets = convertToAssets(_shares);
        _withdraw(_assets, _shares, _msgSender(), _owner, _receiver);
    }
```

```solidity
    function _withdraw(uint256 _assets, uint256 _shares, address _caller, address _owner, address _receiver) internal {
        require(_shares != 0, "B");

        if (_caller != _owner) {
            _spendAllowance(_owner, _caller, _shares);
        }

>>>     _processRewardsToPodLp(0, block.timestamp);

        _totalAssets -= _assets;
        _burn(_owner, _shares);
        IERC20(_asset()).safeTransfer(_receiver, _assets);
        emit Withdraw(_owner, _receiver, _receiver, _assets, _shares);
    }
```

This will cause the `withdraw/redeem` operation to not consider the latest `totalAssets`, resulting in users losing their deserved assets.

## Recommendations

Trigger `_processRewardsToPodLp` before calculating `_shares` and `_assets`.

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

