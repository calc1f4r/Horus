---
# Core Classification
protocol: Tensor Tlock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47511
audit_firm: OtterSec
contest_link: https://www.tensor.trade/
source_link: https://www.tensor.trade/
github_link: https://github.com/tensor-hq/tlock

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
  - Tamta Topuria
  - OtterSec
---

## Vulnerability Title

Missing Collection Check

### Overview


This bug report highlights an issue in the withdraw function of a contract where users are not required to specify the collection of their NFT when withdrawing. This allows an attacker to deposit a cheaper NFT and prompt the maker to withdraw it instead of their more expensive NFT, resulting in the maker losing funds. The report suggests adding a way to specify the NFT's collection and ensuring the maker receives an NFT from the same collection they provided as collateral. The bug has been fixed in the latest update of the contract.

### Original Finding Content

## NFT Withdrawal Vulnerability

In `withdraw_collateral_compressed` and `withdraw_collateral_legacy`, users do not have to specify the collection of the NFT they are withdrawing. Therefore, the order taker may deposit an NFT from a cheaper collection into the order and prompt the maker to withdraw the provided cheaper NFT while keeping the maker’s more expensive NFT in the order for withdrawal by the taker themselves later. This loses funds for the order’s maker, regardless of whether the order is profitable, always leaving the maker with a much cheaper NFT.

## Proof of Concept

1. The attacker, the order taker, sends a random NFT A with a low price to `order_vault`.
2. The attacker then calls either `withdraw_collateral_compressed` or `withdraw_collateral_legacy` for the maker, providing the NFT A. This action gives the maker the low-cost NFT.
3. Finally, the attacker withdraws the high-cost NFT, which was provided as collateral for the order by the maker.

## Remediation

Provide a way to specify the NFT’s collection in `withdraw_*` instructions. Ensure the maker always receives an NFT from the same collection they provided as collateral. This may be enforced with a whitelist account and verify functions, as in the rest of the contract.

## Patch

Resolved in de02fdf.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tensor Tlock |
| Report Date | N/A |
| Finders | Tamta Topuria, OtterSec |

### Source Links

- **Source**: https://www.tensor.trade/
- **GitHub**: https://github.com/tensor-hq/tlock
- **Contest**: https://www.tensor.trade/

### Keywords for Search

`vulnerability`

