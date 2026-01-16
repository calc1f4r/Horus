---
# Core Classification
protocol: CLOBER
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7263
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - dos
  - blacklisted

protocol_categories:
  - dexes
  - bridge
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Desmond Ho
  - Grmpyninja
  - Christoph Michel
  - Throttle
  - Taek Lee
---

## Vulnerability Title

Atomic fees delivery susceptible to funds lockout

### Overview


This bug report concerns the "collectFees" function in the OrderBook.sol code. This function is responsible for delivering both quoteToken and baseToken parts of fees atomically and simultaneously to both the DAO and the host. The bug is that if one of the addresses is blacklisted or a token in a pair is malicious and configured to cause a transfer to one of the addresses to revert, it can block the fees delivery. This could happen if a malicious host wants to block the function for the DAO or a hacked DAO renounces ownership to brick the collectFees across multiple markets. 

The recommendation is to parametrize the collectFee to choose a token to collect and keep separate counters of delivered fees. This issue was fixed in PR 359 and verified by Spearbit. The function was parametrized to deliver a given token to a single recipient.

### Original Finding Content

## Severity: Medium Risk

## Context
- OrderBook.sol#L791-L798 
- OrderBook.sol#L804-L805

## Description
The `collectFees` function delivers the `quoteToken` part of fees as well as the `baseToken` part of fees atomically and simultaneously to both the DAO and the host. In case a single address is blacklisted (e.g., via USDC blacklist feature) or a token in a pair is maliciously configured, it is possible for transfers to one of the addresses to revert, blocking fees delivery.

```solidity
function collectFees() external nonReentrant { // @audit delivers both tokens atomically
    require(msg.sender == _host(), Errors.ACCESS);
    if (_baseFeeBalance > 1) {
        _collectFees(_baseToken, _baseFeeBalance - 1);
        _baseFeeBalance = 1;
    }
    if (_quoteFeeBalance > 1) {
        _collectFees(_quoteToken, _quoteFeeBalance - 1);
        _quoteFeeBalance = 1;
    }
}
```

```solidity
function _collectFees(IERC20 token, uint256 amount) internal { // @audit delivers to both wallets
    uint256 daoFeeAmount = (amount * _DAO_FEE) / _FEE_PRECISION;
    uint256 hostFeeAmount = amount - daoFeeAmount;
    _transferToken(token, _daoTreasury(), daoFeeAmount);
    _transferToken(token, _host(), hostFeeAmount);
}
```

There are multiple scenarios where this situation can occur. For instance, a malicious host might block the function for the DAO to prevent collecting at least the guaranteed valuable `quoteToken`, or a hacked DAO could swap the treasury to an invalid address and renounce ownership, thereby bricking `collectFees` across multiple markets. 

Taking into account the current implementation, if it is not possible to transfer tokens, it is necessary to swap the problematic address; however, depending on the specific case, this might not be trivial.

## Recommendation
It is recommended to parametrize `collectFee` to allow the choice of a token to collect and keep separate counters for delivered fees.

### Clober
Fixed in PR 359.

### Spearbit
Verified. The function was parametrized to deliver a given token to a single recipient.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | CLOBER |
| Report Date | N/A |
| Finders | Desmond Ho, Grmpyninja, Christoph Michel, Throttle, Taek Lee |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf

### Keywords for Search

`DOS, Blacklisted`

