---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53478
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-16] Adding a node operator does not increase the nonce

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** NodeOperatorRegistry.sol:addNodeOperator#L302-L322

**Description:**

The function to add a new node operator to the node operator registry does not increase the staking module nonce, even though this nonce should increase upon the activation of a node operator according to the spec.
```
function addNodeOperator(string _name, address _rewardAddress) external returns (uint256 id) {
    _onlyValidNodeOperatorName(_name);
    _onlyNonZeroAddress(_rewardAddress);
    _auth(MANAGE_NODE_OPERATOR_ROLE);

    id = getNodeOperatorsCount();
    require(id < MAX_NODE_OPERATORS_COUNT, "MAX_OPERATORS_COUNT_EXCEEDED");

    TOTAL_OPERATORS_COUNT_POSITION.setStorageUint256(id + 1);

    NodeOperator storage operator = _nodeOperators[id];

    uint256 activeOperatorsCount = getActiveNodeOperatorsCount();
    ACTIVE_OPERATORS_COUNT_POSITION.setStorageUint256(activeOperatorsCount + 1);

    operator.active = true;
    operator.name = _name;
    operator.rewardAddress = _rewardAddress;

    emit NodeOperatorAdded(id, _name, _rewardAddress, 0);
}
```

**Remediation:**  Add a call to `_increaseValidatorsKeysNonce()` at the end of `addNodeOperator`.

**Status:**  Acknowledged

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

