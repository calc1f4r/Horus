---
# Core Classification
protocol: $BOBA Teleportation and Token as a Fee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60675
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/boba-teleportation-and-token-as-a-fee/72fc60f1-efe4-4f86-8a3f-6ada60d11005/index.html
source_link: https://certificate.quantstamp.com/full/boba-teleportation-and-token-as-a-fee/72fc60f1-efe4-4f86-8a3f-6ada60d11005/index.html
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
finders_count: 5
finders:
  - Pavel Shabarkin
  - Ibrahim Abouzied
  - Andy Lin
  - Adrian Koegl
  - Valerian Callens
---

## Vulnerability Title

Attacker May Drain `Boba_GasPriceOracle` of Value Given Arbitrage Opportunities

### Overview


This bug report discusses a potential vulnerability in the Boba_GasPriceOracle.sol file. The current structure of the file allows for an attacker to drain the contract of ETH if the market price of BOBA increases by a certain percentage. This can happen due to high volatility or unreliable price feeds. The report recommends pulling the marketPriceRatio whenever a certain function is called to prevent this attack. It also suggests verifying the price feed contracts on the blockchain and assessing the risks involved.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation: One reason to maintain the current structure is to allow change of oracles, while we look for ways to add a wrapper that allows aggregation. Since Boba_GasPriceOracle (implementation) is a predeploy and is also stored as a constant in the contract ‘Lib_PredeployAddresses’, any updates to Boba_GasPriceOracle would demand an update to all contracts that import ‘Lib_PredeployAddresses’ to be safe. Hence, we are currently avoiding doing changes to the contracts that are not critical/high, but taking a note of them to include in the subsequent bedrock network upgrade

**File(s) affected:**`Boba_GasPriceOracle.sol`

**Description:** When swapping BOBA for ETH through `swapBOBAForETHMetaTransaction(..)`, the exchange rate is determined by `marketPriceRatio`. To perform such a swap, the user has to pay an additional `_metaTransactionFee`, currently 3 BOBA.

An attacker could drain `Boba_GasPriceOracle` of value if the `owner` fails to update `marketPriceRatio` in times of high volatility. [The Gas Price Oracle service](https://github.com/bobanetwork/boba/tree/develop/packages/boba/gas-price-oracle) updates the `marketPriceRatio` in intervals of five minutes. If the actual market price of 0.005 ETH is 3 BOBA higher than through `marketPriceRatio`, an attacker is incentivized to drain `Boba_GasPriceOracle` of ETH.

To formalize, an attacker has an incentive to drain the value whenever the following holds true:

```
0.005 ETH * actual_market_price > 0.05 ETH * marketPriceRatio + 3 BOBA
```

As of April 6 2023, 0.005 ETH is worth about 41 BOBA. Therefore, a relative value increase of 8% would suffice to create an incentive for an attacker. Phases of high volatility and/or when the service is unreliable at times might open a window for such an attacker. Please note that a lower required value increase might suffice in the future, depending on price developments.

While `priceRatio` may be stale as well, it might only lead to cheaper transaction fees which do not create a strong incentive for attackers.

The oracle creates another point of vulnerability. Its possible for the oracle to provide an incorrect price where the price of BOBA is overestimated in comparison with the price of ETH.

This could happen in two situations:

*   a flash-crash of one of the two tokens ETH and BOBA would take time to be reflected in the contract. The team mentioned that price feeds are updated every 5 minutes.
*   price manipulation by oracles: According to the documentation (https://docs.boba.network/other/oracle) the oracle network used by the contract (`Boba_Straw`) allows a minimum of one provider per price feed. It is profitable for oracles to manipulate the price feed for a short period if the number of native tokens to steal from the contract is higher than what they staked for financial sanctions for preventing price manipulation.

**Recommendation:** We recommend pulling the `marketPriceRatio` whenever `swapBOBAForETHMetaTransaction(..)` is called. This would remove this attack vector of draining the contract of ETH funds. However, If the current design is maintained, make sure to update `metaTransactionFee` to reduce the risk of such incentive windows by updating the required value increase.

Additionally, consider verifying the price feed contracts on the blockchain explorers to allow anyone to verify on-chain the activity of the network of oracles. Also, consider assessing the risks described above. If necessary, update the polling interval to update price feeds and limit the number of tokens owned by the contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | $BOBA Teleportation and Token as a Fee |
| Report Date | N/A |
| Finders | Pavel Shabarkin, Ibrahim Abouzied, Andy Lin, Adrian Koegl, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/boba-teleportation-and-token-as-a-fee/72fc60f1-efe4-4f86-8a3f-6ada60d11005/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/boba-teleportation-and-token-as-a-fee/72fc60f1-efe4-4f86-8a3f-6ada60d11005/index.html

### Keywords for Search

`vulnerability`

