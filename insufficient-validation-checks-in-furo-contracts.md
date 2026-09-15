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
solodit_id: 19597
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

Insufficient Validation Checks in Furo Contracts

### Overview

See description below for full details.

### Original Finding Content

## Description

This is a list of parameter checks that appear to be missing and may benefit the contract if added.

- **FuroStream.createStream()**
  - amount has no zero check.
  - recipient has no zero check.
  - token has no zero check.
  
- **FuroStream.withdrawFromStream()**
  - sharesToWithdraw has no zero check and will proceed to make external calls and create events.
  
- **FuroVesting.updateSender()**
  - sender has no zero address check.
  
- **FuroVesting.updateStream()**
  - topUpAmount and extendTime have no zero check: both could be zero at the same time.
  
- **FuroVesting.createVesting()**
  - stepDuration has no zero check; if it is zero, `_balanceOf()` will divide by zero causing deposited funds to be locked.
  - steps has no zero check.
  
- **FuroVesting.withdraw()**
  - If `canClaim == 0` on line [109], consider returning instead of making external calls and creating events.
  
- **FuroVesting.updateOwner()**
  - newOwner has no zero address check.

## Recommendations

Review the issues above and consider implementing fixes to them.

## Resolution

The development team has reviewed and acknowledged the issue. Some of the recommendations have been implemented.

- **FuroVesting.createVesting()**
  - stepDuration and steps have zero checks.
  
- **FuroVesting.withdraw()**
  - If `canClaim == 0` on line [109], the function now returns zero.

This is shown in PR 17.

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

