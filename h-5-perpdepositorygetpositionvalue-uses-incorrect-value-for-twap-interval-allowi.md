---
# Core Classification
protocol: UXD Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6592
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/33
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/249

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - services
  - derivatives
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - DecorativePineapple
  - 0x52
  - cccz
  - berndartmueller
  - 0Kage
---

## Vulnerability Title

H-5: PerpDepository#getPositionValue uses incorrect value for TWAP interval allowing more than intended funds to be extracted

### Overview


This bug report is about an issue found in the PerpDepository#getPositionValue function which queries the exchange for the mark price to calculate the unrealized PNL. The issue is that it uses the 15 second TWAP instead of the 15 minute TWAP, as defined in the documentation and the ClearHouseConfig contract. This means the mark price and by extension the position value will frequently be different from the true mark price of the market, allowing for larger rebalances than should be possible. The bug was found by berndartmueller, DecorativePineapple, cccz, HonorLt, 0x52, ctf\_sec, and 0Kage. The code snippet which shows the bug can be found at https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L708-L713. The recommended fix is to pull the TWAP fresh each time from ClearingHouseConfig, or make it a constant and change it from 15 to 900. The fix was proposed by hrishibhat and was accepted by IAm0x52.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/249 

## Found by 
berndartmueller, DecorativePineapple, cccz, HonorLt, 0x52, ctf\_sec, 0Kage

## Summary

PerpDepository#getPositionValue queries the exchange for the mark price to calculate the unrealized PNL. Mark price is defined as the 15 minute TWAP of the market. The issue is that it uses the 15 second TWAP instead of the 15 minute TWAP

## Vulnerability Detail

As stated in the [docs](https://support.perp.com/hc/en-us/articles/5331299807513-Liquidation) and as implemented in the [ClearHouseConfig](https://optimistic.etherscan.io/address/0xa4c817a425d3443baf610ca614c8b11688a288fb#readProxyContract) contract, the mark price is a 15 minute / 900 second TWAP.

    function getPositionValue() public view returns (uint256) {
        uint256 markPrice = getMarkPriceTwap(15);
        int256 positionSize = IAccountBalance(clearingHouse.getAccountBalance())
            .getTakerPositionSize(address(this), market);
        return markPrice.mulWadUp(_abs(positionSize));
    }

    function getMarkPriceTwap(uint32 twapInterval)
        public
        view
        returns (uint256)
    {
        IExchange exchange = IExchange(clearingHouse.getExchange());
        uint256 markPrice = exchange
            .getSqrtMarkTwapX96(market, twapInterval)
            .formatSqrtPriceX96ToPriceX96()
            .formatX96ToX10_18();
        return markPrice;
    }

As seen in the code above getPositionValue uses 15 as the TWAP interval. This means it is pulling a 15 second TWAP rather than a 15 minute TWAP as intended.

## Impact

The mark price and by extension the position value will frequently be different from true mark price of the market allowing for larger rebalances than should be possible.

## Code Snippet

https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L708-L713

## Tool used

Manual Review

## Recommendation

I recommend pulling pulling the TWAP fresh each time from ClearingHouseConfig, because the TWAP can be changed at anytime. If it is desired to make it a constant then it should at least be changed from 15 to 900.

## Discussion

**hrishibhat**

Fix: https://github.com/UXDProtocol/uxd-evm/pull/21


**IAm0x52**

Fix looks good. TWAP corrected from 15 to 900

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | UXD Protocol |
| Report Date | N/A |
| Finders | DecorativePineapple, 0x52, cccz, berndartmueller, 0Kage, HonorLt, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/249
- **Contest**: https://app.sherlock.xyz/audits/contests/33

### Keywords for Search

`vulnerability`

