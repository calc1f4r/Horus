---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 18501
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/115

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
  - oracle
  - liquidation
  - denial-of-service

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0x52
  - nobody2018
---

## Vulnerability Title

M-7: BlueBerryBank#getPositionValue causes DOS if reward token is added that doens't have an oracle

### Overview


This bug report is about BlueBerryBank#getPositionValue which is a function in the BlueBerryBank.sol file. It is found by 0x52, nobody2018 and it causes a Denial-of-Service (DOS) attack if reward tokens are added to pools that don't have an oracle. This means that liquidations, which are a key process that should have 100% uptime, are temporarily prevented which can result in bad debt accumulating in a volatile market. 

The code snippet for this vulnerability can be found in BlueBerryBank.sol#L392-L417. It was found through manual review. 

The recommendation for this bug is to return a zero valuation if extra reward tokens can't be priced. This should prevent the DOS attack and keep the liquidation process running smoothly.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/115 

## Found by 
0x52, nobody2018
## Summary

collToken.pendingRewards pulls the most recent reward list from Aura/Convex. In the event that reward tokens are added to pools that don't currently have an oracle then it will DOS every action (repaying, liquidating, etc.). While this is only temporary it prevents liquidation which is a key process that should have 100% uptime otherwise the protocol could easily be left with bad debt.

## Vulnerability Detail

[BlueBerryBank.sol#L408-L413](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/BlueBerryBank.sol#L408-L413)

          (address[] memory tokens, uint256[] memory rewards) = IERC20Wrapper(
              pos.collToken
          ).pendingRewards(pos.collId, pos.collateralSize);
          for (uint256 i; i < tokens.length; i++) {
              rewardsValue += oracle.getTokenValue(tokens[i], rewards[i]);
          }

Using the pendingRewards method pulls a fresh list of all tokens. When a token is added as a reward but can't be priced then the call to getTokenValue will revert. Since getPostionValue is used in liquidations, it temporarily breaks liquidations which in a volatile market can cause bad debt to accumulate.

## Impact

Temporary DOS to liquidations which can result in bad debt

## Code Snippet

[BlueBerryBank.sol#L392-L417](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/BlueBerryBank.sol#L392-L417)

## Tool used

Manual Review

## Recommendation

Return zero valuation if extra reward token can't be priced.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | 0x52, nobody2018 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/115
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Oracle, Liquidation, Denial-Of-Service`

