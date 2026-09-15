---
# Core Classification
protocol: Eggs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46032
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/eeda9a4d-2065-4ea6-a3f1-b22e36beef3c
source_link: https://cdn.cantina.xyz/reports/cantina_eggs_february2025.pdf
github_link: none

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
finders_count: 2
finders:
  - Kaden
  - Optimum
---

## Vulnerability Title

Inconsistent interest charged due to integer truncation 

### Overview


This bug report discusses an issue in the Eggs contract that calculates the interest fee for loans. The problem arises when using integers instead of real numbers, resulting in a significant difference in the interest fee. This can be exploited by borrowers to pay less interest by repeatedly extending short-term loans instead of creating a full-duration loan. The recommendation is to use a larger denominator and a mulDiv function to prevent overflow. The bug has been fixed in the Eggs Finance and Cantina Managed contracts. 

### Original Finding Content

## Interest Fee Calculation in Eggs.sol

## Context
**Location:** Eggs.sol#L209

## Description
In `Eggs.getInterestFeeInEggs`, we compute the interest fee with the following logic:

```solidity
uint256 interest = ((3900 * numberOfDays) / 365) + 100;
```

Using `numberOfDays = 1` as an example, we can compare the output of this logic using integers versus real numbers:

- **Integers:** 
  - \( 3900 * 1 / 365 = 10 \) (0.01%).
  
- **Real numbers:** 
  - \( 3.9\% * 1 / 365 \approx 0.0106849315\% \).

Here we can see that the output using integers is rounded down by nearly 7%. Since Solidity arithmetic uses integers, this becomes a problem. This can be intentionally exploited by borrowing for shorter durations and repeatedly extending the loan instead of creating a full duration loan. We can see how this creates a variance in the interest paid for one 365-day loan versus 365 one-day loans:

- **One 365-day loan:**
  - \( 3900 * 365 / 365 = 3900 \) (3.9%).
  
- **365 one-day loans:**
  - \( (3900 * 1 / 365) * 365 = 3650 \) (3.65%).

## Recommendation
We can represent the interest rate using a larger denominator to get more precision. A good option would be to use `1e18`, adjusting the math accordingly. Additionally, we should use a `mulDiv` function to prevent overflow in the intermediary value:

```solidity
- uint256 interest = ((3900 * numberOfDays) / 365) + 100;
+ uint256 interest = mulDiv(0.039e18, numberOfDays, 365) + 0.001e18;
```

```solidity
- return ((amount * interest) / 100 / FEE_BASE_1000);
+ return mulDiv(amount, interest, 1e18);
```

**Note:** The above logic has not been tested.

## Status
- **Eggs Finance:** Fixed in commit `2f02fb77`.
- **Cantina Managed:** Fixed as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Eggs |
| Report Date | N/A |
| Finders | Kaden, Optimum |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_eggs_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/eeda9a4d-2065-4ea6-a3f1-b22e36beef3c

### Keywords for Search

`vulnerability`

