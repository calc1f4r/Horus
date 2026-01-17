---
# Core Classification
protocol: Yield Ninja
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19128
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-11-01-Yield Ninja.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[L-02] If `underlying` or `rewardToken` is a two-address token then `inCaseTokensGetStuck` method can be used to rug users

### Overview

See description below for full details.

### Original Finding Content

**Proof of Concept**

Some ERC20 tokens on the blockchain are deployed behind a proxy, so they have at least 2 entrypoints (the proxy and the implementation) for their functionality. Example is Synthetix’s `ProxyERC20` contract from where you can interact with `sUSD, sBTC etc). If such a token was used as the `underlying`token in a vault, then the owner will be able to rug all depositors with the`inCaseTokensGetStuck` method, even though it has the following checks

```solidity
if (_token == address(underlying)) {
      revert NYProfitTakingVault__CannotWithdrawUnderlying();
}
if (_token == address(rewardToken)) {
      revert NYProfitTakingVault__CannotWithdrawRewardToken();
}
```

Since the tokens have multiple addresses the admin can give another address and pass those checks.

**Impact**

The potential impact is 100% loss of deposited tokens for users, but it requires a malicious/compromised owner and a special type of ERC20 token used in the vault.

**Recommendation**

Instead of checking the address of the withdrawn token, it is a better approach to check the balance of `underlying` and `rewardToken` before and after the transfer and to verify it is the same.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Yield Ninja |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-11-01-Yield Ninja.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

