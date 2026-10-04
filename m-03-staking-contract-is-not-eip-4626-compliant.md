---
# Core Classification
protocol: Lucidly June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36391
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Lucidly-security-review-June.md
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

[M-03] Staking contract is not EIP-4626 compliant

### Overview


The current staking implementation charges fees on assets deposited into the vault, but it does not account for these fees when converting from assets to shares. This can cause unexpected behavior and integration issues in the future. To fix this, the `previewDeposit()` and `previewMint()` functions should be overridden to include fees.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

The current staking implementation charges fees on assets deposited into the vault, as shown below:

```solidity
    function _deposit(address by_, address to_, uint256 tokens_, uint256 shares_) internal virtual override {
        SafeTransferLib.safeTransferFrom(asset(), by_, address(this), tokens_);
        uint256 _fee = (shares_ * depositFeeBps) / 1e4;
        _mint(to_, shares_ - _fee);
        _mint(protocolFeeAddress, _fee);

        emit Deposit(by_, to_, tokens_, shares_);

        _afterDeposit(tokens_, shares_);
    }
```

According to [EIP4626](https://eips.ethereum.org/EIPS/eip-4626), `previewDeposit()` and `previewMint()` must be inclusive of deposit fees:

> MUST be inclusive of deposit fees. Integrators should be aware of the existence of deposit fees.

However, the current staking implementation (i.e. OpenZeppelin impl) does not account for these fees when converting from assets to shares. This omission can lead to unexpected behavior and integration issues in the future.

**Recommendations**

Consider overriding the `previewDeposit()` and `previewMint()` functions to include fees.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Lucidly June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Lucidly-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

