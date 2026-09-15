---
# Core Classification
protocol: Stakepet
chain: everychain
category: logic
vulnerability_type: documentation

# Attack Vector Details
attack_type: documentation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26164
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
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
  - documentation
  - business_logic

protocol_categories:
  - yield
  - farm
  - gaming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Hans
  - 0kage
---

## Vulnerability Title

Closedown condition is inconsistent with the stated documentation of majority agreement

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Description:** [Documentation](https://hackmd.io/CPINxScvSE2vo-t8mwY_Og#Risks) states the following:

_"Closing the Contract: If the majority of the pets agree, they can vote to close the contract. Once closed, the remaining funds will be divided among the surviving pets. This is the most beneficial scenario for you, as you’ll earn the base rewards, early withdrawal rewards, and rewards from dead pets."_

Inline comments for the [`StakePet::closedown`](https://github.com/Ranama/StakePet/blob/9ba301823b5062d657baa3462224da498dc4bb46/src/StakePet.sol#L398C2-L398C2) function state the following"

```
    /// @notice Close down the contract if majority wants it, after closedown everyone can withdraw without getting a yield cut and no pet can die.
    function closedown(uint256[] memory _idsOfMajorityThatWantsClosedown) external {
...
}
```

In both cases, condition for closedown is for `majority of pets` to agree for a closedown. However, the check used for `closedown` is that the total collateral of pets wanting a closedown should be atleast 50% of the total collateral. This would mean that a single or few pet owners with large collateral deposits can trigger a closedown even if its not something that a majority of pet owners agree to.

Having 50% of value agreement and having majority agreement could be 2 different things.

**Impact:** The current model can be hijacked by whales who can trigger closedown of contract whenever they wish to. This could create a bad user experience for majority of pet owners who want to stay in the contract

**Recommended Mitigation:** Please make documentation consistent with the vision for stake pets.

**Client:** Fixed in [54a4dcb](https://github.com/Ranama/StakePet/commit/54a4dcbb696da3138dc0fdd8e7032d664d32b7da)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Stakepet |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Documentation, Business Logic`

