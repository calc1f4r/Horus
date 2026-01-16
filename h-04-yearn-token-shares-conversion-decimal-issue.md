---
# Core Classification
protocol: Sublime
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1187
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-sublime-contest
source_link: https://code4rena.com/reports/2021-12-sublime
github_link: https://github.com/code-423n4/2021-12-sublime-findings/issues/134

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - wrong_math
  - decimals

protocol_categories:
  - dexes
  - cdp
  - services
  - leveraged_farming
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-04] Yearn token <> shares conversion decimal issue

### Overview


A bug has been reported in the Yearn strategy "YearnYield". This bug affects the token and shares conversion, resulting in the incorrect amount of tokens or shares being paid out. This could lead to a loss for either the protocol or user. The bug is caused by the use of `1e18` in the `getTokensForShares` function, when it should be divided by `10**vault.decimals()` instead. The same fix should also be applied to the `getSharesForTokens` function. The recommended mitigation steps are to divide by `10**vault.decimals()` instead of `1e18` in `getTokensForShares` and to apply the same fix in `getSharesForTokens`.

### Original Finding Content

_Submitted by cmichel_

The yearn strategy `YearnYield` converts shares to tokens by doing `pricePerFullShare * shares / 1e18`:

    function getTokensForShares(uint256 shares, address asset) public view override returns (uint256 amount) {
        if (shares == 0) return 0;
        // @audit should divided by vaultDecimals 
        amount = IyVault(liquidityToken[asset]).getPricePerFullShare().mul(shares).div(1e18);
    }

But Yearn's `getPricePerFullShare` seems to be [in `vault.decimals()` precision](https://github.com/yearn/yearn-vaults/blob/03b42dacacec2c5e93af9bf3151da364d333c222/contracts/Vault.vy#L1147), i.e., it should convert it as `pricePerFullShare * shares / (10 ** vault.decimals())`.
The vault decimals are the same [as the underlying token decimals](https://github.com/yearn/yearn-vaults/blob/03b42dacacec2c5e93af9bf3151da364d333c222/contracts/Vault.vy#L295-L296)

#### Impact

The token and shares conversions do not work correctly for underlying tokens that do not have 18 decimals.
Too much or too little might be paid out leading to a loss for either the protocol or user.

#### Recommended Mitigation Steps

Divide by `10**vault.decimals()` instead of `1e18` in `getTokensForShares`.
Apply a similar fix in `getSharesForTokens`.

**[ritik99 (Sublime) confirmed](https://github.com/code-423n4/2021-12-sublime-findings/issues/134)** 



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Sublime |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-sublime
- **GitHub**: https://github.com/code-423n4/2021-12-sublime-findings/issues/134
- **Contest**: https://code4rena.com/contests/2021-12-sublime-contest

### Keywords for Search

`Wrong Math, Decimals`

