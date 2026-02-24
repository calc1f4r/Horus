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
solodit_id: 59276
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

Insufficient Charge of User Operation Execution Fees

### Overview


The client has marked a bug as "Fixed" and it has been addressed in the `bf4934791a3d537d0f6cb0c0031ad48f06dfb937` update. However, this fix has caused an ERC-7562 storage violation in the `ERC20PaymasterV06` contract. This is due to an issue with the calculation of gas usage, which results in the paymaster being underpaid. The `actualTokenNeeded` variable is calculated inaccurately, causing the issue. The recommendation is to modify the calculation to accurately reflect the gas cost and also make changes for when a guarantor is used.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `bf4934791a3d537d0f6cb0c0031ad48f06dfb937`. This fix does introduce an ERC-7562 storage violation in the `ERC20PaymasterV06` contract by necessity, which is however fine with the taken whitelist approach (see [PIM-3](https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html#findings-qs3)).

**File(s) affected:**`ERC20PaymasterV06.sol`

**Description:** The ERC-20 token fees are first transferred from the user operation sender or the guarantor to the paymaster. After the user operation is executed, a refund is issued based on the actual gas usage.

In `ERC20PaymasterV06`, the gas usage is calculated inaccurately and will be less than the real used amount, causing the paymaster to be underpaid. When a guarantor is not used, the `actualTokenNeeded` amount is calculated as:

`uint256 actualTokenNeeded = (actualGasCost + refundPostOpCost) * priceMarkup * tokenPrice / (1e18 * PRICE_DENOMINATOR);`

The `actualGasCost` variable represents the gas cost in ETH. However, the `refundPostOpCost` variable is the estimated gas amount, which should be multiplied by the gas price to get the gas cost in ETH. A possible fix is to calculate:

`uint256 actualTokenNeeded = (actualGasCost + refundPostOpCost * gasPrice) * priceMarkup * tokenPrice / (1e18 * PRICE_DENOMINATOR);`

where `gasPrice` can simply be the `maxFeePerGas` specified in the user operations or the [`getUserOpGasPrice()` function](https://github.com/eth-infinitism/account-abstraction/blob/v0.6.0/contracts/core/EntryPoint.sol#L600-L610) implemented in Entrypoint v0.6.

**Recommendation:** Consider modifying the calculation of `actualTokenNeeded` to reflect the actual gas cost. The case where a guarantor is used also needs to be modified.

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

