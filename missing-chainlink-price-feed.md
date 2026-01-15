---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27621
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - FalconHoof
---

## Vulnerability Title

Missing chainlink price feed

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/README.md#compatibilities">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/README.md#compatibilities</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/GMXOracle.sol#L62-70">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/GMXOracle.sol#L62-70</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/GMXOracle.sol#L194-214">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/GMXOracle.sol#L194-214</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/GMXOracle.sol#L311-315">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/GMXOracle.sol#L311-315</a>


## Summary
Chainlink does not provide a price feed for SOL token on Avalanche.

## Vulnerability Details
One of the in-scope tokens ```SOL``` on the ```Avalanche``` blockchain (see README.md) does not have a corresponding Chainlink pricefeed which makes pricing impossible as currently designed.
See available Chainlink pricefeeds [here](https://data.chain.link/ethereum/mainnet/crypto-usd/sol-usd)

Price Feeds are not set in the constructor of ```GMXVault.sol``` so it is possible that the Strategy Vault could be deployed before the missing price feed was noticed.

## Impact
This issue affects some core protocol functions, which would make the core operations of a Strategy Vault using SOL on Avalanche impossible:
 ```GMXReader.sol::convertToUsdValue()```
 ```GMXReader.sol::delta()```
 ```GMXOracle.sol::_getTokenPriceMinMaxFormatted()```

## Tools Used
Manual Review

## Recommendations
Use another Oracle for pricing SOL or remove SOL from the scope of eligible tokens on the AValanche chain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | FalconHoof |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

