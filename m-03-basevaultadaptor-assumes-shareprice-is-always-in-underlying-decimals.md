---
# Core Classification
protocol: Gro Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42240
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-gro
source_link: https://code4rena.com/reports/2021-06-gro
github_link: https://github.com/code-423n4/2021-06-gro-findings/issues/114

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] `BaseVaultAdaptor` assumes `sharePrice` is always in underlying decimals

### Overview


The bug report submitted by cmichel highlights an issue with the `BaseVaultAdaptor.calculateShare` function. This function calculates the number of shares based on the amount and share price of a vault. However, it assumes that the share price is always in the same decimals as the token, which may not be the case for all protocols. This could lead to potential losses when integrating a token with different precision. The report suggests that this function should be made abstract and implemented in specific adaptors to avoid protocol-specific conversions. The issue has been confirmed and shares have been removed from the release version.

### Original Finding Content

_Submitted by cmichel_

The two `BaseVaultAdaptor.calculateShare` functions compute `share = amount.mul(uint256(10)**decimals).div(sharePrice)`

```solidity
uint256 sharePrice = _getVaultSharePrice();
// amount is in "token" decimals, share should be in "vault" decimals
share = amount.mul(uint256(10)**decimals).div(sharePrice);
```

This assumes that the `sharePrice` is always in _token_ decimals and that _token_ decimals is the same as _vault_ decimals.

Both these assumptions happen to be correct for Yearn vaults, but that will not necessarily be the case for other protocols.
As this functionality is in the `BaseVaultAdaptor`, and not in the specific `VaultAdaptorYearnV2_032`, consider generalizing the conversion.

Integrating a token where the token or price is reported in a different precision will lead to potential losses as more shares are computed.

Because the conversion seems highly protocol-specific, it is recommended that `calculateShare` should be an abstract function (like `_getVaultSharePrice`) that is implemented in the specific adaptors.

**- [kristian-gro (Gro) confirmed](https://github.com/code-423n4/2021-06-gro-findings/issues/114)**
> Confirmed and shares have been removed from release version.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gro Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-gro
- **GitHub**: https://github.com/code-423n4/2021-06-gro-findings/issues/114
- **Contest**: https://code4rena.com/reports/2021-06-gro

### Keywords for Search

`vulnerability`

