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
solodit_id: 60287
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

Manual Liquidity Control Could Delay USDe Redemptions

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Internally team will maintain ~$200k worth of collateral available for hot redemptions. However team and our custodian does have liquidity control for redemptions

**File(s) affected:**`EthenaMinting.sol`

**Description:** Documentation and the code suggest that the `EthenaMinting` contract doesn't hold any underlying LST assets, but rather custodial wallets do. This is evident in the documentation and the `_transferCollateral` function where collateral is transferred elsewhere. As funds are not stored in the contract itself, the team controls the liquidity that is managed in this contract. As a result, there is the potential that there could be friction for USDe redemptions if there is insufficient liquidity in the Ethena Minting contract.

**Recommendation:** Make clear to the user the schedule for funding the minting smart contract from custodian wallets.

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

