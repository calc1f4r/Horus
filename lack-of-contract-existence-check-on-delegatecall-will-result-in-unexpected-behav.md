---
# Core Classification
protocol: DeGate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17860
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/DeGate.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/DeGate.pdf
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
finders_count: 3
finders:
  - Shaun Mirani
  - Will Song
  - Devashish Tomar
---

## Vulnerability Title

Lack of contract existence check on delegatecall will result in unexpected behavior

### Overview


This bug report is about the Proxy contract using the delegatecall proxy pattern. If the implementation contract is incorrectly set or is self-destructed, the Proxy contract may not be able to detect failed executions. The Proxy contract includes a payable fallback function that does not have a contract existence check. This means that a delegatecall to a destructed contract will return success without changing the state or executing code, which can be exploited by malicious users.

In the short-term, the contract should implement a contract existence check before each delegatecall. It should also document the fact that using suicide and selfdestruct can lead to unexpected behavior, and prevent future upgrades from using these functions.

In the long-term, the Solidity documentation should be carefully reviewed, especially the "Warnings" section, and the pitfalls of using the delegatecall proxy pattern. References include the Contract Upgrade Anti-Patterns and Breaking Aave Upgradeability.

### Original Finding Content

## Security Assessment Report

## Difficulty: Undetermined

## Type: Data Validation

## Target: thirdparty/proxies/Proxy.sol

### Description
The Proxy contract uses the delegatecall proxy pattern. If the implementation contract is incorrectly set or is self-destructed, the Proxy contract may not be able to detect failed executions.

The Proxy contract includes a payable fallback function that is invoked when proxy calls are executed. This function lacks a contract existence check (figure 8.1).

```solidity
function _fallback() private {
    address _impl = implementation();
    require(_impl != address(0));
    assembly {
        let ptr := mload(0x40)
        calldatacopy(ptr, 0, calldatasize())
        let result := delegatecall(gas(), _impl, ptr, calldatasize(), 0, 0)
        let size := returndatasize()
        returndatacopy(ptr, 0, returndatasize())
        switch result
        case 0 { revert(ptr, size) }
        default { return (ptr, size) }
    }
}
```

**Figure 8.1:** The _fallback function in Proxy.sol

A delegatecall to a destructed contract will return success (figure 8.2). Due to the lack of contract existence checks, a series of batched transactions may appear to be successful even if one of the transactions fails.

The low-level functions call, delegatecall, and staticcall return true as their first return value if the account called is non-existent, as part of the design of the EVM. Account existence must be checked prior to calling if needed.

**Figure 8.2:** A snippet of the Solidity documentation detailing unexpected behavior related to delegatecall.

---

## Exploit Scenario
Eve upgrades the proxy to point to an incorrect new implementation. As a result, each delegatecall returns success without changing the state or executing code. Eve uses this defect to scam users.

## Recommendations
- **Short term:** Implement a contract existence check before each delegatecall. Document the fact that using suicide and selfdestruct can lead to unexpected behavior, and prevent future upgrades from using these functions.
- **Long term:** Carefully review the Solidity documentation, especially the "Warnings" section, and the pitfalls of using the delegatecall proxy pattern.

## References
- Contract Upgrade Anti-Patterns
- Breaking Aave Upgradeability

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | DeGate |
| Report Date | N/A |
| Finders | Shaun Mirani, Will Song, Devashish Tomar |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/DeGate.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/DeGate.pdf

### Keywords for Search

`vulnerability`

