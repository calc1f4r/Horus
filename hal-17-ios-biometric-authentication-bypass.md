---
# Core Classification
protocol: SSP Wallet, Relay and Key
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52589
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/influx-technologies/ssp-wallet-relay-and-key
source_link: https://www.halborn.com/audits/influx-technologies/ssp-wallet-relay-and-key
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
  - Halborn
---

## Vulnerability Title

HAL-17 - iOS - BIOMETRIC AUTHENTICATION BYPASS

### Overview


This bug report discusses a vulnerability found in an application that uses biometric authentication, such as Touch ID or Face ID. The report explains how the vulnerability can be exploited using a tool called Objection, which can manipulate the fingerprint reading function to bypass the biometric authentication. The report also provides a proof of concept video and a recommendation for the developers to implement anti-hook and anti-debug protections, custom jailbreak detection, and runtime code obfuscation to prevent similar vulnerabilities in the future. The issue has been addressed by the InFlux Technologies team.

### Original Finding Content

##### Description

The application utilizes biometric authentication mechanisms, including older Touch ID and Face ID technologies, for authentication purposes. These mechanisms are often perceived as robust, leveraging the uniqueness of biometric data like fingerprints. However, vulnerabilities in local authentication implementations can undermine this trust.

Biometric authentication works by validating users locally with stored device credentials, such biometric data (face or fingerprint). This ensures secure and convenient access to app functionality, either by resuming a session with a remote service or performing step-up authentication for sensitive operations.

In this application, a bypass was identified using the Objection framework, which exploits the application’s reliance on the native fingerprint evaluation API. Specifically, Objection was used to manipulate the response of the fingerprint reading function (evaluatePolicy) to return a successful authentication result, even when the biometric validation had failed.

##### Proof of Concept

`Objection` shared overrides the return of the `evaluatePolicy` function so that it returns **True** even if the authentication was unsuccessful.

**Video:** [[](https://halborn.zoom.us/clips/share/8djM8N8nFwz4UfJYOQCOweJWQQMu-oehvy4oQKmg6MOBdJqcbuTlGKJAMc5JgFcLYFj-fvBh.Aq9eg9S9yr4OiZMj)[Proof of concept](https://halborn.zoom.us/clips/share/A2F3MRY0ZW5pOWtma1I5V1FHRWNCRGx3ekpnAQ)[]](https://halborn.zoom.us/clips/share/8djM8N8nFwz4UfJYOQCOweJWQQMu-oehvy4oQKmg6MOBdJqcbuTlGKJAMc5JgFcLYFj-fvBh.Aq9eg9S9yr4OiZMj)

##### Score

Impact: 4  
Likelihood: 2

##### Recommendation

1. **Anti-Hook and Anti-Debug Protections**

• Implement runtime checks to detect and prevent hooking and debugging attempts using frameworks like Frida.

• Adopt the IOSSecuritySuite, an open-source solution offering anti-hook, anti-debug, and jailbreak detection functionalities.

Repository: [IOS Security Suite](https://github.com/securing/IOSSecuritySuite)

2. **Custom Jailbreak Detection**

• Incorporate additional checks tailored to your application to identify and mitigate tampering or execution on jailbroken devices.

3. **Runtime Code Obfuscation**

• Use runtime obfuscation tools to make reverse engineering and tampering attempts more challenging.

##### Remediation

**SOLVED:** The **InFlux Technologies team** addressed the issue by implementing checks against the identified risk.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | SSP Wallet, Relay and Key |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/influx-technologies/ssp-wallet-relay-and-key
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/influx-technologies/ssp-wallet-relay-and-key

### Keywords for Search

`vulnerability`

