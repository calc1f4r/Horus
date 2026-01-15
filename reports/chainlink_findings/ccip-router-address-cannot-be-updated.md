---
# Core Classification
protocol: stake.link
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29735
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clqf7mgla0001yeyfah59c674
source_link: none
github_link: https://github.com/Cyfrin/2023-12-stake-link

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
  - ljj
---

## Vulnerability Title

CCIP router address cannot be updated

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-stake-link/blob/main/contracts/core/ccip/SDLPoolCCIPControllerPrimary.sol">https://github.com/Cyfrin/2023-12-stake-link/blob/main/contracts/core/ccip/SDLPoolCCIPControllerPrimary.sol</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-stake-link/blob/main/contracts/core/ccip/SDLPoolCCIPControllerSecondary.sol">https://github.com/Cyfrin/2023-12-stake-link/blob/main/contracts/core/ccip/SDLPoolCCIPControllerSecondary.sol</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-stake-link/blob/main/contracts/core/ccip/WrappedTokenBridge.sol">https://github.com/Cyfrin/2023-12-stake-link/blob/main/contracts/core/ccip/WrappedTokenBridge.sol</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-stake-link/blob/main/contracts/core/ccip/base/SDLPoolCCIPController.sol">https://github.com/Cyfrin/2023-12-stake-link/blob/main/contracts/core/ccip/base/SDLPoolCCIPController.sol</a>


## Summary

CCIP Router addresses cannot be updated in `SDLPoolCCIPController.sol, SDLPoolCCIPControllerPrimary.sol, SDLPoolCCIPControllerSecondary.sol, WrappedTokenBridge.sol` . 

## Vulnerability Details

On contracts that inherit from `CCIPReceiver`, router addresses need to be updateable. Chainlink may update the router addresses as they did before. This issue introduces a single point of failure that is outside of the protocol's control.

[An example contract](https://github.com/smartcontractkit/ccip-tic-tac-toe/blob/main/contracts/TTTDemo.sol#L81-L83) that uses CCIP. [Taken from Chainlink docs](https://docs.chain.link/ccip/examples#ccip-tic-tac-toe).

[Chainlink documents noticing users about router address updating on testnet.](https://docs.chain.link/ccip/release-notes#v120-release-on-testnet---2023-12-08)

> CCIP v1.0.0 has been deprecated on testnet. You must use the new router addresses mentioned in the [CCIP v1.2.0 configuration page](https://docs.chain.link/ccip/supported-networks/v1_2_0/testnet) **before January 31st, 2024**
> 

On Testnets, router contracts in v1.0.0 and v1.2.0 are different. It means that router contract addresses can change from version to version. So CCIPReceivers should accommodate this. Mainnet is on v1.0.0 which means its router addresses can change with an update.

## Impact

Impact: High
Likelihood: Low

Router address deprecation will cause the protocol to stop working.

## Tools Used

Manual review.

## Recommendations

Implement a function to update the `_router` address. Example shown below:

```jsx
function updateRouter(address routerAddr) external onlyOwner {
        _router = routerAddr;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | stake.link |
| Report Date | N/A |
| Finders | ljj |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-stake-link
- **Contest**: https://www.codehawks.com/contests/clqf7mgla0001yeyfah59c674

### Keywords for Search

`vulnerability`

