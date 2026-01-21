---
# Core Classification
protocol: SphereX Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33041
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/spherex-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Potential Issues in Systems Using Factory and Beacon Patterns

### Overview


The report discusses issues with various smart contract systems that add contracts dynamically based on user actions. These systems can become operational immediately upon creation, but with SphereX protection, an admin must separately add each new contract, causing centralization and complexity. Additionally, making changes to admin and engine addresses on these contracts can be complicated and prone to errors. There is also a risk of censorship due to SphereX's ability to exclude specific addresses. It is suggested to implement Role-Based Access Control (RBAC) to address these concerns, such as creating a role with permissions to add allowed senders or establishing an administrative function for factories to add new contracts. The report also suggests using a single contract for updating and querying configurations and separating the storage of added addresses to prevent censorship. However, these issues have not been fully resolved in a recent update.

### Original Finding Content

Various smart contract systems implement patterns that dynamically add contracts to the system based on user actions. Some notable examples include pool creation in AMMs, personal proxies in Maker, and multi-signature (multi-sig) Safe creation. When protected by SphereX, each newly created instance of a factory-created contract would need to be separately added by the admin, preventing the contract from becoming immediately operational upon creation, adding a centralizing step, and adding operational complexity.


Furthermore, performing changes to admin and engine addresses on the dynamically generated contracts will be operationally complex and error-prone.


Moreover, these systems can pose a risk of targeted censorship due to the capability of SphereX to exclude a specific personal proxy address from the allowed senders.


Consider implementing Role-Based Access Control (RBAC) as described in the [OpenZeppelin documentation](https://docs.openzeppelin.com/contracts/4.x/access-control#using-access-control). One possible approach could be creating a `SENDER_CONFIG_ROLE` with the permissions to add allowed senders. This will allow the general admin to assign this role to the factory contract when needed. Alternatively, consider establishing an additional administrative function that enables a factory contract to independently add a newly created contract as an approved sender.


To resolve the configuration issues, consider utilizing a single contract for updating and querying the configuration in the client's project.


To alleviate the censorship risk, consider separating the storage of factory-added addresses and disallowing the removal of any specific address from that set. Alternatively, consider implementing a long delay for removing senders, such that a censored personal proxy owner will have time to exit the system if both SphereX and the Client project are forced to censor it.


***Update**: Partially resolved in [pull request #27](https://github.com/spherex-collab/spherex-protect/pull/27) at commit [052bb05](https://github.com/spherex-collab/spherex-protect/pull/27/commits/052bb0555f5fdebf74404af957074e54f1eb4e59). A role-based system was implemented, allowing factories to add new senders on-chain. The configuration and censorship concerns were not resolved.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | SphereX Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/spherex-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

