---
# Core Classification
protocol: Yearn v2 Vaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16952
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
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
finders_count: 2
finders:
  - Gustavo Grieco
  - Mike Martel
---

## Vulnerability Title

Large withdrawals can block other users from making withdrawals

### Overview


Bug report summary:
This bug report is about a data validation issue in the Vault.vy code. It is classified as a high difficulty bug. The issue is that when a user calls the withdraw function, the amount withdrawn is determined using the total number of free tokens in the vault and the amount of totalDebt of each strategy in the withdrawalQueue. This could cause a large withdrawal to block other users from making subsequent withdrawals. The short-term recommendation is to clearly document withdrawal-related properties to make users of the vaults aware of them, and the long-term recommendation is to review how the system invariants affect the usability of the contract and properly document corner cases so that users will know what to expect if a contract interaction is blocked.

### Original Finding Content

## Type: Data Validation
## Target: Vault.vy

**Difficulty:** High

### Description
When a user calls the `withdraw` function, the amount withdrawn is determined using the total number of free tokens in the vault and the amount of `totalDebt` of each strategy in the `withdrawalQueue`.

```python
for strategy in self.withdrawalQueue:
    if strategy == ZERO_ADDRESS:
        break
    vault_balance: uint256 = self.token.balanceOf(self)
    if value <= vault_balance:
        break
    amountNeeded: uint256 = value - vault_balance
    amountNeeded = min(amountNeeded, self.strategies[strategy].totalDebt)
    if amountNeeded == 0:
        continue
    loss: uint256 = Strategy(strategy).withdraw(amountNeeded)
    withdrawn: uint256 = self.token.balanceOf(self) - vault_balance
```

*Figure 10.1:* Part of the vault’s withdrawal function detailing the maximum withdrawal amount for each strategy.

Since the vault can contain more assets than a user can withdraw, a large withdrawal can block other vault users from making subsequent withdrawals.

### Exploit Scenario
Eve makes a large withdrawal from a vault, draining the available tokens from the vault and the strategies in the `withdrawalQueue`. Other users of the vault panic because they cannot retrieve funds.

### Recommendations
- **Short term:** Clearly document withdrawal-related properties to make users of the vaults aware of them.
- **Long term:** Review how the system invariants affect the usability of the contract and properly document corner cases so that users will know what to expect if a contract interaction is blocked.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yearn v2 Vaults |
| Report Date | N/A |
| Finders | Gustavo Grieco, Mike Martel |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf

### Keywords for Search

`vulnerability`

