---
# Core Classification
protocol: Beanstalk Bip
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31265
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
github_link: none

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
finders_count: 2
finders:
  - Giovanni Di Siena
  - Carlos Amarante
---

## Vulnerability Title

`LibEthUsdOracle::getEthUsdPrice` design changes should be documented

### Overview

See description below for full details.

### Original Finding Content

Before BIP-38, the `LibEthUsdOracle::getEthUsdPrice` function had the following behavior:
1. If the difference between the Chainlink ETH/USD oracle and the Uniswap ETH/USDC TWAP oracle (considering a 15-minute window) prices was below `0.5%`, then it would return the average of both values. Now, this difference should be below `0.3%`.
2. If the difference between the Chainlink ETH/USD oracle and the Uniswap ETH/USDC TWAP oracle (considering a 15-minute window) was greater than the difference between the Chainlink ETH/USD oracle and the Uniswap ETH/USDT TWAP oracle (considering a 15-minute window), then:
    * If the difference between the Chainlink ETH/USD oracle and the Uniswap ETH/USDT TWAP oracle (considering a 15 minute-window) prices was below `2%`, it would return the average of these two prices. Now, this difference should be less than `1%`.
    * Otherwise, it would return 0, indicating that the oracle is broken or stale. Now, it returns the Chainlink ETH/USD oracle price, assuming it is correct.
3. Otherwise:
    * If the difference between the Chainlink ETH/USD oracle and the Uniswap ETH/USDC TWAP oracle (considering a 15-minute window) prices was below `2%`, it would return the average of these two prices. Now, this difference should be less than `1%`.
    * Otherwise, it would return 0, indicating that the oracle is broken or stale. Now, it returns the Chainlink ETH/USD oracle price, assuming it is correct.

In essence, this function now assumes that the Chainlink ETH/USD price is correct as long as it is not stale or broken (if it returns 0). In cases where the difference between this price and the Uniswap ETH/USDC TWAP oracle price or Uniswap ETH/USDT TWAP oracle price is outside certain thresholds, it considers and averages with one of these values. Previously, if this difference was not within certain bounds, the oracle was considered to be broken.

**Beanstalk Farms:** This change was actually made before BIP-37 was deployed, but this modification was omitted from the previous Cyfrin audit. Thus, no functionality in `getEthUsdPrice` changed as a part of BIP-38.

The comments in `LibEthUsdOracle` were not correct and have been updated in commit [968f783](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/968f783d3d062b93f9f692accc9e7ad60d4f1ab6).

**Cyfrin:** Acknowledged. Comments now match the code's intention.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Beanstalk Bip |
| Report Date | N/A |
| Finders | Giovanni Di Siena, Carlos Amarante |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

