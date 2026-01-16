---
# Core Classification
protocol: Olympus Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8717
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/60
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-olympus-judging/issues/4

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.47
financial_impact: high

# Scoring
quality_score: 2.3333333333333335
rarity_score: 1.3333333333333333

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - 0x52
  - Bahurum
  - cducrest-brainbot
  - hickuphh3
  - carrot
---

## Vulnerability Title

H-3: Adversary can stake LP directly for the vault then withdraw to break lp accounting in BLVaultManagerLido

### Overview


This bug report concerns the BLVaultManagerLido contract in the Sherlock Olympus audit. The issue is that a malicious user can stake LP directly for their vault and then call withdraw on their vault, which would cause the LP tracking to break and some users would be permanently trapped in the vault. 

The vulnerability is found in BaseRewardPool.sol, where users can stake directly for another address. In BLVaultLido.sol, once the LP has been staked the adversary can immediately withdraw it. This calls decreaseTotalLP on BLVaultManagerLido, which permanently breaks the LP account. If the amount is ever greater than totalLP it will cause decreaseTotalLP to revert. This means that if a user withdraws LP that was never deposited to a vault, it permanently breaks other users from being able to withdraw. 

The impact of this issue is that LP accounting is broken and users are permanently trapped. A code snippet of the issue can be found in BLVaultLido.sol. The bug was found through manual review. The recommendation is that individual vaults should track how much they have deposited and shouldn't be allowed to withdraw more than deposited. A fix implementation was provided by 0xLienid, which can be found in the link provided.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-olympus-judging/issues/4 

## Found by 
0x52, carrot, cducrest-brainbot, hickuphh3, Bahurum

## Summary

The AuraRewardPool allows users to stake directly for other users. In this case the malicious user could stake LP directly for their vault then call withdraw on their vault. This would cause the LP tracking to break on BLVaultManagerLido. The result is that some users would now be permanently trapped because their vault would revert when trying to withdraw.

## Vulnerability Detail

[BaseRewardPool.sol#L196-L207](https://github.com/aurafinance/convex-platform/blob/1d6e9c403a4440c712396422e1bd5af7e5ea1ecf/contracts/contracts/BaseRewardPool.sol#L196-L207)

    function stakeFor(address _for, uint256 _amount)
        public
        returns(bool)
    {
        _processStake(_amount, _for);

        //take away from sender
        stakingToken.safeTransferFrom(msg.sender, address(this), _amount);
        emit Staked(_for, _amount);
        
        return true;
    }

AuraRewardPool allows users to stake directly for another address with them receiving the staked tokens.

[BLVaultLido.sol#L218-L224](https://github.com/sherlock-audit/2023-03-olympus/blob/main/sherlock-olympus/src/policies/BoostedLiquidity/BLVaultLido.sol#L218-L224)

        manager.decreaseTotalLp(lpAmount_);

        // Unstake from Aura
        auraRewardPool().withdrawAndUnwrap(lpAmount_, claim_);

        // Exit Balancer pool
        _exitBalancerPool(lpAmount_, minTokenAmounts_);

Once the LP has been stake the adversary can immediately withdraw it from their vault. This calls decreaseTotalLP on BLVaultManagerLido which now permanently break the LP account.

[BLVaultManagerLido.sol#L277-L280](https://github.com/sherlock-audit/2023-03-olympus/blob/main/sherlock-olympus/src/policies/BoostedLiquidity/BLVaultManagerLido.sol#L277-L280)

    function decreaseTotalLp(uint256 amount_) external override onlyWhileActive onlyVault {
        if (amount_ > totalLp) revert BLManagerLido_InvalidLpAmount();
        totalLp -= amount_;
    }
    
If the amount_ is ever greater than totalLP it will cause decreaseTotalLP to revert. By withdrawing LP that was never deposited to a vault, it permanently breaks other users from being able to withdraw.

Example:
User A deposits wstETH to their vault which yields 50 LP. User B creates a vault then stake 50 LP and withdraws it from his vault. The manager now thinks there is 0 LP in vaults. When User A tries to withdraw their LP it will revert when it calls manger.decreaseTotalLp. User A is now permanently trapped in the vault.

## Impact

LP accounting is broken and users are permanently trapped.

## Code Snippet

[BLVaultLido.sol#L203-L256](https://github.com/sherlock-audit/2023-03-olympus/blob/main/sherlock-olympus/src/policies/BoostedLiquidity/BLVaultLido.sol#L203-L256)

## Tool used

Manual Review

## Recommendation

Individual vaults should track how much they have deposited and shouldn't be allowed to withdraw more than deposited.

## Discussion

**0xLienid**

Fix Implementation: https://github.com/0xLienid/sherlock-olympus/pull/5/files

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 2.3333333333333335/5 |
| Rarity Score | 1.3333333333333333/5 |
| Audit Firm | Sherlock |
| Protocol | Olympus Update |
| Report Date | N/A |
| Finders | 0x52, Bahurum, cducrest-brainbot, hickuphh3, carrot |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-olympus-judging/issues/4
- **Contest**: https://app.sherlock.xyz/audits/contests/60

### Keywords for Search

`vulnerability`

