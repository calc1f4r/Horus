---
# Core Classification
protocol: Lisk Governance, Staking, Reward, Vesting, and Airdrop Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33142
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-05-lisksmartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-05-lisksmartcontracts-securityreview.pdf
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
finders_count: 3
finders:
  - Maciej Domanski
  - Priyanka Bose
  - Elvis Skoždopolj
---

## Vulnerability Title

Missing certiﬁcate validation

### Overview


The report states that there is a high difficulty bug in the system that can lead to a Denial of Service attack. This is caused by the client-side verification of the server certificate being disabled in the DB class. This allows for server impersonation and man-in-the-middle attacks when the DB_SSLMODE environment variable is set to true. An attacker can pose as the PostgreSQL server and present a fake certificate, which is accepted due to the disabled verification. To fix this issue, the recommendation is to re-enable TLS certificate verification in the DB class constructor and review the TLS configuration to ensure it is using modern protocols and ciphers. In the long term, it is suggested to incorporate a tool called Semgrep with a specific rule to catch similar issues early on in the development process. 

### Original Finding Content

## Vulnerability Report

**Difficulty:** High  
**Type:** Denial of Service  

## Description
The client-side verification of the server certificate is disabled in the DB class, allowing for server impersonation and person-in-the-middle attacks when the `DB_SSLMODE` environment variable is set to true (Figure 3.1).

```javascript
process.env.DB_SSLMODE === 'true'
  ? {
      ssl: {
      },
      require: true,
      rejectUnauthorized: false,
    }
  : {};
```

**Figure 3.1:** The setup of TLS in the DB class’s constructor  
(lisk-token-claim/packages/claim-backend/src/db.ts#20–27)

## Exploit Scenario
An attacker poses as the PostgreSQL server and presents a fake certificate. Because verification of the server certificate is disabled, the attacker’s certificate is accepted, allowing them to interfere with communication.

## Recommendations
- **Short term:** Re-enable TLS certificate verification in the DB class constructor. Review the TLS configuration to ensure it uses modern TLS protocol versions and ciphers.
- **Long term:** Incorporate the Semgrep tool with the `bypass-tls-verification` rule in the CI/CD process to catch issues like this early on.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Lisk Governance, Staking, Reward, Vesting, and Airdrop Contracts |
| Report Date | N/A |
| Finders | Maciej Domanski, Priyanka Bose, Elvis Skoždopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-05-lisksmartcontracts-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-05-lisksmartcontracts-securityreview.pdf

### Keywords for Search

`vulnerability`

