---
# Core Classification
protocol: Stella
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19048
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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
  - front-running
  - first_depositor_issue

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-4 First depositor can steal asset tokens of others

### Overview


This bug report is about a potential attack in which an attacker can take advantage of a rounding down operation when calculating the amount of shares in a pool if the supply is non-zero. This attack can be done when the pool has no share supply and the amount of shares to be minted is equal to the assets provided. 

The scenario described in the report is that Alice wants to deposit 2M * 1e6 USDC to a pool. Bob observes Alice's transaction, frontruns to deposit 1 wei USDC to mint 1 wei share, and transfers 1 M * 1e6 USDC to the pool. As a result, Alice receives 1 share, the pool has 3M*1e6 +1 assets and distributed 2 shares, and Bob profits 0.5 M while Alice loses 0.5 M USDC.

The team fixed the bug by increasing the interest-bearing token decimal by 18 to prevent attackers from manipulating the share price by precision loss, and made themself the first depositor to prevent potential attacks.

### Original Finding Content

**Description:**
The first depositor can be front run by an attacker and as a result will lose a considerable 
part of the assets provided.
When the pool has no share supply, in `_mintInternal()`, the amount of shares to be minted is 
equal to the assets provided. An attacker can abuse of this situation and profit of the 
rounding down operation when calculating the amount of shares if the supply is non-zero. 
```solidity
        function _mintInternal(address _receiver, uint _balanceIncreased, uint _totalAsset
             ) internal returns (uint mintShares) {
                unfreezeTime[_receiver] = block.timestamp + mintFreezeInterval;
        if (freezeBuckets.interval > 0) {
             FreezeBuckets.addToFreezeBuckets(freezeBuckets, _balanceIncreased.toUint96());
        }
                 uint _totalSupply = totalSupply();
                    if (_totalAsset == 0 || _totalSupply == 0) {
                     mintShares = _balanceIncreased + _totalAsset;
                 } else {
             mintShares = (_balanceIncreased * _totalSupply) / _totalAsset;
             }
            if (mintShares == 0) {
        revert ZeroAmount();
        }
        _mint(_receiver, mintShares);
        }
``` 
Consider the following scenario.
1. Alice wants to deposit 2M * 1e6 USDC to a pool.
2. Bob observes Alice's transaction, frontruns to deposit 1 wei USDC to mint 1 wei share, and 
transfers 1 M * 1e6 USDC to the pool.
3. Alice's transaction is executed, since **_totalAsset = 1M * 1e6 + 1** and **totalSupply = 1**, Alice 
receives 2M * 1e6 * 1 / (1M * 1e6 + 1) = 1 share.
4. The pool now has 3M*1e6 +1 assets and distributed 2 shares.
Bob profits 0.5 M and Alice loses 0.5 M USDC.

**Recommended Mitigation:**
When **_totalSupply == 0**, send the first min liquidity LP tokens to the zero address to enable 
share dilution
Another option is to use the ERC4626 implementation(https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol#L199C14-L208) from OZ.

**Team response:**
Fixed.

**Mitigation Review:**
The team increased the interest-bearing token decimal by 18 to prevent attackers from 
manipulating the share price by precision loss, and made themself the first depositor to 
prevent potential attacks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Front-Running, First Depositor Issue`

