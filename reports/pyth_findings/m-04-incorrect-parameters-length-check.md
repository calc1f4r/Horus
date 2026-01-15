---
# Core Classification
protocol: ReyaNetwork-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41129
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
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

[M-04] Incorrect parameters length check

### Overview


The report is about a bug in the PythOffchainLookupNode. The impact of the bug is low, but the likelihood of it occurring is high. The bug is related to the `isValid` function, which checks the length of the parameters data. The current check is incorrect and can cause issues when registering a node. The bug can be fixed by changing the check to `32 * 2` instead of `32 * 4`. 

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

`PythOffchainLookupNode.isValid` check on the length of the parameters data is incorrect.

```solidity
    // Must have correct length of parameters data
    if (nodeDefinition.parameters.length != 32 * 4) {
        return false;
    }
```

The parameters data for Pyth nodes is composed of the oracle adapter address and the pair id (of type bytes32) ABI encoded, which is 64 bytes long, not 128 bytes long.

As a result, registering a node with the correct parameters will fail. On the other hand, padding the parameters data with 64 bytes after the correct parameters will enable users to register the same node data multiple times, by changing the padding data.

## Proof of concept

```solidity
function test_pythParams() public {
    IPythPriceInformationModule oracleAdaptersProxy = IPythPriceInformationModule(address(1));
    bytes32 pairId = bytes32(uint256(2));
    bytes memory parameters = abi.encode(oracleAdaptersProxy, pairId);
    assertEq(parameters.length, 32 * 2);
}
```

## Recommendations

```diff
        // Must have correct length of parameters data
-       if (nodeDefinition.parameters.length != 32 * 4) {
+       if (nodeDefinition.parameters.length != 32 * 2) {
            return false;
        }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | ReyaNetwork-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

