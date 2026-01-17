---
# Core Classification
protocol: Stella
chain: everychain
category: logic
vulnerability_type: slippage

# Attack Vector Details
attack_type: slippage
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19052
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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
  - slippage
  - business_logic

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-8 “Exact output” swaps cannot be executed, blocking repayment of debt

### Overview


This bug report is about an issue with Uniswap V2 and V3 when performing “exact output” swaps. The maximum input amount argument was set to 0, which caused the slippage check in the Uniswap contracts to always revert because the swaps would require more input tokens. This was considered high-severity because an “exact output” swap is mandatory when closing a position that doesn’t have enough tokens to repay the borrowed amount. 

The recommended mitigation was to set the maximum input amount arguments to type(uint256).max. The team fixed the issue as recommended, and the mitigation was reviewed.

### Original Finding Content

**Description:**
When performing “exact output” swaps via Uniswap V2 and V3, the maximum input amount 
argument (**amountInMax** when calling Uniswap V2’s `swapTokensForExactTokens()`, 
**amountInMaximum** when calling V3’s `exactOutput()`) is set to 0. As a result, swapping 
attempts will always revert because no more than 0 input tokens can be sold (the slippage 
check in the Uniswap contracts will always revert because the swaps will require more input 
tokens).
We consider it high-severity because an “exact output” swap is mandatory when closing a 
position that doesn’t have enough tokens to repay(https://github.com/AlphaFinanceLab/stella-arbitrum-private-contract/blob/3a4e99307e9cbf790279e49a4d90771e5486c51d/contracts/stella-strategies/strategies/base/BaseStrategy.sol#L224) the borrowed amount. Thus, since “exact 
output” swaps are not possible, closing some positions won’t be possible as well, leaving funds 
locked in the contract.

**Recommended Mitigation:**
Taking into account that the protocol implements delayed slippage checks, consider setting 
the maximum input amount arguments to **type(uint256).max.**

**Team response:**
Fixed.

**Mitigation Review:**
The team has fixed it as recommended to make the logic correct.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Slippage, Business Logic`

