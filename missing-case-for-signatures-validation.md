---
# Core Classification
protocol: Chainport
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35587
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-24-ChainPort.md
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
  - Zokyo
---

## Vulnerability Title

Missing case for signatures validation.

### Overview


The bug report is about a function called "verifySignature()" in a file called "Validator.sol". The function is supposed to check if the signer's address matches the signatory address. However, the signatory address is not checked before deployment, so it could be set to a zero address, which would allow for invalid signatures. The severity of this bug is marked as low because it is expected to be used during upgrades of valid contracts, but it could still cause issues during redeployments on different networks or versions. The recommendation is to add a check to make sure the signatory address is not set to a zero address either during initialization or in the function itself. After the audit, the Chainport team confirmed that the deployment process includes a check for the signatory address, but it was only added during initialization.

### Original Finding Content

**Severity**: Low

**Status**: Resolved 

**Description**

Validator.sol, verifySignature()

The function recovers the signer from the signature and compares it with the signatory
address. However, the signaioryAddress is not validated during the deployment and may
appear to be zero address, allowing invalid signatures.

The issue is marked as Low, as auditors recognize, that the functionality is expected to be
used during the upgrade of current valid contracts. However the issue may appear during
the redeployments on other networks or protocol versions.

**Recommendation:**

Add the check that the signatoryAddress is not zero address (either into the initializer or into
the function)

**Post audit.**

The Chainport team verified, that the deployment procedure include checksum scripts which
ensure the signatory was properly updated. Though the check was added into the initialized.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Chainport |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-24-ChainPort.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

