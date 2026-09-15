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
solodit_id: 52612
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

HAL-23 - API - LACK OF RATE LIMITATION ON SSP RELAY ENDPOINTS

### Overview


This report discusses a bug found in the SSP Relay server, which is used to help the SSP Wallet and SSP Key communicate with each other. The bug involves the absence of rate-limiting on critical endpoints, which could potentially make them vulnerable to denial-of-service or brute-force attacks. The recommendation is to implement rate limiting to prevent abuse or attacks, and the issue has since been resolved by the InFlux Technologies team. 

### Original Finding Content

##### Description

The SSP Relay server facilitates communication between the SSP Wallet and SSP Key by relaying requests for synchronization, signing, and other wallet operations. The SSP Wallet can function offline, and critical wallet operations, including signing transactions and synchronizing keys, can be completed without relying on the SSP Relay server. This reduces the reliance on the relay server, minimizing the potential impact of abuse. However, despite the reduced risk, the absence of rate-limiting leaves the endpoints theoretically susceptible to denial-of-service (DoS) or brute-force attacks, potentially impacting availability.

##### Proof of Concept

![](https://halbornmainframe.com/proxy/audits/images/677fdc7f6287e28dcdbb4374)![rate-limit-2.jpg](https://halbornmainframe.com/proxy/audits/images/677fdc8c6287e28dcdbb4377)

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

Implementing rate limiting on critical SSP Relay endpoints is still recommended to prevent potential abuse or denial-of-service attacks. Applying a reasonable request rate limit (e.g., X requests per minute per IP or per wallet identity) can help mitigate the risk of endpoint overloading.

##### Remediation

**SOLVED:** The **InFlux Technologies team** resolved the issue by implementing the rate limitation protection.

##### Remediation Hash

a17bd2596fb89c3a851b6ff8dab334055895031f

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

