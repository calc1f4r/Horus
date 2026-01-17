---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36550
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/sUSX/README.md#4-centralization-risks
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
  - MixBytes
---

## Vulnerability Title

Centralization Risks

### Overview


This bug report discusses issues with the ownership and role management structure of a contract. These issues could lead to centralized control and potential exploitation. The report recommends implementing measures such as using a multisig account for ownership, assigning certain roles to verified and audited contracts, and establishing procedures for managing interest rates and preventing rate desynchronization.

### Original Finding Content

##### Description
The issue was identified within the contract's ownership and role management structure, presenting several centralization risks:
1. Owners have the capability to upgrade the contract implementation.
2. The `PAUSER_ROLE` can pause all transfers of sUSX, including mints and burns, effectively halting withdrawal activities.
3. The `BRIDGER_ROLE` is capable of minting and burning new tokens, necessitating that this role be exclusively assigned to verified and audited contracts.
4. Owners are responsible for setting the interest rate configurations to ensure that the incoming rewards are collateralized by the treasury assets.
5. Owners must set valid mintCap values to ensure that rewards do not exceed these caps and that the caps are less than the collateral in the treasury.
6. Owners are responsible for synchronizing the exchangeRate across different chains to prevent arbitrage activities.

These centralization risks highlight the significant control owners have over the system's critical functions, which could be exploited if not managed properly.

The issue is classified as **medium** severity due to the potential for abuse of power, which can impact the system's integrity and users' trust.

##### Recommendation
We recommend implementing the following measures to mitigate centralization risks:
1. Ensure the owner is a multisig account to distribute control among multiple parties.
2. Assign the `BRIDGER_ROLE` exclusively to verified and audited contracts.
3. Establish valid configurations and procedures to guarantee the collateralization of rewards.
4. Ensure prompt actions can be taken to prevent rate desynchronization and potential arbitrage opportunities.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/sUSX/README.md#4-centralization-risks
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

