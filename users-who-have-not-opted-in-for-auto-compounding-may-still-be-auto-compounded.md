---
# Core Classification
protocol: DefiApp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53448
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8410dfc1-a319-4bb0-be1c-bc92a25e57a9
source_link: https://cdn.cantina.xyz/reports/cantina_competition_defi_app_february2025.pdf
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
finders_count: 3
finders:
  - Jonatas Martins
  - aksoy
  - TamayoNft
---

## Vulnerability Title

Users who have not opted in for auto-compounding may still be auto-compounded 

### Overview


The MFDBase contract has a function called `claimAndCompound` which claims and compounds rewards for users. However, this function does not check if the user has authorized reward claims and auto-compounding. This means that unauthorized users could receive rewards when they should not. The code for this function should be updated to include a check for user authorization. This issue has been fixed in the DeFi App with commit 8b8d7e5e.

### Original Finding Content

## Context
MFDBase.sol#L365-L388

## Description
The function `claimAndCompound` in the MFDBase contract claims rewards on behalf of a user and compounds them into more staked tokens. For this to work, the user must opt-in to auto-compound through the `toggleAutocompound()` function. However, the `claimAndCompound()` function doesn't verify if the user has authorized reward claims and auto-compounding. This means the RewardCompounder actor could process transactions for unauthorized users when it should be prevented from doing so. 

Check the following code of `claimAndCompound()`:

```solidity
function claimAndCompound(address _onBehalf) external whenNotPaused {
    MultiFeeDistributionStorage storage $ = _getMFDBaseStorage();
    if (msg.sender != $.rewardCompounder) revert InsufficientPermission();
    MFDLogic.updateReward($, _onBehalf);
    //@audit Doesnt check if the user opt-in to auto compound
    uint256 length = $.rewardTokens.length;
    for (uint256 i; i < length;) {
        address token = $.rewardTokens[i];
        if (token != $.emissionToken) {
            MFDLogic.trackUnseenReward($, token);
            uint256 reward = $.rewards[_onBehalf][token] / PRECISION;
            if (reward > 0) {
                $.rewards[_onBehalf][token] = 0;
                $.rewardData[token].balance = $.rewardData[token].balance - reward;
                IERC20(token).safeTransfer($.rewardCompounder, reward);
                emit RewardPaid(_onBehalf, token, reward);
            }
        }
        unchecked {
            i++;
        }
    }
    $.lastClaimTime[_onBehalf] = block.timestamp;
}
```

## Recommendation
Consider adding a check if the user opt-in to auto compound.

## DeFi App
Fixed in commit 8b8d7e5e.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | DefiApp |
| Report Date | N/A |
| Finders | Jonatas Martins, aksoy, TamayoNft |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_defi_app_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8410dfc1-a319-4bb0-be1c-bc92a25e57a9

### Keywords for Search

`vulnerability`

