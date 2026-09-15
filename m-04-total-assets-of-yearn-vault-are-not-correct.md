---
# Core Classification
protocol: Popcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22001
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/728

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
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hansfriese
  - rbserver
---

## Vulnerability Title

[M-04] Total assets of yearn vault are not correct

### Overview


A bug has been identified in the YearnAdapter code, where the total assets of the current yVault are being extracted incorrectly. This results in incorrect calculations between the asset and the shares. The issue is caused by the use of `_yTotalAssets`, which extracts the total assets of the current yVault, instead of using `totalIdle` from the yearn vault implementation. This is because `totalIdle` is the tracked value of tokens, which is same as the vault's balance in most cases, but can be larger due to an attack or other's fault. As a result, the result of `_yTotalAssets` can be inflated than the correct total assets, leading to incorrect calculations.

To mitigate this bug, it is recommended to use `yVault.totalIdle` instead of balance. This has been confirmed by RedVeil (Popcorn).

### Original Finding Content


Total assets of yearn vault are not correct so the calculation between the asset and the shares will be wrong.

### Proof of Concept

In `YearnAdapter` the total assets of current `yValut` are extracted using `_yTotalAssets`.

        function _yTotalAssets() internal view returns (uint256) {
            return IERC20(asset()).balanceOf(address(yVault)) + yVault.totalDebt(); //@audit
        }

But in the yearn vault implementation, `self.totalIdle` is used instead of current balance.

    def _totalAssets() -> uint256:
        # See note on `totalAssets()`.
        return self.totalIdle + self.totalDebt

In yearn valut, `totalIdle` is the tracked value of tokens, so it is same as vault's balance in most cases, but the balance can be larger due to an attack or other's fault. Even `sweep` is implemented for the case in the vault implementation.

        if token == self.token.address:
            value = self.token.balanceOf(self) - self.totalIdle

        log Sweep(token, value)
        self.erc20_safe_transfer(token, self.governance, value)

So the result of `_yTotalAssets` can be inflated than the correct total assets and the calculation between the asset and the shares will be incorrect.

### Recommended Mitigation Steps

Use `yVault.totalIdle` instead of balance.

**[RedVeil (Popcorn) confirmed](https://github.com/code-423n4/2023-01-popcorn-findings/issues/728)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | hansfriese, rbserver |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/728
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`vulnerability`

