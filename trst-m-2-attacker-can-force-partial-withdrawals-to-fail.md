---
# Core Classification
protocol: Ninja Yield Farming 
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18880
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-08-Ninja Yield Farming v3.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-2 Attacker can force partial withdrawals to fail

### Overview


This bug report is about an issue in Ninja Vaults, which is a token-based platform. The issue arises when users call the `withdraw()` function to take back their deposited tokens. The issue is that the calculated value of r (the relative share of the user's shares of the total balance kept in the vault) can be more than the _amount, causing an overflow in `withdraw()` and freezing the withdrawal. This can be done by an attacker sending a tiny amount of underlying token directly to the contract, to make the shares go out of sync.

The team response to this bug report was to accept it after further investigation. The proposed mitigation was to redesign the user structure, taking into account that the balance of the underlying token can be externally manipulated. The team also agreed to remove the double accounting (user.amount) and to dynamically calculate the value from the users share balance * price per share. Additionally, a public view function, getUserUnderlyingBalance, was added to assist (which also allows dynamic underlying decimals).

### Original Finding Content

**Description:**
In Ninja vaults, users call `withdraw()` to take back their deposited tokens. There is 
bookkeeping on remaining amount:

```solidity
      uint256 userAmount = balanceOf(msg.sender);
         // - Underlying (Frontend ONLY)
            if (userAmount == 0) {
            user.amount = 0;
         } else {
         user.amount -= r;
      }
```
If the withdraw is partial (some tokens are left), user.amount is decremented by r.

```solidity
      uint256 r = (balance() * _shares) / totalSupply();
```
Above, r is calculated as the relative share of the user's _shares of the total balance kept in 
the vault.

We can see that user.amount is incremented in deposit().

```solidity
      function deposit(uint256 _amount) public nonReentrant {
      …
            user.amount += _amount;
      …
         }
```
The issue is that the calculated r can be more than _amount , causing an overflow in 
`withdraw()` and freezing the withdrawal. All attacker needs to do is send a tiny amount of 
underlying token directly to the contract, to make the shares go out of sync.

**Recommended Mitigation:**
Redesign **user** structure, taking into account that balance of underlying can be externally 
manipulated

**Team Response:**
Accepted after further investigation. we agreed to remove the double accounting 
(user.amount) and to dynamically calculate the value from the users share balance * price 
per share. We added the public view function getUserUnderlyingBalance to assist (which 
also allows dynamic underlying decimals).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Ninja Yield Farming  |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-08-Ninja Yield Farming v3.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

