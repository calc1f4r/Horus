---
# Core Classification
protocol: Metamask Delegationframework Part
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58674
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-01-cyfrin-metamask-delegationFramework-part3-v2.0.md
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
  - 0kage
---

## Vulnerability Title

Missing zero address checks in DelegationMetaSwapAdapter

### Overview

See description below for full details.

### Original Finding Content

**Description:** Missing zero address checks in the `constructor` and `setSwapApiSigner` functions of `DelegationMetaSwapAdapter`.

```solidity

  constructor(
        address _owner,
        address _swapApiSigner,
        IDelegationManager _delegationManager,
        IMetaSwap _metaSwap,
        address _argsEqualityCheckEnforcer
    )
        Ownable(_owner)
    {
        swapApiSigner = _swapApiSigner; //@audit missing address(0) check
        delegationManager = _delegationManager; //@audit missing address(0) check
        metaSwap = _metaSwap; //@audit missing address(0) check
        argsEqualityCheckEnforcer = _argsEqualityCheckEnforcer; //@audit missing address(0) check
        emit SwapApiSignerUpdated(_swapApiSigner);
        emit SetDelegationManager(_delegationManager);
        emit SetMetaSwap(_metaSwap);
        emit SetArgsEqualityCheckEnforcer(_argsEqualityCheckEnforcer);
    }
  function setSwapApiSigner(address _newSigner) external onlyOwner {
        swapApiSigner = _newSigner; //@audit missing address(0) check
        emit SwapApiSignerUpdated(_newSigner);
    }
```



**Recommended Mitigation:** Consider adding zero address checks.

**Metamask:** Resolved in commit [6912e73](https://github.com/MetaMask/delegation-framework/commit/6912e732e2ed65699152c6bfdb46a0ed433f1263).

**Cyfrin:** Resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Metamask Delegationframework Part |
| Report Date | N/A |
| Finders | 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-01-cyfrin-metamask-delegationFramework-part3-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

