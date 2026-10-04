---
# Core Classification
protocol: Hubble
chain: everychain
category: uncategorized
vulnerability_type: first_depositor_issue

# Attack Vector Details
attack_type: first_depositor_issue
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1517
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-hubble-contest
source_link: https://code4rena.com/reports/2022-02-hubble
github_link: https://github.com/code-423n4/2022-02-hubble-findings/issues/42

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - first_depositor_issue

protocol_categories:
  - dexes
  - services
  - derivatives
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - danb
  - cmichel
---

## Vulnerability Title

[H-03] InsuranceFund depositors can be priced out & deposits can be stolen

### Overview


This bug report is about a vulnerability in the InsuranceFund.sol contract, which is part of the 2022-02-hubble repository on GitHub. The vulnerability allows attackers to increase the share price to very high amounts and price out smaller depositors. An attacker can call the deposit and withdraw functions to mint zero shares and receive the entire pool balance, making a profit. The recommended mitigation steps are to require a minimum deposit amount and sending initial shares to the zero address, like UniswapV2 does to make the attack more expensive.

### Original Finding Content

_Submitted by cmichel, also found by danb_

<https://github.com/code-423n4/2022-02-hubble/blob/8c157f519bc32e552f8cc832ecc75dc381faa91e/contracts/InsuranceFund.sol#L44-L54><br>

The `InsuranceFund.deposit` function mints initial `shares` equal to the deposited amount.<br>
The deposit / withdraw functions also use the VUSD contract balance for the shares computation. (`balance() = vusd.balanceOf(address(this))`)

It's possible to increase the share price to very high amounts and price out smaller depositors.

### Proof of Concept

*   `deposit(_amount = 1)`: Deposit the smallest unit of VUSD as the first depositor. Mint 1 share and set the total supply and VUSD balance to `1`.
*   Perform a direct transfer of `1000.0` VUSD to the `InsuranceFund`. The `balance()` is now `1000e6 + 1`
*   Doing any deposits of less than `1000.0` VUSD will mint zero shares: `shares = _amount * _totalSupply / _pool = 1000e6 * 1 / (1000e6 + 1) = 0`.
*   The attacker can call `withdraw(1)` to burn their single share and receive the entire pool balance, making a profit. (`balance() * _shares / totalSupply() = balance()`)

I give this a high severity as the same concept can be used to always steal the initial insurance fund deposit by frontrunning it and doing the above-mentioned steps, just sending the frontrunned deposit amount to the contract instead of the fixed `1000.0`.
They can then even repeat the steps to always frontrun and steal any deposits.

### Recommended Mitigation Steps

The way [UniswapV2 prevents this](https://github.com/Uniswap/v2-core/blob/4dd59067c76dea4a0e8e4bfdda41877a6b16dedc/contracts/UniswapV2Pair.sol#L121) is by requiring a minimum deposit amount and sending `1000` initial shares to the zero address to make this attack more expensive.
The same mitigation can be done here.

**[atvanguard (Hubble) confirmed](https://github.com/code-423n4/2022-02-hubble-findings/issues/42)**



***
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Hubble |
| Report Date | N/A |
| Finders | danb, cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-hubble
- **GitHub**: https://github.com/code-423n4/2022-02-hubble-findings/issues/42
- **Contest**: https://code4rena.com/contests/2022-02-hubble-contest

### Keywords for Search

`First Depositor Issue`

