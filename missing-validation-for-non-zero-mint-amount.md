---
# Core Classification
protocol: Mintify $MINT Token
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52184
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/mintify/mintify-mint-token
source_link: https://www.halborn.com/audits/mintify/mintify-mint-token
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
  - Halborn
---

## Vulnerability Title

Missing Validation for Non-Zero Mint Amount

### Overview

See description below for full details.

### Original Finding Content

##### Description

The contract fails to verify that the amount to be minted is strictly greater than zero.

  

Even though `_mint` ensures a non-zero recipient address, zero-token minting remains possible, creating unnecessary transactions with no meaningful effect.

  

Code Location
-------------

Code of `mint` function:

```
function mint(address account, uint256 amount) external onlyMinter {
    _mint(account, amount);
}
```

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:N/Y:N (0.0)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:N/Y:N)

##### Recommendation

It is recommended to include a check within the `mint` function:

```
require(amount > 0, "Mint zero tokens");
```

This ensures all mint operations involve a positive token amount, improving clarity and saving gas.

##### Remediation

**ACKNOWLEDGED**: The **Mintify team** has acknowledged this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Mintify $MINT Token |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/mintify/mintify-mint-token
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/mintify/mintify-mint-token

### Keywords for Search

`vulnerability`

