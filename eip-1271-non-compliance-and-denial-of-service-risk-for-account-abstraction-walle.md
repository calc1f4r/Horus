---
# Core Classification
protocol: OP Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40524
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/1b6a9e55-49a8-46e9-8272-a849fd60fcc4
source_link: https://cdn.cantina.xyz/reports/cantina_competition_optimism_may2024.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - bronzepickaxe
  - J4X98
  - deth
  - nmirchev8
  - elhaj
---

## Vulnerability Title

EIP-1271 non-compliance and denial of service risk for account abstraction wallets in council safe 

### Overview


The bug report states that there is a problem with the validation logic for smart contract wallet signatures in the Council Safe. This is causing issues for owners who are trying to sign transactions. The problem lies in the checkNSignatures function, where the contract is calling the isValidSignature function with the wrong types of inputs. This is due to a discrepancy between the ISignatureValidator in the EIP1271 and the interface used in this version of the safe. This can lead to two major issues: owners with smart contract wallets are unable to sign transactions, and the Council Safe could become dysfunctional if the number of smart contract wallet owners is greater than the difference between the total number of owners and the required number to approve a transaction. Additionally, the FALLBACK_OWNER is also a Safe wallet, which could cause further issues if it adopts or upgrades to a different version. 

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
Owners using smart contract wallets (account abstraction) are facing a blocking issue when trying to sign transactions on the Council Safe. This is due to the use of incorrect validation logic for smart contract wallet signatures as defined in EIP1271 in the version of the contract used by the Council Safe. 

The problem occurs in the `checkNSignatures` function. The contract calls the `isValidSignature` function with the wrong types of inputs:

```solidity
require(ISignatureValidator(currentOwner).isValidSignature(
    data,
    contractSignature
) == EIP1271_MAGIC_VALUE, ' GS024 ')
```

The `ISignatureValidator` in the EIP1271 takes `(bytes32, bytes)`, while the interface used in this version of the safe defines it as `(bytes, bytes)`. This leads to different function signatures and thus different `EIP1271_MAGIC_VALUE`. Therefore, `EIP1271_MAGIC_VALUE` expected to be returned when the validation is successful is incorrectly implemented when compared to the standard defined in EIP-1271.

- `safe_magic_value => 0x20c13b0b`
- `EIP1271_magic_value => 0x1626ba7e`

## Implications
This issue can lead to two major problems:

1. Owners with smart contract wallets (account abstraction) are unable to sign transactions, violating this specified property.
2. More severely, the Council Safe could become entirely dysfunctional. If the number of owners with smart contract wallets (smartWallets owners) is greater than the difference between the total number of owners (ownersCount) and the required number to approve a transaction (threshold), no transactions can be executed. This situation could arise if a smart contract wallet is added as a new owner, or if there is a change in the threshold, etc.

Moreover, the `FALLBACK_OWNER` is itself a Safe wallet, and if it adopts or upgrades to the new version...

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Cantina |
| Protocol | OP Labs |
| Report Date | N/A |
| Finders | bronzepickaxe, J4X98, deth, nmirchev8, elhaj, Putra Laksmana, BoRonGod |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_optimism_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/1b6a9e55-49a8-46e9-8272-a849fd60fcc4

### Keywords for Search

`vulnerability`

