---
# Core Classification
protocol: Derive
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53724
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Bids Can Be Blocked By Depositing Tokens To Liquidator

### Overview


The report discusses a bug in the liquidator bidding process where a call to deposit an asset to the liquidator's account can block the bid. This is because a check is performed to ensure the liquidator only has cash in their account, but this check can be bypassed by sending a non-cash asset to the bidder/liquidator. This issue was previously identified and fixed for Options assets, but it is still possible to exploit it by depositing wrapped ERC20 tokens without requiring approval. The recommendation is to extend the approval system to wrapped token deposits, but the development team has stated that they will not be changing this due to the possibility of creating wrapper contracts to bypass the check.

### Original Finding Content

## Description

Liquidator bids can be blocked by being front-run with a call to deposit an asset to the liquidator’s account. When bidding on auctions, _ensureBidderCashBalance() is called to ensure a liquidator only has cash in their account. The check is required for gas reasons, as then no portfolio risk check has to be performed on the liquidator.

This leads to a problem where any account can front-run a bid by sending a non-cash asset to the bidder/liquidator, which results in the bid reverting. This issue was originally highlighted in DRV-02 in the previous security assessment report and fixed for Options assets by requiring approval from the receiving account prior to transfer.

However, no approval is required for depositing/wrapping fresh ERC20 tokens into a recipient account, using `WrappedERC20Asset.deposit()`. As such, it is still possible to send a non-cash asset (wrapped ERC20 in this case) to an arbitrary account, which means this vulnerability is still exploitable.

## Recommendations

Extend the approval system to wrapped token deposits.

## Resolution

The development team has acknowledged the issue with the following comment:

> "As wrapper contracts can be created to atomically create new accounts with cash only and then bidding, this will not be changed."

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Derive |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf

### Keywords for Search

`vulnerability`

