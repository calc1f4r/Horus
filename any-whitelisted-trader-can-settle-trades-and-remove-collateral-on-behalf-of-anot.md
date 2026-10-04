---
# Core Classification
protocol: Native v2 (Security Review)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58955
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/native-v-2-security-review/7c9b3fe3-dbb4-4527-ad0b-f50aa3e15d8c/index.html
source_link: https://certificate.quantstamp.com/full/native-v-2-security-review/7c9b3fe3-dbb4-4527-ad0b-f50aa3e15d8c/index.html
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
  - Valerian Callens
---

## Vulnerability Title

Any Whitelisted Trader Can Settle Trades and Remove Collateral on Behalf of Another Trader

### Overview


The `CreditVault.sol` contract has been updated and now only the trader or authorized settler can perform certain actions, such as settling trades or removing collaterals. However, it has been discovered that the code for this protection is not properly enforcing this rule. This means that someone who is not a trader or authorized settler can still bypass this protection and perform these actions. This can lead to potential exploits, such as a trader intentionally causing another trader to get liquidated and then settling their position to gain the negative requested amounts. It is recommended that the code for the modifier be updated to properly enforce the rule and prevent potential exploits.

### Original Finding Content

**Update**
`CreditVault.sol` has been updated. Only the trader or the authorized settler can perform actions such as settling trades or removing collaterals from the associated address as of commit `9430af6`.

**File(s) affected:**`src/CreditVault.sol`

**Description:** In the `CreditVault.sol` contract, the operations `settle()` and `removeCollateral()` are protected by the modifier `onlyTraderOrSettler`, which has the following code:

```
modifier onlyTraderOrSettler(address trader) {
 if (!isTraders[msg.sender] && !(isTraders[trader] && msg.sender == settlers[trader])) {
 revert ErrorsLib.OnlyTrader();
 }
 _;
}
```

We can observe that having `isTraders[msg.sender] == true` is enough to bypass this condition.

**Exploit Scenario:**

1.   `Alice` is a whitelisted trader and liquidator, and `Bob` is a whitelisted trader. `Alice` can increase the likelihood of `Bob` getting liquidated by making his positions more risky, by successfully getting that request signed by the `signer`.
2.   `Alice` and `Bob` are traders. `Alice` settles the position of `request.trader == Bob` and `request.recipient == Alice`. She gets that request signed by the `signer`. She calls `settle()` with that request and the contract `CreditVault.sol` will transfer the negative requested `amounts` to her.

**Recommendation:** Consider updating the code of the modifier to enforce that only a trader or an authorized settler of that trader can settle trades or remove collaterals from the associated address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Native v2 (Security Review) |
| Report Date | N/A |
| Finders | Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/native-v-2-security-review/7c9b3fe3-dbb4-4527-ad0b-f50aa3e15d8c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/native-v-2-security-review/7c9b3fe3-dbb4-4527-ad0b-f50aa3e15d8c/index.html

### Keywords for Search

`vulnerability`

