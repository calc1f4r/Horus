---
# Core Classification
protocol: Newwit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21000
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2022-10-19-Newwit.md
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
finders_count: 1
finders:
  - AuditOne
---

## Vulnerability Title

Basic validation missing on `mint`and `mintTo`

### Overview

See description below for full details.

### Original Finding Content

**Description:** 

Observe that both `mint`and `mintTo`functions are missing basic validation for `to`address,amount/quantity.

**Recommendations:** 

Add below to mint &mintTo function at ERC20Token.sol

\```

require(to!=address(0)&&amount>0,""Incorrect params"");

\```

Add below to mint &mintTo function at ERC721ACollection.sol

\```

require(quantity>0 &&to!=address(0),""Incorrect params"");// for mintTo require(quantity>0,""Incorrect params"");// for mint

\```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Newwit |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2022-10-19-Newwit.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

