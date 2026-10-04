---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: swap

# Attack Vector Details
attack_type: swap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7044
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - swap
  - slippage

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jonah1005
  - DefSec
  - Gerard Persoon
---

## Vulnerability Title

Check slippage of swaps

### Overview


This bug report is concerned with the OmniBridgeFacet.sol code, which is a function that enables tokens to be swapped and started via an OmniBridge. The code includes a check to ensure that the output of swaps is not 0, but it does not account for the fact that the output could be a positive amount but still lower than expected due to slippage, sandwiching, or MEV. To address this, the report recommends adding a slippage check by specifying a minimum amount of expected tokens, or at least adding a check for amount==0 in all bridges. The LiFi and Spearbit PRs have already been fixed and verified, respectively.

### Original Finding Content

## Severity: Medium Risk

## Context
OmniBridgeFacet.sol#L63-L65

## Description
Several bridges check that the output of swaps isn’t 0. However, it could also happen that a swap gives a positive output, but still lower than expected due to slippage, sandwiching, or MEV. Several AMMs will have a mechanism to limit slippage, but it might be useful to add a generic mechanism as multiple swaps in sequence might have a relatively large slippage.

```solidity
function swapAndStartBridgeTokensViaOmniBridge(...) {
    ...
    uint256 amount = _executeAndCheckSwaps(_lifiData, _swapData, payable(msg.sender));
    if (amount == 0) {
        revert InvalidAmount();
    }
    _startBridge(_lifiData, _bridgeData, amount, true);
}
```

## Recommendation
Consider adding a slippage check by specifying a minimum amount of expected tokens. At least add a check for `amount == 0` in all bridges.

## LiFi
Fixed with PR #75.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf

### Keywords for Search

`Swap, Slippage`

