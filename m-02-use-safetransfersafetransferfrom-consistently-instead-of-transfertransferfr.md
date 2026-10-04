---
# Core Classification
protocol: NFTX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42184
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-05-nftx
source_link: https://code4rena.com/reports/2021-05-nftx
github_link: https://github.com/code-423n4/2021-05-nftx-findings/issues/79

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
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] Use `safeTransfer`/`safeTransferFrom` consistently instead of `transfer`/`transferFrom`

### Overview


The bug report highlights the importance of using `require()` or `safeTransfer`/`safeTransferFrom` statements when transferring tokens to avoid silent failures and incorrect token accounting. It also points out three instances in the `FeeDistributor` contract where these statements are missing, which can lead to issues with withdrawing staking tokens and rescuing arbitrary tokens. The report recommends consistently using these statements and references a similar finding from a previous audit of Fei Protocol. 

### Original Finding Content


It is good to add a `require()` statement that checks the return value of token transfers, or to use something like OpenZeppelin’s `safeTransfer`/`safeTransferFrom` unless one is sure the given token reverts in case of a failure. Failure to do so will cause silent failures of transfers and affect token accounting in contract.

While most places use a `require` or `safeTransfer`/`safeTransferFrom`, there are three missing cases in the withdrawal of staking token and rescue of arbitrary tokens sent to the `FeeDistributor` contract.

Reference this similar medium-severity finding from [Consensys Diligence Audit of Fei Protocol](https://consensys.net/diligence/audits/2021/01/fei-protocol/#unchecked-return-value-for-iweth-transfer-call).

Recommend using `safeTransfer`/`safeTransferFrom` or `require()` consistently.

**- [0xKiwi (NFTX) confirmed](https://github.com/code-423n4/2021-05-nftx-findings/issues/79)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-nftx
- **GitHub**: https://github.com/code-423n4/2021-05-nftx-findings/issues/79
- **Contest**: https://code4rena.com/reports/2021-05-nftx

### Keywords for Search

`vulnerability`

