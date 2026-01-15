---
# Core Classification
protocol: ArkProject: NFT Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38513
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clz2gpi0o000ps6nj8stws2bd
source_link: none
github_link: https://github.com/Cyfrin/2024-07-ark-project

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
  - haxatron
  - Draiakoo
---

## Vulnerability Title

Starknet bridge contract does not check if the collection supports IERC721Metadata interface, so the ones that do not implement it will not be able to bridge NFTs

### Overview

The Starknet bridge contract currently does not check if a collection supports the IERC721Metadata interface before attempting to bridge NFTs from that collection. This means that collections that do not implement this interface will not be able to be bridged from Starknet to Ethereum. This is a medium risk issue, as it affects the functionality of the bridge for certain collections. To fix this, a check should be implemented to ensure that the collection supports the interface before attempting to bridge NFTs. This can be done manually through a review of the code. 

### Original Finding Content

## Summary

Starknet bridge contract does not check if the collection supports IERC721Metadata interface, so the ones that do not implement it will not be able to bridge NFTs

## Vulnerability Details

In the Ethereum bridge, when a user deposits an NFT it is needed to get the name, symbol, baseURI and tokenURIs from the specific collection. To do that, it first checks if the contract collection supports this interface.

```Solidity
    function erc721Metadata(
        address collection,
        uint256[] memory tokenIds
    )
        internal
        view
        returns (string memory, string memory, string memory, string[] memory)
    {        
        bool supportsMetadata = ERC165Checker.supportsInterface(
            collection,
            type(IERC721Metadata).interfaceId
        );
        
        if (!supportsMetadata) {
            return ("", "", "", new string[](0));
        }

        IERC721Metadata c = IERC721Metadata(collection);
        // How the URI must be handled.
        // if a base URI is already present, we ignore individual URI
        // else, each token URI must be bridged and then the owner of the collection
        // can decide what to do
        (bool success, string memory _baseUri) = _callBaseUri(collection);
        if (success) {
            return (c.name(), c.symbol(), _baseUri, new string[](0));
        }
        else {
            string[] memory URIs = new string[](tokenIds.length);
            for (uint256 i = 0; i < tokenIds.length; i++) {
                URIs[i] = c.tokenURI(tokenIds[i]);
            }
            return (c.name(), c.symbol(), "", URIs);
        }
    }
```

As we can see, if the collection does not support this interface it is returned all fields empty. Otherwise, the functions to retrieve all the informations are called.

However, in the Starknet bridge, no interface is checked and the functions to retrieve all these informations are called directly.

```Solidity
fn erc721_metadata(
    contract_address: ContractAddress,
    token_ids: Option<Span<u256>>
) -> Option<ERC721Metadata> {
    let erc721 = IERC721Dispatcher { contract_address };

    ...

    Option::Some(
        ERC721Metadata {
            name: erc721.name(),
            symbol: erc721.symbol(),
            base_uri: "",
            uris
        }
    )
}
```

This missing check for the interface will make NFT collections that do not implement the IERC721Metadata interface unable to be bridged because these functions will not exist and the transaction will revert.

Note that the IERC721Metadata is an OPTIONAL interface as stated in the EIP:

> The metadata extension is OPTIONAL for ERC-721 smart contracts (see “caveats”, below). This allows your smart contract to be interrogated for its name and for details about the assets which your NFTs represent.

That means that a collection will be ERC721 compliant even though it does not implement the IERC721Metadata interface. But will be unable to work with the Starknet bridge.

## Impact

Medium, collections that do not implement this interface will be unable to be bridge from Starknet to Ethereum

## Tools Used

Manual review

## Recommendations

Check if the collection supports the interface before calling these methods just as the Ethereum bridge does

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | ArkProject: NFT Bridge |
| Report Date | N/A |
| Finders | haxatron, Draiakoo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-ark-project
- **Contest**: https://codehawks.cyfrin.io/c/clz2gpi0o000ps6nj8stws2bd

### Keywords for Search

`vulnerability`

