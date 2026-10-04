---
# Core Classification
protocol: Dpnmdefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44541
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-DPNMDEFI.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Underflow/overflow cases are not avoided

### Overview


This bug report describes an issue with the phenomanelTree.sol code, where unexpected revert messages are received when filling trees for different users. The cause of this issue is an underflow case that is not being avoided, resulting in an out of bounds array index and potential underflow/overflow errors. To fix this issue, the code needs to be refactored and require statements need to be added to validate input in the correct places. This has been addressed in the code fix presented in 60761c1.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

phenomanelTree.sol - Testing has shown that in cases where we are filling trees for different users, sometimes unexpected revert messages are received (i.e. related to underflow/overflow) while the expected message according to the use case is Tree is filled. By investigating this we see that underflow cases are not avoided, for instance we have the following (i.e. on calling positionUser):
lvlsDeep -> take any value 0-255.
Triggers findPositionSpot, we find that lvlsDeep should have been validated to be non-zero because of lvlsDeep-lvl and lvl starts by 1.
Triggers calcTreeNetwork, we find _depth which should be at least 1 to have a proper for loop. Since we have lvlsDeep-lvl=_depth while maximum value of lvl can be lvl+1 we see it ends up having _depth = -1 which is not possible as it reverts.
Also, based on previous point, lvlsDeep-lvl should be less than 15. Otherwise, it goes out of bounds of array index. Therefore, lvlsDeep < 16 because lvl >= 1.
Underflow/Overflow might be more severe if we face those errors in valid states; we need to be careful to avoid them.

**Recommendation** 

After Refactoring the data representation of phenomanelTree as recommended in other issues. This part needs to require statements that validate input to be added in the right places in order to avoid unintended revert messages. Reimplementing this method in order to avoid that is also needed.

**Fix** - Require statement has been added in order to validate that input is within an acceptable bound. Code fix is presented in 60761c1.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Dpnmdefi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-DPNMDEFI.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

