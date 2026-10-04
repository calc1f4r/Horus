---
# Core Classification
protocol: UMA Optimistic Governor Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10543
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-optimistic-governor-audit/
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
  - bridge
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Change of collateral could result in unintended bond value

### Overview


The OptimisticGovernor contract requires users to provide a preconfigured quantity of an ERC20 token as bond to propose a set of transactions. If the set of transactions is rejected, the proposer will lose their bond. To change the collateral token address and its amount the contract owner will generally have to call two separate functions, setBond and setCollateral. If the contract owner is an EOA, then setBond and setCollateral will be called in two separate transactions which allows a third party to call proposeTransactions in between. This will lead to the creation of a proposal with an unintended bond value, potentially lower than intended. To solve this issue, the developers proposed renaming setCollateral to setCollateralAndBond and updating both the bond value and the bond token address in the same function call. This bug has now been fixed in commit 5794c2040cc85aced20ef1145aa0329a1c8d8236 in pull request #3912.

### Original Finding Content

The [`OptimisticGovernor`](https://github.com/UMAprotocol/protocol/blob/fca8e24275e928f7ddf660b5651eb93b87f70afb/packages/core/contracts/zodiac/OptimisticGovernor.sol) contract requires users to provide a preconfigured quantity of an ERC20 token as bond to propose a set of transactions. If the set of transactions is rejected, the proposer will lose their bond.


To change the collateral token address and its amount the contract owner will generally have to call two separate functions, namely [`setBond`](https://github.com/UMAprotocol/protocol/blob/fca8e24275e928f7ddf660b5651eb93b87f70afb/packages/core/contracts/zodiac/OptimisticGovernor.sol#L119) to set the new amount and [`setCollateral`](https://github.com/UMAprotocol/protocol/blob/fca8e24275e928f7ddf660b5651eb93b87f70afb/packages/core/contracts/zodiac/OptimisticGovernor.sol#L128) to set the new ERC20 address of the bond token.


If the contract owner is an EOA, then `setBond` and `setCollateral` will be called in two separate transactions which allows a third party to call [`proposeTransactions`](https://github.com/UMAprotocol/protocol/blob/fca8e24275e928f7ddf660b5651eb93b87f70afb/packages/core/contracts/zodiac/OptimisticGovernor.sol#L180) in between. This will lead to the creation of a proposal with an unintended bond value. In fact, the realized bond could potentially have a much lower value than intended.


Consider renaming `setCollateral` to `setCollateralAndBond` and updating both the bond value and the bond token address in the same function call.


***Update:** Fixed as of commit `5794c2040cc85aced20ef1145aa0329a1c8d8236` in [pull request #3912](https://github.com/UMAprotocol/protocol/pull/3912).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Optimistic Governor Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-optimistic-governor-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

