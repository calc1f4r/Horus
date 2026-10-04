---
# Core Classification
protocol: Hyperstable_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57818
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-18] Vault is susceptible to inflation attack by first depositor

### Overview

See description below for full details.

### Original Finding Content

The `Vault` contract is vulnerable to an inflation attack where the first user to deposit can manipulate the share valuation, allowing him to redeem a disproportionate amount of assets.

Consider minting an initial share amount (minting dead shares) to a dead address (`address(0)`):

```diff
    constructor(address _asset, address _priceFeed, uint256 _mcr) ERC4626(IERC20(_asset)) ERC20("", "") {
        _initializeOwner(msg.sender);
        priceFeed = IPriceFeed(_priceFeed);
        MCR = _mcr;
+      _mint(address(0),1e3);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

