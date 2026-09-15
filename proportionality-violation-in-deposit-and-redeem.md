---
# Core Classification
protocol: Plume Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53274
audit_firm: OtterSec
contest_link: https://plumenetwork.xyz/
source_link: https://plumenetwork.xyz/
github_link: https://github.com/plumenetwork/contracts

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
finders_count: 3
finders:
  - Nicholas R. Putra
  - Robert Chen
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Proportionality Violation in Deposit and Redeem

### Overview


The YieldToken platform has a bug where the expected relationship between assets and shares is not being followed. When users deposit assets, the number of shares minted is always the maximum value, regardless of the amount of assets deposited. This means that the number of shares a user owns does not accurately reflect the amount of assets they have deposited. Similarly, when redeeming shares, the assets transferred are determined by the maximum value stored, rather than being calculated based on the proportionality of shares. This means that users cannot trust the platform to fairly distribute assets based on ownership. The bug has been fixed in the latest patch.

### Original Finding Content

## YieldToken Issues with Proportionality

In YieldToken, the expected logic of proportionality between assets and shares is violated. In the deposit process, regardless of the assets that are passed by the user, the number of shares minted is the maximum number stored in the `$.sharesDepositRequest[controller]` mapping. The value in `$.sharesDepositRequest` does not dynamically compute proportionality based on assets. Instead, it is treated as a static pre-set value.

Similarly, in the redeem process, regardless of the shares passed by the user, the assets transferred are determined by the maximum stored in `$.assetsRedeemRequest[controller]`, rather than being calculated based on the proportionality of shares. Thus, share ownership no longer reflects the actual amount of underlying assets deposited, and users will be unable to trust the vault to fairly distribute assets based on ownership.

## Remediation

Ensure that the number of minted shares reflects the proportion of assets deposited relative to the vault’s current total assets and shares, and the number of assets redeemed reflects the proportion of shares burned relative to the total vault shares.

## Patch

Resolved in `4f16028`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Plume Network |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://plumenetwork.xyz/
- **GitHub**: https://github.com/plumenetwork/contracts
- **Contest**: https://plumenetwork.xyz/

### Keywords for Search

`vulnerability`

