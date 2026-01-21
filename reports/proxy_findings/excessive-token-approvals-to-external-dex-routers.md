---
# Core Classification
protocol: Bellum Core
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52350
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/bellum-exchange/bellum-core
source_link: https://www.halborn.com/audits/bellum-exchange/bellum-core
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

Excessive Token Approvals to External DEX Routers

### Overview


The report discusses a bug found in the `BellumFactory` contract. The contract approves an unlimited amount of tokens to external DEX routers, which could lead to security risks if the routers are compromised. This could result in the draining of tokens, manipulation of token launches, and impact on multiple tokens. The report suggests replacing the unlimited approvals with exact amount approvals during token launch to mitigate the risk. The Bellum Exchange team has implemented this recommendation to solve the bug. The remediation hash for this solution is 24b6f9b4508a1d5e5ae26923a5bdac602841c939.

### Original Finding Content

##### Description

The `BellumFactory` contract approves an unlimited amount (i.e.: `type(uint256).max`) of newly created tokens to external DEX routers (`TJ_ROUTER` or `PHARAOH_ROUTER`). While this is done for convenience, it creates a security risk:

  

If either router contract is compromised through:

* Implementation vulnerabilities
* Upgradeable proxy attacks
* Admin key compromise
* Future bugs

  

The attacker could:

* Drain all tokens held by the BellumFactory
* Manipulate token launches
* Extract value from the protocol
* Impact multiple tokens simultaneously

##### BVSS

[AO:A/AC:L/AX:M/R:N/S:U/C:N/A:N/I:H/D:M/Y:L (6.3)](/bvss?q=AO:A/AC:L/AX:M/R:N/S:U/C:N/A:N/I:H/D:M/Y:L)

##### Recommendation

Replace infinite approvals with exact amount approvals during token launch.

##### Remediation

**SOLVED**: The suggested mitigation was implemented by the **Bellum Exchange team**.

##### Remediation Hash

24b6f9b4508a1d5e5ae26923a5bdac602841c939

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Bellum Core |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/bellum-exchange/bellum-core
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/bellum-exchange/bellum-core

### Keywords for Search

`vulnerability`

