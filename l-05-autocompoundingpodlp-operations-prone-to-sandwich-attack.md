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
solodit_id: 46012
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-05] `AutoCompoundingPodLp` operations prone to sandwich attack

### Overview

See description below for full details.

### Original Finding Content

Key functions within `AutoCompoundingPodLp`, including `deposit`, `mint`, `withdraw`, and `redeem`, will trigger `_processRewardsToPodLp` during their operations, providing no slippage protection. Within `_processRewardsToPodLp`, several swap operations are performed, and without proper slippage protection, these operations are vulnerable to sandwich attacks.

```solidity
    function deposit(uint256 _assets, address _receiver) external override returns (uint256 _shares) {
>>>     _processRewardsToPodLp(0, block.timestamp);
        _shares = convertToShares(_assets);
        _deposit(_assets, _shares, _receiver);
    }
```

```solidity
    function mint(uint256 _shares, address _receiver) external override returns (uint256 _assets) {
>>>     _processRewardsToPodLp(0, block.timestamp);
        _assets = convertToAssets(_shares);
        _deposit(_assets, _shares, _receiver);
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

Consider implementing slippage protection within these functions. An oracle could be used to calculate the price and the expected minimum output, which can then be provided to `_processRewardsToPodLp`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

