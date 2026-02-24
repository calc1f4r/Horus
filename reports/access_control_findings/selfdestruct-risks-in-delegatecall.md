---
# Core Classification
protocol: Brink
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7276
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Brink-Spearbit-Security-Review-Engagement-1.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Brink-Spearbit-Security-Review-Engagement-1.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Selfdestruct risks in delegateCall()

### Overview


This bug report is about the risk of a potential self-destruct of an address where Account.sol gets deployed, which could result in user wallets getting bricked. After an investigation, it was found that there is no hole in the access control. To minimize the risk, three changes have been recommended: (1) explicitly enforce that the functions delegateCall, metaDelegateCall, and metaDelegateCall_EIP1271 are only delegatecalled; (2) change the contract to a library; and (3) deploy Account.sol via CREATE2 so it can be redeployed if necessary. The bug report has been resolved and fixed in commit 3afeaf1.

### Original Finding Content

## Security Analysis Report

## Severity
**Medium Risk**

## Context
**File:** Account.sol  
**Line Range:** L48-L57  

```solidity
function delegateCall(address to, bytes memory data) external {
    require(proxyOwner() == msg.sender, "NOT_OWNER");
    assembly {
        let result := delegatecall(gas(), to, add(data, 0x20), mload(data), 0, 0)
        if eq(result, 0) {
            returndatacopy(0, 0, returndatasize())
            revert(0, returndatasize())
        }
    }
}
```

The address where `Account.sol` gets deployed can be directly called. There is a risk of a potential `selfdestruct`, which would result in user wallets getting bricked. This risk depends on the access control of the functions `delegateCall`, `metaDelegateCall`, and `metaDelegateCall_EIP1271`. However, we couldn’t find a hole in the access control. 

We would still recommend the following changes:

1. **Explicitly enforce that these functions are only delegatecalled.** The following contract demonstrates how this can be achieved.

   ```solidity
   abstract contract OnlyDelegateCallable {
       address immutable deploymentAddress = address(this);
       modifier onlyDelegateCallable() {
           require(address(this) != deploymentAddress);
           _;
       }
   }
   ```

2. **Note:** The Solidity compiler enforces call protection for libraries. The compiler automatically adds an equivalent of the above `onlyDelegateCallable` modifier to state modifying functions. Changing the contract to a library would require additional changes in the codebase.

3. **Deploy `Account.sol` via `CREATE2`** so it can be redeployed if necessary.

**Note:** Assuming that the current access control can be broken, and that the address corresponding to the `Account.sol` contract holds funds, then an attacker can steal these funds from this address. However, this is not the most significant risk.

## Brink
**Fixed in commit:** 3afeaf1.

## Spearbit
**Resolved.**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Brink |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Brink-Spearbit-Security-Review-Engagement-1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Brink-Spearbit-Security-Review-Engagement-1.pdf

### Keywords for Search

`vulnerability`

