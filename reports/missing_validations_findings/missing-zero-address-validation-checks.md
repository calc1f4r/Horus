---
# Core Classification
protocol: Common Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52015
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/rfx-exchange/common-pool
source_link: https://www.halborn.com/audits/rfx-exchange/common-pool
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

Missing zero address validation checks

### Overview

See description below for full details.

### Original Finding Content

##### Description

It was found that addresses parameter were not totally validated not to be equal to zero, that could lead to failure of business logic if that happen:

* CommonPool.sol→updateApprovedExternalAddr
* CommonPool.sol→updateOracleId
* swaps/SwapModule.sol→setModuleAddr

  

For example, in `updateOracleId`:

```
function updateOracleId(address[] calldata _token, bytes32[] calldata _oracleId) external onlyOwner {
    if (_token.length != _oracleId.length) revert IErrors.InvalidLength();
    for (uint256 i; i < _token.length;) {
        oracleId[_token[i]] = _oracleId[i];
        unchecked {
            i++;
        }
    }

    emit OracleIdUpdated(_token, _oracleId);
}
```

##### Score

Impact:   
Likelihood:

##### Recommendation

It is recommended to validate that addresses cannot be the zero address before updating variables.

##### Remediation

**SOLVED**: the **RFX Exchange team** solved this issue by adding the missing zero checks.

##### Remediation Hash

<https://github.com/relative-finance/common-pool/pull/11/commits/5ba7a297725acfddfb72c2f49f24a083232df637#r1759606457>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Common Pool |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/rfx-exchange/common-pool
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/rfx-exchange/common-pool

### Keywords for Search

`vulnerability`

