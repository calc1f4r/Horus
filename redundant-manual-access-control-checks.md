---
# Core Classification
protocol: Symbiotic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64350
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
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
finders_count: 4
finders:
  - 0kage
  - Aleph-v
  - ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3
  - Farouk
---

## Vulnerability Title

Redundant manual access control checks

### Overview

See description below for full details.

### Original Finding Content

**Description:** In both `BaseRewards` and `BaseSlashing` contracts, functions perform manual access control checks (`_checkRewarder` and `_checkSlasher`) instead of using the already-defined `onlyRewarder` and `onlySlasher` modifiers. Specifically:

* `distributeStakerRewards` and `distributeOperatorRewards` in `BaseRewards`

* `slashVault` and `executeSlashVault` in `BaseSlashing`

This inconsistency reduces code readability and increases the risk of missing or duplicating access control logic in the future.

**Recommended Mitigation:** Replace manual `_checkRewarder` and `_checkSlasher` calls with their corresponding modifiers for cleaner and more consistent access control enforcement:

```solidity
function distributeStakerRewards(...) public virtual onlyRewarder { ... }

function distributeOperatorRewards(...) public virtual onlyRewarder { ... }

function slashVault(...) public virtual onlySlasher returns (...) { ... }

function executeSlashVault(...) public virtual onlySlasher returns (...) { ... }
```

This ensures access checks are declarative, standardized, and easier to maintain.

**Symbiotic:** Acknowledged. Intended to decrease bytecode size.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Symbiotic |
| Report Date | N/A |
| Finders | 0kage, Aleph-v, ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

