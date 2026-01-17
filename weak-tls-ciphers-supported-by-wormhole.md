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
solodit_id: 17337
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

Weak TLS ciphers supported by wormhole

### Overview


This bug report is about the configuration of the Wormhole TLS server. It has been identified as having a medium difficulty level. The server supports weak SSL ciphers which are deemed insufficient for modern transport security. These ciphers include TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_256_GCM_SHA384, TLS_RSA_WITH_AES_128_CBC_SHA256, TLS_RSA_WITH_AES_256_CBC_SHA256, TLS_RSA_WITH_AES_128_CBC_SHA, and TLS_RSA_WITH_AES_256_CBC_SHA, all of which have a safety rating of WEAK. In addition, the server allows connections from outdated devices and browsers, such as Android 2.3.7, Android 4.0.4, Android 4.1.1, Android 4.2.2, Android 4.3, Android 4.4.2, and IE7.

The exploit scenario is that Alice connects to the Wormhole server using an out of date Android device which only supports insufficient ciphers. Eve notices this and uses a cryptographic attack to compromise the transport encryption, revealing Alice's confidential data.

The recommendation is to disable all TLS ciphers listed above in the short term, and to always ensure that only the most recent cipher suites and versions of TLS are enabled in the long term. This will ensure that downgrade attacks and the like cannot be carried out against users of the Wormhole service. References to SSL and TLS Deployment Best Practices are included.

### Original Finding Content

## Type: Configuration
## Target: Wormhole TLS

### Difficulty: Medium

### Description
The wormhole server supports the following weak SSL ciphers which have been deemed to be insufficient for modern transport security:

| Cipher                                         | Mode | Safety Rating | Key Size |
|------------------------------------------------|------|---------------|----------|
| TLS_RSA_WITH_AES_128_GCM_SHA256 (0x9c)       |      | WEAK          | 128      |
| TLS_RSA_WITH_AES_256_GCM_SHA384 (0x9d)       |      | WEAK          | 256      |
| TLS_RSA_WITH_AES_128_CBC_SHA256 (0x3c)       |      | WEAK          | 128      |
| TLS_RSA_WITH_AES_256_CBC_SHA256 (0x3d)       |      | WEAK          | 256      |
| TLS_RSA_WITH_AES_128_CBC_SHA (0x2f)           |      | WEAK          | 128      |
| TLS_RSA_WITH_AES_256_CBC_SHA (0x35)           |      | WEAK          | 256      |

Additionally, connections from the following outdated devices and browsers are allowed by the server:
- Android 2.3.7
- Android 4.0.4
- Android 4.1.1
- Android 4.2.2
- Android 4.3
- Android 4.4.2
- IE7

### Exploit Scenario
Alice connects to the wormhole server using an out-of-date Android device which only supports insufficient ciphers. Eve notices and uses a cryptographic attack to compromise the transport encryption, revealing Alice’s confidential data.

### Recommendation
Short term, disable all TLS ciphers listed above.

Long term, always ensure that only the most recent cipher suites and versions of TLS are enabled. This will ensure that downgrade attacks and the like cannot be carried out against users of the wormhole service.

### References
- SSL and TLS Deployment Best Practices

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

