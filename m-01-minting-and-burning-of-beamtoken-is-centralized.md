---
# Core Classification
protocol: Beam
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27256
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-10-01-Beam.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Minting and burning of `BeamToken` is centralized

### Overview


This bug report addresses the potential for malicious or compromised admin/minter/burner accounts to endlessly inflate the token supply or burn any user's token balance on the BeamToken platform. This would result in a high impact for users, as they would stand to lose their funds. The likelihood of this happening is low, as it requires malicious or compromised accounts. 

The report recommends that the `mint` and `burn` methods in `BeamToken` be controlled by contracts that have a Timelock mechanism, which would give users enough time to exit their positions if they disagree with a transaction of the admin/minter/burner. This would help protect users from potential losses due to malicious or compromised accounts.

### Original Finding Content

**Severity**

**Impact:**
High, as token supply can be endlessly inflated and user tokens can be burned on demand

**Likelihood:**
Low, as it requires a malicious or compromised admin/minter/burner

**Description**

Currently the `mint` and `burn` methods in `BeamToken` are controlled by `MINTER_ROLE` and `BURNER_ROLE` respectively. Those roles are controlled by the `DEFAULT_ADMIN_ROLE` which is given to the `BeamToken` deployer. This means that if the admin or minter or burner account is malicious or compromised it can decide to endlessly inflate the token supply or to burn any user's token balance, which would lead to a loss of funds for users.

**Recommendations**

Give those roles only to contracts that have a Timelock mechanism so that users have enough time to exit their `BeamToken` positions if they decide that they don't agree with a transaction of the admin/minter/burner.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Beam |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-10-01-Beam.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

