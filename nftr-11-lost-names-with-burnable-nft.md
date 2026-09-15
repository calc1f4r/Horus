---
# Core Classification
protocol: Nftr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26734
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-07-27-NFTR.md
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
  - Guardian Audits
---

## Vulnerability Title

NFTR-11 | Lost Names With Burnable NFT

### Overview


A bug has been reported regarding the NFTR protocol which allows users to register a special name for their ERC721-compliant burnable NFT. If the user then proceeds to burn their NFT, the special name is lost as ownership is relinquished and it cannot be changed or transferred. It is recommended that a function be added so that if an owner does not exist for a particular NFT, then that NFT’s registered name can be dereserved. The NFTR Team has determined that this is expected behavior and no further action is needed.

### Original Finding Content

**Description**

Consider the scenario where a user registers a special name for their ERC721-compliant burnable NFT. They then proceed to burn their NFT, and ownership is relinquished. As a result, the name of the NFT cannot be changed nor transferred. The special name, a coveted asset to the NFTR protocol, is now lost.

**Recommendation**

Consider whether or not this is expected behavior. If unexpected, add a function so that if an owner does not exist for a particular NFT, then that NFT’s registered name can be dereserved.

**Resolution**

NFTR Team:

- This is expected behavior.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Nftr |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-07-27-NFTR.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

