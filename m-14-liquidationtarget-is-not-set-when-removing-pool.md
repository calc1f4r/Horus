---
# Core Classification
protocol: DODO V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20861
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/89
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/246

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
finders_count: 1
finders:
  - Protocol Team
---

## Vulnerability Title

M-14: liquidationTarget is not set when removing pool.

### Overview


This bug report is about the issue M-14, where the liquidationTarget is not set when removing a pool. The protocol team found this bug and it was found through manual review. The bug could happen in the second step of the remove pool process, where liquidator only rebalances tokens in the pool, and it can't update the vault borrow recording. If the DODO team wants to call finishLiquidation(), they will find that the liquidationTarget wasn't set and they will not be able to balance the vault borrow recording. This could impact the successful removal of the pool.

The recommendation is to calculate liquidationTarget in removeD3Pool() and call finishLiquidation() to finish pool balance before calling finishPoolRemove(). Additionally, there is a suggestion to transfer the realDebt into the vault. This issue is not part of the contest submissions and is not eligible for contest rewards.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/246 

## Found by 
Protocol Team
Remove pool has 3 steps:
1. call removeD3Pool(address) and force the pool into liquidation state. However, the vault call ID3MM(pool).startLiquidation() directly and skip setting liquidationTarget
2. DODO team uses liquidationByDODO() to balance all tokens. 
3. call finishPoolRemove() and finish removing.

The bugs could happen in step 2. During liquidationByDODO, liquidator only rebalance tokens in pool. It can't update vault borrow recording. If dodo team want to call finishLiquidation(), they will find liquidationTarget wasn't set and they could not balance vault borrow recording.

## Impact
It may not remove pool successfully.

## Tool Used
Manual Review

## Recommandation
1. Calculation liquidationTarget in removeD3Pool()
2. call finishLiquidation() to finish pool balance and then call finishPoolRemove()
Thinking of balance > debt situation, it could transfer realDebt into vault:
https://github.com/sherlock-audit/2023-06-dodo/blob/a8d30e611acc9762029f8756d6a5b81825faf348/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultLiquidation.sol#L141C1-L145C67
```solidity
            // note: During liquidation process, the pool's debt will slightly increase due to the generated interests. 
            // The liquidation process will not repay the interests. Thus all dToken holders will share the loss equally.
            uint256 realDebt = borrows.div(record.interestIndex == 0 ? 1e18 : record.interestIndex).mul(info.borrowIndex);
            IERC20(token).transferFrom(pool, address(this), debt);
```
change into:
```solidity
IERC20(token).transferFrom(pool, address(this), realDebt);
``` 



## Discussion

**hrishibhat**

Please note: This issue is not part of the contest submissions and is not eligible for contest rewards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | DODO V3 |
| Report Date | N/A |
| Finders | Protocol Team |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/246
- **Contest**: https://app.sherlock.xyz/audits/contests/89

### Keywords for Search

`vulnerability`

