---
# Core Classification
protocol: Superform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54329
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9
source_link: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
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
  - cergyk
---

## Vulnerability Title

Liﬁvalidator.validatetxdata calldata can decode to bridgedata type but also be compatible with generic swap 

### Overview


The bug report discusses an issue with the `LiFiValidator.validateTxData` function. This function assumes that if the calldata is valid for a generic swap function call, it will fail to decode during `extractMainParameters`. However, it is possible for a malicious user to create calldata that is valid for both `extractMainParameters` and `swapTokensGeneric` on the LiFi diamond. This allows them to bypass the validation logic and execute a local swap while indicating a cross-chain deposit. The report recommends matching on the selector called instead of relying on encoding matching, which can be prone to collisions.

### Original Finding Content

## LiFiValidator: Validation Logic Analysis

## Context
(No context files were provided by the reviewer)

## Description
`LiFiValidator.validateTxData` uses the assumption that if the calldata is valid for the generic swap function call, it will fail to decode during `extractMainParameters`. This is why the cross-chain case is handled in a try block, whereas local calls are managed in the catch block.

However, it is possible to create calldata that is validly decoded by `extractMainParameters`, and is also valid when calling `swapTokensGeneric` on the LiFi diamond. Furthermore, the sets of parameters that these encodings represent do not overlap, which means a malicious user can entirely bypass the validation logic, and use an arbitrary local swap when indicating a cross-chain deposit to superform.

Note that in this case, `swapTokensGeneric`, which has the following signature:

```solidity
function swapTokensGeneric(
    bytes32 _transactionId,
    string calldata _integrator,
    string calldata _referrer,
    address payable _receiver,
    uint256 _minAmount,
    LibSwap.SwapData[] calldata _swapData
) external payable
```

has the same arbitrary blob `_transactionId`, which can be used to specify an offset for the location of the dynamic type `BridgeData`. Therefore, a malicious user can use this to bypass the `validateTx` chain entirely and execute a local swap while indicating a cross-chain deposit to superform.

## Recommendation
Match on the selector called, instead of relying on encoding matching (which can be collision prone).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | cergyk |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9

### Keywords for Search

`vulnerability`

