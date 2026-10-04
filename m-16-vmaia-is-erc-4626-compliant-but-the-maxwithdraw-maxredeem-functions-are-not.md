---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: erc4626

# Attack Vector Details
attack_type: erc4626
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26085
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/585

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:
  - erc4626
  - eip-4626

protocol_categories:
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - BPZ
  - Noro
---

## Vulnerability Title

[M-16] `vMaia` is ERC-4626 compliant, but the `maxWithdraw` & `maxRedeem` functions are not fully up to EIP-4626's specification

### Overview


This bug report is about the `maxWithdraw` & `maxRedeem` functions in the ERC4626 contract. The functions should return `0` when the withdrawal is paused, according to the EIP-4626 specifications. However, it was returning the `balanceOf[user]`.

The `vMaia Withdrawal` is only allowed once per month during the 1st Tuesday (UTC+0) of the month. This is checked by the function beforeWithdraw which checks if the unstake period has not ended yet and if it is the 1st Tuesday of the month. If not, it reverts the UnstakePeriodNotLive.

The recommended mitigation steps are to use an if-else block and if the time period is within the 1st Tuesday (UTC+0) of the month, return `balanceOf[user]` and `else` return `0`. This was confirmed and addressed by 0xLightt (Maia).

### Original Finding Content


The `maxWithdraw` & `maxRedeem` functions should return the `0` when the withdrawal is paused. But here, it's returning `balanceOf[user]`.

### Proof of Concept

`vMaia Withdrawal` is only allowed once per month during the 1st Tuesday (UTC+0) of the month.

It's checked by the below function:

```

     102       function beforeWithdraw(uint256, uint256) internal override {
                /// @dev Check if unstake period has not ended yet, continue if it is the case.
                if (unstakePeriodEnd >= block.timestamp) return;
        
                uint256 _currentMonth = DateTimeLib.getMonth(block.timestamp);
                if (_currentMonth == currentMonth) revert UnstakePeriodNotLive();
        
                (bool isTuesday, uint256 _unstakePeriodStart) = DateTimeLib.isTuesday(block.timestamp);
                if (!isTuesday) revert UnstakePeriodNotLive();
        
                currentMonth = _currentMonth;
                unstakePeriodEnd = _unstakePeriodStart + 1 days;
    114        }
```

<https://github.com/code-423n4/2023-05-maia/blob/main/src/maia/vMaia.sol#L102C1-L114C6>

```

    173            function maxWithdraw(address user) public view virtual override returns (uint256) {
                      return balanceOf[user];
                  }
              
                  /// @notice Returns the maximum amount of assets that can be redeemed by a user.
                  /// @dev Assumes that the user has already forfeited all utility tokens.
                  function maxRedeem(address user) public view virtual override returns (uint256) {
                      return balanceOf[user];
    181              }
```
<https://github.com/code-423n4/2023-05-maia/blob/main/src/maia/tokens/ERC4626PartnerManager.sol#L173C3-L181C6>

Other than that period (during the 1st Tuesday (UTC+0) of the month ), the `maxWithdraw` & `maxRedeem` functions should return the `0`.

According to [EIP-4626 specifications](<https://eips.ethereum.org/EIPS/eip-4626>):

`maxWithdraw`

     MUST factor in both global and user-specific limits, like if withdrawals are entirely disabled (even temporarily) it MUST
     return 0.

`maxRedeem`

     MUST factor in both global and user-specific limits, like if redemption is entirely disabled (even temporarily) it MUST
     return 0.

### Recommended Mitigation Steps

Use an if-else block and if the time period is within the 1st Tuesday (UTC+0) of the month, return `balanceOf[user]` and `else` return `0`.

For more information, reference [here](<https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-2#non-standard-erc-4626-vault-functionality>).

### Assessed type

ERC4626

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/585#issuecomment-1655656724)**

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/585#issuecomment-1709162142):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/585).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | BPZ, Noro |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/585
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`ERC4626, EIP-4626`

