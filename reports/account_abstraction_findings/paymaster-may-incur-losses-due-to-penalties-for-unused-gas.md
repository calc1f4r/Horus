---
# Core Classification
protocol: Pimlico ERC20 Paymaster
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59277
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html
source_link: https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html
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
  - Shih-Hung Wang
  - Nikita Belenkov
  - Ruben Koch
---

## Vulnerability Title

Paymaster May Incur Losses Due to Penalties for Unused Gas

### Overview


The client has marked a bug as "Fixed" in the `ERC20PaymasterV07.sol` file. The issue was that a 10% penalty for unused execution gas was not being properly accounted for, potentially causing a loss for the paymaster. To fix this, it is recommended to charge the user for the 10% penalty in the `_postOp()` function.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `3aace4c057e2d242ef13566995886438f34d0e32` and `fb9f52e4fdaa56981bf74f8b5b1d10177c40c3a5`.

**File(s) affected:**`ERC20PaymasterV07.sol`

**Description:** The user operation sender or guarantor is refunded based on the `actualGasCost` and `actualUserOpFeePerGas` values provided to the `_postOp()` function. The gas cost of the user operation is then multiplied by `priceMarkup`, providing the paymaster a profit margin.

However, in Entrypoint v0.7, a 10% penalty for unused execution gas is introduced to prevent user operation senders from reserving a large part of the gas space in the bundle but leaving it unused. The penalty is applied after the `postOp()` execution, and therefore, is not included in the `actualGasCost`.

A malicious user could set an excessively large `callGasLimit` or `paymasterPostOpGasLimit` in the user operation, causing the paymaster to pay a large penalty. If the penalty exceeds the profit the paymaster earned from the user, it suffers from a loss, which happens specifically when:

`unusedGas * 10% > usedGas * (priceMarkup - 1e6)`

**Recommendation:** A possible mitigation is to charge the user for the 10% penalty in the `_postOp()` function based on the difference between `prefundTokenAmount` and `actualTokenNeeded`. This way, the user would be responsible for setting proper call gas limits.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Pimlico ERC20 Paymaster |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Nikita Belenkov, Ruben Koch |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html

### Keywords for Search

`vulnerability`

