---
# Core Classification
protocol: Compound Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11827
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - liquidity_manager
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Incorrect Whitepaper Interest Rate

### Overview


This bug report is related to the Compound Finance whitepaper. The whitepaper states that the interest rate earned by suppliers is equal to the borrowing interest rate multiplied by the utilization rate. However, the `supplyRatePerBlock` function calculates it as the borrow interest rate multiplied by `borrowsPer` which is not identical to the whitepaper utilization rate. It is then multiplied again by (1 – the reserve factor). This is not equivalent to the value specified in the whitepaper. Therefore, it is suggested to update the whitepaper or the calculation for consistency.

### Original Finding Content

The [Compound Finance whitepaper](https://compound.finance/documents/Compound.Whitepaper.pdf) states in section 2.3:



> 
>  The interest rate earned by suppliers is *implicit*, and is equal to the borrowing interest rate multiplied by the utilization rate.
> 
> 
> 


In fact, the [`supplyRatePerBlock` function](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L420) calculates it as the borrow interest rate multiplied by `borrowsPer` (which is not identical to the whitepaper utilization rate), and then multiplied again by (1 – the reserve factor). This is a related but not equivalent value to the specified one.


Consider updating the whitepaper or the calculation for consistency.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

