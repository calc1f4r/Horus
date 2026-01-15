---
# Core Classification
protocol: Sei EVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47387
audit_firm: OtterSec
contest_link: https://www.sei.io/
source_link: https://www.sei.io/
github_link: https://github.com/sei-protocol

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
finders_count: 2
finders:
  - James Wang
  - Naoya Okanami
---

## Vulnerability Title

Missing Ownership Verification

### Overview


The CW721ERC721Pointer::transferFrom function does not check if the provided from address is the true owner of the token being transferred, which is a crucial step in the ERC721 standard. Instead, it uses a different authorization mechanism through sendNft, which does not explicitly validate ownership. This could lead to confusion for contracts that handle ERC721 through the precompiled contract. The issue has been fixed in version 1017882 and it is recommended to assert that from owns the non-fungible token for CW721ERC721Pointer::transferFrom.

### Original Finding Content

## CW721ERC721Pointer::transferFrom Issues

The `CW721ERC721Pointer::transferFrom` method lacks a check to verify whether the provided `from` address is the true owner of the token being transferred. In the ERC721 standard, this verification step is crucial to ensure that only the rightful owner may transfer their non-fungible tokens. Instead of directly verifying ownership, the CW721 standard employs a different authorization mechanism through `sendNft`. While this method confirms if the caller is authorized to manage the non-fungible token, it does not explicitly validate ownership.

> _sei-chain/contracts/src/CW721ERC721Pointer.sol Solidity_

```solidity
function transferFrom(address from, address to, uint256 tokenId) public override {
    if (to == address(0)) {
        revert ERC721InvalidReceiver(address(0));
    }
    string memory recipient = _formatPayload("recipient", _doubleQuotes(AddrPrecompile.getSeiAddr(to)));
    string memory tId = _formatPayload("token_id", _doubleQuotes(Strings.toString(tokenId)));
    string memory req = _curlyBrace(_formatPayload("transfer_nft", _curlyBrace(_join(recipient, tId, ","))));
    _execute(bytes(req));
    emit Transfer(from, to, tokenId);
}
```

Without the ownership verification step, there may exist a mismatch between the specified `tokenId` and `owner`, resulting in confusion for EVM contracts that handle ERC721 through the precompiled contract.

## Remediation
Assert that `from` owns the non-fungible token for `CW721ERC721Pointer.transferFrom`.

## Patch
Fixed in 1017882.

© 2024 Otter Audits LLC. All Rights Reserved. 20/37

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sei EVM |
| Report Date | N/A |
| Finders | James Wang, Naoya Okanami |

### Source Links

- **Source**: https://www.sei.io/
- **GitHub**: https://github.com/sei-protocol
- **Contest**: https://www.sei.io/

### Keywords for Search

`vulnerability`

