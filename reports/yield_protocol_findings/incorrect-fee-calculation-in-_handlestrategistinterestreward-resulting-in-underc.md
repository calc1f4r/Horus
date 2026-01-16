---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21843
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-Mon and Natalie
  - Jonah1005
  - Blockdev
---

## Vulnerability Title

Incorrect fee calculation in _handleStrategistInterestReward resulting in undercharged fees in PublicVault

### Overview


This bug report is about the PublicVault contract in the LienToken.sol file. It has been observed that the TotalAssets of the PublicVault does not change in the makePayment process, resulting in a smaller fee collection by the protocol. The severity of this bug is rated as Medium Risk. 

The bug was caused by the line of code “uint256 feeInShares = fee.mulDivDown(totalSupply(), totalAssets() - fee);”, which should have been “uint256 feeInShares = fee.mulDivDown(totalSupply(), totalAssets());”. 

To illustrate the bug, assume totalAssets = 2000, interestPaid = 1000, and Vault_FEE = 50%. Then, the totalSupply, totalAssets, protocolFee, protocolShares, and pricePerShare at t0, t1, and t2 would be as follows: 

t0: totalSupply = 1000, totalAssets = 2000, protocolFee = --, protocolShares = --, pricePerShare = 2
t1: totalSupply = 1000, totalAssets = 2000, protocolFee = 500, protocolShares = 500/2 = 250, pricePerShare = 2
t2: totalSupply = 1250, totalAssets = 2000, protocolFee = 500, protocolShares = 250, pricePerShare = 1.6

In this scenario, the protocol should collect 500$, but it only collects 250 * 1.6 = 400. 

The bug has been fixed in PR 350 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
LienToken.sol#L392-L430

## Description
In the `PublicVault` contract, the function `_handleStrategistInterestReward` is being called during the `makePayment` process. However, it has been observed that the `TotalAssets` of the `PublicVault` does not change in `makePayment`, assuming it is a normal payment scenario. 

`_mint(owner(), feeInShares);` would result in a smaller fee collection by the protocol.

### Example Calculation
Assume:
- `totalAssets = 2000`
- `interestPaid = 1000`
- `Vault_FEE = 50%`

| totalSupply | totalAssets | protocolFee | protocolShares | pricePerShare |
|-------------|-------------|--------------|----------------|----------------|
| t0          | 1,000       | 2000         | --             | --             | 2              |
| t1          | 1,000       | 2000         | 500            | 500 / 2 = 250  | -              |
| t2          | 1,250       | 2000         | 500            | 250            | 1.6            |

While the protocol should collect $500, it only collects \( 250 \times 1.6 = 400 \).

The code should be:
```solidity
uint256 feeInShares = fee.mulDivDown(totalSupply(), totalAssets() - fee);
```
instead of:
```solidity
uint256 feeInShares = fee.mulDivDown(totalSupply(), totalAssets());
```

## Resolution
- **Astaria**: Fixed in PR 350.
- **Spearbit**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Jonah1005, Blockdev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf

### Keywords for Search

`vulnerability`

