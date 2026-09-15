---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25505
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-07-connext
source_link: https://code4rena.com/reports/2021-07-connext
github_link: https://github.com/code-423n4/2021-07-connext-findings/issues/47

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-04] Expired transfers will lock user funds on the sending chain

### Overview


This bug report was submitted by 0xRajeev and it is related to the cancelling relayer being paid in `receivingAssetId` on the `sendingChain` instead of in `sendingAssetID`. This means that if the user relies on a relayer to cancel transactions, and the `receivingAssetId` asset does not exist on the sending chain, the cancel transaction from the relayer will always revert and user’s funds will remain locked on the sending chain.

The impact of this bug is that expired transfers can never be cancelled and user funds will be locked forever if the user relies on a relayer. To fix this issue, the code should be changed to change `receivingAssetId` to `sendingAssetId` in `transferAsset()` on `TransactionManager.sol` [L514](https://github.com/code-423n4/2021-07-connext/blob/8e1a7ea396d508ed2ebeba4d1898a748255a48d2/contracts/TransactionManager.sol#L510-L517). This issue was confirmed and patched by LayneHaber (Connext) and the patch can be found here: https://github.com/connext/nxtp/pull/25.

### Original Finding Content

_Submitted by 0xRajeev_

The cancelling relayer is being paid in `receivingAssetId` on the `sendingChain` instead of in `sendingAssetID`. If the user relies on a relayer to cancel transactions, and that `receivingAssetId` asset does not exist on the sending chain (assuming only `sendingAssetID` on the sending chain and `receivingAssetId` on the receiving chain are assured to be valid and present), then the cancel transaction from the relayer will always revert and user’s funds will remain locked on the sending chain.

The impact is that expired transfers can never be cancelled and user funds will be locked forever if user relies on a relayer.

Recommend changing `receivingAssetId` to `sendingAssetId` in `transferAsset()` on `TransactionManager.sol` [L514](https://github.com/code-423n4/2021-07-connext/blob/8e1a7ea396d508ed2ebeba4d1898a748255a48d2/contracts/TransactionManager.sol#L510-L517).

**[LayneHaber (Connext) confirmed and patched](https://github.com/code-423n4/2021-07-connext-findings/issues/47#issuecomment-879510286):**
 > https://github.com/connext/nxtp/pull/25



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Connext |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-connext
- **GitHub**: https://github.com/code-423n4/2021-07-connext-findings/issues/47
- **Contest**: https://code4rena.com/reports/2021-07-connext

### Keywords for Search

`vulnerability`

