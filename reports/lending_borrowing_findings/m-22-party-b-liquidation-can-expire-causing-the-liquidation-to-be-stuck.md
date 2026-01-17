---
# Core Classification
protocol: Symmetrical
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21223
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/85
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-symmetrical-judging/issues/293

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
finders_count: 14
finders:
  - cergyk
  - panprog
  - sinarette
  - Ch\_301
  - volodya
---

## Vulnerability Title

M-22: Party B liquidation can expire, causing the liquidation to be stuck

### Overview


This bug report is about an issue found in the LiquidationFacetImpl library of the SYMM-IO project. The issue is that the liquidation of Party B can get stuck if the liquidation timeout is reached and the positions are not liquidated within the timeout period. This is due to the signature verification process that requires the signature to be created within the liquidation timeout period. If the signature is created beyond the liquidation timeout, the signature is treated as expired, resulting in the liquidation function to revert and rendering the liquidation of Party B stuck. This issue impacts Party A's locked balance which is not decremented by the liquidatable position and Party B's liquidations status is stuck and remains set to `true`, resulting in the `notLiquidated` and `notLiquidatedPartyB` modifiers to revert. The tool used to find this issue was manual review. A recommendation was given to add functionality to reset the liquidation status of Party B once the liquidation timeout is reached. A fixed code PR link was also provided.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-symmetrical-judging/issues/293 

## Found by 
Ch\_301, Kose, Yuki, berndartmueller, bin2chen, cergyk, josephdara, libratus, panprog, shaka, simon135, sinarette, volodya, xiaoming90
## Summary

The liquidation of Party B can get stuck if the liquidation timeout is reached and the positions are not liquidated within the timeout period.

## Vulnerability Detail

The insolvent Party B's positions are liquidated by the liquidator via the `liquidatePositionsPartyB` function in the `LiquidationFacetImpl` library. This function requires supplying the `QuotePriceSig memory priceSig` parameter, which includes a timestamp and a signature from the Muon app. The signature is verified to ensure the `priceSig` values were actually fetched by the trusted Muon app.

The signature is expected to be created within the liquidation timeout period. This is verified through the validation of the `priceSig.timestamp`, as seen in lines 318-322. Failure to do so, i.e., providing a signature that's created beyond the liquidation timeout, results in the signature being treated as expired, thereby causing the function to revert and rendering the liquidation of Party B stuck.

## Impact

Party A's [locked balance is not decremented by the liquidatable position](https://github.com/sherlock-audit/2023-06-symmetrical/blob/main/symmio-core/contracts/facets/liquidation/LiquidationFacetImpl.sol#L348). Party B's liquidations status is stuck and remains set to `true`, resulting in the `notLiquidated` and `notLiquidatedPartyB` modifiers to revert.

## Code Snippet

[contracts/facets/liquidation/LiquidationFacetImpl.sol#L318-L322](https://github.com/sherlock-audit/2023-06-symmetrical/blob/main/symmio-core/contracts/facets/liquidation/LiquidationFacetImpl.sol#L318-L322)

```solidity
308: function liquidatePositionsPartyB(
309:     address partyB,
310:     address partyA,
311:     QuotePriceSig memory priceSig
312: ) internal {
313:     AccountStorage.Layout storage accountLayout = AccountStorage.layout();
314:     MAStorage.Layout storage maLayout = MAStorage.layout();
315:     QuoteStorage.Layout storage quoteLayout = QuoteStorage.layout();
316:
317:     LibMuon.verifyQuotePrices(priceSig);
318: @>  require(
319: @>      priceSig.timestamp <=
320: @>          maLayout.partyBLiquidationTimestamp[partyB][partyA] + maLayout.liquidationTimeout,
321: @>      "LiquidationFacet: Expired signature"
322: @>  );
323:     require(
324:         maLayout.partyBLiquidationStatus[partyB][partyA],
325:         "LiquidationFacet: PartyB is solvent"
326:     );
327:     require(
328:         block.timestamp <= priceSig.timestamp + maLayout.liquidationTimeout,
329:         "LiquidationFacet: Expired price sig"
330:     );
```

## Tool used

Manual Review

## Recommendation

Consider adding functionality to reset the liquidation status (i.e., `maLayout.partyBLiquidationStatus[partyB][partyA] = false` and `maLayout.partyBLiquidationTimestamp[partyB][partyA] = 0`) of Party B once the liquidation timeout is reached.




## Discussion

**MoonKnightDev**

Fixed code PR link:
https://github.com/SYMM-IO/symmio-core/pull/9

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Symmetrical |
| Report Date | N/A |
| Finders | cergyk, panprog, sinarette, Ch\_301, volodya, simon135, josephdara, Yuki, bin2chen, Kose, xiaoming90, berndartmueller, shaka, libratus |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-symmetrical-judging/issues/293
- **Contest**: https://app.sherlock.xyz/audits/contests/85

### Keywords for Search

`vulnerability`

