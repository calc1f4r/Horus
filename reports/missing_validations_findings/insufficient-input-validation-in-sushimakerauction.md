---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19596
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/auction-maker-furo/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/auction-maker-furo/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Insufficient Input Validation in SushiMakerAuction

### Overview

See description below for full details.

### Original Finding Content

Description
•Zero or small rewardAmount
It is possible to bid on tokens which have zero or smaller than desirable rewardAmount instartBid() . This may
occur if a user’s call to startBid() is not mined in the time it takes another auction to execute.
Consider adding a minimumRewardAmount parameter to startBid() and ensuring the balance of the reward token
is larger than minimumRewardAmount .
•Zero addresses
Missing zero address checks on the input parameter toinstart() and placeBid() can lead to lost funds for
the bidder. By setting bid.bidder to the zero address the auction reaches an invalid state. This is because that
value is used to determine the auction’s state: When bid.bidder is zero, the auction is considered finished. It is
assumed that transfers and correct accounting of stakedBidToken has been applied in end() . Even though this
is not true in this scenario, the auction can be restarted.
Recommendations
We recommend adding the suggested input validation checks for zero address and zero amounts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/auction-maker-furo/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/auction-maker-furo/review.pdf

### Keywords for Search

`vulnerability`

