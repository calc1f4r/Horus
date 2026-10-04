---
# Core Classification
protocol: IntentX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59432
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/intent-x/a195e62f-30b6-4219-b9e5-42af8a9e2fd5/index.html
source_link: https://certificate.quantstamp.com/full/intent-x/a195e62f-30b6-4219-b9e5-42af8a9e2fd5/index.html
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
  - Mustafa Hasan
  - Adrian Koegl
  - Cameron Biniamow
---

## Vulnerability Title

Unpurchased INTX Is Locked Once the Vesting Period Begins

### Overview


The client has marked a bug as "Fixed" in the `PublicSaleINTX.sol` file. The bug caused an issue in the `buy()` function, which allows users to purchase INTX in exchange for raiseToken (USDC). Once the vesting period begins, the `buy()` function fails and any unpurchased INTX is locked in the contract with no way to remove it. This can lead to a loss of 500,000 INTX if only 1,500,000 INTX was purchased out of the total allocation of 2,000,000 INTX. The recommendation is to add a function to transfer unpurchased INTX to the multisig once the vesting period begins. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `c5435f1b14c72211cff7645a18a0d6e9dc91ec29`. The client provided the following explanation:

> withdrawUnallocatedIntx function added to withdraw INTX that hasn't been sold.

**File(s) affected:**`PublicSaleINTX.sol`

**Description:** In the`PublicSaleINTX`contract, the contract is funded with two million INTX via a one-time call to the `deposit()` function. After the contract is funded, users can call the`buy()` function to purchase INTX in exchange for`raiseToken`(USDC) where the exchange rate is calculated as follows:

```
intxOwed = totalIntxAllocation * raiseTokenDepositAmount / totalToRaise
```

Where`totalIntxAllocation`equals`2,000,000` INTX and`totalToRaise`equals`400,000` USDC. This means that for every`1` USDC deposited, the user will purchase`5` INTX. However, once the vesting period begins,INTX purchases are no longer available, and the`buy()`function fails when called. Therefore, if less than the total allocation of INTX(2,000,000) is purchased once the vesting period begins, the unpurchased INTX is locked in the`PublicSaleINTX`contract as the`buy()`function is locked, and there is no functionality to remove the unpurchased INTX.

**Exploit Scenario:** Assume the`PublicSaleINTX`contract is deployed with a`totalAllocation`of 2,000,000 INTX and a`totalToRaise`of 400,000 USDC.

1.   The public sale begins.
2.   A total of 1,500,000 INTX is purchased for 300,000 USDC.
3.   The vesting period begins, and the INTX sale expires.
4.   500,000 INTX is locked in the`PublicSaleINTX`contract.

**Recommendation:** Add a function to `PublicSaleINTX` that transfers all unpurchased INTX to the multisig once the vesting period begins.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | IntentX |
| Report Date | N/A |
| Finders | Mustafa Hasan, Adrian Koegl, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/intent-x/a195e62f-30b6-4219-b9e5-42af8a9e2fd5/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/intent-x/a195e62f-30b6-4219-b9e5-42af8a9e2fd5/index.html

### Keywords for Search

`vulnerability`

