---
# Core Classification
protocol: ZecWallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17338
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/zecwallet.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/zecwallet.pdf
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
finders_count: 5
finders:
  - 2019: Initial report delivered Final report delivered
  - Changelog April 12
  - 2019: May 7
  - John Dunlap
  - David Pokora
---

## Vulnerability Title

Wormhole server supports TLS 1.0 and 1.1

### Overview


This bug report is about the security of a Qt Wallet desktop and Android application. It is considered to be of medium difficulty. The issue is that the outdated encryption protocols TLS 1.0 and 1.1 are still being used, which can lead to a downgrade attack. This attack would allow an attacker to strip the connection of its transport security, thus exposing the user's data and leading to compromise. 

To fix this issue, the short term solution is to remove support for TLS 1.0 and 1.1. The long term solution is to always ensure that only the most recent versions of TLS are enabled. This will prevent downgrade attacks and other similar attacks against users of the service. 

References for this bug report include SSL and TLS Deployment Best Practices.

### Original Finding Content

## Type: Cryptography
**Target:** Qt Wallet desktop, Android

**Difficulty:** Medium

## Description
TLS 1.0 and 1.1 are not considered to be modern, up-to-date encryption protocols and may facilitate downgrade attacks resulting in the loss of confidentiality. As both TLS 1.0 and 1.1 are deprecated, they should never be made available to users.

## Exploit Scenario
Alice connects to the wormhole server using an out-of-date Android device which only supports TLS 1.0. Eve notices and proceeds to launch a downgrade attack against Alice, stripping her connection of transport security. Alice’s data is exposed to Eve, leading to compromise.

## Recommendation
- **Short term:** Remove support for TLS 1.0 and 1.1.
- **Long term:** Always ensure that only the most recent cipher suites and versions of TLS are enabled. This will ensure that downgrade attacks and the like cannot be carried out against users of the wormhole service.

## References
- SSL and TLS Deployment Best Practices  
- ZecWallet Product Assessment | 41

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | ZecWallet |
| Report Date | N/A |
| Finders | 2019: Initial report delivered Final report delivered, Changelog April 12, 2019: May 7, John Dunlap, David Pokora |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/zecwallet.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/zecwallet.pdf

### Keywords for Search

`vulnerability`

