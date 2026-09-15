---
# Core Classification
protocol: Hypercerts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20448
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-Hypercerts.md
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
  - Pashov
---

## Vulnerability Title

[C-01] Users can split a token to more fractions than the `units` held at `tokenID`

### Overview


This bug report is about a problem with the `_splitValue` method in `SemiFungible1155`, a protocol that is part of the ERC1155 implementation of OpenZeppelin. This method does not follow the Checks-Effects-Interactions pattern, which is a common pattern used to make sure that code is executed in a secure and safe manner. Because of this, the method calls `_mintBatch` from the ERC1155 implementation, which can cause the code to reenter itself and mint a large amount of tokens. 

The impact of this bug is high, as it breaks an important protocol invariant, and the likelihood of it happening is also high, as those types of issues are common and easily exploitable. 

The recommendation to fix the bug is to follow the Checks-Effects-Interactions pattern, which is done by changing the order of the `_mintBatch` and `tokenValues[_tokenID]` calls. 

In conclusion, this bug report is about a problem with the `_splitValue` method in `SemiFungible1155`. It has a high impact and likelihood, and the recommendation to fix it is to follow the Checks-Effects-Interactions pattern.

### Original Finding Content

**Impact**
High, as it breaks an important protocol invariant

**Likelihood**
High, as those types of issues are common and are easily exploitable

**Description**

The `_splitValue` method in `SemiFungible1155` does not follow the Checks-Effects-Interactions pattern and it calls `_mintBatch` from the ERC1155 implementation of OpenZeppelin which will actually do a hook call to the recipient account as a safety check. This call is unsafe as it can reenter the `_splitValue` method and since `tokenValues[_tokenID]` hasn't been updated yet, it can once again split the tokens into more fractions and then repeat until a huge amount of tokens get minted.

**Recommendation**

Follow the Checks-Effects-Interactions pattern

```diff
-_mintBatch(_account, toIDs, amounts, "");
-
-tokenValues[_tokenID] = valueLeft;
+tokenValues[_tokenID] = valueLeft;
+
+_mintBatch(_account, toIDs, amounts, "");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hypercerts |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-Hypercerts.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

