---
# Core Classification
protocol: Umee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16900
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Paweł Płatek
  - Dominik Czarnota
---

## Vulnerability Title

Incorrect price assumption in the GetExchangeRateBase function

### Overview


This bug report is about a data validation issue in the umee/x/oracle/keeper/keeper.go file. The GetExchangeRateBase function returns 1 if the denominator string passed to it contains the substring "USD". This could lead to incorrect exchange rate for assets, which could enable token theft. It could also lead to an undercollateralized loan and allow funds to be drawn from the system if the price of a stablecoin drops, but the x/leverage module fails to detect the change.

To solve this issue, it is recommended to remove the condition that causes the GetExchangeRateBase function to return a price of USD 1 for any asset whose name contains “USD”.

### Original Finding Content

## Umee Security Assessment

**Diﬃculty:** High  
**Type:** Data Validation  
**Target:** umee/x/oracle/keeper/keeper.go  

## Description

If the denominator string passed to the `GetExchangeRateBase` function contains the substring “USD” (figure 7.1), the function returns 1, presumably to indicate that the denominator is a stablecoin. If the system accepts an ERC20 token that is not a stablecoin but has a name containing “USD,” the system will report an incorrect exchange rate for the asset, which may enable token theft. Moreover, the price of an actual USD stablecoin may vary from USD 1. Therefore, if a stablecoin used as collateral for a loan loses its peg, the loan may not be liquidated correctly.

```go
// GetExchangeRateBase gets the consensus exchange rate of an asset
// in the base denom (e.g. ATOM -> uatom)
func (k Keeper) GetExchangeRateBase(ctx sdk.Context, denom string) (sdk.Dec, error) {
    if strings.Contains(strings.ToUpper(denom), types.USDDenom) {
        return sdk.OneDec(), nil
    }
    // (...)
}
```
*Figure 7.1: umee/x/oracle/keeper/keeper.go#L89-L94*

```go
func (k Keeper) TokenPrice(ctx sdk.Context, denom string) (sdk.Dec, error) {
    if !k.IsAcceptedToken(ctx, denom) {
        return sdk.ZeroDec(), sdkerrors.Wrap(types.ErrInvalidAsset, denom)
    }
    price, err := k.oracleKeeper.GetExchangeRateBase(ctx, denom)
    // (...)
    return price, nil
}
```
*Figure 7.2: umee/x/leverage/keeper/oracle.go#L12-L34*

## Exploit Scenario

Umee adds the `cUSDC` ERC20 token as an accepted token. Upon its addition, its price is USD 0.02, not USD 1. However, because of the incorrect price assumption, the system sets its price to USD 1. This enables an attacker to create an undercollateralized loan and to draw funds from the system.

## Exploit Scenario 2

The price of a stablecoin drops significantly. However, the `x/leverage` module fails to detect the change and reports the price as USD 1. This enables an attacker to create an undercollateralized loan and to draw funds from the system.

## Recommendations

Short term, remove the condition that causes the `GetExchangeRateBase` function to return a price of USD 1 for any asset whose name contains “USD.”

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Umee |
| Report Date | N/A |
| Finders | Paweł Płatek, Dominik Czarnota |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf

### Keywords for Search

`vulnerability`

