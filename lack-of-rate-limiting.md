---
# Core Classification
protocol: Adena Wallet Chrome Extension
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52671
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/onbloc/adena-wallet-chrome-extension
source_link: https://www.halborn.com/audits/onbloc/adena-wallet-chrome-extension
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

LACK OF RATE LIMITING

### Overview


The report describes a vulnerability in an API that can be exploited by sending too many requests at the same time. This can cause the API to become unresponsive or use up too many resources. The report also includes a proof of concept and a recommendation to implement request throttling to prevent this vulnerability. The issue has been resolved by the Onbloc team.

### Original Finding Content

##### Description

API requests consume resources such as network, CPU, memory, and storage. This vulnerability occurs when too many requests arrive simultaneously, and the API does not have enough compute resources to handle those requests.

During the assessment, no rate limitation policy was found on the API service. An attacker could exploit this vulnerability to overload the API by sending more requests than it can handle. As a result, the API becomes unavailable or unresponsive to new requests, or resources of bandwidth and CPU usage could be abused as well.

##### Proof of Concept

During the assessment, some example interesting endpoints where found allowing multiple parallel requests (**POST** HTTP request to [**https://test5.api.onbloc.xyz/v1/gno**](https://test5.api.onbloc.xyz/v1/gno)):

![Endpoint allowing multiple requests](https://halbornmainframe.com/proxy/audits/images/67979aa7c1f69dd5c66ee1cc)

##### Score

Impact: 3  
Likelihood: 4

##### Recommendation

This vulnerability is due to the application accepting requests from users at a given time without performing request throttling checks. It is recommended to follow the following best practices:

* Implement a limit on how often a client can call the API within a defined timeframe.
* Notify the client when the limit is exceeded by providing the limit number and the time the limit will be reset.

##### Remediation

**SOLVED:** The **Onbloc team** solved this finding.

##### Remediation Hash

<https://github.com/onbloc/onbloc-api-v2/pull/23/files>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Adena Wallet Chrome Extension |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/onbloc/adena-wallet-chrome-extension
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/onbloc/adena-wallet-chrome-extension

### Keywords for Search

`vulnerability`

