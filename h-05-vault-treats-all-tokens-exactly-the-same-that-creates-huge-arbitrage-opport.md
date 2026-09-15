---
# Core Classification
protocol: yAxis
chain: everychain
category: logic
vulnerability_type: flash_loan

# Attack Vector Details
attack_type: flash_loan
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 766
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/2

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - flash_loan
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - jonah1005
  - cmichel  itsmeSTYJ
---

## Vulnerability Title

[H-05] Vault treats all tokens exactly the same that creates (huge) arbitrage opportunities.

### Overview


Jonah1005 reported a vulnerability in the v3 vault, which treats all valid tokens exactly the same. This means that depositing 1 million DAI would get the same share as depositing 1 million USDT. The user can then withdraw their share in another token, with a withdrawal fee of 0.1%. This could make the vault vulnerable to a flashloan attack, as the arbitrage space is about 0.8%.

The issue is located at the deposit function, where the share is minted according to the calculation and burned at another point. A sample exploit in web3.py was provided to demonstrate the vulnerability.

The recommended mitigation steps suggest either taking iearn token's architecture as a reference, or creating a vault for each token.

### Original Finding Content

_Submitted by jonah1005, also found by cmichel and itsmeSTYJ_

#### Impact
The v3 vault treats all valid tokens exactly the same. Depositing 1M DAI would get the same share as depositing 1M USDT. User can withdraw their share in another token. Though there's `withdrawalProtectionFee` (0.1 percent), the vault is still a no slippage stable coin exchange.

Also, I notice that 3crv_token is added to the vault in the test. Treating 3crv_token and all other stable coins the same would make the vault vulnerable to flashloan attack. 3crv_token is an lp token and at the point of writing, the price of it is 1.01. The arbitrage space is about 0.8 percent and makes the vault vulnerable to flashloan attacks.

Though the team may not add crv_token and dai to the same vault, its design makes the vault vulnerable. Strategies need to be designed with super caution or the vault would be vulnerable to attackers.

Given the possibility of a flashloan attack, I consider this a high-risk issue.

#### Proof of Concept
The issue locates at the deposit function ([Vault.sol#L147-L180](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/Vault.sol#L147-L180)).
The share is minted according to the calculation here

```solidity
_shares = _shares.add(_amount);
```

The share is burned at [Vault.sol L217](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/Vault.sol#L217)
```solidity
uint256 _amount = (balance().mul(_shares)).div(totalSupply());
```

Here's a sample exploit in web3.py.

```python
deposit_amount = 100000 * 10**6
user = w3.eth.accounts[0]
get_token(usdt, user, deposit_amount)
usdt.functions.approve(vault.address, deposit_amount).transact()
vault.functions.deposit(usdt.address, deposit_amount).transact()
vault.functions.withdrawAll(t3crv.address).transact()


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | jonah1005, cmichel  itsmeSTYJ |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/2
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`Flash Loan, Business Logic`

