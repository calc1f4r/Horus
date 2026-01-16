---
# Core Classification
protocol: Kuiper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 802
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-kuiper-contest
source_link: https://code4rena.com/reports/2021-09-defiprotocol
github_link: https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/79

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-14] Basket.sol#handleFees() could potentially cause disruption of minting and burning

### Overview


This bug report is about a vulnerability in the WatchPug contract. The issue is that when the time difference between when the last fee was paid and the current block timestamp, multiplied by the license fee, is large enough, it can cause the fee percentage to be greater than the base, which will cause an underflow when subtracting the fee percentage from the base. This disrupts the minting and burning of the basket token until the publisher updates the license fee. To replicate the issue, a basket token with a license fee of 1000% per year is created and the basket is left inactive for two months. Calling mint and burn will cause the contract to revert. The recommended mitigation step is to limit the max value of fee percentage.

### Original Finding Content

## Handle

WatchPug


## Vulnerability details

https://github.com/code-423n4/2021-09-defiProtocol/blob/main/contracts/contracts/Basket.sol#L110-L129

```solidity=
function handleFees() private {
    if (lastFee == 0) {
        lastFee = block.timestamp;
    } else {
        uint256 startSupply = totalSupply();

        uint256 timeDiff = (block.timestamp - lastFee);
        uint256 feePct = timeDiff * licenseFee / ONE_YEAR;
        uint256 fee = startSupply * feePct / (BASE - feePct);

        _mint(publisher, fee * (BASE - factory.ownerSplit()) / BASE);
        _mint(Ownable(address(factory)).owner(), fee * factory.ownerSplit() / BASE);
        lastFee = block.timestamp;

        uint256 newIbRatio = ibRatio * startSupply / totalSupply();
        ibRatio = newIbRatio;

        emit NewIBRatio(ibRatio);
    }
}
```

`timeDiff * licenseFee` can be greater than `ONE_YEAR` when `timeDiff` and/or `licenseFee` is large enough, which makes `feePct` to be greater than `BASE` so that `BASE - feePct` will revert on underflow.


## Impact

Minting and burning of the basket token are being disrupted until the publisher update the `licenseFee`.

## Proof of Concept

1. Create a basket with a `licenseFee` of `1e19` or 1000% per year and mint 1 basket token;
2. The basket remain inactive (not being minted or burned) for 2 months;
3. Calling `mint` and `burn` reverts at `handleFees()`.

## Recommended Mitigation Steps

Limit the max value of `feePct`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kuiper |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-defiprotocol
- **GitHub**: https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/79
- **Contest**: https://code4rena.com/contests/2021-09-kuiper-contest

### Keywords for Search

`vulnerability`

