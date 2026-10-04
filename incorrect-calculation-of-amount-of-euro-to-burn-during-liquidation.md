---
# Core Classification
protocol: The Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41601
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl
source_link: none
github_link: https://github.com/Cyfrin/2023-12-the-standard

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
finders_count: 12
finders:
  - 0xAraj
  - carlitox477
  - bbl4de
  - KrisRenZo
  - haxatron
---

## Vulnerability Title

Incorrect calculation of amount of EURO to burn during liquidation

### Overview


The bug report discusses an issue with the calculation of the amount of EURO to burn during liquidation in a financial system. The severity of this issue is considered high risk. The report provides a link to the relevant code on GitHub and explains the vulnerability in detail. It states that the current code does not accurately calculate the amount of EURO to burn during liquidation, which can cause the EURO to depeg. The report suggests using a simpler calculation method to avoid this issue. The impact of this bug is that it can lead to the EURO depegging, causing financial losses. The report also mentions that the bug was identified through a manual review. The recommendation provided is to use a different calculation method to determine the amount of EURO to burn during liquidation.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/LiquidationPool.sol#L220">https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/LiquidationPool.sol#L220</a>


## Vulnerability Details

In order to maintain a peg, we must ensure that when a position is liquidated, we liquidate more than or equal to the amount of stablecoin that is borrowed.

Let us say Alice locks up 12000 EURO worth of collateral into her vault and borrows 10000 EURO, with a minimum collateralisation rate of 120%. For simplicity, we assume a single staker owns the entire LP containing 10000 EURO. Now, assume that Alice's collateral value locked falls to 11000 EURO due to rapid price action (but it is still above 100% collateralisation rate)

During liquidation, the amount of EURO to burn is computed in https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/LiquidationPool.sol#L220

```
uint256 costInEuros = _portion * 10 ** (18 - asset.token.dec) * uint256(assetPriceUsd) / uint256(priceEurUsd) * _hundredPC / _collateralRate;
```

A high level explanation of this code is:
```
Asset Value in EURO * 100 / Collateral Rate
```

So computing the costInEuros we receive
```
11000 * 100 / 120 = 9166 EURO
```

Which results in 9166 EURO being burnt which is much lower than the 10000 EURO Alice borrowed. This can cause the EURO to depeg.

The fundamental assumption that is wrong here is that the developers have assumed that liquidation immediately occurs when the asset value falls below 120% collateralisation rate (or in the example above 12000 EURO, which results in the correct EURO to be burnt 12000 * 100 / 120 = 10000 EURO).

## Impact

EURO depegging.

## Tools Used

Manual Review

## Recommendations

To calculate the cost of EUROs to be burned, use the amount of tokens minted for a particular position as opposed to the complex calculation above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | The Standard |
| Report Date | N/A |
| Finders | 0xAraj, carlitox477, bbl4de, KrisRenZo, haxatron, khramov, 0xCiphky, rvierdiiev, Cosine |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-the-standard
- **Contest**: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl

### Keywords for Search

`vulnerability`

