---
# Core Classification
protocol: Geodefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20754
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/11/geodefi/
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sergii Kravchenko
  -  Christian Goll
  -  Chingiz Mardanov

---

## Vulnerability Title

A sandwich attack on fetchUnstake

### Overview


This bug report discusses an issue with the incentive system for operators in the system. Operators are incentivized to withdraw their stake when there is a debt in the system so that they can take advantage of the arbitrage opportunity. However, the process of withdrawing and signaling unstake can take days, so someone else can take the arbitrage opportunity before the operator does. This is because the DWP contract's swap function is external and can be used by anyone. Furthermore, someone else can take the arbitrage opportunity with no risk or personal funds by taking advantage of the situation when `fetchUnstake()` gets sandwiched. This means that the debt is still there when the Oracle calls `fetchUnstake()`, and the searcher can use the ETH from the surplus to get the profit. This bug could potentially create unhealthy situations when withdrawals are required in case of a serious de-peg.

### Original Finding Content

#### Description


Operators are incentivized to withdraw the stake when there is a debt in the system. Withdrawn ETH will be sold in the DWP, and a portion of the arbitrage profit will be sent to the operator. But the operators cannot unstake and earn the arbitrage boost instantly. Node operator will need to start the withdrawal process, signal unstake, and only then, after some time, potentially days, Oracle will trigger `fetchUnstake` and will take the arbitrage opportunity if it is still there.


**code/contracts/Portal/utils/StakeUtilsLib.sol:L1276-L1288**



```
function fetchUnstake(
 StakePool storage self,
 DataStoreUtils.DataStore storage DATASTORE,
 uint256 poolId,
 uint256 operatorId,
 bytes[] calldata pubkeys,
 uint256[] calldata balances,
 bool[] calldata isExit
) external {
 require(
 msg.sender == self.TELESCOPE.ORACLE\_POSITION,
 "StakeUtils: sender NOT ORACLE"
 );

```
In reality, the DWP contract’s swap function is external and can be used by anyone, so anyone could try and take the arbitrage.


**code/contracts/Portal/withdrawalPool/Swap.sol:L341-L358**



```
function swap(
 uint8 tokenIndexFrom,
 uint8 tokenIndexTo,
 uint256 dx,
 uint256 minDy,
 uint256 deadline
)
 external
 payable
 virtual
 override
 nonReentrant
 whenNotPaused
 deadlineCheck(deadline)
 returns (uint256)
{
 return swapStorage.swap(tokenIndexFrom, tokenIndexTo, dx, minDy);
}

```
In fact, one could take this arbitrage with no risk or personal funds. This is due to the fact that `fetchUnstake()` could get sandwiched. Consider the following case:


1. There is a debt in the DWP and the node operator decides to withdraw the stake to take the arbitrage opportunity.
2. After some time the Oracle will actually finalize the withdrawal by calling `fecthUnstake`.
3. If debt is still there MEV searcher will see that transaction in the mem-pool and will take an ETH loan to buy cheap gETH.
4. `fetchUnstake()` will execute and since the debt was repaid in the previous step all of the withdrawn ETH will go into `surplus`.
5. Searcher will redeem gETH that they bought for the oracle price from surplus and will get all of the profit.


At the end of the day, the goal of regaining the peg will be accomplished, but node operators will not be interested in withdrawing early later. This will potentially create unhealthy situations when withdrawals are required in case of a serious de-peg.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Geodefi |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Christian Goll,  Chingiz Mardanov
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/11/geodefi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

