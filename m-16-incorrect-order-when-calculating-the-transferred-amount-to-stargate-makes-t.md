---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31454
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
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

[M-16] Incorrect order when calculating the transferred amount to Stargate makes the `participate()` function unusable

### Overview


There is a bug in the Stargate helper contract that causes the participate() function to not work properly. This only happens when calling the participate function and it always reverts back to the original functionality. The cause of this bug is the way Tapioca calculates the amount transferred to Stargate for refunding dust amounts. This calculation always reverts due to a mistake in the code. To fix this bug, a simple change in the code is recommended. The code should be changed from "uint256 transferred = balanceAfter - balanceBefore;" to "uint256 transferred = balanceBefore - balanceAfter;". This will help prevent the bug from occurring.

### Original Finding Content

**Severity**

Impact: Medium, as the functionality will always revert

Likelihood: Medium, as it only occurs when calling `participate`

**Description**

The participate() function in Stargate helper contract will not work.

The cause of this, is the way on how you Tapioca is calculating the amount transferred to Stargate to refund the dust amounts that Stargate returns:

```
uint256 transferred = balanceAfter - balanceBefore;
```

Let's put an example without decimals for simplicity.

- I, as the msg.sender, transfer 50 tokens: `balanceBefore = 50`

- Those 50 tokens are then sent to the pool. Let's say Stargate returns 1 token as dust.

- Then it will be: `uint256 transferred = 1 - 50;`

therefore the calculation will always revert.

**Recommendations**

```diff
uint256 balanceAfter = IERC20(stargateData.srcToken).balanceOf(
            address(this)
        );
+        uint256 transferred = balanceBefore  - balanceAfter;
-        uint256 transferred = balanceAfter - balanceBefore;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

