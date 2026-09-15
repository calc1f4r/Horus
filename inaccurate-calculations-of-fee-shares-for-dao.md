---
# Core Classification
protocol: Liquistake
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58499
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-08-LiquiStake.md
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
  - zokyo
---

## Vulnerability Title

Inaccurate calculations of fee shares for DAO.

### Overview


The StWSX.sol file has a bug in the oracle Claim Rewards() function. When users claim their rewards, a portion of it is supposed to go to the DAO as protocol fees. However, the fees are not being calculated correctly and this results in the DAO receiving less than what it should. This can also lead to users receiving less rewards. The recommendation is to only add the portion of the reward that goes to users to the 'totalPooledWSX' before minting shares, and then add the remaining portion after minting. This has been fixed after a re-audit.

### Original Finding Content

**Description**

StWSX.sol: oracle Claim Rewards().
When rewards are claimed, part of them are allocated to the DAO in the form of shares as protocol fees. However, the fees are not calculated accurately since the whole amount of the reward amount` is added to the 'totalPooledWSX before the calculating and minting of fees. As a result, the DAO will actually receive less when shares are redeemed. And in case rewardAmount is added to the totalPooledWSX after minting, DAO will receive more, cutting user rewards.

**Recommendation**

Before minting shares, add only the reward amount that should be distributed to users (reward Amount - reward FeeAmount) to the 'totalPooledWSX. The rest (rewardFeeAmount) should be added after minting.
Example of the code:
totalPooledWSX += (reward Amount - reward FeeAmount);
uint256 reward FeesShares = getSharesByPooledWSX(rewardFeeAmount);
_mintShares(DAO_ADDRESS, reward FeesShares);
totalPooledWSX += rewardFeeAmount;

**Re-audit comment**

Resolved.

Post-audit. Changes were applied.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Liquistake |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-08-LiquiStake.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

