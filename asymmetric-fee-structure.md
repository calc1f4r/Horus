---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40976
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/53e12fbd-182a-45f9-a115-55fdea33c5c4
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_dss-lite-psm_oct2023.pdf
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
  - m4rio
  - shung
  - Christoph Michel
---

## Vulnerability Title

Asymmetric fee structure 

### Overview

See description below for full details.

### Original Finding Content

## DssLitePsm.sol

## Description
`buyGem()` adds fees on top of the input token while `sellGem()` removes the fees from the output token. This is an asymmetric design in which the same values of `tin` and `tout` represent slightly different fees.

For example, assume 10% wad is set for both `tin` and `tout`:
- **sellGem()**: Selling 100 gem gets 90 dai with fee and 100 dai without fee.
- **buyGem()**: Selling 100 dai gets ~90.9 gem with fee and 100 gem without fee.

## Recommendation
Due to the system working with the expectation that fees are always collected from dai, no change is recommended. However, governance should be aware of this asymmetric behaviour when setting `tin` and `tout` fees.

## Maker DAO
Acknowledged. This is by design, and it's already the mechanism in place for the existing version. Collecting fees in Dai makes it easier for the protocol to incorporate them, as any other token would have to be converted to Dai before being incorporated into the surplus buffer.

## Cantina Managed
Acknowledged.

## Additional Comments
The Cantina team reviewed MakerDao’s dss-lite-psm changes holistically on commit hash `3ec57f35fdd910ab765379c324a4dc2a7c08d54a` and determined that all issues were acknowledged and no new issues were identified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, shung, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_dss-lite-psm_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/53e12fbd-182a-45f9-a115-55fdea33c5c4

### Keywords for Search

`vulnerability`

