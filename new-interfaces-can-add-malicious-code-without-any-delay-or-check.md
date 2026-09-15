---
# Core Classification
protocol: Geodefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20750
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/11/geodefi/
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
finders_count: 3
finders:
  - Sergii Kravchenko
  -  Christian Goll
  -  Chingiz Mardanov

---

## Vulnerability Title

New interfaces can add malicious code without any delay or check

### Overview


A bug was found in the Geode Finance system, which uses an ERC1155 gETH contract with planet id acting as a token id. The bug is that planet maintainers can whitelist new interfaces without needing approval, which could allow them to steal all derivative tokens in circulation in one transaction. To fix the issue, the code/contracts/Portal/utils/StakeUtilsLib.sol should be updated to have the avoidance be set on a per-interface basis and avoiding new interfaces by default. This way, users would need to allow the new tokens to access the balances.

### Original Finding Content

#### Description


Geode Finance uses an interesting system of contracts for each individual staked ETH derivative. At the base of it all is an ERC1155 gETH contract where planet id acts as a token id. To make it more compatible with the rest of DeFi the Geode team pairs it up with an ERC20 contract that users would normally interact with and where all the allowances are stored. Naturally, since the balances are stored in the gETH contract, ERC20 interfaces need to ask gETH contract to update the balance. It is done in a way where the gETH contract will perform any transfer requested by the interface since the interface is expected to do all the checks and accountings. The issue comes with the fact that planet maintainers can whitelist new interfaces and that process does not require any approval. Planet maintainers could whitelist an interface that will send all the available tokens to the maintainer’s wallet for example. This essentially allows Planet maintainers to steal all derivative tokens in circulation in one transaction.


#### Examples


**code/contracts/Portal/utils/StakeUtilsLib.sol:L165-L173**



```
function setInterface(
 StakePool storage self,
 DataStoreUtils.DataStore storage DATASTORE,
 uint256 id,
 address \_interface
) external {
 DATASTORE.authenticate(id, true, [false, true, true]);
 \_setInterface(self, DATASTORE, id, \_interface);
}

```
#### Recommendation


`gETH.sol` contract has a concept of avoiders. One of the ways to fix this issue is to have the avoidance be set on a per-interface basis and avoiding new interfaces by default. This way users will need to allow the new tokens to access the balances.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Geodefi |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Christian Goll,  Chingiz Mardanov
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/11/geodefi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

