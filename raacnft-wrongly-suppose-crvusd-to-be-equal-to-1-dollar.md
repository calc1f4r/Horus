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
solodit_id: 57305
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
finders_count: 8
finders:
  - s4muraii77
  - 0rpseqwe
  - 0xalexsr
  - t0x1c
  - 0xgremlincat
---

## Vulnerability Title

RAACNFT wrongly suppose crvUSD to be equal to 1 dollar 

### Overview


The RAACNFT protocol has a bug where it assumes that the value of crvUSD is always equal to 1 USD. However, historical data shows that this is not always the case. This bug can have a high impact on users, as they may end up paying more or less than the actual value of the house. The report recommends adding another oracle to calculate the crvUSD-USD exchange rate and using it in house price calculations.

### Original Finding Content

## Summary

RAACNFT mint is done with crvUSD and house price is returned in USD thus expecting a crvUSD price of 1 USD which won't be the case during depeg.

## Vulnerability Details

Looking on `crvUSD` price history on \[coinmarketcap]\(<https://coinmarketcap.com/currencies/crvusd/>), we can see that it is rarely worth exactly 1 USD

US average home price is \~\$400k. A 0.5% difference would represents a \$2k difference

in RAACNFT::mint

```Solidity
    function mint(uint256 _tokenId, uint256 _amount) public override {
        uint256 price = raac_hp.tokenToHousePrice(_tokenId);
        if(price == 0) { revert RAACNFT__HousePrice(); }
        if(price > _amount) { revert RAACNFT__InsufficientFundsMint(); }

        token.safeTransferFrom(msg.sender, address(this), _amount);
      ...
    }
```

price is the amount to be paid in crvToken by the user.

The price is retrieved from raac\_hp.tokenToHousePrice(tokenId)

in RAACHousePrices, tokenToHousePrice mapping is set via the `setHousePrice` function

```Solidity
    /// @notice Mapping from RAAC tokenId to house price in USD
    mapping(uint256 => uint256) public tokenToHousePrice;

    function setHousePrice(
        uint256 _tokenId,
        uint256 _amount
    ) external onlyOracle {
        tokenToHousePrice[_tokenId] = _amount;
        lastUpdateTimestamp = block.timestamp;
        emit PriceUpdated(_tokenId, _amount);
    }
```

As mentionned in the comment, house price is in USD not in crvUSD.

The house price is set by the RAACHousePriceOracle which is likely to be in USD making the comment reliable.

At not point in the flow, the USD value is converted to crvUSD, thus the protocol expects a 1-1 exchange rate between USD and crvUSD.

## Impact

Users won't pay the real USD value of the houses price but a crvUSD value which can sometimes be beneficial for the users and sometimes no.

The protocol makes the  assumption that crvUSD-USD exchange rate is 1-1 and that it will always remain the same, during peak market volatility the exchange rate impact can be even higher especially considering the low marketcap of crvUSD being only around 74m.

The impact is high and the likelihood is high considering the price history where price is rarely 1-1 between crvUSD and USD

## Recommendations

Add another oracle for the crvUSD-USD exchange rate and used the exchange rate in house price calculations for users to spend an amount in crvUSD.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | s4muraii77, 0rpseqwe, 0xalexsr, t0x1c, 0xgremlincat, tadev, pronobis4, dobrevaleri |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

