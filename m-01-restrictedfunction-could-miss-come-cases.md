---
# Core Classification
protocol: Hytopiawallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31468
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-23-HYTOPIAWallet.md
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

[M-01] `RestrictedFunction` could miss come cases

### Overview


This bug report discusses a potential issue with a contract that could result in funds being stolen. The severity of this bug is considered high because it could lead to a large amount of funds being stolen beyond the allowed limit. However, the likelihood of this happening is considered low as it only applies to certain tokens that use a specific function. 

The issue lies in the fact that only two functions, `approve` and `setApprovalForAll`, are considered restricted, but there are other functions that could also change the token allowance. An example of this is the `increaseApproval` and `decreaseApproval` functions in the RNDR token contract. 

The report recommends either removing the `MAGIC_CONTRACT_ALL_FUNCTION_SELECTORS` option or restricting it to privileged roles to prevent this bug from being exploited. 

### Original Finding Content

**Severity**

**Impact:** High, because the fund in the contract could all be stolen, much beyond allowed amount.

**Likelihood:** Low, because it only applies to cases when MAGIC_CONTRACT_ALL_FUNCTION_SELECTORS being used, and not all tokens have this problem.

**Description**

Only `approve` and `setApprovalForAll` are considered restricted function, however it is possible that the token allowance could be chaged by other functions:
Such as [RNDR](https://etherscan.io/address/0x1a1fdf27c5e6784d1cebf256a8a5cc0877e73af0#code), has `increaseApproval()/decreaseApproval()` function, which is not standard ERC20 functions.

```solidity
File: contracts\modules\SessionCalls\SessionCalls.sol
448:     function _isRestrictedFunction(bytes4 _functionSelector) private pure returns (bool isRestricted_) {
449:         if (
450:             _functionSelector == IERC20.approve.selector || _functionSelector == IERC721.approve.selector
451:                 || _functionSelector == IERC721.setApprovalForAll.selector
452:                 || _functionSelector == IERC1155.setApprovalForAll.selector
453:         ) {
454:             isRestricted_ = true;
455:         }
456:     }

// https://etherscan.io/address/0x1a1fdf27c5e6784d1cebf256a8a5cc0877e73af0#code
  function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }

  function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
    uint oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue > oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }
```

**Recommendations**

- just remove `MAGIC_CONTRACT_ALL_FUNCTION_SELECTORS` option, or restrict it to privileged roles

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hytopiawallet |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-23-HYTOPIAWallet.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

