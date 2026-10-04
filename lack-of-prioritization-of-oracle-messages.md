---
# Core Classification
protocol: Umee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16913
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
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
finders_count: 2
finders:
  - Paweł Płatek
  - Dominik Czarnota
---

## Vulnerability Title

Lack of prioritization of oracle messages

### Overview


This bug report is about an issue in the Umee system where Oracle messages are not prioritized over other transactions for inclusion in a block. This can be a problem if the network is congested, as the messages may not be included in a block. To address this, Tactics for prioritizing important transactions have been suggested, such as using the custom CheckTx implementation, reimplementing part of the Tendermint engine, and using Substrate's dispatch classes. The exploit scenario is if the Umee network is congested, validators send their exchange rate votes, but the exchange rates are not included in a block. An attacker can then exploit the situation by draining the network of its tokens. The short-term recommendation is to use a custom CheckTx method to prioritize oracle messages, and the long-term recommendation is to ensure that operations that affect the whole system cannot be front-run or delayed by attackers or blocked by network congestion.

### Original Finding Content

## Umee Security Assessment

**Difficulty:** Medium

**Type:** Undefined Behavior

**Target:** umee/x/oracle

## Description
Oracle messages are not prioritized over other transactions for inclusion in a block. If the network is highly congested, the messages may not be included in a block. Although the Umee system could increase the fee charged for including an oracle message in a block, that solution is suboptimal and may not work.

Tactics for prioritizing important transactions include the following:
- Using the custom **CheckTx** implementation introduced in Tendermint version 0.35, which returns a priority argument.
- Reimplementing part of the Tendermint engine, as Terra Money did.
- Using Substrate’s dispatch classes, which allow developers to mark transactions as normal, operational, or mandatory.

## Exploit Scenario
The Umee network is congested. Validators send their exchange rate votes, but the exchange rates are not included in a block. An attacker then exploits the situation by draining the network of its tokens.

## Recommendations
- **Short term:** Use a custom **CheckTx** method to prioritize oracle messages. This will help prevent validators’ votes from being left out of a block and ignored by an oracle.
- **Long term:** Ensure that operations that affect the whole system cannot be front-run or delayed by attackers or blocked by network congestion.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Umee |
| Report Date | N/A |
| Finders | Paweł Płatek, Dominik Czarnota |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf

### Keywords for Search

`vulnerability`

