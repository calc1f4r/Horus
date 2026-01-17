---
# Core Classification
protocol: UMA Across V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10606
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-across-v2-audit/
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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Relayers may request invalid repayments

### Overview


This bug report is related to the Across V2 system, which is a decentralized protocol for trading assets across multiple blockchains. The issue is that when a relayer fills a relay, they specify a `repaymentChainId` to indicate which chain they want to be refunded on, but this is not validated against any set of acceptable values. This means that if an invalid `repaymentChainId` is used, the repayment may not be made and the user could lose funds. 

The UMA team has acknowledged the issue and intends to address it off-chain. They plan to create a UMIP that lists valid repayment chain IDs or points to where to find them, and provide a default repayment chain ID for invalid ones. For example, the UMIP could stipulate that any invalid repayment chain IDs are repaid on mainnet. This should help ensure that users are not surprised by losing funds due to an invalid `repaymentChainId`.

### Original Finding Content

When a relayer [fills a relay](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/SpokePool.sol#L371), they specify a [`repaymentChainId`](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/SpokePool.sol#L377) to indicate which chain they want to be refunded on. However, the `repaymentChainId` is not validated against any set of acceptable values. Instead, it is included in the [`_emitFillRelay`](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/SpokePool.sol#L400) event, which is used for generating root bundles in the system.


Since not all tokens may exist on all chains, and some chain ID’s may not exist or be a part of the Across V2 system, consider specifying valid values for `repaymentChainId` for a given token, and implementing logic similar to that for [`enabledDepositRoutes`](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/SpokePool.sol#L58) to use for checking `repaymentChainId`. Alternatively, consider specifying in the UMIP some procedures for root bundle proposers to determine whether a `repaymentChainId` is valid, and what to do if it is not. In this case, invalid `repaymentChainId`s may mean a repayment is simply not repaid – if this is chosen, ensure that this is made very clear in any documentation about the system, so that users are not surprised by losing funds.


**Update**: *Acknowledged. The UMA team intends to address this off-chain. They state:*



> We believe that this issue can be resolved in a well-defined UMIP that lists valid repayment chain IDs (or points to where to find them), and provide a default repayment chain ID for invalid ones. For example, the UMIP could stipulate that any invalid repayment chain IDs are repaid on mainnet.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Across V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-across-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

