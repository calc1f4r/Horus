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
solodit_id: 17339
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

Failure to use platform encryption

### Overview


This bug report is about a cryptography issue in the Qt Wallet desktop, Android, and Wormhole applications. The data at rest in these applications is stored without using platform encryption, which is a high difficulty issue. This means that the highly sensitive financial data stored in the applications is not protected from tampering or abuse, as there are no tools such as MacOS keychain or Windows certificate store being used. Without these tools, local attackers will have easy access to sensitive data. 

The exploit scenario is that an attacker, Eve, has access to an unlocked workstation and is able to take advantage of the unsecured private keys on the workstation to compromise Alice's wallet. 

The recommendation is to implement file system encryption on all sensitive data that rests on the system in the short term, and to move all sensitive data to the strongest secure possible on each platform in the long term. For example, use the MacOS keychain for MacOS systems.

### Original Finding Content

## Cryptography Report

**Type:** Cryptography  
**Target:** Qt Wallet desktop, Android, and Wormhole  

**Difficulty:** High  

## Description
Data at rest is stored without using platform encryption. Tools such as the MacOS keychain or the Windows certificate store are not used to protect the highly sensitive financial data contained by this application from tampering and abuse. Data is instead stored in flat files, or in local databases without any protection.

Keychains, hardware security modules, and trusted platform modules are designed in order to prevent sensitive data from being accessed by attackers. Without them, local attackers will have easy access to sensitive data.

## Exploit Scenario
Alice walks away from her unlocked workstation to have lunch. Eve approaches the unlocked workstation and takes advantage of the large number of unsecured private keys on the workstation to compromise Alice’s wallet.

## Recommendation
- **Short term:** Implement file system encryption on all sensitive data that rests on the system.
- **Long term:** Move all sensitive data to the strongest secure possible on each platform. For instance, use the MacOS keychain for MacOS systems.

## References
- Keychain Services  
- ZecWallet Product Assessment | 42

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

