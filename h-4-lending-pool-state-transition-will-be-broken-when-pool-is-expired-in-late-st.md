---
# Core Classification
protocol: Carapace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6613
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/40
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/230

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Jeiwan
  - rvierdiiev
---

## Vulnerability Title

H-4: Lending pool state transition will be broken when pool is expired in late state

### Overview


A bug report has been found by Jeiwan and rvierdiiev which states that the Lending pool state transition will be broken when pool is expired in late state. This issue can be found in the ReferenceLendingPools._getLendingPoolStatus function and the GoldfinchAdapter.isLendingPoolExpired function. The issue is that if the lending pool is in the late state and the loan has ended or is fully repaid, then the capital will not be unlocked as there is no transition from Late to Expired. This can result in the capital being locked forever or the protection buyers not being compensated. The recommendation is to think about transition for lending pool in such cases. The issue is being looked into and it is likely to be fixed using the recommendation mentioned in a duplicate #251.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/230 

## Found by 
Jeiwan, rvierdiiev

## Summary
Lending pool state transition will be broken when pool is expired in late state
## Vulnerability Detail
Each lending pool has its state. State is calculated inside `ReferenceLendingPools._getLendingPoolStatus` function.
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ReferenceLendingPools.sol#L318-L349
```solidity
  function _getLendingPoolStatus(address _lendingPoolAddress)
    internal
    view
    returns (LendingPoolStatus)
  {
    if (!_isReferenceLendingPoolAdded(_lendingPoolAddress)) {
      return LendingPoolStatus.NotSupported;
    }


    ILendingProtocolAdapter _adapter = _getLendingProtocolAdapter(
      _lendingPoolAddress
    );


    if (_adapter.isLendingPoolExpired(_lendingPoolAddress)) {
      return LendingPoolStatus.Expired;
    }


    if (
      _adapter.isLendingPoolLateWithinGracePeriod(
        _lendingPoolAddress,
        Constants.LATE_PAYMENT_GRACE_PERIOD_IN_DAYS
      )
    ) {
      return LendingPoolStatus.LateWithinGracePeriod;
    }


    if (_adapter.isLendingPoolLate(_lendingPoolAddress)) {
      return LendingPoolStatus.Late;
    }


    return LendingPoolStatus.Active;
  }
```

Pls, note, that the first state that is checked is `expired`.
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/adapters/GoldfinchAdapter.sol#L62-L77
```solidity
  function isLendingPoolExpired(address _lendingPoolAddress)
    external
    view
    override
    returns (bool)
  {
    ICreditLine _creditLine = _getCreditLine(_lendingPoolAddress);
    uint256 _termEndTimestamp = _creditLine.termEndTime();


    /// Repaid logic derived from Goldfinch frontend code:
    /// https://github.com/goldfinch-eng/mono/blob/bd9adae6fbd810d1ebb5f7ef22df5bb6f1eaee3b/packages/client2/lib/pools/index.ts#L54
    /// when the credit line has zero balance with valid term end, it is considered repaid
    return
      block.timestamp >= _termEndTimestamp ||
      (_termEndTimestamp > 0 && _creditLine.balance() == 0);
  }
```
As you can see, pool is expired if time of credit line [has ended](https://github.com/goldfinch-eng/mono/blob/main/packages/protocol/contracts/protocol/core/CreditLine.sol#L43) or loan is fully paid.

State transition for lending pool is done inside `DefaultStateManager._assessState` function. This function is responsible to lock capital, when state is late and unlock it when it's changed from late to active again.

Because the first state that is checked is `expired` there can be few problems.

First problem. Suppose that lending pool is in late state. So capital is locked. There are 2 options now: payment was done, so pool becomes active and capital unlocked, payment was not done then pool has defaulted. But in case when state is late, and lending pool expired or loan is fully repaid(so it's also becomes expired), then capital will not be unlocked [as there is no such transition Late -> Expired](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L324-L375). The state will be changed to Expired and no more actions will be done. Also in this case it's not possible to detect if lending pool expired because of time or because no payment was done.

Second problem.
Lending pool is in active state. Last payment should be done some time before `_creditLine.termEndTime()`. Payment was not done, which means that state should be changed to Late and capital should be locked, but state was checked when loan has ended, so it became Expired and again there is no such transition that can detect that capital should be locked in this case. The state will be changed to Expired and no more actions will be done.
## Impact
Depending on situation, capital can be locked forever or protection buyers will not be compensated.
## Code Snippet
Provided above
## Tool used

Manual Review

## Recommendation
These are tricky cases, think about transition for lending pool in such cases.

## Discussion

**vnadoda**

@clems4ev3r We are planning to fix this, possibly using recommendation mentioned in a duplicate #251 

**clems4ev3r**

@vnadoda agreed

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Carapace |
| Report Date | N/A |
| Finders | Jeiwan, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-carapace-judging/issues/230
- **Contest**: https://app.sherlock.xyz/audits/contests/40

### Keywords for Search

`vulnerability`

