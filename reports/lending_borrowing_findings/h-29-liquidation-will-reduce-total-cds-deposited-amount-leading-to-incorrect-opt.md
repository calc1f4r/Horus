---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45482
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/993

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x73696d616f
---

## Vulnerability Title

H-29: Liquidation will reduce total cds deposited amount, leading to incorrect option fees

### Overview


This bug report discusses an issue with the liquidation process in the Autonomint blockchain system. The problem is that when a borrower is liquidated, the total amount of cds deposited is reduced, but the option fees are not adjusted accordingly. This leads to an overcharge of option fees for borrowers. The root cause of the issue is that the reduction of the total cds deposited amount is not accounted for in the calculation of option fees. This bug can be exploited by a borrower who deposits 1 ETH and borrows 800 USDa when the ETH price is 1000 USD/ETH. If the price drops to 800 USD/ETH, the borrower will be liquidated and the total cds deposited amount will be reduced. However, when a new borrower deposits and pays option fees, the calculation of the cumulative rate is incorrect and the cds depositor will receive more option fees than they should. This bug can be mitigated by adjusting the cumulative rate when reducing the cds deposited amount. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/993 

## Found by 
0x73696d616f

### Summary

`borrowLiquidation::liquidationType1()` [reduces](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L248) `omniChainData.totalCdsDepositedAmount`, so the option fees will be calculated on this reduced total cds depositors, but the normalized deposit of each borrower still amounts to their initial value, overcharging option fees.

### Root Cause

In `borrowLiquidation:248`, the `omniChainData.totalCdsDepositedAmount` is reduced, but the option fees normalized deposits are not accounted for.

### Internal pre-conditions

None.

### External pre-conditions

None.

### Attack Path

1. ETH price is 1000 USD / ETH.
2. Cds depositor deposits 1000 USDa.
3. Borrower deposits 1 ETH and borrows 800 USDa. Assume no option fees are charged.
4. Price drops to 800 USD / ETH.

At this point, the total normalized amount of the cds depositor is 1000 (1000 USda divided by 1 rate).
6. Borrower is liquidated and `omniChainData.totalCdsDepositedAmount` becomes `360` (`1000 - (800 + 20 - 180)`, where 800 is the debt, 20 is the amount to return to abond and 180 is the cds profits).
7. New borrower deposits and pays 50 USD option fees. [CDS::calculateCumulativeRate()](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L163) calculates `percentageChange` as `50 / 360`. The new rate becomes `1 * (1 + 50 / 360) = 1.1389`.
8. Borrower withdraws.
9. Cds depositor withdraws, getting from option fees `1000 * 1.1389 - 1000 = 138.9`, way more than it should.

### Impact

Cds depositor gets much more option fees than it should.

### PoC

See above.

### Mitigation

Adjust the cumulative rate when reducing the cds deposited amount with option fees or similar.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | 0x73696d616f |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/993
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

