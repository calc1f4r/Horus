---
# Core Classification
protocol: Governance & Timelock Updates
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50145
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/moonwell/governance-timelock-updates-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/moonwell/governance-timelock-updates-smart-contract-security-assessment
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

TIMELOCK DELAY IS SET TO ZERO IN THE CONSTRUCTOR

### Overview


Issue: The timelock delay is set to zero in the constructor, which means that proposals can bypass the timelock and cause inconsistency.

Impact: The impact of this bug is moderate, with a score of 3 out of 5.

Likelihood: The likelihood of this bug occurring is also moderate, with a score of 3 out of 5.

Recommendation: The Moonwell Team has solved this issue by setting the delay function. The commit ID for the solution is 4e8bec5926339106c225d0f85120ba182e52f2dd.

### Original Finding Content

##### Description

The timelock delay is set to zero in the constructor. That can cause inconsistency in the proposals, and each proposal can bypass the timelock.

Code Location
-------------

#### Timelock.sol

```
    constructor(address admin_, uint delay_) public {
        require(delay_ >= MINIMUM_DELAY, "Timelock::constructor: Delay must exceed minimum delay.");
        require(delay_ <= MAXIMUM_DELAY, "Timelock::setDelay: Delay must not exceed maximum delay.");
        admin = admin_;
        delay = 0;
    }

```

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED:** The `Moonwell Team` solved this issue by setting the **delay** function.

`Commit ID:` [4e8bec5926339106c225d0f85120ba182e52f2dd](https://github.com/moonwell-fi/contracts-open-source/commit/4e8bec5926339106c225d0f85120ba182e52f2dd)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Governance & Timelock Updates |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/moonwell/governance-timelock-updates-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/moonwell/governance-timelock-updates-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

