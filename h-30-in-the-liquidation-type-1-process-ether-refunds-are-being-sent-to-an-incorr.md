---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: cross_chain

# Attack Vector Details
attack_type: cross_chain
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45483
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/998

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 19
finders:
  - volodya
  - DenTonylifer
  - Audinarey
  - 0x23r0
  - RampageAudit
---

## Vulnerability Title

H-30: In the Liquidation Type 1 process, Ether refunds are being sent to an incorrect recipient address

### Overview


The report describes a bug in the Liquidation Type 1 process where Ether refunds are being sent to the wrong recipient address. This can result in the admin, who is responsible for the process, losing funds that should be refunded to them. The bug was found by multiple individuals and can be mitigated by updating the recipient address in the refund logic.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/998 

## Found by 
0x23r0, 0xAristos, Audinarey, AuditorPraise, Aymen0909, DenTonylifer, Flashloan44, John44, LZ\_security, Ocean\_Sky, RampageAudit, nuthan2x, santiellena, super\_jack, t.aksoy, theweb3mechanic, valuevalk, volodya, wellbyt3

### Summary

In the Liquidation Type 1 process, Ether refunds are being sent to an incorrect [recipient address](https://github.com/sherlock-audit/2024-11-autonomint-bluenights004/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L303). Specifically, refunds should be directed to the admin user, who acts as the liquidation operator and is the legitimate recipient. However, the current implementation mistakenly sends the refund to the borrower’s address.

```Solidity
File: borrowLiquidation.sol
302:         if (liqAmountToGetFromOtherChain == 0) {
303:             (bool sent, ) = payable(user).call{value: msg.value}(""); //@note wrong address 
304:             require(sent, "Failed to send Ether");
305:         }
```

### Root Cause

When liqAmountToGetFromOtherChain is zero or cross-chain operations are unnecessary, the Ether refund is incorrectly sent to the borrower’s address instead of the admin’s address. This misdirection can result in the admin losing funds that should rightfully be refunded to them.

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

Here is the scenario
1. Execution of Liquidation Type 1: A loan is liquidated using Liquidation Type 1.
2. Zero Cross-Chain Amount: In this liquidation, liqAmountToGetFromOtherChain is zero, indicating that no Ether is needed for cross-chain operations.
3. Refund Process: Ether is intended to be refunded to the liquidator, which is the admin.
4. Incorrect Recipient Address: Due to a flaw in the code, the refund is mistakenly sent to the borrower’s address instead of the admin’s address.
5. Loss of Funds: As a result, the admin loses the funds that should have been refunded.

### Impact

The admin, who is responsible for executing the Liquidation Type 1 process, loses Ether refunds that should be rightfully sent to them. 

### PoC

see attack path

### Mitigation

Update the recipient address in the refund logic to the admin’s address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | volodya, DenTonylifer, Audinarey, 0x23r0, RampageAudit, theweb3mechanic, John44, valuevalk, 0xAristos, Aymen0909, nuthan2x, santiellena, t.aksoy, super\_jack, Ocean\_Sky, Flashloan44, wellbyt3, AuditorPraise, LZ\_security |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/998
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`Cross Chain`

