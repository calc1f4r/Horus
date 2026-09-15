---
# Core Classification
protocol: Evterminal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34061
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/EVTerminal-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-10] The Owner should be able to change the Liquidity Provider

### Overview


This bug report addresses an issue with liquidity providers in a contract. If a liquidity provider's account is compromised, the owner should be able to replace them before the liquidity lock is reached. However, the current code only allows the liquidity provider to make changes, making it impossible for the owner to do so. The report suggests changing the code to allow the owner to make changes as well, without compromising the design of the contract. This bug has a high impact on the contract and a low likelihood of occurring. 

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

Liquidity providers have the ability to remove reserves which will drain the contracts balance.
Only tokens with a trusted liquidity provider are likely to be active - if the liquidity provider account is compromised:

- Private key leaked
- Seized

In such cases, the `owner` should be able to replace the liquidity provider before the liquidity lock is reached. However, the `owner` cannot replace the liquidity provider because `setLiquidityProvider` can only be called by the liquidity provider

```solidity
    function setLiquidityProvider(
        address _newLiquidityProvider
    ) external onlyLiquidityProvider {
        _liquidityProvider = _newLiquidityProvider;
        if (_newLiquidityProvider == address(0)) _opt.liquidityProviderRenounced = true;
        if (_newLiquidityProvider != address(0)) _opt.liquidityProviderRenounced = false;
    }
```

**Recommendations**

Consider changing the `onlyLiquidityProvider` to allow calls from the liquidity provider AND the owner.

**EV Terminal comment**

_We want to keep the design so that even when owner is renounced, liquidity can still be extended/withdrawn if needed._

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Evterminal |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/EVTerminal-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

