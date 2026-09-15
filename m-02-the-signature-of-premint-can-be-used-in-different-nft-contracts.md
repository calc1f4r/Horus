---
# Core Classification
protocol: Harvestflowv2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55529
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarvestFlowV2-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-02] The Signature of `preMint()` Can Be Used in Different NFT Contracts

### Overview


The bug report states that there is a problem with the `preMint()` function in the code. The function uses a signature verification process to ensure that the caller is authorized to mint a specific amount of tokens. However, the signature does not include the NFT address, which means that it can be used in other contracts as well. This is a medium risk bug as it can lead to unexpected behavior. The team has fixed the issue by adding the contract address in the signature's parameters.

### Original Finding Content

## Severity

Medium Risk

## Description

In `preMint()`, the signature is verified through `_verifyAddressSigner()`, with the parameters of the signature being `msg.sender` and `maxMintAmount`:

```solidity
/// @notice Verify the `signature` is a hash of `msg.sender` and `maxMintAmount`, signed by the `signerAddress`.
function _verifyAddressSigner(bytes memory signature, uint256 maxMintAmount) internal view {
    bytes32 hash = keccak256(abi.encodePacked(msg.sender, maxMintAmount));
    if (hash.recover(signature) != signerAddress) {
        revert InvalidSignature();
    }
}
```

The problem here lies in the lack of the NFT address in the signature parameters. Since multiple NFTs could exist in this protocol, the signature might be replayed across other NFT contracts.

For example:

1. Alice, as the owner and signer, created two NFTs.
2. She wanted Bob to participate in the `preMint()` of NFT1, so she generated a signature for Bob.
3. Since the signature does not include the NFT address, Bob can use the same signature to participate in the `preMint()` of NFT2 as well, which does not meet Alice's expectations.

## Location of Affected Code

File: [LendingNFT.sol#L601-L607](https://github.com/tokyoweb3/HARVESTFLOW_Ver.2/blob/05f0814caa51dcb034dd01f610315d4c6efedce8/contracts/src/LendingNFT.sol#L601-L607)

## Impact

The signature of `preMint()` can be used in different NFT contracts, which may not meet the signer's expectations.

## Recommendation

Add the contract address in the signature's parameter.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Harvestflowv2 |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarvestFlowV2-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

