---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41219
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#7-griefing-of-csmoduleaddvalidatorkeyseth-with-csmoduledepositeth
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

Griefing of `CSModule.addValidatorKeysETH()` with `CSModule.depositETH()`

### Overview


The report describes a bug in the `CSModule` contract where anyone can increase the Node Operator's bond, causing issues with the `CSModule.addValidatorKeysETH()` function. This can be exploited by a griefer who can repeatedly deposit small amounts of ETH, causing the function to fail. There is also a potential for a DoS attack if a user deposits 0 wei of ETH. The recommendation is to make `CSModule.depositETH()` only accessible to the Node Operator manager and to set a minimum limit for ETH deposits. Private pools should also be used for deposits through the DSM contract.

### Original Finding Content

##### Description

`CSModule.addValidatorKeysETH()` [requires](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L388-L393) that `msg.value` is equal to `accounting.getRequiredBondForNextKeys()`. `accounting.getRequiredBondForNextKeys()` [returns a value](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSAccounting.sol#L527) that relies on the current node operator's bond. The `CSModule.depositETH()` [function is permissionless](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L471-L481) so anyone can increase the Node Operator's bond. A griefer may front-run a call to `accounting.getRequiredBondForNextKeys()` and deposit a few weis for 1 bond share. This would cause the initial call to revert. The griefer can do this multiple times, forcing the node operator manager to use another function for adding keys.

Additionally, a potential DoS vector exists if a user deposits 0 wei of ETH. This could block deposits of new keys initiated from the DSM contract because of the nonce update.

##### Recommendation
We recommend making `CSModule.depositETH()` permissioned so that only the Node Operator manager can call it. Additionally, we recommend adding a minimum limit for ETH deposit amounts and using private pools for deposits through the DSM contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#7-griefing-of-csmoduleaddvalidatorkeyseth-with-csmoduledepositeth
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

