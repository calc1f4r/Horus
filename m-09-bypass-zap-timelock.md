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
solodit_id: 1225
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-nftx-contest
source_link: https://code4rena.com/reports/2021-12-nftx
github_link: https://github.com/code-423n4/2021-12-nftx-findings/issues/178

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
finders_count: 1
finders:
  - gzeon
---

## Vulnerability Title

[M-09] Bypass zap timelock

### Overview


This bug report is about a vulnerability in the NFTX protocol, which is used to upgrade tokens. The vulnerability is that the default value of `inventoryLockTime` in `NFTXStakingZap` is `7 days` while `DEFAULT_LOCKTIME` in `NFTXInventoryStaking` is 2 ms. This means that one can reduce their long (e.g. 7 days) timelock to 2 ms by calling `deposit` in `NFTXInventoryStaking`. The applicable timelock is calculated by `block.timestamp + timelockLength`, even when the existing timelock is further in the future. 

The recommended mitigation step is to modify the `_timelockMint` function, so that the timelock is only updated if the new timelock is further in the future. This can be done with the following code: 
```
    function _timelockMint(address account, uint256 amount, uint256 timelockLength) internal virtual {
        uint256 timelockFinish = block.timestamp + timelockLength;
        if(timelockFinish > timelock[account]){
            timelock[account] = timelockFinish;
            emit Timelocked(account, timelockFinish);
        }
        _mint(account, amount);
    }
```
This bug report was submitted by gzeon.

### Original Finding Content

_Submitted by gzeon_

The default value of `inventoryLockTime` in `NFTXStakingZap` is `7 days` while `DEFAULT_LOCKTIME` in `NFTXInventoryStaking` is 2 ms. These timelock value are used in `NFTXInventoryStaking` to eventually call `_timelockMint` in `XTokenUpgradeable`.

<https://github.com/code-423n4/2021-12-nftx/blob/194073f750b7e2c9a886ece34b6382b4f1355f36/nftx-protocol-v2/contracts/solidity/token/XTokenUpgradeable.sol#L74>

```solidity
function _timelockMint(address account, uint256 amount, uint256 timelockLength) internal virtual {
  uint256 timelockFinish = block.timestamp + timelockLength;
  timelock[account] = timelockFinish;
  emit Timelocked(account, timelockFinish);
  _mint(account, amount);
}
```

The applicable timelock is calculated by `block.timestamp + timelockLength`, even when the existing timelock is further in the future. Therefore, one can reduce their long (e.g. 7 days) timelock to 2 ms calling `deposit` in `NFTXInventoryStaking`

#### Proof of Concept

<https://github.com/code-423n4/2021-12-nftx/blob/194073f750b7e2c9a886ece34b6382b4f1355f36/nftx-protocol-v2/contracts/solidity/NFTXStakingZap.sol#L160>
<https://github.com/code-423n4/2021-12-nftx/blob/194073f750b7e2c9a886ece34b6382b4f1355f36/nftx-protocol-v2/contracts/solidity/NFTXInventoryStaking.sol#L30>

#### Recommended Mitigation Steps

```solidity
function _timelockMint(address account, uint256 amount, uint256 timelockLength) internal virtual {
  uint256 timelockFinish = block.timestamp + timelockLength;
  if(timelockFinish > timelock[account]){
    timelock[account] = timelockFinish;
    emit Timelocked(account, timelockFinish);
  }
  _mint(account, amount);
}
```

**[0xKiwi (NFTX) disputed](https://github.com/code-423n4/2021-12-nftx-findings/issues/178)**

**[0xKiwi (NFTX) confirmed and commented](https://github.com/code-423n4/2021-12-nftx-findings/issues/178#issuecomment-1007082108):**
 > After taking another look, this is definitely accurate. Thank you!

**[0xKiwi (NFTX) resolved](https://github.com/code-423n4/2021-12-nftx-findings/issues/178)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-nftx
- **GitHub**: https://github.com/code-423n4/2021-12-nftx-findings/issues/178
- **Contest**: https://code4rena.com/contests/2021-12-nftx-contest

### Keywords for Search

`vulnerability`

