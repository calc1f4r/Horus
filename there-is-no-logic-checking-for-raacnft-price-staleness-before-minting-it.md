---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57194
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 123
finders:
  - newspacexyz
  - kkk
  - laxraw
  - rolando
  - holydevoti0n
---

## Vulnerability Title

There is no logic checking for RAACNFT price staleness before minting it

### Overview


This bug report discusses an issue with the RAACNFT::mint function that allows users to mint House NFTs using ERC20 tokens. The function fails to verify if the house prices are current before accepting payment, which could lead to users minting NFTs at potentially outdated prices. This oversight could result in economic security risks, user protection issues, system integrity problems, and market impact. The report recommends implementing price freshness validation and configuration, as well as adding a price freshness view function.

### Original Finding Content

## \[M-05] There is no logic checking for RAACNFT price staleness before minting it

## Summary

The RAACNFT::mint function allows users to mint House NFTs using ERC20 tokens, but it fails to verify if the house prices are current before accepting payment. While the RAACHousePrices contract maintains a lastUpdateTimestamp that updates when prices are refreshed, the mint function doesn't check this timestamp. This oversight could lead to users minting NFTs at potentially outdated prices, as there's no mechanism to ensure price freshness before accepting payment.

## Vulnerability Details

1. Price Verification Flow:
   * Retrieves price from RAACHousePrices contract
   * Checks for zero price and sufficient funds
   * Transfers tokens without price freshness verification
   * No timestamp validation before accepting payment

2. Current Implementation:

```Solidity
function mint(uint256 _tokenId, uint256 _amount) public override {
    uint256 price = raac_hp.tokenToHousePrice(_tokenId);
    if (price == 0) {
        revert RAACNFT__HousePrice();
    }
    if (price > _amount) {
        revert RAACNFT__InsufficientFundsMint();
    }
    //@audit, there is no check whether the price is stall or not,
    // transfer erc20 from user to contract - requires pre-approval from user
    token.safeTransferFrom(msg.sender, address(this), _amount);
    // mint tokenId to user
    _safeMint(msg.sender, _tokenId);
    // If user approved more than necessary, refund the difference
    if (_amount > price) {
        uint256 refundAmount = _amount - price;
        token.safeTransfer(msg.sender, refundAmount);
    }
    emit NFTMinted(msg.sender, _tokenId, price);
}
```

Missing Price Freshness Check:

* No validation of RAACHousePrices.lastUpdateTimestamp
* No consideration of price update intervals
* No mechanism to prevent minting with stale prices

## Impact

The lack of price staleness checking creates several critical issues:

1. Economic Security Risks:
   * Users may mint NFTs at outdated prices
   * Potential for significant financial losses
   * Market manipulation opportunities
   * Inconsistent pricing across transactions

2. User Protection Issues:
   * No way to verify price freshness
   * Users may unknowingly overpay
   * No mechanism to prevent stale price usage
   * Inadequate protection against price manipulation

3. System Integrity Problems:
   * Inconsistent pricing mechanism
   * Potential for price arbitrage
   * Lack of price validation
   * Incomplete security measures

4. Market Impact:
   * Could lead to market inefficiencies
   * May affect NFT pricing dynamics
   * Could create unfair market advantages
   * Potentially destabilizes the market

## Tools Used

Manual Review

## Recommendations

Implement Price Freshness Validation:

```solidity
function mint(uint256 _tokenId, uint256 _amount) public override {
    uint256 price = raac_hp.tokenToHousePrice(_tokenId);
    uint256 lastUpdate = raac_hp.tokenLastUpdateTimestamp(_tokenId);
    
    // Check price freshness
    require(
        block.timestamp - lastUpdate <= MAX_PRICE_STALENESS,
        "RAACNFT__PriceTooStale"
    );
    
    if (price == 0) {
        revert RAACNFT__HousePrice();
    }
    if (price > _amount) {
        revert RAACNFT__InsufficientFundsMint();
    }
    
    token.safeTransferFrom(msg.sender, address(this), _amount);
    _safeMint(msg.sender, _tokenId);
    
    if (_amount > price) {
        uint256 refundAmount = _amount - price;
        token.safeTransfer(msg.sender, refundAmount);
    }
    
    emit NFTMinted(msg.sender, _tokenId, price);
}
```

Implement Price Freshness Configuration:

```Solidity
uint256 public constant MAX_PRICE_STALENESS = 24 hours; // Configurable

function setMaxPriceStaleness(uint256 _newMaxStaleness) public onlyOwner {
    require(_newMaxStaleness > 0, "RAACNFT__InvalidStaleness");
    MAX_PRICE_STALENESS = _newMaxStaleness;
}
```

Add Price Freshness View Function:

```solidity
function getPriceFreshness(uint256 _tokenId) 
    public 
    view 
    returns (
        uint256 price,
        uint256 lastUpdate,
        bool isFresh
    ) {
    price = raac_hp.tokenToHousePrice(_tokenId);
    lastUpdate = raac_hp.tokenLastUpdateTimestamp(_tokenId);
    isFresh = block.timestamp - lastUpdate <= MAX_PRICE_STALENESS;
    return (price, lastUpdate, isFresh);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | newspacexyz, kkk, laxraw, rolando, holydevoti0n, valy001, danielarmstrong, 0xmsf14, skidd0016, kwakudr, elvin_a_block, zukanopro, greese, federodes, dobrevaleri, maze, francohacker, i3arba, aravn, 4rdiii, 0xlouistsai, bigsam, h2134, mizila_firox, princekay, 0xgondar, josh4324, freesultan, 0xdemon, falendar, player, 0xtimefliez, pabloperezacc6, allamloqman, jefextar, x1485967, amarfares, pedrodowsers, 1337web3, vasquez, frerrs, patitonar, 0xyashar, kobbyeugene, eta, akhoronko, ace_30, sovaslava, gajiknownnothing, damilolaedwards, avoloder, biakia, recur, 0xbc000, 0xblockhound, 0xblackadam, 0xhacksmithh, 6ty8ty, minusone, whitekittyhacker, maa_ly, 0xrazb, julianavantgarde, r4bbit, adeolasola01, rampage, sunless_, oldmonk, agbanusijohn, kupiasec, tinnohofficial, 0xdarko, 0xasad97, joicygiore, nomadic_bear, ibukunola, xcrypt, lin0x9a7a, alexczm, kiarash, uddercover, s4muraii77, lamsy, cd_pandora, vs_, 0xalexsr, heliosophistxiv, t0x1c, kvltbyte, satanic_angel_, wekaali4355, 0xisboss, davide, aslanbekaibimov, yas000x, parmakhanm786, igdbaxe, 0xbz, kalii, danzero, 0xterrah, 0xluckyluke, tutkata, 0xmystery, 0xlrivo, oct0pwn, farismaulana, waydou, escrow, orangesantra, 0xaadi |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

