---
# Core Classification
protocol: NashPoint
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53054
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/16ca9765-fc97-471e-aece-ef52f5bbc877
source_link: https://cdn.cantina.xyz/reports/cantina_nashpoint_january_2025.pdf
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
finders_count: 3
finders:
  - Jonatas Martins
  - Kurt Barry
  - Gerard Persoon
---

## Vulnerability Title

Missing validation for ERC-7540 asynchronous functionality interfaces 

### Overview

See description below for full details.

### Original Finding Content

## Context
- **BaseRouter.sol**: Lines 68-89
- **QuoterV1.sol**: Line 64
- **QuoterV1.sol**: Line 260

## Description
According to the EIP-7540 documentation, vaults can optionally implement asynchronous flows for deposits and redemptions. If a vault doesn’t implement asynchronous deposits, calls to `pendingDepositRequest` and `claimableDepositRequest` will revert.

## Recommendation
Consider validating vault interfaces using `ERC165.supportsInterface()`:
- `type(IERC7540Redeem).interfaceId == 0x620ee8e4` == Asynchronous redemption
- `type(IERC7540Deposit).interfaceId == 0xce3bbe50` == Asynchronous deposit

Add these checks to either `BaseRouter::setWhitelistStatus()` / `BaseRouter::batchSetWhitelistStatus()` or `Quoter::setErc7540()` to ensure proper router type selection and component compatibility. As this check is specific for the type of vault, it’s best to implement the check itself in the related router.

## NashPoint
Acknowledged.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | NashPoint |
| Report Date | N/A |
| Finders | Jonatas Martins, Kurt Barry, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_nashpoint_january_2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/16ca9765-fc97-471e-aece-ef52f5bbc877

### Keywords for Search

`vulnerability`

