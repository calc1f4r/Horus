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
solodit_id: 45990
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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

[H-03] Freezing the deposit in MetaVault indefinitely

### Overview


A high severity bug has been found in the LendingAssetVault.sol contract. This bug can be exploited by an attacker to freeze a victim's assets permanently. The bug occurs when the victim deposits into the Meta Vault and then tries to withdraw at a later block. The attacker can frontrun the victim's withdrawal and deposit just 1 wei of assets, causing the victim's withdrawal to fail and their assets to be frozen. It is recommended that the contract should not allow deposits on behalf of others to prevent this bug from being exploited.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description:

Consider the following -->

1.) Victim has deposited into the LendingAssetVault.sol (what we call the Meta Vault), let's say when the victim deposited the

block.number = 50 i.e. `_lastDeposit[victim] = 50`

2.) Now at block 80 the victim wants to withdraw, he calls the withdraw function providing the assets he wants to withdraw.

3.) The attacker sees this tx in the mempool, frontruns the withdraw call of the victim and calls the deposit function with just 1 wei of assets,

(or the minimum amount required so that the shares are non-zero) and sets the victim's address as the receiver address -->

```solidity

function deposit(uint256 _assets, address _receiver) external override returns (uint256 _shares) {
        _updateInterestAndMdInAllVaults(address(0));
        _shares = convertToShares(_assets);
        _deposit(_assets, _shares, _receiver);
    }
```

this would update the victim's ` _lastDeposit[victim]` to 80 here -->

```solidity
function _deposit(uint256 _assets, uint256 _shares, address _receiver) internal {
        require(_assets != 0 && _shares != 0, "M");
        _totalAssets += _assets;
        _lastDeposit[_receiver] = block.number; <-- here
        _mint(_receiver, _shares);
        IERC20(_asset).safeTransferFrom(_msgSender(), address(this), _assets);
        emit Deposit(_msgSender(), _receiver, _assets, _shares);
    }
```

4.) Now when the victim's withdraw tx executes it would revert due to this check in the `_withdraw` call -->

` require(!_lastDepEnabled || block.number > _lastDeposit[_owner], "MIN");`

L178 of LendingAssetVault.sol

Therefore, as long as the attacker performs this frontrunning the victim can not withdraw his assets back from the vault which would mean
a permanent freeze of those assets.

## Recommendation

We recommend that it should not be allowed to deposit on someone else's behalf.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

