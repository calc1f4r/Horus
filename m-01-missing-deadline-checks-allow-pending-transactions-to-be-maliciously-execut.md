---
# Core Classification
protocol: Possum
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44138
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Possum-Security-Review.md
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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-01] Missing Deadline Checks Allow Pending Transactions To Be Maliciously Executed For `convert()`, `buyPortalEnergy()` and `sellPortalEnergy()` Functions

### Overview


The `Portal.sol` contract has a bug that does not allow users to set a deadline for a certain action called `convert()`. This means that if a transaction is submitted to the Mempool (a place where transactions wait to be executed) and it stays there for a long time, the price of the tokens involved in the transaction could change drastically. This can result in the user unknowingly performing a bad conversion. The affected code is located in the `Portal.sol` file and the recommendation is to introduce a `deadline` parameter to the functions involved. The team has responded that they have fixed the issue. 

### Original Finding Content

## Severity

Medium Risk

## Description

The `Portal.sol` contract does not allow users to submit a deadline for `convert()` action. This missing feature enables pending transactions to be maliciously executed at a later point.

The following scenario can happen:

1. Alice wants to convert `1,000,000` PSM tokens for `100` X tokens. She signs the transaction calling `Portal.convert()` with `_token = X token address` and `_minReceived = 99 X tokens` to allow for some slippage.
2. The transaction is submitted to the Mempool, however, Alice chose a transaction fee that is too low for miners to be interested in including her transaction in a block. The transaction stays pending in the Mempool for extended periods, which could be hours, days, weeks, or even longer.
3. When the average gas fee drops far enough for Alice's transaction to become interesting again for miners to include it, her conversation will be executed. In the meantime, the price of `X token` could have drastically changed. She will still at least get `99 X tokens` due to `_minReceived`, but the `X token` value of that output might be significantly lower. She has unknowingly performed a bad conversion due to the pending transaction she forgot about.

## Location of Affected Code

File: [contracts/Portal.sol](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol)

```solidity
function convert(
    address _token,
    uint256 _minReceived
) external nonReentrant {

function buyPortalEnergy(
    uint256 _amountInput,
    uint256 _minReceived
) external nonReentrant {

function sellPortalEnergy(
    uint256 _amountInput,
    uint256 _minReceived
) external nonReentrant {
```

## Recommendations

Introduce a `deadline` parameter to the mentioned functions.

```diff
function X(
+   uint256 deadline
) external nonReentrant {
+   if (deadline < block.timestamp) revert DeadlineExpired();
    .
    .
    .
}
```

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Possum |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Possum-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

