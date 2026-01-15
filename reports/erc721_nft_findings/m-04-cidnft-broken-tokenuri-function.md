---
# Core Classification
protocol: Canto Identity Protocol
chain: everychain
category: uncategorized
vulnerability_type: abi_encoding

# Attack Vector Details
attack_type: abi_encoding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8872
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-canto-identity-protocol-contest
source_link: https://code4rena.com/reports/2023-01-canto-identity
github_link: https://github.com/code-423n4/2023-01-canto-identity-findings/issues/89

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4.0216169476869865

# Context Tags
tags:
  - abi_encoding
  - erc721
  - 0x

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - horsefacts
---

## Vulnerability Title

[M-04] `CidNFT`: Broken `tokenURI` function

### Overview


This bug report is regarding an issue in the CidNFT smart contract. The vulnerability is that the uint256 _id argument is not converted to a string before being interpolated into the token URI. This means that the raw bytes of the 32-byte ABI encoded integer _id will be interpolated into the token URI, resulting in malformed, incorrect, or invalid URIs. The impact of this is that the CidNFT tokens will have invalid tokenURI's. This can lead to offchain tools that read the tokenURI view breaking or displaying malformed data.

The suggested solution is to convert the _id to a string before calling abi.encodePacked. This can be done using the LibString helper library included in the latest version of Solmate. A test case has been provided to demonstrate the issue.

In conclusion, this bug report covers a vulnerability in the CidNFT smart contract, which can lead to invalid tokenURI's. The suggested solution is to convert the _id to a string before calling abi.encodePacked using the LibString helper library.

### Original Finding Content


[`CidNFT#tokenURI`](https://github.com/code-423n4/2023-01-canto-identity/blob/dff8e74c54471f5f3b84c217848234d474477d82/src/CidNFT.sol#L133-L142) does not convert the `uint256 _id` argument to a string before interpolating it in the token URI:

```solidity
    /// @notice Get the token URI for the provided ID
    /// @param _id ID to retrieve the URI for
    /// @return tokenURI The URI of the queried token (path to a JSON file)
    function tokenURI(uint256 _id) public view override returns (string memory) {
        if (ownerOf[_id] == address(0))
            // According to ERC721, this revert for non-existing tokens is required
            revert TokenNotMinted(_id);
        return string(abi.encodePacked(baseURI, _id, ".json"));
    }

```

This means the raw bytes of the 32-byte ABI encoded integer `_id` will be interpolated into the token URI, e.g. `0x0000000000000000000000000000000000000000000000000000000000000001` for ID `#1`.

Most of the resulting UTF-8 strings will be malformed, incorrect, or invalid URIs. For example, token ID `#1` will show up as the invisible "start of heading" control character, and ID `#42` will show as the asterisk symbol `*`. URI-unsafe characters will break the token URIs altogether.

### Impact

*   `CidNFT` tokens will have invalid `tokenURI`s. Offchain tools that read the `tokenURI` view may break or display malformed data.

### Suggestion

Convert the `_id` to a string before calling `abi.encodePacked`. Latest Solmate includes a `LibString` helper library for this purpose:

```solidity
    import "solmate/utils/LibString.sol";

    /// @notice Get the token URI for the provided ID
    /// @param _id ID to retrieve the URI for
    /// @return tokenURI The URI of the queried token (path to a JSON file)
    function tokenURI(uint256 _id) public view override returns (string memory) {
        if (ownerOf[_id] == address(0))
            // According to ERC721, this revert for non-existing tokens is required
            revert TokenNotMinted(_id);
        return string(abi.encodePacked(baseURI, LibString.toString(_id), ".json"));
    }

```

### Test case

```solidity
    function test_InvalidTokenURI() public {
        uint256 id1 = cidNFT.numMinted() + 1;
        uint256 id2 = cidNFT.numMinted() + 2;
        // mint id1
        cidNFT.mint(new bytes[](0));
        // mint id2
        cidNFT.mint(new bytes[](0));

        // These pass — the raw bytes '0000000000000000000000000000000000000000000000000000000000000001' are interpolated as _id.
        assertEq(string(bytes(hex"7462643a2f2f626173655f7572692f00000000000000000000000000000000000000000000000000000000000000012e6a736f6e")), cidNFT.tokenURI(id1));
        assertEq(string(bytes(hex"7462643a2f2f626173655f7572692f00000000000000000000000000000000000000000000000000000000000000022e6a736f6e")), cidNFT.tokenURI(id2));

        // These fail - the generated string on the right is not the expected string on the left. 
        assertEq("tbd://base_uri/1.json", cidNFT.tokenURI(id1));
        assertEq("tbd://base_uri/2.json", cidNFT.tokenURI(id2));
    }
```

**[OpenCoreCH (Canto Identity) confirmed and commented](https://github.com/code-423n4/2023-01-canto-identity-findings/issues/89#issuecomment-1426179080):**
 > Great catch!



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4.0216169476869865/5 |
| Audit Firm | Code4rena |
| Protocol | Canto Identity Protocol |
| Report Date | N/A |
| Finders | horsefacts |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-canto-identity
- **GitHub**: https://github.com/code-423n4/2023-01-canto-identity-findings/issues/89
- **Contest**: https://code4rena.com/contests/2023-01-canto-identity-protocol-contest

### Keywords for Search

`ABI Encoding, ERC721, 0x`

