---
# Core Classification
protocol: Mantle Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43404
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/cMETH/README.md#5-centralization-risks
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


This report discusses several centralization risks in a project, including full control over exchange rates, incorrect configuration, strategist privileges, and admin control over the vault. These risks could lead to manipulation of asset values, misuse of funds, and halting of user operations. To mitigate these risks, the report recommends implementing a multi-signature wallet, introducing time delays for critical functions, decentralizing governance, and implementing real-time monitoring and alerts. These measures would reduce the project's exposure to centralization risks and distribute control among multiple parties. 

### Original Finding Content

##### Description
The project presents several centralization risks, including:

- **Full control over exchange rates:** The admin or a specific role has the authority to set and update exchange rates, potentially manipulating asset values.
- **Risk of incorrect configuration (e.g., Merkle Root setup):** If the Merkle Root is misconfigured, it could invalidate key functionality or compromise access control mechanisms.
- **Strategist privileges:** The Strategist has the ability to deposit or withdraw unlimited amounts of tokens in whitelisted protocols, which could be abused to mismanage funds.
- **Ability to lock withdrawals, deposits, and transfers:** Certain roles have the power to pause essential functions like withdrawals, deposits, and transfers, potentially halting user operations.
- **Admin control over BoringVault:** The admin has complete control over vault operations, which can lead to a single point of failure or misuse of assets stored in the vault.

This issue is classified as **medium severity** because it does not directly impact security under normal operation, but centralization poses a risk if malicious or erroneous actions are taken by the privileged entities.

##### Recommendation
To mitigate these centralization risks, we recommend the following:

1. **Implement a Multi-Signature Wallet for Administrative Actions:**
   Require multiple authorized signatures for any critical actions, such as setting exchange rates, modifying the Merkle Root, or making significant deposits and withdrawals. This reduces the risk of a single point of failure or misuse of authority.

2. **Introduce Timelocks for Critical Functions:**
   Add a time delay for executing sensitive operations like changing exchange rates, adjusting withdrawal/deposit settings, or making strategic changes. This provides the community or stakeholders time to review and react to potential harmful actions.

4. **Decentralize Governance:**
   Introduce a governance model where critical decisions, such as pausing withdrawals or modifying vault operations, require community or token-holder votes. This would distribute control and ensure decisions reflect the interests of a wider group of stakeholders.

5. **Transparent Monitoring and Alerts:**
   Implement real-time monitoring and alerts for all sensitive actions, especially those carried out by the admin or strategist roles.

By distributing control across multiple parties, implementing time delays, and increasing transparency, these recommendations would significantly reduce the project's exposure to centralization risks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Mantle Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/cMETH/README.md#5-centralization-risks
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

