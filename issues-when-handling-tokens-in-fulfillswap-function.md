---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49965
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - zukanopro
  - bube
---

## Vulnerability Title

Issues when handling tokens in `fulfillSwap()` function

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Details

In `StabilityBranch#fulfillSwap()`function, it use Chainlink's Data Stream to verify price:

```Solidity
    //@note https://docs.chain.link/data-streams/reference/interfaces
    function verifyOffchainPrice(Data storage self, bytes memory priceData) internal returns (UD60x18 priceX18) {
        bytes memory reportData = ChainlinkUtil.getReportData(priceData);

        IVerifierProxy chainlinkVerifier = self.chainlinkVerifier;
        (FeeAsset memory fee) = ChainlinkUtil.getEthVericationFee(chainlinkVerifier, reportData);
        bytes memory verifiedPricetData = ChainlinkUtil.verifyReport(chainlinkVerifier, fee, priceData);

        PremiumReport memory premiumReport = abi.decode(verifiedPricetData, (PremiumReport));

        if (block.timestamp > premiumReport.validFromTimestamp + self.maxVerificationDelay) {
            revert Errors.DataStreamReportExpired();
        }

        priceX18 = ud60x18(int256(premiumReport.price).toUint256());
    }
```

From scope, these tokens are supported:

```Solidity
  - ETH
  - WETH
  - WEETH
  - WSTETH
  - WBTC
  - USDC
  - USDT
  - USDE
  - SUSDE
```

But there are 2 problems at here:

* SUSDE and WEETH token do not exist in data stream, lead to unable to verify price of these tokens. WBTC do not have also, but we should not assume WBTC = BTC, because [WBTC has depegged down to 0.98 before](https://thedefiant.io/wbtc-depeg)
* Assuming all price returned have 18 decimals:

  ```Solidity
  // get price from report in 18 dec
  ctx.priceX18 = stabilityConfiguration.verifyOffchainPrice(priceData);
  ```

Despite with some tokens in scope that already have data stream feeds, its deciamls is 18 already, but with token mentioned above, its price can be 8 decimals when data stream's feed created because price decimals could be 8 or 18 [link](https://docs.chain.link/data-streams/getting-started#examine-the-code):

```Solidity
struct ReportV3 {
    bytes32 feedId; // The stream ID the report has data for.
    uint32 validFromTimestamp; // Earliest timestamp for which price is applicable.
    uint32 observationsTimestamp; // Latest timestamp for which price is applicable.
    uint192 nativeFee; // Base cost to validate a transaction using the report, denominated in the chain’s native token (e.g., WETH/ETH).
    uint192 linkFee; // Base cost to validate a transaction using the report, denominated in LINK.
    uint32 expiresAt; // Latest timestamp where the report can be verified onchain.
    int192 price; // DON consensus median price (8 or 18 decimals).    // <--
    int192 bid; // Simulated price impact of a buy order up to the X% depth of liquidity utilisation (8 or 18 decimals).
    int192 ask; // Simulated price impact of a sell order up to the X% depth of liquidity utilisation (8 or 18 decimals).
}
```

## Impact

Some token in scope could not be used to fulfill swap, and its price can have wrong decimals if its data stream is created later

## Recommendations

Currently,dont interact with token that do not have data stream feeds, and do not assume its price is always 18 decimals.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | zukanopro, bube |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

