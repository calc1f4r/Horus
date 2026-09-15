---
# Core Classification
protocol: Colbfinance Web2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64060
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/ColbFinance-Web2-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-02] Lack of Server-Side Validation Allows Tampering with Pool Exchange Rates in the Dapp

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The backoffice endpoint `/backoffice/api/pools-exchange-rates` accepts POST requests that directly update exchange rate records for investment pools. The server does not validate the rate or `createdAt` parameters, allowing an attacker to submit arbitrary values, including negative rates and impossible dates far in the future.

In the following PoC, the following parameters were modified:

- rate to `-100000`
- createdAt to `5025-08-06T11:00:08.889Z`

These changes were reflected in the Managed Pools interface under Earn Products, confirming that the tampering is stored and displayed without sanitization.

Vulnerable POST request example:

```bash
POST /backoffice/api/pools-exchange-rates HTTP/2
Host: backoffice.testnet.colb.io
Content-Type: application/json
Token: <valid_jwt>

{
  "poolType": "Balance",
  "rate": -100000,
  "createdAt": "5025-08-06T11:00:08.889Z"
}
```

The tampered parameters were processed in the UI. No server-side rejection or normalization occurred:

<img width="1342" height="754" alt="Image" src="https://github.com/user-attachments/assets/129f69be-c506-4813-8d7e-4e129d772352" />

<img width="1304" height="736" alt="Image" src="https://github.com/user-attachments/assets/8457c853-f185-4ff1-b429-f4ab0e6d06a9" />

### Justification by OWASP:

OWASP API Security Top 10 – API6:2023 – Unrestricted Access to Sensitive Business Flows
The endpoint allows direct manipulation of financial records without adequate safeguards. Sensitive operations like updating investment exchange rates must be protected by strict business logic validations, input constraints, and user privilege checks.

OWASP API Security Top 10 – API8:2023 – Security Misconfiguration
The lack of server-side validation for critical fields such as `rate` and `createdAt` represents a misconfiguration. Accepting unchecked inputs into core business logic is a failure of secure-by-default design principles.

OWASP API Security Top 10 – API9:2023 – Improper Inventory Management
There is no evidence of endpoint classification or access restriction based on sensitivity. A high-impact operation is exposed without logging, throttling, or validation layers, suggesting a lack of asset inventory and protection based on data sensitivity.

## Impact

Data Integrity Compromise: Tampering with the financial rate record. Reputation Damage: Public dashboards or investor reports could display misleading figures.

## Location of Affected Code

File: [backoffice/api/pools-exchange-rates](https://github.com/COLB-DEV/ColbUI/blob/main/apps/backoffice/pages/api/pools-exchange-rates.ts)

Link: [backoffice.testnet.colb.io](https://app.testnet.colb.io/app/balance)

Link: [backoffice.testnet.colb.io](https://backoffice.testnet.colb.io/)

## Recommendation

Server-Side Validation:

- Reject negative rates or rates exceeding realistic bounds.
- Enforce valid date ranges (`createdAt` should be within a reasonable timeframe).

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Colbfinance Web2 |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/ColbFinance-Web2-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

