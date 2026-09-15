---
# Core Classification
protocol: Sandclock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1290
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/66

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
  - yield
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - danb
  - leastwood
---

## Vulnerability Title

[M-12] investedAssets() Does Not Take Into Consideration The Performance Fee Charged On Strategy Withdrawals

### Overview


A bug was discovered in the `investedAssets()` function, which is implemented by the vault's strategy contracts as a way to express a vault's investments in terms of the underlying currency. This bug could allow an attacker to avoid paying their fair share of the performance fee by withdrawing their assets before several calls to `finishRedeemStable()` are made and reenter the vault once the fee is charged. This was discovered through manual code review and discussions with the Sandclock team.

To mitigate this bug, it is recommended that when calculating the `investedAssets()` amount (expressed in the underlying currency), the expected performance fee should be considered if all the strategy's assets are withdrawn from the Anchor protocol. This will ensure that `investedAssets()` returns the most accurate amount, preventing users from gaming the protocol.

### Original Finding Content

## Handle

leastwood


## Vulnerability details

## Impact

The `investedAssets()` function is implemented by the vault's strategy contracts as a way to express a vault's investments in terms of the underlying currency. While the implementation of this function in `BaseStrategy.sol` and `NonUSTStrategy.sol` is mostly correct. It does not account for the performance fee charged by the treasury as shown in `finishRedeemStable()`.

Therefore, an attacker could avoid paying their fair share of the performance fee by withdrawing their assets before several calls to `finishRedeemStable()` are made and reenter the vault once the fee is charged.

## Proof of Concept

https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/strategy/BaseStrategy.sol#L180-L204
```
function finishRedeemStable(uint256 idx) public virtual {
    require(redeemOperations.length > idx, "not running");
    Operation storage operation = redeemOperations[idx];
    uint256 aUstBalance = _getAUstBalance() + pendingRedeems;
    uint256 originalUst = (convertedUst * operation.amount) / aUstBalance;
    uint256 ustBalanceBefore = _getUstBalance();

    ethAnchorRouter.finishRedeemStable(operation.operator);

    uint256 redeemedAmount = _getUstBalance() - ustBalanceBefore;
    uint256 perfFee = redeemedAmount > originalUst
        ? (redeemedAmount - originalUst).percOf(perfFeePct)
        : 0;
    if (perfFee > 0) {
        ustToken.safeTransfer(treasury, perfFee);
        emit PerfFeeClaimed(perfFee);
    }
    convertedUst -= originalUst;
    pendingRedeems -= operation.amount;

    operation.operator = redeemOperations[redeemOperations.length - 1]
        .operator;
    operation.amount = redeemOperations[redeemOperations.length - 1].amount;
    redeemOperations.pop();
}
```

https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/strategy/BaseStrategy.sol#L263-L277
```
function investedAssets()
    external
    view
    virtual
    override(IStrategy)
    returns (uint256)
{
    uint256 underlyingBalance = _getUnderlyingBalance() + pendingDeposits;
    uint256 aUstBalance = _getAUstBalance() + pendingRedeems;

    return
        underlyingBalance +
        ((exchangeRateFeeder.exchangeRateOf(address(aUstToken), true) *
            aUstBalance) / 1e18);
}
```

https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/strategy/NonUSTStrategy.sol#L120-L136
```
function investedAssets()
    external
    view
    override(BaseStrategy)
    returns (uint256)
{
    uint256 underlyingBalance = _getUnderlyingBalance();
    uint256 aUstBalance = _getAUstBalance() + pendingRedeems;

    uint256 ustAssets = ((exchangeRateFeeder.exchangeRateOf(
        address(aUstToken),
        true
    ) * aUstBalance) / 1e18) + pendingDeposits;
    return
        underlyingBalance +
        curvePool.get_dy_underlying(ustI, underlyingI, ustAssets);
}
```

## Tools Used

Manual code review.
Discussions with the Sandclock team (mostly Ryuhei).

## Recommended Mitigation Steps

When calculating the `investedAssets()` amount (expressed in the underlying currency), consider calculating the expected performance fee to be charged if all the strategy's assets are withdrawn from the Anchor protocol. This should ensure that `investedAssets()` returns the most accurate amount, preventing users from gaming the protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | danb, leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/66
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`vulnerability`

