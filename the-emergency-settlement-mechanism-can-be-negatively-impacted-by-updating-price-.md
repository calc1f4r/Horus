---
# Core Classification
protocol: Secured Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59981
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
source_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
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
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

The Emergency Settlement Mechanism Can Be Negatively Impacted by Updating Price Feed Decimals

### Overview


The report discusses an issue where updating the number of decimals in the CurrencyController after an emergency termination can affect price calculations during a settlement process. The client recommends adding a check to prevent this from happening. This issue has been addressed in a recent update.

### Original Finding Content

**Update**
Now, when the market is terminated in case of emergency, `LendingMarketController` stores the current price and number of decimals currently stored in `CurrencyController`. As a result, a later update of decimals number in `CurrencyController` will not affect the price calculations done when the user does an emergency settlement. Addressed in: `b469f1a999368796bbd56c176a4995a905f44e9c`.

The client provided the following explanation:

> _The updated points are as follows:_
> 
> 
> *   _Add logic to cache currency decimals values instead of the CurrencyContoroller updates_
> *   _Add a check to prevent the update of collateral currency in TokenVault at emergency termination_

**File(s) affected:**`CurrencyController.sol`

**Description:** In case of an emergency, a termination mechanism can be executed by the owner of the contract `LendingMarketController` to cease the operations of the protocol. Once executed, this operation cannot be reverted. For each active currency, the last aggregated price returned by the oracle is stored in the mapping `marketTerminationPrices`. Values in this mapping have the number of decimals stored in the mapping `CurrencyController.decimalCaches[]`. Then, users can force a settlement of all lending and borrowing positions via the function `executeEmergencySettlement()`.

Once the protocol is terminated, it is possible to update the values in the mapping `CurrencyController.decimalCaches[]`, which would affect the prices used during the settlement process and obtained via the functions `FundManagementLogic._convertToBaseCurrencyAtMarketTerminationPrice()` and `FundManagementLogic._convertFromBaseCurrencyAtMarketTerminationPrice()`.

**Recommendation:** Consider adding a check to prevent the update of a price feed once the protocol has been terminated via the emergency termination process.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Secured Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html

### Keywords for Search

`vulnerability`

