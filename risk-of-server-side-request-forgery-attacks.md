---
# Core Classification
protocol: Umee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16903
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
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
finders_count: 2
finders:
  - Paweł Płatek
  - Dominik Czarnota
---

## Vulnerability Title

Risk of server-side request forgery attacks

### Overview


This bug report is about the price-feeder module which sends HTTP requests to configured providers' APIs. If any of the HTTP responses is a redirect response, the module will automatically issue a new request to the address provided in the response's header. This could be exploited by an attacker to gain control over the Osmosis API, and redirect the request to a local address, potentially one that provides access to restricted services. This would allow the attacker to remove a transaction from a Tendermint validator's mempool. 

The recommendation is to use a function such as CheckRedirect to disable redirects, or at least redirects to local services, in all HTTP clients. This will help protect against the attack described in the bug report.

### Original Finding Content

## Security Assessment Documentation

## Difficulty: Low

## Type: Data Validation

### Target: price-feeder

### Description
The price-feeder sends HTTP requests to configured providers’ APIs. If any of the HTTP responses is a redirect response (e.g., one with HTTP response code 301), the module will automatically issue a new request to the address provided in the response’s header. The new address may point to a local address, potentially one that provides access to restricted services.

### Exploit Scenario
An attacker gains control over the Osmosis API. He changes the endpoint used by the price-feeder such that it responds with a redirect like that shown in figure 10.1, with the goal of removing a transaction from a Tendermint validator’s mempool. The price-feeder automatically issues a new request to the Tendermint REST API. Because the API does not require authentication and is running on the same machine as the price-feeder, the request is successful, and the target transaction is removed from the validator's mempool.

```
HTTP/1.1 301 Moved Permanently
Location: http://localhost:26657/remove_tx?txKey=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```
*Figure 10.1: The redirect response*

### Recommendations
Short term, use a function such as `CheckRedirect` to disable redirects, or at least redirects to local services, in all HTTP clients.

---

**Trail of Bits**  
*UMEE Security Assessment*  
*PUBLIC*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Umee |
| Report Date | N/A |
| Finders | Paweł Płatek, Dominik Czarnota |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf

### Keywords for Search

`vulnerability`

