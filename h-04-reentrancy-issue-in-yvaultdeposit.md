---
# Core Classification
protocol: JPEG'd
chain: everychain
category: reentrancy
vulnerability_type: reentrancy

# Attack Vector Details
attack_type: reentrancy
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1910
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-jpegd-contest
source_link: https://code4rena.com/reports/2022-04-jpegd
github_link: https://github.com/code-423n4/2022-04-jpegd-findings/issues/81

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - reentrancy

protocol_categories:
  - lending
  - dexes
  - cdp
  - services
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-04] Reentrancy issue in yVault.deposit

### Overview


This bug report is about an exploit in the yVault contract. When the deposit function is triggered, the balance is cached and then a token.transferFrom is triggered which can lead to exploits if the token is a token that gives control to the sender, like ERC777 tokens. An example of this exploit is if the balance is 1000 and 1000 is deposited, the attacker can split the 1000 into two 500 deposits and use re-entrancy to profit. This would allow them to withdraw 1250 shares and receive 1111.111111111 tokens, which is a profit of 111 tokens. To mitigate this exploit, it is recommended that the safeTransferFrom should be the last call in the deposit function.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-04-jpegd/blob/e72861a9ccb707ced9015166fbded5c97c6991b6/contracts/vaults/yVault/yVault.sol#L144-L145


## Vulnerability details

## Impact
In `deposit`, the balance is cached and then a `token.transferFrom` is triggered which can lead to exploits if the `token` is a token that gives control to the sender, like ERC777 tokens.

#### POC
Initial state: `balance() = 1000`, shares `supply = 1000`.
Depositing 1000 amount should mint 1000 supply, but one can split the 1000 amounts into two 500 deposits and use re-entrancy to profit.

- Outer `deposit(500)`: `balanceBefore = 1000`. Control is given to attacker ...
- Inner `deposit(500)`: `balanceBefore = 1000`. `shares = (_amount * supply) / balanceBefore = 500 * 1000 / 1000 = 500` shares are minted ...
- Outer `deposit(500)` continues with the mint: `shares = (_amount * supply) / balanceBefore = 500 * 1500 / 1000 = 750` are minted.
- Withdrawing the `500 + 750 = 1250` shares via `withdraw(1250)`, the attacker receives `backingTokens = (balance() * _shares) / supply = 2000 * 1250 / 2250 = 1111.111111111`. The attacker makes a profit of `1111 - 1000 = 111` tokens.
- They repeat the attack until the vault is drained.

## Recommended Mitigation Steps
The `safeTransferFrom` should be the last call in `deposit`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | JPEG'd |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-jpegd
- **GitHub**: https://github.com/code-423n4/2022-04-jpegd-findings/issues/81
- **Contest**: https://code4rena.com/contests/2022-04-jpegd-contest

### Keywords for Search

`Reentrancy`

