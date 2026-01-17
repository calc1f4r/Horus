---
# Core Classification
protocol: Pheasant Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60341
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
source_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
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
finders_count: 5
finders:
  - Danny Aksenov
  - Faycal Lalidji
  - Ruben Koch
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

Privileged Roles and Ownership

### Overview


This bug report discusses issues with the roles and privileges in the Pheasant Network Bridge Child and Core Child Checkpoint Manager smart contracts. The owner and relayer roles have the ability to make changes to important variables, which can result in trades becoming unslashable. The update mechanism also presents risks, as it can change the values used for processing trades and disputes. The report recommends refactoring the contract and providing clear documentation to users about the level of privilege given to the owner and relayer. 

### Original Finding Content

**Update**
The team documented the roles and privileges in user-facing documentation.

*   Relayer role : https://docs.pheasant.network/contracts/technical-details#update-functions
*   Owner role: https://docs.pheasant.network/contracts/technical-details#owner

**File(s) affected:**`PheasantNetworkBridgeChild.sol`, `CoreChildCheckpointManager.sol`

**Description:** Smart contracts will often have `owner` or other variables to designate persons with special privileges to make modifications to the smart contract.

*   The `owner` role of the `PheasantNetworkBridgeChild` (currently set to the same address as the relayer) contract can arbitrarily pause the contract, most importantly resulting in pending trades being unslashable. While trades can no longer be disputed in that case, the relayer can continue to accept trades.
*   The `relayer` role of the `PheasantNetworkBridgeChild` contract can initiate arbitrary updates to most of the global state variables required for processing trades and their disputes possibly making slashable trades unslashable.
*   Owners of the `CoreChildCheckpointManager` contracts of any of the supported networks can update the `rootCheckpointManager`, i.e. the L1 address from which the block hash is expected to be forwarded, via the same two-step mechanism, three hours delay process present in the `PheasantNetworkBridgeChild` contract. This can theoretically result in incorrect configurations, where block hashes can no longer be forwarded, resulting in trades becoming unslashable.

The current update mechanism can lead to issues, as a user could expect the relayer to operate under a different set of values for the updatable state variables. After the 3h mark, the update can be finalized at any time, resulting in all recently requested and currently slashable trades only to be considered under the new updated values, e.g. marking some network unslashable that previously was slashable or making users pay a higher amount of fees than anticipated). This also could result in pending, slashable trades becoming unslashable.

**Recommendation:** We recommend assessing all the related risks and refactoring the contract accordingly. This centralization of power needs to be made clear to the users via end-user documentation, especially depending on the level of privilege the contract allows to the owner and relayer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Pheasant Network |
| Report Date | N/A |
| Finders | Danny Aksenov, Faycal Lalidji, Ruben Koch, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html

### Keywords for Search

`vulnerability`

