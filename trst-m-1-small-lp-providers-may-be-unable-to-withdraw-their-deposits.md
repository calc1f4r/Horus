---
# Core Classification
protocol: Lyra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18896
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-1 small LP providers may be unable to withdraw their deposits

### Overview


This bug report is about LiquidityPool’s initiateWithdraw() function, which requires that the withdrawn value is above a minimum parameter or that withdrawn tokens is above the minimum parameter. The issue is that minDepositWithdraw is measured in dollars while amountLiquidityToken is LP tokens. This means that users may not be able to withdraw LP with the token amount that was above the minimum at deposit time, or vice versa. A recommended mitigation suggested was to calculate an average exchange rate at which users have minted and use it to verify withdrawal amount is satisfactory. However, the team response was that this solution would add far more complexity to the system than the benefit it would provide, and so small (<$1) LPs will need to find an alternative place to liquidate their holdings like a uniswap pool. This will not be resolved at the protocol level, as the minimums are necessary to prevent unwanted spam.

### Original Finding Content

**Description:**
In LiquidityPool’s initiateWithdraw(), it’s required that withdrawn value is above a minimum 
parameter, or that withdrawn tokens is above the minimum parameter.
```solidity 
      if (withdrawalValue < lpParams.minDepositWithdraw && 
          amountLiquidityToken < lpParams.minDepositWithdraw) {
      revert MinimumWithdrawNotMet(address(this), withdrawalValue, lpParams.minDepositWithdraw);
      }
```
The issue is that **minDepositWithdraw** is measured in dollars while **amountLiquidityToken** is 
LP tokens. The intention was that if LP tokens lost value and a previous deposit is now worth 
less than **minDepositWithdraw**, it would still be withdrawable. However, the current 
implementation doesn’t check for that correctly, since the LP to dollar exchange rate at 
deposit time is not known, and is practically being hardcoded as 1:1 here. The impact is that 
users may not be able to withdraw LP with the token amount that was above the minimum at 
deposit time, or vice versa

**Recommended Mitigation:**
Consider calculating an average exchange rate at which users have minted and use it to verify 
withdrawal amount is satisfactory.

**Team Response:**
While valid, the proposed solution adds far more complexity to the system than the benefit it 
would provide. Small (<$1) LPs will need to find an alternative place to liquidate their holdings 
like a uniswap pool. This will not be resolved at the protocol level.
As keepers process deposits and withdrawals, the minimums are necessary to prevent 
unwanted spam.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Lyra Finance |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

