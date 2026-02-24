---
# Core Classification
protocol: Canto Identity Subprotocols
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16185
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-03-canto-identity-subprotocols-contest
source_link: https://code4rena.com/reports/2023-03-canto-identity
github_link: https://github.com/code-423n4/2023-03-canto-identity-findings/issues/209

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
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

[M-05] If the underlying NFT is burned, getPFP may return incorrect results

### Overview


This bug report concerns the ProfilePicture.getPFP() function in the code-423n4/2023-03-canto-identity repository, which can return incorrect information if the underlying NFT is burned. The bug occurs in the following scenario: Alice mints a ProfilePicture NFT (pfp NFT) with the underlying NFT, and later mints a CidNFT by transferring the pfp NFT to the CidNFT contract. Alice does not call AddressRegistry.register to register the CidNFT. Alice then sends the underlying NFT to Bob, who does the same as Alice before. Bob then sells the underlying NFT to Charlie, who burns it. If Alice or Bob calls ProfilePicture.getPFP(), it will return the contract address and ID of the underlying NFT since getAddress() == ownerOf() == address(0). This incorrect result can cause bugs when integrating with other projects.

To mitigate this bug, the code should be changed to the code shown in the Recommended Mitigation Steps section of the report.

### Original Finding Content


ProfilePicture.getPFP will return information about the underlying NFT and when `addressRegistry.getAddress(cidNFTID) ! = ERC721(nftContract).ownerOf(nftID)`, it will return 0.

But if the underlying NFT is burned, getPFP may return incorrect information

```solidity
    function getPFP(uint256 _pfpID) public view returns (address nftContract, uint256 nftID) {
        if (_ownerOf[_pfpID] == address(0)) revert TokenNotMinted(_pfpID);
        ProfilePictureData storage pictureData = pfp[_pfpID];
        nftContract = pictureData.nftContract;
        nftID = pictureData.nftID;
        uint256 cidNFTID = cidNFT.getPrimaryCIDNFT(subprotocolName, _pfpID);
        IAddressRegistry addressRegistry = cidNFT.addressRegistry();
        if (cidNFTID == 0 || addressRegistry.getAddress(cidNFTID) != ERC721(nftContract).ownerOf(nftID)) {
            nftContract = address(0);
            nftID = 0; // Strictly not needed because nftContract has to be always checked, but reset nevertheless to 0
        }
    }
```

Consider the following scenario.

1.  Alice mints a ProfilePicture NFT (pfp NFT) with the underlying NFT, and later mints a CidNFT by transferring the pfp NFT to the CidNFT contract.<br>
    **Noting that alice does not call AddressRegistry.register to register the CidNFT.**<br>
    Since getAddress returns 0, ProfilePicture.getPFP will also return 0.

```solidity
    function getAddress(uint256 _cidNFTID) external view returns (address user) {
        user = ERC721(cidNFT).ownerOf(_cidNFTID);
        if (_cidNFTID != cidNFTs[user]) {
            // User owns CID NFT, but has not registered it
            user = address(0);
        }
    }
```

2.  Alice sends the underlying NFT to Bob, who does what Alice did before.

3.  Bob sold the underlying NFT to Charlie and Charlie burned it for some reason, now if Alice or Bob calls ProfilePicture.getPFP(), it will return the contract address and id of the underlying NFT since `getAddress() == ownerOf() == address(0)`.

When integrating with other projects, there may be bugs because getPFP returns an incorrect result.

### Proof of Concept

<https://github.com/code-423n4/2023-03-canto-identity/blob/077372297fc419ea7688ab62cc3fd4e8f4e24e66/canto-pfp-protocol/src/ProfilePicture.sol#L94-L105><br>
<https://github.com/code-423n4/2023-03-canto-identity/blob/077372297fc419ea7688ab62cc3fd4e8f4e24e66/canto-identity-protocol/src/AddressRegistry.sol#L86-L92>

### Recommended Mitigation Steps

Change to

```diff
    function getPFP(uint256 _pfpID) public view returns (address nftContract, uint256 nftID) {
        if (_ownerOf[_pfpID] == address(0)) revert TokenNotMinted(_pfpID);
        ProfilePictureData storage pictureData = pfp[_pfpID];
        nftContract = pictureData.nftContract;
        nftID = pictureData.nftID;
        uint256 cidNFTID = cidNFT.getPrimaryCIDNFT(subprotocolName, _pfpID);
        IAddressRegistry addressRegistry = cidNFT.addressRegistry();
-       if (cidNFTID == 0 || addressRegistry.getAddress(cidNFTID) != ERC721(nftContract).ownerOf(nftID)) {
+       if (cidNFTID == 0 || ERC721(nftContract).ownerOf(nftID) == 0 || addressRegistry.getAddress(cidNFTID) != ERC721(nftContract).ownerOf(nftID)) {
            nftContract = address(0);
            nftID = 0; // Strictly not needed because nftContract has to be always checked, but reset nevertheless to 0
        }
    }
```

**[OpenCoreCH (Canto Identity) confirmed and commented](https://github.com/code-423n4/2023-03-canto-identity-findings/issues/209#issuecomment-1489270847):**
 > Very interesting edge case, enjoyed reading it! For an ERC721 compliant NFT this is not the case, because the standard explicitly says:
> ```
>     /// @dev NFTs assigned to zero address are considered invalid, and queries
>     ///  about them do throw.
> ```
> Therefore, the existing `ownerOf` will throw.
> 
> However, in my experience there are some NFTs that do not adhere strictly to ERC721 when it comes to this. Because of that, I'll still implement a fix for this.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto Identity Subprotocols |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2023-03-canto-identity
- **GitHub**: https://github.com/code-423n4/2023-03-canto-identity-findings/issues/209
- **Contest**: https://code4rena.com/contests/2023-03-canto-identity-subprotocols-contest

### Keywords for Search

`vulnerability`

