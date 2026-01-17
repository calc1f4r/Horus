---
# Core Classification
protocol: Uniswap Wallet Browser Extension
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34307
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-02-uniswap-wallet-browserextension-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-02-uniswap-wallet-browserextension-securityreview.pdf
github_link: none

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
  - Paweł Płatek
  - Maciej Domański
---

## Vulnerability Title

Price of stablecoins is hard coded

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Cryptography

### Description
The Uniswap wallet browser extension uses a hard-coded price of 1 USD for selected stablecoins (see figure 27.1). The actual price of a stablecoin may vary from 1 USD. The wallet incorrectly determines the prices of stablecoins when their real price varies significantly from 1 USD. The hard-coded price informs users about the estimated transaction and fee prices (figure 27.2). Presenting incorrect estimates may misguide users. The impact of the finding is undetermined because the hard-coded price is mostly used in the Super Swap functionality, which was not audited.

```javascript
if (currencyIsStablecoin) {
    // handle stablecoin
    return new Price(stablecoin, stablecoin, '1', '1');
}
```
*Figure 27.1: Part of the useUSDCPrice method, which is used by the useUSDValue method (universe/packages/wallet/src/features/routing/useUSDCPrice.ts#61–64)*

```javascript
const gasFeeUSD = useUSDValue(chainId, networkFee);
```
*Figure 27.2: Example use of the useUSDValue method (universe/apps/stretch/src/background/features/dappRequests/requestContent/SendTransactionContent.tsx#28)*

### Exploit Scenario
The price of a stablecoin drops significantly. However, the Uniswap wallet fails to detect the change and reports the price as 1 USD. Uniswap wallet users are misguided when performing transactions.

### Recommendations
Short term, research the impact of unexpectedly high stablecoin price volatility on the system. Evaluate the security risk of the scenario if a stablecoin—whose price is assumed to be 1 USD by the extension—depegs significantly. If the risks are nonnegligible, consider removing the hard-coded price from the useUSDCPrice method.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Uniswap Wallet Browser Extension |
| Report Date | N/A |
| Finders | Paweł Płatek, Maciej Domański |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-02-uniswap-wallet-browserextension-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-02-uniswap-wallet-browserextension-securityreview.pdf

### Keywords for Search

`vulnerability`

