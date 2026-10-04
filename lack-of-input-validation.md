---
# Core Classification
protocol: Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51607
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/anzen-finance/anzen-v2
source_link: https://www.halborn.com/audits/anzen-finance/anzen-v2
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

Lack of Input Validation

### Overview

See description below for full details.

### Original Finding Content

##### Description

During the security assessment, it was found that critical parameters could be set to undesired values such as `address(0)` or unrealistic numbers. For instance:

1. **Constructor Zero Address Checks**: Some constructors of the project lack validation to ensure that zero addresses are not accepted for essential parameters. This omission could lead to unexpected behavior due to non-initialized values.

2. **Constructor Unbounded Values**: Apart from addresses, some of the constructors contained integer values that were not checked against valid ranges. For example, on `sUSDz`, any cooldown period (`_CDPeriod`) would be accepted even though not any value may be desirable.

3. **Setter Functions Validation**: Furthermore, even some setters did not have address 0 or boundary checks either. Notice a `newPeriod` or `0` or `type(uint256).max` could be set using the `setNewVestingPeriod()` function of `sUSDz`:

```
function setNewVestingPeriod(uint256 newPeriod) external onlyRole(POOL_MANAGER_ROLE) {
  vestingPeriod = newPeriod;
  emit VestingPeriodChanged(newPeriod, block.timestamp);
}
```

##### BVSS

[AO:S/AC:M/AX:M/C:N/I:H/A:N/D:N/Y:N/R:N/S:U (0.7)](/bvss?q=AO:S/AC:M/AX:M/C:N/I:H/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

To address these issues, consider implementing input validation checks to ensure that zero addresses or unwanted values are not accepted for essential parameters.

  

### Remediation Plan

**PARTIALLY SOLVED:** The **Anzen team** partially solved the issue by implemented a valid check in the `SUSDz` constructor. However, there are still other functions missing range or address validations.

Finally, it was noted that one of the added fixes is not provideiding a useful check. This is because it is not properly checking any range value. See the new require statement in the `setNewVestingPeriod(uint256 newPeriod)` function:

```
require(newPeriod > 0 && newPeriod < type(uint256).max, "SHOULD_BE_LESS_THAN_UINT256_MAX_AND_GREATER_THAN_ZERO");
```

Notice that verifying if the `newPeriod` value is between the values 0 and `type(uint256).max` is like not doing any verification at all, as all `uint256` fall into that range.

##### Remediation Hash

<https://github.com/Anzen-Finance/protocol-v2/commit/783f6403428ae6f2336aede93bb71d63fceb4380>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol V2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/anzen-finance/anzen-v2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/anzen-finance/anzen-v2

### Keywords for Search

`vulnerability`

