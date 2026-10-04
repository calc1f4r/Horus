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
solodit_id: 25644
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-timeswap
source_link: https://code4rena.com/reports/2022-01-timeswap
github_link: https://github.com/code-423n4/2022-01-timeswap-findings/issues/43

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
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] no reentrancy guard on mint() function that has a callback

### Overview


A bug has been identified in the CollateralizedDebt.sol contract, which is part of the Timeswap protocol. The mint() function in the contract calls \_safeMint() which has a callback to the "to" address argument. This could leave the protocol vulnerable to malicious actors both from inside and outside the system. To mitigate this, a reentrancy guard modifier should be added to the mint() function in CollateralizedDebt.sol. This has been confirmed by Mathepreneur (Timeswap). Reentrancy guards are important protection mechanisms in smart contracts that help to protect against malicious actors by preventing them from executing malicious code multiple times. This is done by ensuring that the contract is in a consistent state before and after the execution of the malicious code.

### Original Finding Content

_Submitted by jayjonah8, also found by Fitraldys_

In CollateralizedDebt.sol, the mint() function calls \_safeMint() which has a callback to the "to" address argument.  Functions with callbacks should have reentrancy guards in place for protection against possible malicious actors both from inside and outside the protocol.

#### Proof of Concept

- <https://github.com/code-423n4/2022-01-timeswap/blob/main/Timeswap/Timeswap-V1-Convenience/contracts/CollateralizedDebt.sol#L76>

- <https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L263>

- <https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L395>

#### Recommended Mitigation Steps

Add a reentrancy guard modifier on the mint() function in CollateralizedDebt.sol


**[Mathepreneur (Timeswap) confirmed](https://github.com/code-423n4/2022-01-timeswap-findings/issues/43)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Timeswap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-timeswap
- **GitHub**: https://github.com/code-423n4/2022-01-timeswap-findings/issues/43
- **Contest**: https://code4rena.com/reports/2022-01-timeswap

### Keywords for Search

`vulnerability`

