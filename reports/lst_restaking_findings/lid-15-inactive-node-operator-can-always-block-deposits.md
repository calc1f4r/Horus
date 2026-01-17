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
solodit_id: 53472
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-15] Inactive node operator can always block deposits

### Overview


This bug report discusses a medium severity issue found in the NodeOperatorRegistry contract. The function responsible for depositing ETH to the DepositContract requires a set of signatures, one of which is the staking module nonce. This nonce increases whenever there is a change in the staking module, such as a node operator adding or removing their deposit keys. However, if a node operator were to spam these changes, the nonce would increase and the signatures would no longer be valid, blocking deposits. Additionally, even inactive node operators can still invoke these functions, causing further issues. The recommended solution is to modify the `_onlyNodeOperatorManager` function to only allow active node operators to call these functions. The bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** NodeOperatorRegistry.sol:_increaseValidatorsKeysNonce#L1315-L1321

**Description:**

The function to deposit ETH to the DepositContract requires a set of signatures of the deposit data. One element is the staking module nonce, which has to be equal to the current on-chain nonce of the staking module.

This staking module nonce increases upon any deposit data change in the staking module. For example, in the NodeOperatorRegistry this happens whenever there is a data change for a node operator. Node operators can invoke these changes themselves by adding or removing their deposit keys, which then increases the nonce.

If a node operator would front-run or spam adding and removing keys, then the nonce would increase and the signatures of the deposit data would no longer be valid, causing a block of deposits.

Furthermore, a node operator that has been set inactive due to leaving or becoming malicious can still invoke these functions to add or remove keys, because it only checks whether the node operator ID exists, not whether it is still active.

As a result, any node operator that ever existed, including kicked ones, can still always block deposits of ETH to the deposit contract.

```function _increaseValidatorsKeysNonce() internal {
    uint256 keysOpIndex = KEYS_OP_INDEX_POSITION.getStorageUint256() + 1;
    KEYS_OP_INDEX_POSITION.setStorageUint256(keysOpIndex);
    /// @dev [DEPRECATED] event preserved for tooling compatibility
    emit KeysOpIndexSet(keysOpIndex);
    emit NonceChanged(keysOpIndex);
}
```

**Remediation:**  We would recommend to modify `_onlyNodeOperatorManager` such that the node operator manager can only call these kind of functions if the node operator is also active.

For example:
```
function _onlyNodeOperatorManager(address _sender, uint256 _nodeOperatorId) internal view {
    bool isRewardAddress = _sender == _nodeOperators[_nodeOperatorId].rewardAddress;
    bool isActive = _nodeOperators[_nodeOperatorId].active;
    _requireAuth((isRewardAddress && isActive) || canPerform(_sender, MANAGE_SIGNING_KEYS, arr(_nodeOperatorId)));
}
```

**Status:**  Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

