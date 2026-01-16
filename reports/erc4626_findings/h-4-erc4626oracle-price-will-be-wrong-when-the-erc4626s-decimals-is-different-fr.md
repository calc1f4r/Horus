---
# Core Classification
protocol: Sentiment
chain: everychain
category: uncategorized
vulnerability_type: erc4626

# Attack Vector Details
attack_type: erc4626
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3352
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1
source_link: none
github_link: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/025-H

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - erc4626
  - decimals

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - 0x52
  - Bahurum
  - WATCHPUG
  - berndartmueller
  - Lambda
---

## Vulnerability Title

H-4: `ERC4626Oracle` Price will be wrong when the ERC4626's `decimals` is different from the underlying token’s decimals

### Overview


This bug report concerns a malfunction in the `ERC4626Oracle` when the decimals of the ERC4626 is different from the underlying token's decimals. This issue was found by Lambda, JohnSmith, WATCHPUG, 0x52, berndartmueller, and Bahurum. The current implementation uses `IERC4626(token).decimals()` as the `IERC4626(token).asset()`'s decimals to calculate the ERC4626's price, however, EIP-4626 does not require the decimals must be the same as the underlying token’s decimals. This causes the price of ERC4626 to be significantly underestimated when the underlying token's decimals > ERC4626's decimals, and be significantly overestimated when the underlying token's decimals < ERC4626's decimals. The Sentiment Team fixed the issue as recommended and Lead Senior Watson confirmed the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/025-H 
## Found by 
Lambda, JohnSmith, WATCHPUG, 0x52, berndartmueller, Bahurum

## Summary

EIP-4626 does not require the decimals must be the same as the underlying tokens' decimals, and when it's not, `ERC4626Oracle` will malfunction.

## Vulnerability Detail

In the current implementation, `IERC4626(token).decimals()` is used as the `IERC4626(token).asset()`'s decimals to calculate the ERC4626's price.

However, while most ERC4626s are using the underlying token’s decimals as `decimals`, there are some ERC4626s use a different decimals from underlying token’s decimals since EIP-4626 does not require the decimals must be the same as the underlying token’s decimals:

> Although the convertTo functions should eliminate the need for any use of an EIP-4626 Vault’s decimals variable, it is still strongly recommended to mirror the underlying token’s decimals if at all possible, to eliminate possible sources of confusion and simplify integration across front-ends and for other off-chain users.

Ref: https://eips.ethereum.org/EIPS/eip-4626

## Impact

The price of ERC4626 will be significantly underestimated when the underlying token's decimals > ERC4626's decimals, and be significantly overestimated when the underlying token's decimals < ERC4626's decimals.

## Code Snippet

https://github.com/sentimentxyz/oracle/blob/59b26a3d8c295208437aad36c470386c9729a4bc/src/erc4626/ERC4626Oracle.sol#L35-L43

```solidity
    function getPrice(address token) external view returns (uint) {
        uint decimals = IERC4626(token).decimals();
        return IERC4626(token).previewRedeem(
            10 ** decimals
        ).mulDivDown(
            oracleFacade.getPrice(IERC4626(token).asset()),
            10 ** decimals
        );
    }
```

## Tool used

Manual Review

## Recommendation

`getPrice()` can be changed to:

```solidity
    function getPrice(address token) external view returns (uint) {
        uint decimals = IERC4626(token).decimals();
        address underlyingToken = IERC4626(token).asset();
        return IERC4626(token).previewRedeem(
            10 ** decimals
        ).mulDivDown(
            oracleFacade.getPrice(underlyingToken),
            10 ** IERC20Metadata(underlyingToken).decimals()
        );
    }
```
## Sentiment Team
Fixed as recommended. PR [here](https://github.com/sentimentxyz/oracle/pull/34).

## Lead Senior Watson
Confirmed fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment |
| Report Date | N/A |
| Finders | 0x52, Bahurum, WATCHPUG, berndartmueller, Lambda, JohnSmith |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/025-H
- **Contest**: https://app.sherlock.xyz/audits/contests/1

### Keywords for Search

`ERC4626, Decimals`

