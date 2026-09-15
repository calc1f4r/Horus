---
# Core Classification
protocol: Index Fun Order Book
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63702
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1197
source_link: none
github_link: https://github.com/sherlock-audit/2025-10-index-fun-order-book-contest-judging/issues/25

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
  - typicalHuman
  - 0xeix
  - axelot
  - merlin
  - sakibcy
---

## Vulnerability Title

M-2: PositionTokens violates one of the MUST rules defined in EIP-1155.

### Overview


This bug report is about a contract called `PositionTokens` that is violating one of the rules from the EIP-1155 standard. This rule states that the contract's URI (Uniform Resource Identifier) must point to a JSON file that follows the ERC-1155 Metadata URI JSON Schema. However, in the current implementation, the URI is set to an empty string, which is not allowed. This can cause issues with displaying token information on marketplaces and other platforms, and it cannot be fixed in the future because the contract does not have a way to update the URI. This is considered a medium severity issue and can negatively affect user experience and integration with other platforms. To fix this, the contract should be initialized with a valid URI or an admin-only function should be introduced to update the URI after deployment.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-10-index-fun-order-book-contest-judging/issues/25 

## Found by 
0xeix, axelot, merlin, sakibcy, typicalHuman

### Summary

`PositionTokens` violates one of the **MUST** rules defined in [[EIP-1155](https://eips.ethereum.org/EIPS/eip-1155#:~:text=in%20RFC%203986.-,The%20URI%20MUST%20point%20to%20a%20JSON%20file%20that%20conforms%20to%20the%20%22ERC%2D1155%20Metadata%20URI%20JSON%20Schema%22.,-%40return%20URI%20string)](https://eips.ethereum.org/EIPS/eip-1155#:~:text=in%20RFC%203986.-,The%20URI%20MUST%20point%20to%20a%20JSON%20file%20that%20conforms%20to%20the%20%22ERC%2D1155%20Metadata%20URI%20JSON%20Schema%22.,-%40return%20URI%20string).
The rule states:

> “The URI **MUST** point to a JSON file that conforms to the ERC-1155 Metadata URI JSON Schema.”

However, in the current implementation, the URI is set to an **empty string**, violating this requirement.

### Root Cause

In `PositionTokens` at https://github.com/sherlock-audit/2025-10-index-fun-order-book-contest/blob/main/orderbook-solidity/src/Token/PositionTokens.sol#L32, the contract initializes `ERC1155` with the `uri` parameter set to an empty string.
This directly violates one of the **MUST** rules from EIP-1155.

Additionally, the sponsor’s README explicitly states that violations of **MUST** EIP rules should be considered **medium severity** issues.


### Internal Preconditions

*

### External Preconditions

*

### Attack Path

*

### Impact

This issue goes beyond a formal EIP-1155 rule violation:

1. **Incorrect Rendering on Marketplaces** - Because the URI is empty, all position tokens will render incorrectly or not appear at all on NFT marketplaces, explorers, and indexing websites that rely on the ERC-1155 metadata standard. This prevents external interfaces from displaying token names, images, or attributes.
2. **Permanent Invalid Metadata** - The contract does not provide a way to update or set the URI after deployment. As a result, all positions will permanently reference an invalid (empty) URI, and the protocol will have no ability to fix or correct metadata in the future.
3. **Specification Violation** - This directly violates an EIP-1155 **MUST** rule, which by the sponsor’s README is considered a **medium severity** issue.

Overall, this negatively affects user experience, token discoverability, and integration with third-party platforms.

### Proof of Concept (PoC)

-

### Mitigation

Initialize `PositionTokens` with a valid URI that points to a proper ERC-1155 metadata JSON file.
Alternatively, introduce an admin-only function to update the URI if it needs to be set or changed after deployment.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Index Fun Order Book |
| Report Date | N/A |
| Finders | typicalHuman, 0xeix, axelot, merlin, sakibcy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-10-index-fun-order-book-contest-judging/issues/25
- **Contest**: https://app.sherlock.xyz/audits/contests/1197

### Keywords for Search

`vulnerability`

