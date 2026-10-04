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
solodit_id: 52218
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/zkpass/chromium-browser-extension
source_link: https://www.halborn.com/audits/zkpass/chromium-browser-extension
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Outdated packages

### Overview

See description below for full details.

### Original Finding Content

##### Description

Multiple outdated packages were identified in the extension, which could significantly increase the risk of security vulnerabilities. These outdated dependencies may contain known security flaws that have been publicly disclosed, leaving the extension vulnerable to a variety of potential attacks. Exploiting these vulnerabilities could lead to issues such as unauthorized access, data breaches, or even complete compromise of the system. By continuing to use outdated packages, the extension may miss out on critical security patches and performance improvements provided by more recent versions, thereby increasing the overall attack surface of the application.

##### Proof of Concept

|  |  |  |
| --- | --- | --- |
| **Issue** | **Package** | **Patched version** |
| protobufjs Prototype Pollution vulnerability | protobufjs | >=7.2.5 |
| PostCSS line return parsing error | postcss | >=8.4.31 |
| @adobe/css-tools Regular Expression Denial of Service | @adobe/css-tools | >=4.3.1 |
| @adobe/css-tools Improper Input Validation and Inefficient | @adobe/css-tools | >=4.3.2 |
| Follow Redirects improperly handles URLs in the url.parse() | follow-redirects | >=1.15.4 |
| follow-redirects' Proxy-Authorization header kept across | follow-redirects | >=1.15.6 |
| browserify-sign upper bound check issue in `dsaVerify` leads | browserify-sign | >=4.2.2 |
| Path traversal in webpack-dev-middleware | webpack-dev-middleware | >=5.3.4 |
| Express.js Open Redirect in malformed URLs | express | >=4.19.2 |
| express vulnerable to XSS via response.redirect() | express | >=4.20.0 |
| Babel vulnerable to arbitrary code execution when compiling | @babel/traverse | >=7.23.2 |
| Axios Cross-Site Request Forgery Vulnerability | axios | >=1.6.0 |
| Server-Side Request Forgery in axios | axios | >=1.7.4 |
| Uncontrolled resource consumption in braces | braces | >=3.0.3 |
| ejs lacks certain pollution protection | ejs | >=3.1.10 |
| ws affected by a DoS when handling a request with many HTTP | ws | >=8.17.1 |
| Regular Expression Denial of Service (ReDoS) in micromatch | micromatch | >=4.0.8 |
| Webpack's AutoPublicPathRuntimeModule has a DOM Clobbering | webpack | >=5.94.0 |
| body-parser vulnerable to denial of service when url | body-parser | >=1.20.3 |
| send vulnerable to template injection that can lead to XSS | send | >=0.19.0 |
| serve-static vulnerable to template injection that can lead | serve-static | >=1.16.0 |
| path-to-regexp outputs backtracking regular expressions | path-to-regexp | >=0.1.10 |
| Regular Expression Denial of Service in content | content | >=3.0.7 |
| Inefficient Regular Expression Complexity in nth-check | nth-check | >=2.0.1 |
| ws affected by a DoS when handling a request with many HTTP | ws | >=7.5.10 |
| Elliptic allows BER-encoded signatures | elliptic | >=6.5.7 |
| Elliptic's ECDSA missing check for whether leading bit of r and s is zero | elliptic | >=6.5.7 |
| Elliptic's EDDSA missing signature length check | elliptic | >=6.5.7 |

##### Score

Impact: 2  
Likelihood: 2

##### Recommendation

Ensure that all dependencies are updated to the latest stable versions. Use your package manager to check for available updates and apply them. Regular updates would ensure that your extension benefits from the latest security patches and performance improvements.

##### Remediation

**RISK ACCEPTED:** The **zkPass team** stated: "*During the upgrade process, we discovered a large number of package incompatibilities, so we have decided not to proceed with the upgrade for now*."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

