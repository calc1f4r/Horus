---
# Core Classification
protocol: Initia_2025-06-17
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61430
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Initia-security-review_2025-06-17.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-05] XSS possible via unfiltered `src` in `img.initia.xyz` proxy endpoint

### Overview


This bug report describes a security issue that allows attackers to inject malicious code into a website through the use of unvalidated and unfiltered URLs in an image proxy service. This vulnerability could potentially lead to cross-site scripting (XSS) attacks, which can have a high impact on the website's security. The report recommends implementing measures such as whitelisting or domain validation, sanitizing data URIs, and using a safer proxy layer to prevent this issue. It also suggests updating the affected component to include input validation and reject unsafe schemes.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Low

## Description

An XSS vulnerability exists due to the use of unvalidated and unfiltered URLs passed into an image proxy service (`img.initia.xyz`). This affects the image rendering logic within the `Image.tsx` component, which directly binds the `src` attribute from potentially untrusted input.

The function `getProxyImage` prepends `https://img.initia.xyz/?url=` to the provided URL unless it starts with a `data:image/` prefix. However, this allows attackers to inject malicious payloads via base64-encoded HTML/JavaScript content through a `data:text/html;base64,...` scheme.

A working XSS payload example:

```
https://img.initia.xyz/?url=data:text/html;
base64,PHNjcmlwdD5hbGVydCgiWFNTIGhlcmUiKTwvc2NyaXB0Pg==
```

Since the widget directly renders the image using the `src` from `getProxyImage`, the browser treats the URL as valid and executes the embedded script.

Additionally, there is no validation or sanitization of the incoming `src` value in the component. The code path:

```
<Img
  ...
  src={getProxyImage(src)}
  ...
/>
```

shows that even malformed or malicious input is proxied and rendered.

Code Location : [link](https://github.com/initia-labs/widget/blob/c7c7fc23a5d65cafbd8d748711a607abf695052a/packages/widget-react/src/components/Image.tsx#L31-L32)

## Recommendations

* Add **whitelisting or domain validation** on the `src` parameter before binding it to the image tag.
* Sanitize or reject any `data:` URIs that do not begin with `data:image/`.
* Consider rendering images via a safe CDN or a stricter proxy layer that prevents HTML/JS payloads.
* Update the `Image.tsx` component to include input validation and reject unsafe schemes like `data:text/html`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Initia_2025-06-17 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Initia-security-review_2025-06-17.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

