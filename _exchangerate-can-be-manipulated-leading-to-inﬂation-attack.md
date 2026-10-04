---
# Core Classification
protocol: OpalProtocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54291
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007
source_link: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
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
finders_count: 5
finders:
  - Chad0
  - J4X98
  - golu
  - Victor Okafor
  - 0xTheBlackPanther
---

## Vulnerability Title

_exchangerate can be manipulated, leading to inﬂation attack 

### Overview


The Omnipool contract has a vulnerability that allows attackers to manipulate the exchange rate during deposits, making it unprofitable for other users to deposit into the pool. This can also lead to the attacker draining all funds from the pool. One solution is to execute a deposit immediately after deployment to set a controlled exchange rate. More recommendations can be found on the OpenZeppelin GitHub issue #3706.

### Original Finding Content

## Vulnerability in Omnipool: Manipulation of Exchange Rate

## Context
Omnipool.sol#L679-L688

## Description
The `_exchangeRate` in the Omnipool can be manipulated, allowing an attacker to set an arbitrary exchange rate during the deposit process. This manipulation can make it unprofitable for other users to deposit into the pool.

## Proof of Concept

1. **Hacker Sets Exchange Rate**: The attacker initiates a deposit by setting the `exchangeRate` during a deposit, for example:
   ```solidity
   vm.startPrank(hacker);
   omnipool.deposit(2, 0);
   token.transfer(address(omnipool), 2);
   vm.stopPrank();
   ```

2. **Victims Attempt to Deposit**: Other users (victims) try to deposit into the Omnipool after the exchange rate manipulation. Due to the manipulated exchange rate, victims receive zero LP tokens for their deposits. Example:
   ```solidity
   vm.startPrank(user);
   token.approve(address(omnipool), 10 ** 18);
   omnipool.deposit(10 ** 18, 0);
   vm.stopPrank();
   ```

3. **Attacker Withdraws All Tokens**: The attacker starts to withdraw all tokens from the pool. Example:
   ```solidity
   vm.startPrank(hacker);
   omnipool.withdraw(1, 0);
   ```

## Impact
- The attacker can make the Omnipool unprofitable for users by manipulating the exchange rate during deposits, causing victims to receive zero LP tokens.
- The attacker can then withdraw all tokens from the pool, essentially draining it of funds.

## Recommendation
One of the simplest solutions is to execute a deposit immediately after the deployment of the contract. By doing so, the `exchangeRate` can be adjusted to a desired and controlled value, mitigating the risk of potential manipulation.

Some of the recommendations, along with their pros and cons, can be found in the [OpenZeppelin GitHub issue #3706](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3706).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpalProtocol |
| Report Date | N/A |
| Finders | Chad0, J4X98, golu, Victor Okafor, 0xTheBlackPanther |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007

### Keywords for Search

`vulnerability`

