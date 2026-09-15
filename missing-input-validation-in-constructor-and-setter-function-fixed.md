---
# Core Classification
protocol: Metamask Delegation Framework April 2025
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56805
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/04/metamask-delegation-framework-april-2025/
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
finders_count: 2
finders:
  -  George Kobakhidze
                        
  - Vladislav Yaroshuk
---

## Vulnerability Title

Missing Input Validation in constructor and Setter Function ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

...

Export to GitHub ...

Set external GitHub Repo ...

Export to Clipboard (json)

Export to Clipboard (text)

#### Resolution

Fixed in commit [6912e732e2ed65699152c6bfdb46a0ed433f1263](https://github.com/MetaMask/delegation-framework/commit/6912e732e2ed65699152c6bfdb46a0ed433f1263) by adding 0-address checks.

#### Description

The `constructor` sets critical contract dependencies such as `swapApiSigner`, `delegationManager`, `metaSwap`, and `argsEqualityCheckEnforcer` without validating the provided addresses. This could result in the contract being initialized with zero addresses or incorrect contracts, leading to broken functionality or security vulnerabilities. Similarly, the `setSwapApiSigner` function allows setting a new signer address without validating that it is non-zero.

#### Examples

**src/helpers/DelegationMetaSwapAdapter.sol:L178-L190**

```
constructor(
    address _owner,
    address _swapApiSigner,
    IDelegationManager _delegationManager,
    IMetaSwap _metaSwap,
    address _argsEqualityCheckEnforcer
)
    Ownable(_owner)
{
    swapApiSigner = _swapApiSigner;
    delegationManager = _delegationManager;
    metaSwap = _metaSwap;
    argsEqualityCheckEnforcer = _argsEqualityCheckEnforcer;

```

**src/helpers/DelegationMetaSwapAdapter.sol:L323-L326**

```
function setSwapApiSigner(address _newSigner) external onlyOwner {
    swapApiSigner = _newSigner;
    emit SwapApiSignerUpdated(_newSigner);
}

```

#### Recommendation

We recommend adding input validation checks to ensure none of the critical addresses passed to the constructor or `setSwapApiSigner` are the zero address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Metamask Delegation Framework April 2025 |
| Report Date | N/A |
| Finders |  George Kobakhidze
                        , Vladislav Yaroshuk |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/04/metamask-delegation-framework-april-2025/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

