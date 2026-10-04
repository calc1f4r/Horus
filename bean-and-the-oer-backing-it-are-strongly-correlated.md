---
# Core Classification
protocol: Beanstalk
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21269
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-07-beanstalk-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-07-beanstalk-securityreview.pdf
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
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator
  - privacy

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Jaime Iglesias
  - Bo Henderson
---

## Vulnerability Title

Bean and the o�er backing it are strongly correlated

### Overview

See description below for full details.

### Original Finding Content

## Beanstalk Security Assessment

**Difficulty:** Undetermined

**Type:** Economic

**Target:** The Beanstalk protocol

## Description

In response to prolonged periods of decreasing demand for Bean tokens, the Beanstalk protocol offers to borrow from users who own Bean tokens, decreasing the available Bean supply and returning the Bean price to its peg. To incentivize users to lend their Bean tokens to the protocol rather than immediately selling them in the market, which would put further downward pressure on the price of Bean, the protocol offers users a reward of more Bean tokens in the future.

The demand for holding Bean tokens at present and the demand for receiving Bean tokens in the future are strongly correlated, introducing reflexive risk. If the demand for Bean decreases, we can expect a proportional increase in the marginal Bean supply and a decrease in demand to receive Bean in the future, weakening the system’s ability to restore Bean to its value peg.

The FIFO queue of lenders is designed to combat reflexivity by encouraging rational actors to quickly support a dip in Bean price rather than selling. However, this mechanism assumes that the demand for Bean will increase in the future; investors may not share this assumption if present demand for Bean is low. Reflexivity is present whenever a stablecoin and the offer backing it are strongly correlated, even if the backing offer is time sensitive.

## Exploit Scenario

Bean goes through an extended period of increasing demand, overextending its supply. Then, the demand for Bean slowly and steadily declines as some users lose interest in holding Bean. These same users also lose interest in receiving Bean tokens in the future, so rather than loaning their tokens to Beanstalk to earn a very high Bean-denominated yield, they sell.

## Recommendations

Explore options for backing Bean’s value with an offer that is not correlated with demand for Bean.

---

**Trail of Bits**  
Beanstalk Security Assessment  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Beanstalk |
| Report Date | N/A |
| Finders | Jaime Iglesias, Bo Henderson |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-07-beanstalk-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-07-beanstalk-securityreview.pdf

### Keywords for Search

`vulnerability`

