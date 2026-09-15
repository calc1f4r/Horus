---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37029
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
github_link: none

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
  - Zokyo
---

## Vulnerability Title

Loss of funds by griefing debt repayment

### Overview


This bug report discusses a high severity issue that has been resolved. The issue occurs when a deposit request is denied on the GMX side, causing the entire transaction to revert. This is due to a problem with the afterDepositCancellation callback function in the VodkaV2GMXHandler. The function is responsible for repaying the leverage amount and transferring native tokens to the user. However, if the user reverts on receiving the tokens, the transaction fails. This can be exploited by a malicious user who creates a deposit request with maximum leverage, leading to a loss of assets. Additionally, the report mentions a potential vulnerability with blacklisted addresses in USDC token contracts, which can cause transfers to fail. The recommendation is to implement a Pull over Push payment pattern and handle errors with a try/catch block. It is also suggested to check if the receiver of USDC is blacklisted before transferring tokens.

### Original Finding Content

**Severity**: High

**Status**:  Resolved

**Description**

When a deposit request is denied on the GMX side (privileged account triggers cancelDeposit from DepositHandler contract), the afterDepositCancellation callback from VodkaV2GMXHandler is invoked as part of the routine. Within this function, the leverage amount is repaid, and the user set in the deposit request receives native tokens.
```solidity
       IWater(strategyAddresses.WaterContract).repayDebt(            dr.leverageAmount,
           dr.leverageAmount
       );


       payable(dr.user).transfer(eventData.uintItems.items[0].value);
```
However, if the user reverts on receiving the native tokens, it causes the entire transaction to revert. A malicious user could craft a deposit that is intended to be canceled on the GMX side, utilizing the maximum possible leverage, which would necessitate a lend from the water contract. As a result, repaying the outstanding debt becomes impossible, leading to a loss of assets.
Moreover, similar vulnerabilities can arise if the user is blacklisted by USDC token contracts, which can allow specific addresses to be blacklisted at the contract level. If a user is blacklisted, any transfer to or from that user's address will fail.

**Recommendation**: 

Implement a Pull over Push payment pattern, allowing users to withdraw tokens manually rather than sending them directly. 
Wrap the token transfer in a try/catch block, ensuring that errors are handled. 
Consider implementing a check if the receiver of USDC is not blacklisted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

