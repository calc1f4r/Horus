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
solodit_id: 34256
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#1-inflation-attack-on-itoken
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

Inflation attack on iToken

### Overview


This bug report discusses an issue with the `iToken` smart contract that allows attackers to manipulate the exchange rate and cause rounding issues in the `mint` and `redeemUnderlying` functions. This can result in users losing some of their underlying assets. The severity of this issue is critical as it can lead to permanent loss of user assets. The report recommends fixing this issue at the code level by either preventing the `iToken` from having a small `totalSupply` or ensuring accurate accounting of the underlying asset in the smart contract.

### Original Finding Content

##### Description
Until `iToken` has sufficient `totalSupply`, an attacker can manipulate the `underlying`/`iToken` exchange rate by directly transferring the underlying asset to the `iToken` smart contract. This leads to rounding issues in `mint` and `redeemUnderlying` causing a user to lose some amount of their underlying assets.

Due to the possibility of permanent loss of user assets, such issues have a critical severity rating.

Related code:
- rounding issues on mint
https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/TokenBase/Base.sol#L199
- rounding issues on redeem underlying in iToken for native token
https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/iETH.sol#L140
- rounding issues on redeem underlying in iToken for ERC20 https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/iToken.sol#L126
##### Recommendation
Although this issue can be hotfixed through accurate deployment procedures and configuration settings, we recommend fixing it at the smart contract code level either by preventing the iToken from having a nonzero but small `totalSupply` or by ensuring accurate accounting of the underlying asset in the smart contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#1-inflation-attack-on-itoken
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

