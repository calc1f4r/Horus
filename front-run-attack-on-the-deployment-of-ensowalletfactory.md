---
# Core Classification
protocol: Enso
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61934
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Enso/Enso%20Wallet/README.md#2-front-run-attack-on-the-deployment-of-ensowalletfactory
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Front-run attack on the deployment of EnsoWalletFactory

### Overview


The EnsoWalletFactory has a bug that allows attackers to gain control of user wallets by inserting their own transactions before the factory is initialized. This can result in the deployment of a modified factory with backdoor functionality. It is recommended to improve the code to prevent arbitrary accounts from gaining ownership or to combine the deployment and initialization process into a single transaction.

### Original Finding Content

##### Description
An attacker can place their transactions between the deployment of the EnsoWalletFactory implementation and [EnsoWalletFactory.initialize()](https://github.com/EnsoFinance/shortcuts-contracts/blob/4902e55608f975f73772310955444110b1cfc4fc/contracts/EnsoWalletFactory.sol#L26) to specify themself as the contract owner and make an upgrade of the EnsoWalletFactory to the modified one. The modified factory contract may implement backdoor functionality to gain control of the deployed user wallets.

##### Recommendation
We recommend improving the code of the upgradeable proxy to disallow the gain of ownership by arbitrary accounts or at least improve the deployment process in order to implement deployment and initialization in a single transaction.




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Enso |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Enso/Enso%20Wallet/README.md#2-front-run-attack-on-the-deployment-of-ensowalletfactory
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

