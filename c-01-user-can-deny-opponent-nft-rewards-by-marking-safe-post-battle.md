---
# Core Classification
protocol: Beetle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62314
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Beetle-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[C-01] User Can Deny Opponent NFT Rewards By Marking Safe Post-Battle

### Overview


This bug report is about a function called `markBeetleSafe()` that allows users to protect their in-game assets in a game called BeetleBattle. The function only checks if the user owns the asset, but doesn't consider when or how the function is being used. This means that a malicious user can wait until after losing a battle and then use the function to protect their assets, even though they should have lost them. This can affect the fairness of battles and the game's reward system. The recommendation is to restrict the function or require additional authorization to prevent misuse. The team has fixed the issue.

### Original Finding Content


## Severity

Critical Risk

## Description

The `markBeetleSafe()` function allows a user to designate one of their staked NFTs as the safe beetle at any time. The function only verifies that the caller is the staker of the token, but does not validate the timing or context of the action. As a result, a user can wait until after losing a battle and then call `markBeetleSafe()` on the threatened NFT. Because `claimBeetleFromVictory()` prohibits transferring a safe beetle, this enables a malicious participant to retroactively protect assets that should otherwise be lost.

## Location of Affected Code

File: [contracts/BeetleBattleGame.sol#L231](https://github.com/rshtirmer/BeetleGame-Contracts/blob/4ab13a82a1f9b7228d5c0ad3a085518a60459036/contracts/BeetleBattleGame.sol#L231)

```solidity
function markBeetleSafe(uint256 _tokenId) public {
  if (isStaked[_tokenId] != msg.sender) revert InvalidTokenOwner();
  safeBeetle[msg.sender] = _tokenId;

  emit SafeBeetleUpdated(msg.sender, _tokenId);
}
```

## Impact

Winners of battles may be unable to claim the opponent’s NFTs, as the defeated party can immediately call `markBeetleSafe()` to shield the asset after the outcome is determined. This undermines the fairness of battles, negates the reward mechanism, and weakens trust in the protocol’s economic model.

## Recommendation

Restrict `markBeetleSafe()` to only be called during the staking process or require a valid signer authorization to confirm the action, preventing post-battle misuse.

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Beetle |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Beetle-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

