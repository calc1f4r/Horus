---
# Core Classification
protocol: Open Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29357
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-opendollar
source_link: https://code4rena.com/reports/2023-10-opendollar
github_link: https://github.com/code-423n4/2023-10-opendollar-findings/issues/243

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
finders_count: 3
finders:
  - kutugu
  - twcctop
  - Haipls
---

## Vulnerability Title

[M-09] Vault721.tokenURI does not comply with ERC721 - Metadata specification

### Overview


This bug report is regarding the `tokenURI` method in the Vault721 contract. According to the Ethereum Improvement Proposal (EIP) 721, this method must be reverted if a non-existent tokenId is passed. However, the Vault721 contract does not follow the specification, leading to a violation of the EIP721 spec.

Tools used to identify this bug include the EIP721 spec. The recommended mitigation step is to add a token existence check at the Vault721 level. This bug was identified by MiloTruck and confirmed by pi0neerpat. The impact is limited, and the severity is medium.

### Original Finding Content


According to the standard, the `tokenURI` method must be reverted if a non-existent tokenId is passed. In the Vault721 contract, this point was ignored. What leads to a [violation of the EIP721 spec](https://eips.ethereum.org/EIPS/eip-721#:\~:text=function%20tokenURI\(uint256%20\_tokenId\)%20external%20view%20returns%20\(string\)%3B).

### Proof of Concept

<https://github.com/open-dollar/od-contracts/blob/v1.5.5-audit/src/contracts/proxies/Vault721.sol#L140-L142>

```js
File: contracts/proxies/Vault721.sol

  /**
   * @dev generate URI with updated vault information
   */
  function tokenURI(uint256 _safeId) public view override returns (string memory uri) {
    // @audit should throw if safeId does not exist according to the ERC721-Metadata specification
    uri = nftRenderer.render(_safeId);
  }
```

The responsibility for checking whether a token exists may be put on the nftRenderer depending on the implementation, and may also be missing, changed or added in the future. But the underlying Vault721 contract that is supposed to comply with the standard does not follow the specification.

Similar problem with violation of ERC721 specification: <https://github.com/code-423n4/2023-04-caviar-findings/issues/44>

### Tools Used

<https://eips.ethereum.org/EIPS/eip-721#specification>

### Recommended Mitigation Steps

Add a token existence check at the Vault721 level, example:

```js
  /**
   * @dev generate URI with updated vault information
   */
  function tokenURI(uint256 _safeId) public view override returns (string memory uri) {
+++ _requireMinted(_safeId);
    uri = nftRenderer.render(_safeId);
  }

```

**[MiloTruck (Judge) commented](https://github.com/code-423n4/2023-10-opendollar-findings/issues/243#issuecomment-1789731499):**
 > Although the impact is extremely limited, the function does violate the ERC-721 spec as shown [here](https://eips.ethereum.org/EIPS/eip-721#:~:text=function%20tokenURI(uint256%20_tokenId)%20external%20view%20returns%20(string)%3B). As such, I agree with Medium Severity.

**[pi0neerpat (OpenDollar) commented](https://github.com/code-423n4/2023-10-opendollar-findings/issues/243#issuecomment-1805207884):**
 > This is a valid finding and recommendation is accurate.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Open Dollar |
| Report Date | N/A |
| Finders | kutugu, twcctop, Haipls |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-opendollar
- **GitHub**: https://github.com/code-423n4/2023-10-opendollar-findings/issues/243
- **Contest**: https://code4rena.com/reports/2023-10-opendollar

### Keywords for Search

`vulnerability`

