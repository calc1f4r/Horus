---
# Core Classification
protocol: Tezoro Snap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31048
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/04/tezoro-snap/
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
finders_count: 1
finders:
  - Valentin Quelquejay

---

## Vulnerability Title

getPriceOfAssetQuotedInUSD Might Return Flawed Asset Prices ✓ Fixed

### Overview


This bug report discusses an issue with the function `getPriceOfAssetQuotedInUSD()` in the Tezoro Project's Metamask Snap code. The function assumes that stablecoins always maintain a 1:1 price ratio with the USD, but there have been instances where this is not the case. Additionally, the function assumes that any token name starting with 'W' is a wrapped token, which can lead to incorrect prices being returned. The report also mentions the potential for issues with relying on hardcoded external APIs. To fix these issues, the report recommends avoiding assumptions about token names and setting up a custom API Gateway for more flexibility.

### Original Finding Content

#### Resolution



Addressed by [tezoroproject/metamask-snap#42](https://github.com/tezoroproject/metamask-snap/pull/42)


#### Description


First, the function `getPriceOfAssetQuotedInUSD()` operates under the assumption that stablecoins—specifically ‘USDT’, ‘USDC’, ‘DAI’, ‘USDP’, and ‘TUSD’—always maintain a 1:1 price ratio with the USD. Although this is generally expected to be the case, there have been instances where some stablecoins failed to uphold their peg to the USD. In such scenarios, this assumption no longer holds true, resulting in the return of inaccurate balances. Furthermore, it’s important to note that the prices returned by this function are quoted in USDT, despite the function’s name suggesting that prices are returned in USD. This could lead to discrepancies if ‘USDT’ diverges from its fiat counterpart.


Second, The function `getPriceOfAssetQuotedInUSD()` assumes that every token name that starts with ‘W’ is a wrapped token. Thus, the initial ‘W’ is removed from the token name before fetching the prices from Binance API. As a result, the subsequent API request made to get the price of the unwrapped token could potentially fail or return an incorrect price, if the token name starts with a ‘W’ but the token is not a wrapped token. For instance, the “WOO” token is present in the list of tokens supported by the Snap. In that case, the price API will error as it will try to fetch the price of the`OOUSDT` pair instead of `WOOUSDT`.


Finally, relying on an hardcoded external APIs is sub-optimal. Indeed, it may be that the API may fail, start returning incorrect data, or simply become outdated and stop working.


#### Example


**packages/snap/src/external/get-price-of-asset-quoted-in-usd.ts:L15-L19**



```
if (assetName.startsWith('W')) {
 // Assume this is a wrapped token
 assetName = assetName.slice(1); // remove W
}
try {

```
**packages/snap/src/external/get-price-of-asset-quoted-in-usd.ts:L20-L23**



```
const response = await fetch(
 `https://api.binance.com/api/v3/ticker/price?symbol=${assetName.toUpperCase()}USDT`,
);
const json = await response.json();

```
#### Recommendation


To mitigate this issue, one should avoid making assumptions about token names. Instead, one would ideally fetch token metadata from a trusted source to determine whether a token is wrapped or not, hardcode this information in the token-list, or directly fetch the price of the wrapped token.


Moreover, instead of hardcoding the price API, we would recommend setting up a custom API Gateway which provides a layer of abstraction between the Snap and the external APIs it uses. This would provide flexibility and allow quickly swapping for other external APIs in case they stop behaving properly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Tezoro Snap |
| Report Date | N/A |
| Finders | Valentin Quelquejay
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/04/tezoro-snap/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

