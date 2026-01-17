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
solodit_id: 45504
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/560

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
finders_count: 2
finders:
  - volodya
  - almurhasan
---

## Vulnerability Title

M-14: omniChainData.cdsPoolValue is not decreased/updated in the  function liquidationType1,as a result cds/ borrow ratio will be bigger than expected.

### Overview


This bug report discusses an issue with the function liquidationType1 in the autonomint protocol. The problem is that the variable omniChainData.cdsPoolValue is not being updated correctly, which can lead to a higher than expected cds/borrow ratio. This can cause issues with new stablecoin minting and withdrawal for cds users. The root cause of this issue is the lack of updating the variable in the mentioned function. The impact can be mitigated by updating and decreasing the variable in the function. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/560 

## Found by 
almurhasan, volodya

### Summary

omniChainData.cdsPoolValue is not decreased/updated in the  function liquidationType1,as a result cds/ borrow ratio will be bigger than expected till all cds depositors(who opted for liquidation amount) don’t withdraw their deposited amount. So there may come a scenario when  the cds/borrow’s real  ratio may become below 0.2 but the protocol will calculate above 0.2(so new stablecoin can be minted/ cds users can withdraw if cds/borrow ratio  is below 0.2).


### Root Cause

omniChainData.cdsPoolValue is not decreased/updated in the  function liquidationType1


### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

1. Let’s assume, currently omniChainData.cdsPoolValue = 500,  omniChainData.vaultValue = 2000, so cds/borrow ratio = 500/2000 = 0.25

2. now the function liquidationType1 is called where 100 amount is liquidated, now omniChainData.vaultValue = 2000-100 = 1900(as 100 usd worth of collateral is allocated for cds depositer) and omniChainData.cdsPoolValue = 500-100 = 400(as 100 is liquidated). So the current cds/borrow ratio should be 400/1900 = 0.21.

3. but as omniChainData.cdsPoolValue is not decreased/updated in the  function liquidationType1,so omniChainData.cdsPoolValue is still 500 and cds/borrow ratio = 500/1900 = 0.26 which is bigger than real cds/borrow ratio.

4. cds/borrow ratio will be corrected when all cds depositors(who opted for liquidation amount) withdraw because after their withdrawals cdspoolvalue is decreased and cds/borrow ratio becomes correct.

5. cds/ borrow ratio will be bigger than expected till all cds depositors(who opted for liquidation amount) don’t withdraw their deposited amount. So there may come a scenario when  the cds/borrow’s real  ratio may become below 0.2 but the protocol will calculate above 0.2(so new stablecoin can be minted/ cds users can withdraw if cds/borrow ratio  is below 0.2).

https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L174


### Impact

cds/ borrow ratio will be bigger than expected till all cds depositors(who opted for liquidation amount) don’t withdraw their deposited amount. So there may come a scenario when  the cds/borrow’s real  ratio may become below 0.2 but the protocol will calculate above 0.2(so new stablecoin can be minted/ cds users can withdraw if cds/borrow ratio  is below 0.2).


### PoC

_No response_

### Mitigation

update/decrease omniChainData.cdsPoolValue in the  function liquidationType1

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | volodya, almurhasan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/560
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

