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
solodit_id: 11107
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/celo-contracts-audit/
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

[M01] Mint and burn functionalities can break

### Overview


This bug report is about the `StableToken` contract, which is part of the Celo Protocol. This contract contains two functions, `mint` and `burn`, which make use of the `getAddressForOrDie` function of the `Registry` contract. The `initialize` function of the `StableToken` contract allows setting an `exchangeRegistryId` state variable, which corresponds to a different `Exchange` contract than the default one. However, the `initialize` function doesn't check if the `exchangeIdentifier` parameter passed as input is a non-null value or if it corresponds to a valid address in the `registry` mapping of the `Registry` contract. If incorrect or null values are set, calls to the `mint` and `burn` functions will fail. To avoid this, the necessary checks should be implemented in the `exchangeIdentifier` parameters before setting it in the `exchangeRegistryId` variable. The cLabs team has decided to not fix this issue for the time being.

### Original Finding Content

The [`mint`](https://github.com/celo-org/celo-monorepo/blob/6b5143a142f4715a9b8bc428b1cf391eec414ec8/packages/protocol/contracts/stability/StableToken.sol#L223) and [`burn`](https://github.com/celo-org/celo-monorepo/blob/6b5143a142f4715a9b8bc428b1cf391eec414ec8/packages/protocol/contracts/stability/StableToken.sol#L272) functions of the `StableToken` contract make use of the [`getAddressForOrDie`](https://github.com/celo-org/celo-monorepo/blob/6b5143a142f4715a9b8bc428b1cf391eec414ec8/packages/protocol/contracts/common/Registry.sol#L42) of the `Registry` contract. This function will revert if the passed parameter is associated with a null address in the [`registry`](https://github.com/celo-org/celo-monorepo/blob/6b5143a142f4715a9b8bc428b1cf391eec414ec8/packages/protocol/contracts/common/Registry.sol#L15) mapping.  

Having said that, one of the changes introduced in the `StableToken` contract is the ability to interact with an `Exchange` contract that is different from the default one. This is represented by the [`exchangeRegistryId`](https://github.com/celo-org/celo-monorepo/blob/6b5143a142f4715a9b8bc428b1cf391eec414ec8/packages/protocol/contracts/stability/StableToken.sol#L71) state variable, which is [set in the `initialize`](https://github.com/celo-org/celo-monorepo/blob/6b5143a142f4715a9b8bc428b1cf391eec414ec8/packages/protocol/contracts/stability/StableToken.sol#L142) function.


The `initialize` function doesn’t check whether the `exchangeIdentifier` parameter passed as input parameter is a non-null value or if it corresponds to a valid address in the `registry` mapping of the `Registry` contract.


If an incorrect or null value is set:


* Calls to the `mint` function will fail in the `getAddressForOrDie` [internal call](https://github.com/celo-org/celo-monorepo/blob/6b5143a142f4715a9b8bc428b1cf391eec414ec8/packages/protocol/contracts/stability/StableToken.sol#L225) even if the caller is a validator.
* Calls to the `burn` function will fail internally [in the `onlyRegisteredContract` modifier](https://github.com/celo-org/celo-monorepo/blob/6b5143a142f4715a9b8bc428b1cf391eec414ec8/packages/protocol/contracts/common/UsingRegistry.sol#L55).


To avoid initializing the `StableToken` contract with incorrect values that could potentially break some functionalities, consider implementing the necessary checks in the `exchangeIdentifier` parameters before setting it in the `exchangeRegistryId` variable.


**Update:** *The cLabs team decided to not fix this for the time being. In their words: “The risk here is only on `StableTokenEUR.sol` and `ExchangeEUR.sol` not working after CR3, and these contracts won’t be active until subsequent proposals regardless, at which point we will make fixes. In fact, we are **intentionally** providing an invalid address via parameters”.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

