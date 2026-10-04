---
# Core Classification
protocol: Celo Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11095
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/celo-contracts-audit/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - launchpad
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L15] Stable token may not be backed up in the reserve

### Overview

See description below for full details.

### Original Finding Content

The [`Reserve` contract](https://github.com/celo-org/celo-monorepo/blob/b2f0a58fcc7667d41585123aae5b24c47aa894f6/packages/protocol/contracts/stability/Reserve.sol#L18) implements the functionality that ensures the price-stability of the stable token with respect to their pegs.


To do that, a tax called [Tobin tax](https://docs.celo.org/celo-codebase/protocol/stability/tobin-tax) allows the protocol to transfer CELO assets into the reserve to preserve the amount of collateral needed for the peg.


If the CELO reserve ratio, [defined as the ratio of the current CELO reserve balance to total stable token valuation](https://github.com/celo-org/celo-monorepo/blob/b2f0a58fcc7667d41585123aae5b24c47aa894f6/packages/protocol/contracts/stability/Reserve.sol#L456), is less than the [`tobinTaxReserveRatio` variable](https://github.com/celo-org/celo-monorepo/blob/b2f0a58fcc7667d41585123aae5b24c47aa894f6/packages/protocol/contracts/stability/Reserve.sol#L39), then it will be applied a [`tobinTax` value](https://github.com/celo-org/celo-monorepo/blob/b2f0a58fcc7667d41585123aae5b24c47aa894f6/packages/protocol/contracts/stability/Reserve.sol#L38) to raise the reserve’s balance of CELO assets.


Nevertheless, the `tobinTaxReserveRatio` variable’s value can be changed by the protocol when calling the [`setTobinTaxReserveRatio` function](https://github.com/celo-org/celo-monorepo/blob/b2f0a58fcc7667d41585123aae5b24c47aa894f6/packages/protocol/contracts/stability/Reserve.sol#L141), where no further validation checks are made to the input parameter. Due to that, if the input parameter is less than 100%, then the collateral that the protocol will seek to ensure the peg with the stable token will not cover the totality of the token’s supply value.


Although it is unlikely that a proposal could be passed, succeeded, and set a problematic value, the human component will allways be present, allowing possible mistaken values in the protocol.


Consider either requiring a `tobinTaxReserveRatio` value greater than 100% or documenting the decision of being able to set lower ratios.


***Update**: Acknowledged, and will not fix. The cLabs team’s response was:*



> 
> It is true that the `TobinTax` represents the on-chain collateralization ratio, which is a problem in some scenarios:  
> 
> – Not all CELO in the reserve is in the reserve contract, some could be held in custody, see https://celoreserve.org/
> 
> 
> * Assuming all CELO in the reserve is in the smart contract, even if we know the target reserve ratio on-chain, there’s no guarantee that the target ratio is met, due to market volatility
> 
> 
> Thus, it is difficult to fully automate when the tobin tax should kick in. Even if all the reserve assets are on chain (like using some wrapped version of BTC, ETH and DAI on Celo), we’d need oracles providing the price for all of them.
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Celo Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/celo-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

