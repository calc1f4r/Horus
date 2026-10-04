---
# Core Classification
protocol: Ethena Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60288
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethena-labs/307f3777-9f03-4b08-8b92-b6c243388ebc/index.html
source_link: https://certificate.quantstamp.com/full/ethena-labs/307f3777-9f03-4b08-8b92-b6c243388ebc/index.html
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

protocol_categories:
  - staking_pool
  - decentralized_stablecoin

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Michael Boyle
  - Jeffrey Kam
  - Jonathan Mevs
---

## Vulnerability Title

Potential Collateral Sent to Non-Team Controlled Addresses

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `9f9527a537cd0b0e80f9c5a88cbeae5892d2d570`. The client provided the following explanation:

> Minters can only transfer assets to whitelisted custodian addresses.

**Description:** There is the potential for collateral to be transferred to addresses that are not controlled by the team as there is no storage in the contract state that contains a set of these addresses that are valid. As a result, there is the potential for USDe-Buy-Orders to be processed that do not transfer the collateral to a team-controlled address. While it is understood that Ethena servers perform validation before sending transactions to the smart contract, we would still like to highlight this possibility.

**Recommendation:** Consider adding a role specifically for custody and only allowing transfers out to go to addresses with this role. This will both improve security and give users peace-of-mind when funds are moved out of the contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethena Labs |
| Report Date | N/A |
| Finders | Michael Boyle, Jeffrey Kam, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethena-labs/307f3777-9f03-4b08-8b92-b6c243388ebc/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethena-labs/307f3777-9f03-4b08-8b92-b6c243388ebc/index.html

### Keywords for Search

`vulnerability`

