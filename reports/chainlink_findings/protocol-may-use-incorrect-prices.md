---
# Core Classification
protocol: Archi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60911
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
source_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
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
finders_count: 4
finders:
  - Mustafa Hasan
  - Zeeshan Meghji
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

Protocol May Use Incorrect Prices

### Overview


The report highlights several issues with the Archi ecosystem's token pricing system. Firstly, the prices for tokens are currently calculated using a function called GMX, which is not part of the audit and may not provide accurate prices. Additionally, there are no checks in place to validate the prices retrieved from functions like `IGmxVault.getMinPrice()` and `IGmxVault.getMaxPrice()`, which could lead to outdated or incorrect prices being used.

To address these concerns, the team has added checks to ensure that the prices returned from `IGmxVault(vault).getMinPrice(_token)` and `IGmxVault(vault).getMaxPrice(_token)` are valid and within a specified deviation from Chainlink prices. However, it is noted that the `vaultPriceFeed` contract only uses a single price oracle address, leaving the ecosystem vulnerable to price manipulation if the oracle is compromised. There is also no way to update the price oracle address, which could cause major issues if the oracle is compromised in the future.

The report recommends implementing a system to aggregate and compare prices from different oracles, as well as adding checks for price staleness and the ability to update oracle contract addresses. These changes would improve the security and accuracy of the token pricing system in the Archi ecosystem.

### Original Finding Content

**Update**
The prices for tokens are now calculated from the return values from calls to GMX, which is essentially used as an oracle. We note that GMX is outside the scope of this audit. Additionally, no validation checks are made on the return value of functions like `IGmxVault.getMinPrice()` and `IGmxVault.getMaxPrice()`.

Furthermore, we note that the functions `IGmxVault.getMinPrice()` and `IGmxVault.getMaxPrice()` retrieve the minimum or maximum prices of the token from the last N Chainlink rounds and thus may be outdated.

We also recommend a safety mechanism that compares the price received from GMX against the chainlink price. If the deviation is too high, then perhaps the transaction should fail.

![Image 74: Alert icon](blob:http://localhost/94c75bd51a0d4e9989cbe9929979ce3d)

**Update**
The team has fixed the issue by adding the following checks:

*   `IGmxVault(vault).getMinPrice(_token)` and `IGmxVault(vault).getMaxPrice(_token)` must return a value greater than zero.
*   Validating that both `IGmxVault(vault).getMinPrice(_token)` and `IGmxVault(vault).getMaxPrice(_token)` return a price that is within a specified deviation from Chainlink prices.

**File(s) affected:**`oracles/PriceOracle.sol`

**Description:** The `vaultPriceFeed` holds the price oracle address (which is supposedly that of Chainlink as per the documentation). However, the contract only uses a single price oracle address to keep track of token prices, which leaves the whole Archi ecosystem vulnerable to price manipulation attacks in case the oracle is compromised.

Additionally, the contract doesn't expose any functionality that allows changing the price oracle address. This would render the Archi ecosystem irreversibly flawed in terms of token price calculation should the oracle be compromised.

Furthermore, no validation checks are performed on the retrieved price, including checking for the staleness of the price and ensuring it is greater than zero.

**Recommendation:** Make sure prices are aggregated and compared from different oracles. Check the returned price for staleness. Add a mechanism to update oracle contract addresses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Archi Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Zeeshan Meghji, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html

### Keywords for Search

`vulnerability`

