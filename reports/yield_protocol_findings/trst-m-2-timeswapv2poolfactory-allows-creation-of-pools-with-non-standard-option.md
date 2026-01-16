---
# Core Classification
protocol: Timeswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20276
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Timeswap.md
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

protocol_categories:
  - liquid_staking
  - yield
  - services
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-2 TimeswapV2PoolFactory allows creation of pools with non-standard option contracts

### Overview


A bug was identified in the `TimeswapV2PoolFactory.create()` function, which did not check that the provided options contract was created via the official TimeswapV2OptionFactory. This posed a severe risk for users who interacted with Timeswap pools, as malicious actors could deploy malicious TimeswapV2Option contracts that would send all funds to the malicious actor after maturity, and create a pool for the malicious options contract using the official Timeswap pool factory. To mitigate this issue, the `TimeswapV2PoolFactory.create()` function was updated to take a pair of token addresses instead of an options contract address, allowing it to get an options contract address from the official TimeswapV2OptionFactory deployment. The bug has been identified and fixed, and a mitigation review was conducted.

### Original Finding Content

**Description:**
The `TimeswapV2PoolFactory.create()` function doesn’t check that the provided options
contract was created via the official TimeswapV2OptionFactory. This allows creation of official
pools (i.e. pools created via the official TimeswapV2PoolFactory) with non-official underlying
options contracts. Since option contracts accept and store user funds, this poses a severe risk
for users who interact with Timeswap pools.

A malicious actor can:
1) deploy a malicious TimeswapV2Option contract that sends all funds to the malicious actor
after maturity;
2) create a pool for the malicious options contract using the official Timeswap pool factory;
3) trick users into using the pool to provide liquidity and lend and borrow options.
Users will trust the pool because it’ll be created via the official factory.

**Recommended Mitigation:**
Consider reworking the `TimeswapV2PoolFactory.create()` function to take a pair of token
addresses instead of an options contract address. Having token addresses, the function can
get an options contract address from the official TimeswapV2OptionFactory deployment.

**Team Response:**
Has been identified and fixed here: commit (https://github.com/Timeswap-Labs/Timeswap-V2-Monorepo/commit/e32cf3697691c20be327978b50947c0172cb2240)

**Mitigation review:**
TimeswapV2PoolFactory.create() was updated as per the recommendation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Timeswap |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Timeswap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

