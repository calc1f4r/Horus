---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37438
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

First deposit attack via share price manipulation

### Overview


This bug report describes a problem in the ERC4626 contracts where an attacker can manipulate the share price and steal tokens from other depositors. The issue is caused by a method in the GlmRouter.sol contract that allows anyone to deposit GM tokens directly into the vault and mint shares. This can lead to a scenario where one depositor inflates the share price and gains more tokens than they deposited, while other depositors receive less than what they deposited. The report recommends implementing a fixed and high amount of shares on the first deposit, seeding the pool during deployment, and sending shares to an empty address to make the attack more difficult. The bug has been resolved.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

ERC4626 contracts are subject to a share price manipulation attack that allows an attacker to steal underlying tokens from other depositors.

In Contract GlmRouter.sol, the method `gmTokenDeposit(..)` allows anyone to deposit GM tokens directly into the vault and mint shares.

Consider the following scenario:

- Alice deposited 1e12 gm tokens using the `gmTokenDeposit(...)` method.
- Vault mints 1 wei share for Alice (1e12 gm tokens when converted to USDC will be 1 wei in the manager contract)
- Now Alice inflated the share price by directly transferring the gm tokens to the Vault contract.
- Now the share price is (total assets/ total supply) => (10*1e6)/(1)

- Now let’s say Bob deposits 19*1e18 GM tokens, and Bob gets shares = (19*1e6)/(10*1e6) => 1 share
- Now Alice can redeem her share for (10+19)/2 = 14.5 GM tokens which is more than what she deposited.
- Bob will also get 14.5 GM tokens, way less than what Bob deposited.

**Recommendation**: 

- On the first deposit consider minting a fixed and high amount of shares irrespective of deposited shares to mitigate the rounding issue.
- Consider seeding the pool during deployment in the constructor.
- Consider sending 1000 wei of shares to `address(0)` to significantly increase the attack cost for the attacker.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

