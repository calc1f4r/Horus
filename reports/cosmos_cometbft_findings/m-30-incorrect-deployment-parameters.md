---
# Core Classification
protocol: veToken Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6151
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-vetoken-finance-contest
source_link: https://code4rena.com/reports/2022-05-vetoken
github_link: https://github.com/code-423n4/2022-05-vetoken-findings/issues/52

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

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Picodes
---

## Vulnerability Title

[M-30] Incorrect deployment parameters

### Overview


This bug report describes an issue with the deployment scripts for G-Uni tokens, which are not up to date. This issue could have an impact on the address of G-Uni tokens. As a proof of concept, for agEUR/USDC, the address is 0xedecb43233549c51cc3268b5de840239787ad56c instead of 0x2bD9F7974Bc0E4Cb19B8813F8Be6034F3E772add. To mitigate this issue, the recommendation is to directly fetch the LP token from the staking contract, for safety.

### Original Finding Content

_Submitted by Picodes_

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/migrations/25_deploy_angle_pools.js#L68>

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/migrations/25_deploy_angle_pools.js#L80>

### Impact

The address of G-Uni tokens in the deployment scripts are not up to date.

### Proof of Concept

For example for agEUR/USDC it is 0xedecb43233549c51cc3268b5de840239787ad56c and not 0x2bD9F7974Bc0E4Cb19B8813F8Be6034F3E772add.

### Recommended Mitigation Steps

For safety why not fetching directly the LP token from the staking contract?

**[jetbrain10 (veToken Finance) confirmed](https://github.com/code-423n4/2022-05-vetoken-findings/issues/52)** 

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/52#issuecomment-1200279065):**
> The warden has shown how a configuration file shows that the settings for the project are using an old address.
> 
> While the finding pertains to a setup script (generally out of scope), given that:
> - The sponsor has confirmed
> - The finding is valid in that using older deployments will cause at the very least a loss of yield
> - We already had an instance of bringing an out-of-scope file into scope via Sponsor-Confirming (See: [#209](https://github.com/code-423n4/2022-05-vetoken-findings/issues/209))
> 
> With the information I have, I believe the finding to be of Medium Severity and believe the sponsor will mitigate by updating to the Warden suggested addresses.


***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | veToken Finance |
| Report Date | N/A |
| Finders | Picodes |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-vetoken
- **GitHub**: https://github.com/code-423n4/2022-05-vetoken-findings/issues/52
- **Contest**: https://code4rena.com/contests/2022-05-vetoken-finance-contest

### Keywords for Search

`vulnerability`

