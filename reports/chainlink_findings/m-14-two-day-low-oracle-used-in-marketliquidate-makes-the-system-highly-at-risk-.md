---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 5743
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/469

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - oracle

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - gs8nrv
  - immeas
  - kaden
  - yamapyblack
  - idkwhatimdoing
---

## Vulnerability Title

[M-14] Two day low oracle used in Market.liquidate() makes the system highly at risk in an oracle attack 

### Overview


This bug report is about a vulnerability in the Market.sol code on the 2022-10-inverse GitHub repository. The vulnerability could be exploited by malicious agents to control the price feed for a short period of time and liquidate any escrow. This could result in more collateral being released than expected, leading to a financial loss for the user. The team has recommended mitigation steps such as taking the current oracle price instead of the 2 day lowest price during the liquidation, while still using the 2 day period for any direct agent interaction. This would help to minimise attacks from both users and liquidators.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L596
https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L594
https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L597


## Vulnerability details

## Impact
Usage of the 2 day low exchange rate when trying to liquidate is highly risky as it incentives even more malicious agents to control the price feed for a short period of time. By controlling shortly the feed, it puts at risk any debt opened for a 2 day period + the collateral released will be overshoot during the liquidation

## Proof of Concept
The attack can be done by either an attack directly on the feed to push bad data, or in the case of Chainlink manipulating for a short period of time the markets to force an update from Chainlink. Then when either of the attacks has been made the attacker call `Oracle.getPrice()`. It then gives a 2 day period to the attacker (and any other agent who wants to liquidate) to liquidate any escrow. 

This has a second drawback, we see that we use the same value at line 596, which is used to compute the liquidator reward (l.597), leading to more collateral released than expected. For instance manipulating once the feed and bring the ETH/USD rate to 20 instead of 2000, liquidator will earn 100 more than he should have had.

## Tools Used

## Recommended Mitigation Steps
Instead of using the 2 day lowest price during the liquidation, the team could either take the current oracle price, while still using the 2 day period for any direct agent interaction to minimise attacks both from users side and liquidators side

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | gs8nrv, immeas, kaden, yamapyblack, idkwhatimdoing, rvierdiiev, Holmgren |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/469
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Oracle`

