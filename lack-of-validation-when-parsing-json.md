---
# Core Classification
protocol: Chromium Browser Extension
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52217
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/zkpass/chromium-browser-extension
source_link: https://www.halborn.com/audits/zkpass/chromium-browser-extension
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

Lack of Validation When Parsing JSON

### Overview


This bug report warns that parsing JSON data without validation can lead to malicious or malformed data being processed, which can result in injection attacks or unexpected behavior. The report specifically mentions a vulnerability in the `jsonParse.ts` file, where JSON data from responses were not validated before being parsed. This makes the application vulnerable to manipulation through malicious JSON inputs. The proof of concept code provided in the report shows how the vulnerability can be exploited. The impact of this bug is rated as 4 out of 5, with a likelihood of 2 out of 5. The recommendation is to implement validation and sanitization checks when parsing JSON data, especially when working with untrusted input or external sources. The remediation plan mentioned that the team has accepted the risk and will only validate the legality of the JSON properties and structure. 

### Original Finding Content

##### Description

Parsing JSON without validation can lead to the processing of malicious or malformed data, which may result in injection attacks or unexpected behavior.

In `jsonParse.ts`, JSON data from responses were parsed without validation, making the application vulnerable to manipulation through malicious JSON inputs.

##### Proof of Concept

```
function genNodeParams(response: TlsResponse, api: API) {
  console.log('-----genNodeParams-----')
  const { records, fullResponse, responseSliceList, requestInfo, accept } = response

  const resStruct = genDataStruct(responseSliceList, api, accept)

  console.log('-----response struct-----', resStruct)
  console.log('-----records-----', records)
  console.log('-----record length-----', records.length)
```

##### Score

Impact: 4  
Likelihood: 2

##### Recommendation

Implement validation and sanitization checks when parsing JSON data, especially when working with untrusted input or external sources.

##### Remediation

**RISK ACCEPTED:** The **zkPass team** stated: "*Since our JSON properties and structure are not fixed, we only validated the JSON’s legality."*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Chromium Browser Extension |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/zkpass/chromium-browser-extension
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/zkpass/chromium-browser-extension

### Keywords for Search

`vulnerability`

