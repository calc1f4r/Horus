---
# Core Classification
protocol: Elektrik
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37557
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-09-Elektrik.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Missing Handling for Tokens with Transfer Fees in `fillOrders()`

### Overview


This bug report discusses an issue with the `fillOrders()` function in the `AdvancedOrderEngine.sol` file. The function does not account for tokens that have transfer fees, such as USDT, resulting in a discrepancy in token balances after order fulfillment. The recommendation is to update the function to handle tokens with transfer fees and carefully choose tokens without fees. The client has provided reasons for not addressing this issue at the moment, including the use of whitelisted tokens and the ability to deploy a new contract if necessary. This decision is to maintain simplicity and focus on core functionalities.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Location**: AdvancedOrderEngine.sol

**Description**

The `fillOrders()` function in `AdvancedOrderEngine.sol` does not account for tokens that force a fee on transfers, such as USDT. This results in a discrepancy in token balances after order fulfillment, breaking the invariant that the vault must not retain nor leak funds post-fulfillment of orders: The vault must not keep funds after the fullfilment of orders. I.e `balance[before] == balance[after]`.

**Recommendation**: 

Updated the `fulfillOrders()` function to correctly handle tokens with transfer fees. Ensure that the protocol accounts for fees when calculating token balances post-fulfillment of orders to avoid the vault leaking funds. Carefully picking tokens that do not impost fee-on-transfer is a solution to be considered.

**Client comment**:  

**Defense Reason**: Design Choice.
**Defense**: 
**Whitelisted Tokens Only**:
- Our platform exclusively supports whitelisted tokens, ensuring that only pre-approved tokens are used within the system. This significantly reduces the risk of encountering tokens with unexpected transfer fees.
**Specific Issue with USDT:**
- The primary concern revolves around USDT, as it is currently the main token with a transfer fee. We acknowledge this limitation and have plans in place to address it when necessary.
**Future Adaptability**:
- When USDT or any other token introduces a transfer fee, we have the flexibility to deploy a new contract. This is feasible because our current contract does not store significant data; it primarily functions as a gateway to validate orders before execution.
**Simplification and Complexity Management**:
- Handling tokens with transfer fees introduces additional complexity into the contract logic. To maintain the system's simplicity and reliability, we have decided not to address this issue at the present moment. This decision allows us to focus on core functionalities and ensure robust performance for the majority of use cases.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Elektrik |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-09-Elektrik.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

