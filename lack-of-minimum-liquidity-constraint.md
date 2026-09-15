---
# Core Classification
protocol: Solend Steamm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53241
audit_firm: OtterSec
contest_link: https://save.finance/
source_link: https://save.finance/
github_link: https://github.com/solendprotocol/steamm

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Michał Bochnak
  - Robert Chen
  - Sangsoo Kang
---

## Vulnerability Title

Lack of Minimum Liquidity Constraint

### Overview


The report states that there is a bug in the bank module where there is no minimum requirement for liquidity, which can make it vulnerable to attacks that manipulate the value of bToken. This can result in a loss for users who deposit. The suggested solution is to enforce a minimum liquidity requirement in the bank module to prevent these attacks. This bug has been fixed in version 6e17d4f.

### Original Finding Content

## Bank Module Liquidity Concerns

The bank module does not have any constraints on the minimum amount of liquidity that should be present at all times. Insufficient minimum liquidity may expose it to inflation attacks, enabling malicious actors to manipulate the value of bToken. 

For example, if the value of bToken exceeds a 1:1 ratio, burning bToken and increasing the amount of the underlying token can trigger zero mint when a user deposits, causing a loss for the user.

## Remediation

Enforce a minimum liquidity requirement in the bank to prevent inflation attacks.

## Patch

Resolved in `6e17d4f`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Solend Steamm |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen, Sangsoo Kang |

### Source Links

- **Source**: https://save.finance/
- **GitHub**: https://github.com/solendprotocol/steamm
- **Contest**: https://save.finance/

### Keywords for Search

`vulnerability`

