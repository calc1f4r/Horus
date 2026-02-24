---
# Core Classification
protocol: Easy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48153
audit_firm: OtterSec
contest_link: https://easy.me
source_link: https://easy.me
github_link: https://github.com/The-Easy-Company/ember

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
finders_count: 3
finders:
  - OtterSec
  - Robert Chen
  - Bruno Halltari
---

## Vulnerability Title

Leak Of Metamask Nonce

### Overview


The application has a bug where the API responsible for importing a Metamask wallet through easy.connect.me may cache the nonce value, which could potentially be accessed by an attacker. The bug has been fixed by adding Cache-Control: no-cache to the HTTP response.

### Original Finding Content

## Metamask Wallet Import and API Caching Vulnerability

The application allows users to import a Metamask wallet through [easy.connect.me](https://easy.connect.me). However, the API responsible for this process, `/api/auth/warrant`, may cache the nonce value via client-side caching if the client implements caching based on the Cache-Control header.

## API Response Example

```http
DART
HTTP/2 200 OK
Access-Control-Allow-Origin: *
Cache-Control: public, max-age=0, must-revalidate
Content-Type: application/json; charset=utf-8
Date: Mon, 01 May 2023 17:49:42 GMT
Etag: W/"2c-G6HcDkOtKKSd8e+AveED+oo4jjY"
Server: Vercel
Strict-Transport-Security: max-age=63072000
X-Vercel-Cache: MISS
X-Vercel-Id: fra1::pdx1::tqk9v-1682963381910-e275bf7da8be
Content-Length: 44
{"nonce":"74311844459642c49da0e92b14e1d2d9"}
```

The `Cache-Control` header with the `public` directive allows the response to be cached by the client-side cache, even if `max-age=0` and `must-revalidate` are present. An attacker who gains access to the client’s device or network traffic may be able to obtain the nonce value.

## Remediation

Implement `Cache-Control: no-cache` inside the HTTP response.

## Patch

Fixed in `b43efa2` by adding `Cache-Control: no-cache` inside the HTTP response.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Easy |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Bruno Halltari |

### Source Links

- **Source**: https://easy.me
- **GitHub**: https://github.com/The-Easy-Company/ember
- **Contest**: https://easy.me

### Keywords for Search

`vulnerability`

