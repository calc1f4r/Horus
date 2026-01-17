---
# Core Classification
protocol: 88mph v3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17606
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/88mph.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/88mph.pdf
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
finders_count: 2
finders:
  - Dominik Teiml
  - Maximilian Krüger
---

## Vulnerability Title

Withdrawing from Yearn to DInterest in a single step can save gas

### Overview

See description below for full details.

### Original Finding Content

## Data Validation
**Target:** EMAOracle.sol

**Difficulty:** Medium

## Description
`YVaultMarket.withdraw` withdraws funds from the YVaultMarket itself, measures the YVaultMarket’s new balance, and transfers the balance to `msg.sender` (figure 5.1).

```solidity
if (amountInShares > 0) {
    vault.withdraw(amountInShares);
}
// Transfer stablecoin to `msg.sender`
actualAmountWithdrawn = stablecoin.balanceOf(address(this));
if (actualAmountWithdrawn > 0) {
    stablecoin.safeTransfer(msg.sender, actualAmountWithdrawn);
}
```
**Figure 5.1:** `withdraw` in YVaultMarket.sol#L65-73

Yearn v2’s `vault.withdraw` takes a second optional parameter, `recipient`, which defaults to `msg.sender` (figure 5.2). This version can also be seen in function #28 of the WBTC yVault on Etherscan.

```solidity
def withdraw(
    maxShares: uint256 = MAX_UINT256,
    recipient: address = msg.sender,
    maxLoss: uint256 = 1,  # 0.01% [BPS]
) -> uint256:
```
**Figure 5.2:** `withdraw` in Vault.vy#L1004-1008

Using this two-parameter version of `withdraw` would be simpler and require less gas (figure 5.3).

```solidity
if (amountInShares > 0) {
    vault.withdraw(amountInShares, msg.sender);
}
```
**Figure 5.3:** Recommended replacement for the code in figure 5.1

## Recommendations
**Short term:** replace the code in figure 5.1 with the code in figure 5.3.

**Long term:** examine the APIs of the protocols that the 88mph protocol depends on to see whether simpler and more gas-efficient means of interaction are available.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | 88mph v3 |
| Report Date | N/A |
| Finders | Dominik Teiml, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/88mph.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/88mph.pdf

### Keywords for Search

`vulnerability`

