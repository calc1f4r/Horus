---
# Core Classification
protocol: WalletConnect v2.0 SDK
chain: everychain
category: uncategorized
vulnerability_type: 1/64_rule

# Attack Vector Details
attack_type: 1/64_rule
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25931
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-walletconnectv2-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-walletconnectv2-securityreview.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - 1/64_rule

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Alex Useche
  - Emilio López
---

## Vulnerability Title

Insecure storage of session data in local storage

### Overview


Bug report summary: HTML5 local storage is vulnerable to XSS attacks, which can allow malicious actors to retrieve keychain data from dApps that support WalletConnect. To mitigate this, short-term solutions include using cookies to store and send tokens, and enabling CSRF libraries. Cookies must also be tagged with httpOnly and secure to ensure that JavaScript cannot access them. References include OWASP HTML5 Security Cheat Sheet and Trail of Bits.

### Original Finding Content

## Target: Browser storage

## Description
HTML5 local storage is used to hold session data, including keychain values. Because there are no access controls on modifying and retrieving this data using JavaScript, data in local storage is vulnerable to XSS attacks.

**Figure 4.1:** Keychain data stored in a browser’s localStorage

## Exploit Scenario
Alice discovers an XSS vulnerability in a dApp that supports WalletConnect. This vulnerability allows Alice to retrieve the dApp’s keychain data, allowing her to propose new transactions to the connected wallet.

## Recommendations
Short term, consider using cookies to store and send tokens. Enable cross-site request forgery (CSRF) libraries available to mitigate these attacks. Ensure that cookies are tagged with `httpOnly`, and preferably `secure`, to ensure that JavaScript cannot access them.

## References
- OWASP HTML5 Security Cheat Sheet: Local Storage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | TrailOfBits |
| Protocol | WalletConnect v2.0 SDK |
| Report Date | N/A |
| Finders | Alex Useche, Emilio López |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-walletconnectv2-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-walletconnectv2-securityreview.pdf

### Keywords for Search

`1/64 Rule`

