---
# Core Classification
protocol: Ecosystem - DualCORE vault b14g
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50809
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/coredao/ecosystem-DualCORE-vault-b14g
source_link: https://www.halborn.com/audits/coredao/ecosystem-DualCORE-vault-b14g
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

Incorrect bounds checking in getReceivers() reverts with empty receivers

### Overview

See description below for full details.

### Original Finding Content

##### Description

In `MergeMarketplaceStrategy.sol`, the `getReceivers()` function has a logical error in its bounds checking:

```
function getReceivers(uint256 start, uint256 end) public view returns (address[] memory) {
    require(start < end && end <= receivers.length(), "Invalid range");
    address[] memory result = new address[](end - start);
    for (uint256 i = start; i < end; i++) {
        result[i - start] = receivers.at(i);
    }
    return result;
}
```

  

* When `receivers.length() == 0`, the function will always revert because:

  + If `end > 0`: reverts because `end <= receivers.length()` is false
  + If `end == 0`: reverts because `start < end` is `false`
  + Therefore, no valid inputs exist when the list is empty

##### BVSS

[AO:A/AC:M/AX:M/R:N/S:U/C:N/A:L/I:N/D:N/Y:N (1.1)](/bvss?q=AO:A/AC:M/AX:M/R:N/S:U/C:N/A:L/I:N/D:N/Y:N)

##### Recommendation

Modify the bounds checking to handle empty lists correctly.

##### Remediation

**PENDING:** The **B14G team** indicated that they will be addressing this finding in the future.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ecosystem - DualCORE vault b14g |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/coredao/ecosystem-DualCORE-vault-b14g
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/coredao/ecosystem-DualCORE-vault-b14g

### Keywords for Search

`vulnerability`

