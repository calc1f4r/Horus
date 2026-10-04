---
# Core Classification
protocol: BendDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36888
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-benddao
source_link: https://code4rena.com/reports/2024-07-benddao
github_link: https://github.com/code-423n4/2024-07-benddao-findings/issues/36

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
  - lending

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - bin2chen
  - oakcobalt
---

## Vulnerability Title

[M-06] `YieldEthStakingLido` lacks a limit on the max stake amount, which may result in the unstake exceeding `MAX_STETH_WITHDRAWAL_AMOUNT`, resulting in the token not being retrieved

### Overview


The YieldEthStakingLido contract has a bug in its unstaking process. When a user tries to unstake their tokens, there is a limit to how much they can withdraw at once. This limit is set by the MAX_STETH_WITHDRAWAL_AMOUNT variable and is currently set to 1000 stETH. If a user tries to unstake more than this amount, their tokens will be locked in the contract and they will not be able to withdraw them. This bug can be mitigated by adding a new method called checkStakeAmount in the YieldStakingBase contract, which will limit the maximum amount that can be unstaked. The severity of this bug has been downgraded to Medium, as it is less likely to occur with large stake amounts. The bug has been fixed in the BendDAO contract.

### Original Finding Content


In `YieldEthStakingLido`, the main processes are as follows:

1. `stake()` -> stEth balance increase
2. `unstake () -> unstETH.requestWithdrawals(allShares)`
3. `repay() -> unstETH.claimWithdrawal()`

The issue is the second step, `unstETH` is with a maximum withdrawal limit: `MAX_STETH_WITHDRAWAL_AMOUNT`

```solidity
contract YieldEthStakingLido is YieldStakingBase {
...
  function protocolRequestWithdrawal(YieldStakeData storage sd) internal virtual override {
    IYieldAccount yieldAccount = IYieldAccount(yieldAccounts[msg.sender]);

    uint256[] memory requestAmounts = new uint256[](1);
    requestAmounts[0] = sd.withdrawAmount;
    bytes memory result = yieldAccount.execute(
      address(unstETH),
@>    abi.encodeWithSelector(IUnstETH.requestWithdrawals.selector, requestAmounts, address(yieldAccount))
    );
    uint256[] memory withdrawReqIds = abi.decode(result, (uint256[]));
    require(withdrawReqIds.length > 0 && withdrawReqIds[0] > 0, Errors.YIELD_ETH_WITHDRAW_FAILED);
    sd.withdrawReqId = withdrawReqIds[0];
  }
```

<https://docs.lido.fi/contracts/withdrawal-queue-erc721/#requestwithdrawals>

> each amount in `_amounts` must be greater than or equal to `MIN_STETH_WITHDRAWAL_AMOUNT` and lower than or equal to `MAX_STETH_WITHDRAWAL_AMOUNT`.

Current configuration [here](https://github.com/lidofinance/lido-dao/blob/master/contracts/0.8.9/WithdrawalQueue.sol#L57).

```solidity
    /// @notice maximum amount of stETH that is possible to withdraw by a single request
    /// Prevents accumulating too much funds per single request fulfillment in the future.
    /// @dev To withdraw larger amounts, it's recommended to split it to several requests
    uint256 public constant MAX_STETH_WITHDRAWAL_AMOUNT = 1000 * 1e18;
```

`lido` suggests that if it exceeds this value, it needs to be taken in batches, but `YieldEthStakingLido.sol` can only be taken at once. If the stake amount exceeds this value, it will not be possible to `unstake()` and the `token` will be locked in the contract.

Assumption: `leverageFactor = 50000 , eth price = $2500`

As long as the value of the nft is greater than `1000 * $2500 / 5 = $500,000` it will be possible to `stake()` more than `MAX_STETH_WITHDRAWAL_AMOUNT`.
After that, when the user performs an `unstake()` it will fail, causing the token to be locked.

### Impact

Excessive amount of stake will result in failure to `unstake()`.

### Recommended Mitigation

`YieldStakingBase` add  method `checkStakeAmount`. Each sub contract override implements its own maximum amount limit, `YieldEthStakingLido` suggests a maximum of `MAX_STETH_WITHDRAWAL_AMOUNT/2`.

### Assessed type

Context

**[0xTheC0der (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/36#issuecomment-2296848336):**
 > Downgrading to Medium due to reduced likelihood of such great stake amounts.

**[thorseldon (BendDAO) confirmed and commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/36#issuecomment-2297881720):**
 > Fixed [here](https://github.com/BendDAO/bend-v2/commit/4af137eb1e2de720d6b7c183fb36fcfef989ebbd).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | bin2chen, oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-benddao
- **GitHub**: https://github.com/code-423n4/2024-07-benddao-findings/issues/36
- **Contest**: https://code4rena.com/reports/2024-07-benddao

### Keywords for Search

`vulnerability`

