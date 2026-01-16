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
solodit_id: 35234
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/17

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
finders_count: 1
finders:
  - bin2chen
---

## Vulnerability Title

[M-15] `confirmUnderwriter()` need to recalculate `getMinTimeBetweenWithdrawalQueues`

### Overview


This bug report discusses an issue with the `getMinTimeBetweenWithdrawalQueues` function in the `Pool` contract. If this function is set to a value that is too small, it can cause problems with the `pendingQueues` and prevent `Loan` from finding the correct `queues` when it pays off. The report recommends calculating `getMinTimeBetweenWithdrawalQueues` based on `MaxDuration + _LOAN_BUFFER_TIME` to prevent early overwriting. However, the report also notes that switching to a new `getUnderwriter` does not recalculate `getMinTimeBetweenWithdrawalQueues`, which can cause issues if the new `getUnderwriter.getMaxDuration` is larger than the old one. The report suggests overriding the `confirmUnderwriter()` function in `Pool` to include a recalculation of `getMinTimeBetweenWithdrawalQueues` and ensuring that the new value is not smaller than the old one. The report also notes that this issue falls under the "Context" category and has been mitigated by the team.

### Original Finding Content


`getMinTimeBetweenWithdrawalQueues` is very important for `Pool`. If `getMinTimeBetweenWithdrawalQueues` is too small, `pendingQueues` will be overwritten too early, and when `Loan` pays off, it won't be able to find the corresponding `queues`.

So we will calculate `getMinTimeBetweenWithdrawalQueues` by `MaxDuration + _LOAN_BUFFER_TIME` to make sure it won't be overwritten too early.

```solidity
    constructor(
        address _feeManager,
        address _offerHandler,
        uint256 _waitingTimeBetweenUpdates,
        OptimalIdleRange memory _optimalIdleRange,
        uint256 _maxTotalWithdrawalQueues,
        uint256 _reallocationBonus,
        ERC20 _asset,
        string memory _name,
        string memory _symbol
    ) ERC4626(_asset, _name, _symbol) LoanManager(tx.origin, _offerHandler, _waitingTimeBetweenUpdates) {

....

@>      getMinTimeBetweenWithdrawalQueues = (IPoolOfferHandler(_offerHandler).getMaxDuration() + _LOAN_BUFFER_TIME)
            .mulDivUp(1, _maxTotalWithdrawalQueues);
```

But switching the new `getUnderwriter/_offerHandler` doesn't recalculate the `getMinTimeBetweenWithdrawalQueues`.

```solidity
    function confirmUnderwriter(address __underwriter) external onlyOwner {
        if (getPendingUnderwriterSetTime + UPDATE_WAITING_TIME > block.timestamp) {
            revert TooSoonError();
        }
        if (getPendingUnderwriter != __underwriter) {
            revert InvalidInputError();
        }

@>      getUnderwriter = __underwriter;
        getPendingUnderwriter = address(0);
        getPendingUnderwriterSetTime = type(uint256).max;

        emit UnderwriterSet(__underwriter);
    }
```

This may break the expectation of `getMinTimeBetweenWithdrawalQueues`, and the new `getUnderwriter.getMaxDuration` is larger than the old one; which may cause `pendingQueues` to be overwritten prematurely.

### Impact

The new `getUnderwriter.getMaxDuration` is larger than the old one, which may cause `pendingQueues` to be overwritten prematurely.

### Recommended Mitigation

`Pool` overrides `confirmUnderwriter()` with an additional recalculation of `getMinTimeBetweenWithdrawalQueues` and must not be smaller than the old one, to avoid premature overwriting of the previous one.

```diff
contract Pool is ERC4626, InputChecker, IPool, IPoolWithWithdrawalQueues, LoanManager, ReentrancyGuard {
-   uint256 public immutable getMinTimeBetweenWithdrawalQueues;
+   uint256 public getMinTimeBetweenWithdrawalQueues;
...
+   function confirmUnderwriter(address __underwriter) external override onlyOwner {
+           super.confirmUnderwriter(__underwriter);
+           uint256 newMinTime = (IPoolOfferHandler(__underwriter).getMaxDuration() + _LOAN_BUFFER_TIME)
+            .mulDivUp(1, _maxTotalWithdrawalQueues);
+           require(newMinTime >= getMinTimeBetweenWithdrawalQueues,"invalid");
+           getMinTimeBetweenWithdrawalQueues = newMinTime;
+    }
```

### Assessed type

Context

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/17#event-12545582338)**

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Added check (`maxDuration` cannot be longer).

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/110), [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/33) and [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/80).

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
| Finders | bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/17
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

