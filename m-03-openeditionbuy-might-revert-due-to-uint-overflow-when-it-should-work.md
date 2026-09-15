---
# Core Classification
protocol: Escher
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6360
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-escher-contest
source_link: https://code4rena.com/reports/2022-12-escher
github_link: https://github.com/code-423n4/2022-12-escher-findings/issues/175

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

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - rwa

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - AkshaySrivastav
  - hansfriese
---

## Vulnerability Title

[M-03] `OpenEdition.buy()` might revert due to uint overflow when it should work.

### Overview


This bug report concerns a vulnerability in the `OpenEdition.buy()` function of the code-423n4/2022-12-escher repository. The code validates the total funds by multiplying the `amount` and `sale.price`, both of which are declared as `uint24` and `uint72` respectively. This can lead to an overflow when the amount and sale price are too large, resulting in the function reverting even when it should work properly. The recommended mitigation step for this is to modify the code to cast the `amount` as a `uint256` before the multiplication.

### Original Finding Content


`OpenEdition.buy()` might revert due to uint overflow when it should work.

### Proof of Concept

`OpenEdition.buy()` validates the total funds like below.

```solidity
    function buy(uint256 _amount) external payable {
        uint24 amount = uint24(_amount);
        Sale memory temp = sale;
        IEscher721 nft = IEscher721(temp.edition);
        require(block.timestamp >= temp.startTime, "TOO SOON");
        require(block.timestamp < temp.endTime, "TOO LATE");
        require(amount * sale.price == msg.value, "WRONG PRICE"); //@audit overflow
```

Here, `amount` was declared as `uint24` and `sale.price` is `uint72`.

And it will revert when `amount * sale.price >= type(uint72).max` and such cases would be likely to happen e.g. `amount = 64(so 2^6), sale.price = 73 * 10^18(so 2^66)`.

As a result, `buy()` might revert when it should work properly.

### Recommended Mitigation Steps

We should modify like below.

```solidity
    require(uint256(amount) * sale.price == msg.value, "WRONG PRICE");
```

**[stevennevins (Escher) confirmed](https://github.com/code-423n4/2022-12-escher-findings/issues/175)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Escher |
| Report Date | N/A |
| Finders | AkshaySrivastav, hansfriese |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-escher
- **GitHub**: https://github.com/code-423n4/2022-12-escher-findings/issues/175
- **Contest**: https://code4rena.com/contests/2022-12-escher-contest

### Keywords for Search

`vulnerability`

