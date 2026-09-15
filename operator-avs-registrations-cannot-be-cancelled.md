---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53722
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Operator AVS Registrations Cannot Be Cancelled

### Overview

See description below for full details.

### Original Finding Content

## Description
EigenLayer Operators are able to provide a signature with a corresponding salt and expiry to an AVS in order to link the AVS and Operator. If an operator accidentally provides a signature to the wrong AVS this signature cannot be cancelled, and is valid until expiry < block.timestamp. Though currently AVS cannot directly slash operators, the state of AVS slashing is not known. However, the risk of unintentional distribution of signature and salts may increase significantly and unexpectedly if AVS obtain the ability to slash.

## Recommendations
- Add functionality to be able to cancel distributed signatures and salts that may have been provided unintentionally.

## Resolution
AVS registration functionality has been moved to the AVSDirectory contract. The `cancelSalt()` function was added to allow an operator to cancel an AVS registration with a specific salt. This issue has been addressed in PR #434.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf

### Keywords for Search

`vulnerability`

