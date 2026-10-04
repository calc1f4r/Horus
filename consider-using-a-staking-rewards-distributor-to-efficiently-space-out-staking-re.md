---
# Core Classification
protocol: Syntetika
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62222
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - Jorge
---

## Vulnerability Title

Consider using a staking rewards distributor to efficiently space out staking rewards, further deterring just-in-time attacks

### Overview

See description below for full details.

### Original Finding Content

**Description:** Consider using a [staking rewards distributor](https://github.com/ethena-labs/bbp-public-assets/blob/main/contracts/contracts/StakingRewardsDistributor.sol) to efficiently space out staking rewards instead of depositing a large amount in one transaction.

The current code uses a post-withdraw cooldown to deter "just in time" yield attacks where a user front-runs a call to `StakingVault::distributeYield` by depositing a large amount then staking it to get a large amount of the yield.

However this attack can still be executed just that the user must then wait for the cooldown to withdraw which can be as long as 90 days. The cooldown can be set by the admin as low as zero though which would enable "just in time" attacks.

Another option is to perform calls to `StakingVault::distributeYield` via [services](https://docs.flashbots.net/flashbots-protect/overview) designed to prevent front-running.

**Syntetika:**
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Syntetika |
| Report Date | N/A |
| Finders | Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

