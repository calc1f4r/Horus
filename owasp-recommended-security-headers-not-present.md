---
# Core Classification
protocol: Kiln - Minitel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64124
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/kiln-minitel/934225af-0b19-4193-aac1-239a95d0ed17/index.html
source_link: https://certificate.quantstamp.com/full/kiln-minitel/934225af-0b19-4193-aac1-239a95d0ed17/index.html
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Albert Heinle
---

## Vulnerability Title

OWASP recommended security headers not present

### Overview


The application is missing important security headers that protect against cross-site scripting, clickjacking, and other client-side attacks. This is due to the design of the application, which allows user-supplied or URL-driven content to be rendered. To fix this, the recommended headers should be implemented at the server or reverse-proxy level for all responses. These headers include `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, and `Strict-Transport-Security`. They should be consistently applied at the lowest level of the application stack to protect all endpoints. 

### Original Finding Content

**Description:** The application does not enforce key HTTP security headers (e.g., Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy) at the lowest level. These headers are critical to mitigating cross-site scripting (XSS), clickjacking, content sniffing, and other client-side attacks. Given the application’s design, which allows rendering user-supplied or URL-driven content, the absence of these headers leaves users exposed to potential exploitation through malicious content injection or UI manipulation.

**Recommendation:** Implement OWASP-recommended security headers at the server or reverse-proxy level for all responses, including static and dynamic content. Recommended headers include: `Content-Security-Policy` (CSP). Restrict scripts, styles, and resources to trusted origins and disable inline execution. `X-Frame-Options` / `frame-ancestors`: Prevent clickjacking by restricting framing of pages. `X-Content-Type-Options: nosniff`: Prevent MIME type sniffing attacks. `Referrer-Policy`: Control referrer information shared with third-party sites. `Strict-Transport-Security (HSTS)`: Enforce HTTPS connections. Ensure these headers are consistently applied at the lowest level in the application stack (web server, reverse proxy, or application server) to protect all endpoints, including any future content rendered from user-supplied data.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Kiln - Minitel |
| Report Date | N/A |
| Finders | Albert Heinle |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/kiln-minitel/934225af-0b19-4193-aac1-239a95d0ed17/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/kiln-minitel/934225af-0b19-4193-aac1-239a95d0ed17/index.html

### Keywords for Search

`vulnerability`

