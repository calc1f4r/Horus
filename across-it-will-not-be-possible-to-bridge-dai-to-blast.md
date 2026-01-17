---
# Core Classification
protocol: Across V3 and Oval Incremental Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34953
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-v3-and-oval-incremental-audit
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

[Across] It Will Not Be Possible to Bridge DAI to Blast

### Overview


The `relayTokens` function in the `Blast_Adapter` contract is used to transfer tokens from Ethereum to Blast. However, when trying to use this function for DAI tokens, it fails because it attempts to call a function that does not exist in the L1 Blast bridge. This means that any transactions trying to transfer DAI to Blast using the `relayTokens` function will not work. To fix this, the `bridgeERC20To` function of the L1 Blast bridge should be used instead. This issue has been resolved in a recent update. 

### Original Finding Content

The [`relayTokens`](https://github.com/across-protocol/contracts/blob/95c4f923932d597d3e63449718bba5c674b084eb/contracts/chain-adapters/Blast_Adapter.sol#L80) function of the `Blast_Adapter` contract is responsible for bridging tokens from Ethereum to Blast. In order to do that, it uses either the L1 standard bridge or the L1 Blast bridge, depending on the token being bridged. In case of DAI, [an attempt to call `depositERC20To`](https://github.com/across-protocol/contracts/blob/95c4f923932d597d3e63449718bba5c674b084eb/contracts/chain-adapters/Blast_Adapter.sol#L98) function of the L1 Blast bridge is made. However, the bridge does not contain this function. This means that all transactions trying to bridge DAI to Blast using the `relayTokens` function will revert.


When DAI is being bridged, consider calling the `bridgeERC20To` function of the L1 Blast bridge instead.


***Update:** Resolved in [pull request \#518](https://github.com/across-protocol/contracts/pull/518) at commit [9b9b3d6](https://github.com/across-protocol/contracts/commit/9b9b3d66b38a7a8f0975aeeb59d35de0640576a1).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across V3 and Oval Incremental Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-v3-and-oval-incremental-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

