---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40517
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/2c5aba7f-d561-4b2b-bbcc-184095521c35
source_link: https://cdn.cantina.xyz/reports/cantina_competition_aave_may2024.pdf
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
finders_count: 1
finders:
  - JCN
---

## Vulnerability Title

Consider documenting explicitly that virtual accounting is a requirement for "normal" re- serves 

### Overview

See description below for full details.

### Original Finding Content

## Context

**File:** DefaultInterestRateStrategyV2.sol#L122-L124

## Description

The documentation regarding Aave's new features currently states that the implementation of the virtual accounting feature includes an optional `virtualUnderlyingBalance` field for assets listed on Aave. Furthermore, "Special" assets like GHO (minted instead of supplied) are to be configured without virtual accounting. 

However, it is not explicitly mentioned (in the documentation and Natspec) that enabling virtual accounting is actually a requirement for "normal" reserves, i.e., reserves which support supplying.

As shown in the context above, any reserve configured with virtual accounting disabled will not have a liquidity rate, and the borrow rate will be capped at the `baseVariableBorrowRate`. For "normal" reserves, this would translate to a loss of interest for suppliers and the treasury (if a reserve factor is set) and break the economic incentives of the interest rate model.

## Recommendation

Aave should consider explicitly documenting (in documentation and Natspec) that virtual accounting is a requirement for "normal" reserves, and outline the implications of "normal" reserves opting out of using the virtual accounting feature.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | JCN |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_aave_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/2c5aba7f-d561-4b2b-bbcc-184095521c35

### Keywords for Search

`vulnerability`

