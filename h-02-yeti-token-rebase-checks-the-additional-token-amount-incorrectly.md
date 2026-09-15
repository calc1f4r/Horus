---
# Core Classification
protocol: Yeti Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1204
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-yeti-finance-contest
source_link: https://code4rena.com/reports/2021-12-yetifinance
github_link: https://github.com/code-423n4/2021-12-yetifinance-findings/issues/121

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hyh
---

## Vulnerability Title

[H-02] Yeti token rebase checks the additional token amount incorrectly

### Overview


This bug report is about a vulnerability in the Yeti Finance smart contract. The issue is that the condition isn't checked when the whole balance is used instead of the Yeti tokens bought back from the market. This means that the amount added to `effectiveYetiTokenBalance` during rebase can exceed the actual amount of the Yeti tokens owned by the contract. If the Yeti token price rises compared to the last used one, this deficit of Yeti tokens can cause a difference between the net worth and the total users’ claims, meaning the contract will be in default if enough users claim. 

The recommended mitigation step is to limit the amount of extra tokens used for the check, meaning `yetiToken.balance - effectiveYetiTokenBalance`, and to simplify the logic in the `_getValueOfContract` function.

### Original Finding Content

_Submitted by hyh_

#### Impact

The condition isn't checked now as the whole balance is used instead of the Yeti tokens bought back from the market.
As it's not checked, the amount added to `effectiveYetiTokenBalance` during rebase can exceed the actual amount of the Yeti tokens owned by the contract.
As the before check amount is calculated as the contract net worth, it can be fixed by immediate buy back, but it will not be the case.

The deficit of Yeti tokens can materialize in net worth terms as well if Yeti tokens price will raise compared to the last used one.
In this case users will be cumulatively accounted with the amount of tokens that cannot be actually withdrawn from the contract, as its net holdings will be less then total users’ claims.
In other words, the contract will be in default if enough users claim after that.

#### Proof of Concept

Now the whole balance amount is used instead of the amount bought back from market.

Rebasing amount is added to `effectiveYetiTokenBalance`, so it should be limited by extra Yeti tokens, not the whole balance:
<https://github.com/code-423n4/2021-12-yetifinance/blob/main/packages/contracts/contracts/YETI/sYETIToken.sol#L247>

#### Recommended Mitigation Steps

It looks like only extra tokens should be used for the check, i.e. `yetiToken.balance - effectiveYetiTokenBalance`.

Now:
```solidity
function rebase() external {
        ...
    uint256 yetiTokenBalance = yetiToken.balanceOf(address(this));
    uint256 valueOfContract = _getValueOfContract(yetiTokenBalance);
    uint256 additionalYetiTokenBalance = ...
    if (yetiTokenBalance < additionalYetiTokenBalance) {
            additionalYetiTokenBalance = yetiTokenBalance;
    }
    effectiveYetiTokenBalance = effectiveYetiTokenBalance.add(additionalYetiTokenBalance);
...
function _getValueOfContract(uint _yetiTokenBalance) internal view returns (uint256) {
    uint256 adjustedYetiTokenBalance = _yetiTokenBalance.sub(effectiveYetiTokenBalance);
    uint256 yusdTokenBalance = yusdToken.balanceOf(address(this));
    return div(lastBuybackPrice.mul(adjustedYetiTokenBalance), (1e18)).add(yusdTokenBalance);
}
```
As the `_getValueOfContract` function isn't used elsewhere, the logic can be simplified.
To be:
```solidity
function rebase() external {
    ...
    uint256 adjustedYetiTokenBalance = (yetiToken.balanceOf(address(this))).sub(effectiveYetiTokenBalance);
    uint256 valueOfContract = _getValueOfContract(adjustedYetiTokenBalance);
    uint256 additionalYetiTokenBalance = ...
    if (additionalYetiTokenBalance > adjustedYetiTokenBalance) {
            additionalYetiTokenBalance = adjustedYetiTokenBalance;
    }
    effectiveYetiTokenBalance = effectiveYetiTokenBalance.add(additionalYetiTokenBalance);
...
function _getValueOfContract(uint _adjustedYetiTokenBalance) internal view returns (uint256) {
    uint256 yusdTokenBalance = yusdToken.balanceOf(address(this));
    return div(lastBuybackPrice.mul(_adjustedYetiTokenBalance), (1e18)).add(yusdTokenBalance);
}
```

**[kingyetifinance (Yeti finance) disagreed with severity and confirmed](https://github.com/code-423n4/2021-12-yetifinance-findings/issues/121):**
 > @LilYeti: 
> 
> This is the logic for the fix which we have already done: 
> 
> if (yetiTokenBalance - effectiveYetiTokenBalance < additionalYetiTokenBalance) 
> 
> Will look into this again before confirming as fixed to see if it is the same as the suggested error. 
> 

**[0xtruco (Yeti finance) commented](https://github.com/code-423n4/2021-12-yetifinance-findings/issues/121#issuecomment-1009823126):**
 > https://github.com/code-423n4/2021-12-yetifinance/pull/12




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yeti Finance |
| Report Date | N/A |
| Finders | hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-yetifinance
- **GitHub**: https://github.com/code-423n4/2021-12-yetifinance-findings/issues/121
- **Contest**: https://code4rena.com/contests/2021-12-yeti-finance-contest

### Keywords for Search

`vulnerability`

