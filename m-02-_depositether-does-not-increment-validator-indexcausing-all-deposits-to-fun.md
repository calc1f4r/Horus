---
# Core Classification
protocol: Mystic Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57716
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Mystic Finance.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.90
financial_impact: medium

# Scoring
quality_score: 4.5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Kann
---

## Vulnerability Title

[M-02] _depositEther Does Not Increment Validator Index,Causing All Deposits to Funnel Into First Validator and Fail Once Full

### Overview


The report states that there is a bug in the stPlumeMinter contract, specifically in the _depositEther() function. This function is responsible for distributing incoming ETH deposits to available validators. However, there is an issue where the function is stuck in a loop, constantly evaluating the same validator and preventing it from progressing to the next one. This means that deposits are not being properly staked and users are not receiving yield-bearing tokens. The team has acknowledged and fixed the issue.

### Original Finding Content

## Severity

Medium

## Description

In the stPlumeMinter contract, the _depositEther() function is responsible for distributing incoming ETH deposits across available validators. This function loops through the validator set
to find suitable validators with enough capacity to stake the deposited ETH.
However, there is a critical issue: the index variable, initialized to 0, is never incremented inside the
while loop. As a result, the loop evaluates the same validator (validators[0]) in every iteration, preventing the function from ever progressing to the next validator in the list.
When the first validator reaches its staking capacity or becomes inactive, the getNextValidator() function
returns a capacity of 0. Since depositSize < minStakeAmount in such cases, the full remaining
amount is stored in the currentWithheldETH variable. This means the user’s deposit is held back and
never actually staked, despite the user receiving yield-bearing tokens.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4.5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Kann |
| Protocol | Mystic Finance |
| Report Date | N/A |
| Finders | Kann |

### Source Links

- **Source**: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/Mystic Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

