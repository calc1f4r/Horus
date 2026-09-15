---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18295
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Swapping tokens/ETH for NFTs may exhibit unexpected behavior for certain values of input amount, trade fees and royalties

### Overview


This bug report is about the _pullTokenInputAndPayProtocolFee() function in the LSSVMPairERC20.sol and LSSVMPairETH.sol files. The function pulls ERC20/ETH from the caller/router and pays the protocol fees, trade fees and royalties proportionately. The problem is that the trade fees have a threshold of MAX_FEE == 50%, which allows 2*fee to be 100%. This means that the protocol fee, trade fee and royalty amounts could add up to be greater than the inputAmount, which causes the transfer of the tradeFeeAmount to either revert due to unavailable funds or use any balance funds from the pair itself.

The recommendation is to check that the protocolFee +royaltyTotal +tradeFeeAmount is less than the inputAmount. It is also suggested to make the order of operations/transfers the same between LSSVMPairERC20 and LSSVMPairETH to make their behavior and failure modes consistent. Sudorandom Labs acknowledged the bug report but has decided to leave out the cases with very high royalty percentages (e.g. 50% or more). Spearbit also acknowledged the bug report.

### Original Finding Content

## Medium Risk Report

**Severity:** Medium Risk  
**Context:** 
- LSSVMPairERC20.sol#L34-L115
- LSSVMPairETH.sol#L22-L73  

**Description:**  
The `_pullTokenInputAndPayProtocolFee()` function pulls ERC20/ETH from the caller/router and pays protocol fees, trade fees, and royalties proportionately. Trade fees have a threshold of `MAX_FEE == 50%`, which allows `2*fee` to be `100%`. Royalty amounts could technically be any percentage as well. This creates edge cases where the protocol fee, trade fee, and royalty amounts add up to be greater than `inputAmount`. 

In `LSSVMPairERC20`, the ordering of subtracting/transferring the `protocolFee` and `royaltyTotal` first causes the final attempted transfer of `tradeFeeAmount` to either revert due to unavailable funds or utilize any balance funds from the pair itself. In `LSSVMPairETH`, the ordering of subtracting/transferring the `tradeFees` and `royaltyTotal` first causes the final attempted transfer of `protocolFee` to either revert due to unavailable funds or utilize any balance funds from the pair itself.

**Recommendation:**  
Check that `protocolFee + royaltyTotal + tradeFeeAmount < inputAmount`. Consider making the order of operations/transfers the same between `LSSVMPairERC20` and `LSSVMPairETH` to ensure their behavior and failure modes are consistent.

**Sudorandom Labs:**  
Acknowledged, no change beyond PR#59 to address the specific trade fee issue. The cases here deal with situations when the royalty percentage is very high (e.g., 50% or more), which we acknowledge but choose to leave out of scope.

**Spearbit:**  
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

