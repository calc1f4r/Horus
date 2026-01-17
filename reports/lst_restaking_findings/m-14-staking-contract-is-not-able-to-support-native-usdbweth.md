---
# Core Classification
protocol: Abracadabra Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32070
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-abracadabra-money
source_link: https://code4rena.com/reports/2024-03-abracadabra-money
github_link: https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/48

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
  - oracle
  - dexes
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - yixxas
---

## Vulnerability Title

[M-14] Staking contract is not able to support native USDB/WETH

### Overview


This bug report discusses an issue where the yield is lost if the USDB/WETH tokens are used as reward tokens in the protocol. The report recommends adding the ability to claim the yields and provides a link to the fixed code.

### Original Finding Content


Loss of yield if USDB/WETH is used as reward token.

### Proof of Concept

From what I understood from the protocol team, they want to support any ERC20 tokens that are considered safe/well known. I believe USDB/WETH falls into this category.

Both USDB and WETH yield mode are AUTOMATIC by default. `LockingMultiRewards.sol` uses internal accounting to track all rewards that are accrued for users. For instance, when users stake `amount`, `stakingTokenBalance` will increase by `amount` and user's balance will increase by `amount` accordingly. Rewards that are distributed to users are based on these internal accounting values.

The issue here is that,

1.  If USDB/WETH tokens are used as reward tokens, the accrued yield due to automatic rebasing are lost as they cannot be claimed.
2.  If protocol team has not used such tokens as reward tokens yet and becomes aware of this, then it means that they will not be able to use these tokens as reward tokens.

### Recommended Mitigation Steps

Add the ability to set native RebasingERC20 token to `CLAIMABLE` and implement a way to claim the yields to the staking contract.

**[0xCalibur (Abracadabra) confirmed and commented](https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/48#issuecomment-2000439614):**
 > It's fixed here:
 >
> https://github.com/Abracadabra-money/abracadabra-money-contracts/blob/main/src/blast/BlastLockingMultiRewards.sol

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Abracadabra Money |
| Report Date | N/A |
| Finders | yixxas |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-abracadabra-money
- **GitHub**: https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/48
- **Contest**: https://code4rena.com/reports/2024-03-abracadabra-money

### Keywords for Search

`vulnerability`

