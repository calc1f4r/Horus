---
# Core Classification
protocol: InsureDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1310
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-insuredao-contest
source_link: https://code4rena.com/reports/2022-01-insure
github_link: https://github.com/code-423n4/2022-01-insure-findings/issues/228

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
  - services
  - cross_chain
  - indexes
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[M-04] System Debt Is Not Handled When Insurance Pools Become Insolvent

### Overview


This bug report describes a vulnerability in an insurance policy redemption system. If an incident occurs where an insurance policy is to be redeemed, the market is put into the 'MarketStatus.Payingout' mode, allowing the '_insurance.insured' account to redeem their cover and receive a payout amount. However, there is currently no mechanism to ensure when 'transferDebt()' is called in 'PoolTemplate.resume()', the accrued system debt is paid off. This could lead to system instability in extreme edge cases.

Proof of concept code for the vulnerability is provided in the report. The recommended mitigation step is to devise a mechanism to ensure the system debt is properly handled. After discussions with the sponsor, it seems that they will be implementing a way to mint 'INSURE' tokens which will be used to cover the shortfall.

### Original Finding Content

_Submitted by leastwood_

If an incident has occurred where an insurance policy is to be redeemed. The market is put into the `MarketStatus.Payingout` mode where the `_insurance.insured` account is allowed to redeem their cover and receive a payout amount. Upon paying out the insurance cover, any user is able to resume the market by calling `PoolTemplate.resume()`. This function will compensate the insurance pool if it is insolvent by querying `IndexTemplate.compensate()` which in turn queries `CDSTemplate.compensate()` to cover any shortage.

In the event none of these entities are able to cover the shortage in debt, the system accrues the debt. However, there is currently no mechanism to ensure when `transferDebt()` is called in `PoolTemplate.resume()`, the accrued system debt is paid off. Therefore, the system may incorrectly handle insolvency on an extreme edge case, generating system instability.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-insure/blob/main/contracts/PoolTemplate.sol#L691-L734>
```solidity
function resume() external {
    require(
        marketStatus == MarketStatus.Payingout &&
            pendingEnd < block.timestamp,
        "ERROR: UNABLE_TO_RESUME"
    );

    uint256 _debt = vault.debts(address(this));
    uint256 _totalCredit = totalCredit;
    uint256 _deductionFromIndex = (_debt * _totalCredit * MAGIC_SCALE_1E6) /
        totalLiquidity();
    uint256 _actualDeduction;
    for (uint256 i = 0; i < indexList.length; i++) {
        address _index = indexList[i];
        uint256 _credit = indicies[_index].credit;
        if (_credit > 0) {
            uint256 _shareOfIndex = (_credit * MAGIC_SCALE_1E6) /
                _totalCredit;
            uint256 _redeemAmount = _divCeil(
                _deductionFromIndex,
                _shareOfIndex
            );
            _actualDeduction += IIndexTemplate(_index).compensate(
                _redeemAmount
            );
        }
    }

    uint256 _deductionFromPool = _debt -
        _deductionFromIndex /
        MAGIC_SCALE_1E6;
    uint256 _shortage = _deductionFromIndex /
        MAGIC_SCALE_1E6 -
        _actualDeduction;

    if (_deductionFromPool > 0) {
        vault.offsetDebt(_deductionFromPool, address(this));
    }

    vault.transferDebt(_shortage);

    marketStatus = MarketStatus.Trading;
    emit MarketStatusChanged(MarketStatus.Trading);
}
```
- <https://github.com/code-423n4/2022-01-insure/blob/main/contracts/IndexTemplate.sol#L421-L450>
- <https://github.com/code-423n4/2022-01-insure/blob/main/contracts/CDSTemplate.sol#L248-L277>


#### Recommended Mitigation Steps

Consider devising a mechanism to ensure system debt is properly handled. After discussions with the sponsor, it seems that they will be implementing a way to mint `INSURE` tokens which will be used to cover the shortfall.

**[oishun1112 (Insure) acknowledged](https://github.com/code-423n4/2022-01-insure-findings/issues/228)**
 > yes, PoolTemplate calls transferDebt() to make his debt to the system debt in case all Index and CDS layers couldn't cover the shortage.
> In this case, we have to repay the system debt somehow since this is the situation that we over-lose money. One way is that someone calls repayDebt() and pay for it (not realistic at all). As we implement the way to payback, we are considering minting INSURE token or, other better mechanism.
> 
 > This is not developed yet, and acknowledged.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | InsureDAO |
| Report Date | N/A |
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-insure
- **GitHub**: https://github.com/code-423n4/2022-01-insure-findings/issues/228
- **Contest**: https://code4rena.com/contests/2022-01-insuredao-contest

### Keywords for Search

`vulnerability`

