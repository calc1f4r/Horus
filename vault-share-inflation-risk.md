---
# Core Classification
protocol: Jito Restaking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46927
audit_firm: OtterSec
contest_link: https://www.jito.network/
source_link: https://www.jito.network/
github_link: https://github.com/jito-foundation/restaking

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
finders_count: 2
finders:
  - Robert Chen
  - Nicola Vella
---

## Vulnerability Title

Vault Share Inflation Risk

### Overview


This report discusses a vulnerability in a vault's mechanism that allows users to manipulate the effective share value of VRT tokens. This can happen after a vault has been slashed, resulting in a skewed ratio of VRT tokens to deposited tokens. This allows users to receive more VRT tokens than their deposit warrants, inflating their share of the vault without an increase in the overall asset value. The main risk is for the first depositor in a vault, who may lose the value of their initial deposit if later depositors exploit this vulnerability. To remedy this, a minimum deposit amount should be enforced to discourage malicious actors from exploiting the system. This issue has been resolved in a recent patch.

### Original Finding Content

## Vulnerability Overview

The vulnerability concerns the vault’s mechanism, particularly the updating of balance and share minting. By sending tokens to the vault and invoking the `UpdateVaultBalance`, a user may manipulate the effective share value associated with VRT tokens. If this action occurs after a vault has been slashed (when the total tokens deposited are significantly reduced), the ratio of VRT tokens to deposited tokens becomes skewed. This allows the user to receive disproportionately more VRT tokens relative to their deposit, inflating their share of the vault without a corresponding increase in the overall asset value.

## Primary Risk

The primary risk involves the first depositor in a vault. If the first depositor’s share value is not adequately protected against slashing, they can effectively lose the value of their initial deposit if later depositors take advantage of this inflation mechanism.

## Remediation

To address this vulnerability, enforce a minimum deposit amount to ensure that only significant deposits are made, thereby reducing the incentive for malicious actors to exploit the system through minimal deposits. The rounding amount may be refunded in `mint_with_fee`.

## Patch

Resolved in PR#150.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Jito Restaking |
| Report Date | N/A |
| Finders | Robert Chen, Nicola Vella |

### Source Links

- **Source**: https://www.jito.network/
- **GitHub**: https://github.com/jito-foundation/restaking
- **Contest**: https://www.jito.network/

### Keywords for Search

`vulnerability`

