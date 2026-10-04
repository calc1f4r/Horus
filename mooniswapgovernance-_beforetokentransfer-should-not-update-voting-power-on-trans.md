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
solodit_id: 13572
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

MooniswapGovernance - _beforeTokenTransfer should not update voting power on transfers to self ✓ Fix Unverified

### Overview


A bug was reported in the Mooniswap governance system, which is based on the liquidity voting system. This system derives a continuous weighted averaged “consensus” value from all the votes. When liquidity tokens are transferred to another address, stake and voting values need to be updated. This is handled by the `MooniswapGovernance._beforeTokenTransfer()` function.

However, in the special case where someone triggers a token transfer where the `from` address equals the `to` address, effectively sending the token to themselves, the `beforeTokenTransfer` callback does not check for this and updates voting power first with `balance - amount` and then with `balance + amount`, which is unnecessary and wastes gas.

To fix this issue, the developer team added [1inch-exchange/[email protected]`7c7126d`](https://github.com/1inch-exchange/1inch-liquidity-protocol/commit/7c7126de7f8be0aa1fcbb1c8324a84c997f0bcbb) to the code, although this has not been verified by Diligence. The recommendation is to not update voting power on LP token transfers where `from == to`.

### Original Finding Content

#### Resolution



Addressed [1inch-exchange/[email protected]`7c7126d`](https://github.com/1inch-exchange/1inch-liquidity-protocol/commit/7c7126de7f8be0aa1fcbb1c8324a84c997f0bcbb)


(This fix is as reported by the developer team, but has not been verified by Diligence).




#### Description


Mooniswap governance is based on the liquidity voting system that is also employed by the mothership or for factory governance. In contrast to traditional voting systems where users vote for discrete values, the liquidity voting system derives a continuous weighted averaged “consensus” value from all the votes. Thus it is required that whenever stake changes in the system, all the parameters that can be voted upon are updated with the new weights for a specific user.


The Mooniswap pool is governed by liquidity providers and liquidity tokens are the stake that gives voting rights in `MooniswapGovernance`. Thus whenever liquidity tokens are transferred to another address, stake and voting values need to be updated. This is handled by `MooniswapGovernance._beforeTokenTransfer()`.


In the special case where someone triggers a token transfer where the `from` address equals the `to` address, effectively sending the token to themselves, no update on voting power should be performed. Instead, voting power is first updated with `balance - amount` and then with `balance + amount` which in the worst case means it is updating first to a zero balance and then to 2x the balance.


Ultimately this should not have an effect on the overall outcome but is unnecessary and wasting gas.


#### Examples


* `beforeTokenTransfer` callback in `Mooniswap` does not check for the NOP case where `from==to`


**code/contracts/governance/MooniswapGovernance.sol:L100-L119**



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

    \_updateOnTransfer(params, mooniswapFactoryGovernance.defaultFee, \_emitFeeVoteUpdate, \_fee);
    \_updateOnTransfer(params, mooniswapFactoryGovernance.defaultSlippageFee, \_emitSlippageFeeVoteUpdate, \_slippageFee);
    \_updateOnTransfer(params, mooniswapFactoryGovernance.defaultDecayPeriod, \_emitDecayPeriodVoteUpdate, \_decayPeriod);
}

```
* which leads to `updateBalance` being called on the same address twice, first with `currentBalance - amountTransferred` and then with `currentBalance + amountTransferred`.


**code/contracts/governance/MooniswapGovernance.sol:L147-L153**



```
if (params.from != address(0)) {
    votingData.updateBalance(params.from, voteFrom, params.balanceFrom, params.balanceFrom.sub(params.amount), params.newTotalSupply, defaultValue, emitEvent);
}

if (params.to != address(0)) {
    votingData.updateBalance(params.to, voteTo, params.balanceTo, params.balanceTo.add(params.amount), params.newTotalSupply, defaultValue, emitEvent);
}

```
#### Recommendation


Do not update voting power on LP token transfers where `from == to`.

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

