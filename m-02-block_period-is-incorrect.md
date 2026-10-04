---
# Core Classification
protocol: zkSync
chain: everychain
category: uncategorized
vulnerability_type: block_period

# Attack Vector Details
attack_type: block_period
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5749
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-zksync-v2-contest
source_link: https://code4rena.com/reports/2022-10-zksync
github_link: https://github.com/code-423n4/2022-10-zksync-findings/issues/259

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - block_period

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Soosh
---

## Vulnerability Title

[M-02] `BLOCK_PERIOD` is incorrect

### Overview


A bug has been reported in the code of the ZKsync project on GitHub. The code has a variable called `BLOCK_PERIOD` set to 13 seconds, which is incorrect as the block time on Ethereum is fixed at 12 seconds per block. This results in incorrect calculation of `PRIORITY_EXPIRATION`, which is used to determine when a transaction in the Priority Queue should be considered expired. This leads to the transaction expiring 5.5 hours earlier than expected. The severity of this issue has been deemed to be Medium. The recommendation is to change the block period to 12 seconds.

### Original Finding Content


[Config.sol#L47](https://github.com/code-423n4/2022-10-zksync/blob/456078b53a6d09636b84522ac8f3e8049e4e3af5/ethereum/contracts/zksync/Config.sol#L47)<br>

The `BLOCK_PERIOD` is set to 13 seconds in `Config.sol`.

```sol
uint256 constant BLOCK_PERIOD = 13 seconds;
```

Since moving to Proof-of-Stake (PoS) after the Merge, block times on ethereum are fixed at 12 seconds per block (slots).
<https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/#:~:text=Whereas%20under%20proof%2Dof%2Dwork,block%20proposer%20in%20every%20slot>.

### Impact

This results in incorrect calculation of `PRIORITY_EXPIRATION` which is used to determine when a transaction in the Priority Queue should be considered expired.

```sol
uint256 constant PRIORITY_EXPIRATION_PERIOD = 3 days;
/// @dev Expiration delta for priority request to be satisfied (in ETH blocks)
uint256 constant PRIORITY_EXPIRATION = PRIORITY_EXPIRATION_PERIOD/BLOCK_PERIOD;
```

The time difference can be calulated

```python
>>> 3*24*60*60 / 13    # 3 days / 13 sec block period
19938.46153846154
>>> 3*24*60*60 / 12    # 3 days / 12 sec block period
21600.0
>>> 21600 - 19938      # difference in blocks
1662
>>> 1662 * 12 / (60 * 60) # difference in hours
5.54
```

By using block time of 13 seconds, a transaction in the Priority Queue incorrectly expires 5.5 hours earlier than is expected.

5.5 hours is a significant amount of time difference so I believe this issue to be Medium severity.

### Recommended Mitigation Steps

Change the block period to be 12 seconds

```sol
uint256 constant BLOCK_PERIOD = 12 seconds;
```

**[miladpiri (zkSync) confirmed and commented](https://github.com/code-423n4/2022-10-zksync-findings/issues/259#issuecomment-1324171828):**
 > This is a valid medium issue! Thanks!

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-10-zksync-findings/issues/259#issuecomment-1329983294):**
 > The warden has shown how, due to an incorrect configuration, L2Transactions will expire earlier than intended.
> 
> The value would normally be rated a Low Severity, however, because the Warden has shown a more specific impact, I agree with Medium Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | zkSync |
| Report Date | N/A |
| Finders | Soosh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-zksync
- **GitHub**: https://github.com/code-423n4/2022-10-zksync-findings/issues/259
- **Contest**: https://code4rena.com/contests/2022-10-zksync-v2-contest

### Keywords for Search

`Block Period`

