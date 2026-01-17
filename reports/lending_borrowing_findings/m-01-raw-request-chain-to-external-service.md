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
solodit_id: 61426
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

[M-01] Raw request chain to external service

### Overview


This bug report describes a medium severity vulnerability in the code of a router-api application. The code includes two endpoints that allow unfiltered access to an external API, without any input validation, path filtering, header or method restrictions, body sanitation, or authentication. This means that attackers can use these endpoints to execute arbitrary calls with custom payloads, potentially targeting internal resources and spoofing headers. The report recommends implementing various security measures, such as stripping and sanitizing headers, only allowing safe methods, and applying DTO validation. 

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Vulnerable code: 
- router-api/src/app/transfer/transfer.controller.ts.
- router-api/src/app/transfer/transfer.service.ts.
- router-api/src/app/transfer/external/skip.service.ts.

The code defines two open proxy-style endpoints (/api/rest/* and /api/rpc/*) that forward the entire raw HTTP Request object, unfiltered, through the application layers and finally into an outbound axios.request(...) call targeting the Skip API (SKIP_GO_API_URL).

There is no:

- Input validation.
- Allowed path filtering.
- Header or method restrictions.
- Body sanitation.
- Authentication or access control.

The result is a generic unauthenticated passthrough interface to an external API, over which clients can execute arbitrary calls with custom payloads.

> **Note**: Note: This vulnerability is documented in detail within the individual findings "No Response Validation for External Skip API" and "Unvalidated Raw Request Injection via msgsDirect and txTrack." This section emphasizes how these vulnerabilities interact to create a compound security risk that amplifies the potential impact beyond what each issue presents in isolation.

```
// transfer.controller.ts:
@All("/api/rest/*path")
apiRest(@Req() req: Request) {
  return this.transferService.api(req);
}

```
```
// transfer.service.ts:
api(req: Request) {
  return this.skipService.api(req);
}

```
```
// skip.service.ts:
api(req: Request) {
  const url = new URL(req.url, SKIP_GO_API_URL);
  return this._requestSkip(url, req.body, req.method);

}

```

Impact:
- If SKIP_GO_API_URL is misconfigured, attackers can target internal resources.
- Ability to spoof headers such as Host, Authorization, Origin.
- Attackers can forward arbitrary requests through your backend.

## Recommendations

Recommendations are already in place for independent findings related to this one. Additionally:
- Strip and Sanitize Headers.
- Only allow safe methods like GET or explicitly defined POST operations.
- Apply DTO validation if the body is used.





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

