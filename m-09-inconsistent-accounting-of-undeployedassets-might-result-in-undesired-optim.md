---
# Core Classification
protocol: Gondi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35228
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/44

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
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - bin2chen
  - oakcobalt
---

## Vulnerability Title

[M-09] Inconsistent accounting of `undeployedAssets` might result in undesired optimal range in the pool

### Overview


The bug report states that the `undeployedAssets` are calculated inconsistently in the Gondi protocol. In `_getUndeployedAssets()`, the protocol collected fees are subtracted, but in `validateOffer`, the protocol collected fees are not subtracted. This causes an inflation of the `undeployedAssets` in the protocol. Additionally, in `_reallocate()`, the collected fees are not accounted for, which affects the optimal range check. This inconsistency in accounting can lead to incorrect checks and undesirable optimal ranges. The recommended mitigation steps include accounting for the collected fees in both `validateOffer` and `_reallocate()`. The bug has been confirmed and mitigated by the Gondi team. 

### Original Finding Content


`undeployedAssets` is calculated inconsistently. Currently in `_getUndeployedAssets()` the protocol collected fees are subtracted; however, in `validateOffer`, the protocol collected fees are not subtracted.

1. `_getUndeployedAssets()`: This is called in `deployWithdrawalQueue()` to [calculate proRata liquid assets](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/pools/Pool.sol#L339) to the `queue.contractAddress`.

```solidity
    function _getUndeployedAssets() private view returns (uint256) {
        return asset.balanceOf(address(this)) + IBaseInterestAllocator(getBaseInterestAllocator).getAssetsAllocated()
|>            - getAvailableToWithdraw - getCollectedFees;
    }
```

2. `uint256 undeployedAssets`: This is manually calculated in `validateOffer` flow, which is used check whether the pool has [enough undeployed Assets to cover `loan.principalAmount`](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/pools/Pool.sol#L407).

```solidity
    function validateOffer(bytes calldata _offer, uint256 _protocolFee) external override onlyAcceptedCallers {
...
        uint256 currentBalance = asset.balanceOf(address(this)) - getAvailableToWithdraw;
        uint256 baseRateBalance = IBaseInterestAllocator(getBaseInterestAllocator).getAssetsAllocated();
         //@audit getCollectedFees is not subtracted
|>        uint256 undeployedAssets = currentBalance + baseRateBalance;
        (uint256 principalAmount, uint256 apr) = IPoolOfferHandler(getUnderwriter).validateOffer(
            IBaseInterestAllocator(getBaseInterestAllocator).getBaseAprWithUpdate(), _offer
        );
...
```

<https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/pools/Pool.sol#L398>

Note that in (2), `undeployedAssets` are inflated because `getCollectedFees` are fees protocol collected from liquidation/repayment flows and shouldn't be considered as liquid assets to cover the loan principal amount.

3. `_reallocate()`: This also manually calculate total `undeployedAssets` amount, but again didn't account for `getCollectedFees`. `_reaalocate()` balances optimal target idle assets ratio by checking `currentBalance`/`total` ratio. Here, `currentBalance` should be additionally subtracted by `getCollectedFees` because fees are set aside and shouldn't be considered idle. This affects [optimal range check](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/pools/Pool.sol#L581).

```solidity
    function _reallocate() private returns (uint256, uint256) {
        /// @dev Balance that is idle and belongs to the pool (not waiting to be claimed)
        uint256 currentBalance = asset.balanceOf(address(this)) - getAvailableToWithdraw;
        if (currentBalance == 0) {
            revert AllocationAlreadyOptimalError();
        }
        uint256 baseRateBalance = IBaseInterestAllocator(getBaseInterestAllocator).getAssetsAllocated();
        uint256 total = currentBalance + baseRateBalance;
        uint256 fraction = currentBalance.mulDivDown(PRINCIPAL_PRECISION, total);
...
```

<https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/pools/Pool.sol#L572>

Inconsistent accounting in various flows may result in incorrect checks or undesirable optimal ranges.

### Recommended Mitigation Steps

Account for `getCollectedFees` in (2) and (3), noted above.

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/44#event-12543633373)**

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Missing collected fees in accounting.

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/104) and [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/74).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gondi |
| Report Date | N/A |
| Finders | bin2chen, oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/44
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

