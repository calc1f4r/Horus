---
# Core Classification
protocol: 1inch Liquidity Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13571
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/12/1inch-liquidity-protocol/
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
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

MooniswapGovernance - votingpower is not accurately reflected when minting pool tokens ✓ Fix Unverified

### Overview


This bug report is about an issue with the MooniswapGovernance contract when a user provides liquidity to the pool. The issue is that the minting event triggers the `_beforeTokenTransfer` callback in `MooniswapGovernance` which updates voting power reflecting the newly minted stake for the user. The bug is caused by a copy-paste error in the way `balanceTo` is determined, which sets `balanceTo` to zero if new token were minted (`from==address(0)`). This results in only the newly minted amount being considered when adjusting voting power. The developer team has proposed a fix, which is to set `balanceTo` to zero when burning (`to == address(0)`) and `balanceOf(to)` when minting. This fix has not been verified yet by Diligence.

### Original Finding Content

#### Resolution



According to the client, this issue is addressed in [1inch-exchange/[email protected]`eb869fd`](https://github.com/1inch-exchange/1inch-liquidity-protocol/commit/eb869fdd2cfdc186408d95abb756105a7ea60c22)


(This fix is as reported by the developer team, but has not been verified by Diligence).




#### Description


When a user provides liquidity to the pool, pool-tokens are minted. The minting event triggers the `_beforeTokenTransfer` callback in `MooniswapGovernance` which updates voting power reflecting the newly minted stake for the user.


There seems to be a copy-paste error in the way `balanceTo` is determined that sets `balanceTo` to zero if new token were minted (`from==address(0)`). This means, that in a later call to `_updateOnTransfer` only the newly minted amount is considered when adjusting voting power.


#### Examples


* If tokens are newly minted `from==address(0)` and therefore `balanceTo -> 0`.


**code/contracts/governance/MooniswapGovernance.sol:L100-L114**



```
function \_beforeTokenTransfer(address from, address to, uint256 amount) internal override {
    uint256 balanceFrom = (from != address(0)) ? balanceOf(from) : 0;
    uint256 balanceTo = (from != address(0)) ? balanceOf(to) : 0;
    uint256 newTotalSupply = totalSupply()
        .add(from == address(0) ? amount : 0)
        .sub(to == address(0) ? amount : 0);

    ParamsHelper memory params = ParamsHelper({
        from: from,
        to: to,
        amount: amount,
        balanceFrom: balanceFrom,
        balanceTo: balanceTo,
        newTotalSupply: newTotalSupply
    });

```
* now, `balanceTo` is zero which would adjust voting power to `amount` instead of the user’s actual balance + the newly minted token.


**code/contracts/governance/MooniswapGovernance.sol:L150-L153**



```

if (params.to != address(0)) {
    votingData.updateBalance(params.to, voteTo, params.balanceTo, params.balanceTo.add(params.amount), params.newTotalSupply, defaultValue, emitEvent);
}

```
#### Recommendation


`balanceTo` should be zero when burning (`to == address(0)`) and `balanceOf(to)` when minting.


e.g. like this:



```
uint256 balanceTo = (to != address(0)) ? balanceOf(to) : 0;

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | 1inch Liquidity Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/12/1inch-liquidity-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

