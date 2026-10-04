---
# Core Classification
protocol: Tezos Crypto Wallets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18065
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/MagmaWallet.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/MagmaWallet.pdf
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
finders_count: 2
finders:
  - Android findings
  - Artur Cygan | ​Trail of Bits Added new iOS
---

## Vulnerability Title

Server lacks OCSP stapling

### Overview


This bug report is about a data exposure vulnerability in the Sentry SDK for iOS and Android. The issue is that the servers do not return the SSL certificate's revocation status via OCSP Stapling, which is a feature that provides clients with the ability to detect whether the server's SSL certificate has been revoked. Apple recommends that OCSP Stapling should be implemented on all mobile endpoints, meaning that it will become a requirement for iOS Apps on the App Store. 

Exploit Scenario: If someone (Alice) gains access to a server using its shared wildcard SSL certificate, compromising the certificate’s private key, clients will continue to allow connections to any server with the certificate—even ones hosted by Alice—because there is no OCSP Stapling. 

Recommendations: To address the issue, Sentry should update all Magma servers and mobile clients to enable support for OCSP Stapling in the short term. In the long term, Sentry should perform certificate revocation exercises to ensure that the protections are sufficient, as well as to train staff on how to react to a compromised SSL credential.

### Original Finding Content

## Data Exposure Report

**Type:** Data Exposure  
**Target:** Sentry SDK in iOS and Android  

**Difficulty:** High  

## Description
The affected servers do not return its SSL certificate’s revocation status via **OCSP Stapling**. This feature provides clients with the ability to detect whether the server’s SSL certificate has been revoked. Apple recommends that OCSP Stapling should be implemented on all mobile endpoints. This implies that OCSP Stapling will become a requirement for iOS Apps on the App Store.

## Exploit Scenario
Alice gains access to a server using its shared wildcard SSL certificate, compromising the certificate’s private key. Even if Tezos revokes the compromised certificate, clients will continue to allow connections to any server with the certificate— even ones hosted by Alice—because there is no OCSP Stapling.

## Recommendation
- **Short term:** Update all Magma servers and mobile clients to enable support for OCSP Stapling.
- **Long term:** Perform certificate revocation exercises to ensure that the protections are sufficient, as well as to train staff on how to react to a compromised SSL credential.

## References
- Apple WWDC 2017: [Your Apps and Evolving Network Security Standards](https://developer.apple.com/videos/play/wwdc2017/10067/)
- Apache SSL/TLS Strong Encryption: [OCSP Stapling](https://httpd.apache.org/docs/current/mod/mod_ssl.html#ocspstapling)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Tezos Crypto Wallets |
| Report Date | N/A |
| Finders | Android findings, Artur Cygan | ​Trail of Bits Added new iOS |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/MagmaWallet.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/MagmaWallet.pdf

### Keywords for Search

`vulnerability`

