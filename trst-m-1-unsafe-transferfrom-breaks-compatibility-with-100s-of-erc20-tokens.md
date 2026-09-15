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
solodit_id: 18879
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

TRST-M-1 Unsafe transferFrom breaks compatibility with 100s of ERC20 tokens

### Overview


The bug report is about a problem with the Ninja vaults. The delegated strategy sends profit tokens to the vault using `depositProfitTokenForUsers()`. However, the code does not use the `safeTransferFrom()` utility from SafeERC20. This means that some profitTokens that don't return a bool in `transferFrom()` will cause a revert and get stuck in the strategy. Examples of such tokens are USDT and BNB. The recommended mitigation for this issue is to use `safeTransferFrom()` from SafeERC20.sol. The team accepted the report and acknowledged that this issue was missed.

### Original Finding Content

**Description:**
In Ninja vaults, the delegated strategy sends profit tokens to the vault using 
`depositProfitTokenForUsers()`. The vault transfers the tokens in using:
```solidity 
         // Now pull in the tokens (Should have permission)
          // We only want to pull the tokens with accounting
                profitToken.transferFrom(strategy, address(this), _amount);
          emit ProfitReceivedFromStrategy(_amount);

```
The issue is that the code doesn't use the `safeTransferFrom()` utility from SafeERC20. 
Therefore, profitTokens that don't return a bool in `transferFrom()` will cause a revert which 
means they are stuck in the strategy. 
Examples of such tokens are USDT, BNB, among hundreds of other tokens.

**Recommended Mitigation:**
Use `safeTransferFrom()` from SafeERC20.sol

**Team Response:**
Accepted. Excellent find. I can't believe we missed this.

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

