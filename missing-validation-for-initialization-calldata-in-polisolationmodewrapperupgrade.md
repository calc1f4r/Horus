---
# Core Classification
protocol: Dolomite Polvaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55626
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
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
  - 0kage
  - Farouk
---

## Vulnerability Title

Missing validation for initialization calldata in `POLIsolationModeWrapperUpgradeableProxy` constructor

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `POLIsolationModeWrapperUpgradeableProxy` constructor accepts initialization calldata without performing any validation on its content before executing it via `delegatecall` to the implementation contract. Specifically:

- The constructor does not verify that the `calldata` targets the expected initialize(address) function
- The constructor does not verify that the provided vaultFactory address parameter is non-zero

```solidity
// POLIsolationModeWrapperUpgradeableProxy.sol
constructor(
    address _berachainRewardsRegistry,
    bytes memory _initializationCalldata
) {
    BERACHAIN_REWARDS_REGISTRY = IBerachainRewardsRegistry(_berachainRewardsRegistry);
    Address.functionDelegateCall(
        implementation(),
        _initializationCalldata,
        "POLIsolationModeWrapperProxy: Initialization failed"
    );
}
```
This lack of validation means the constructor will blindly execute any calldata, potentially setting critical contract parameters incorrectly during deployment.

Note that a similar issue exists in `POLIsolationModeUnwrapperUpgradeableProxy`


**Impact:** The proxy could be initialized with a zero or invalid vaultFactory address, rendering it non-functional or insecure.  Additionally, if the implementation contract is upgraded and introduces new functions with weaker access controls, this pattern would allow those functions to be called during initialization of new proxies.

**Recommended Mitigation:** Consider adding explicit validation for both the function selector and parameters in the constructor:

```solidity
constructor(
    address _berachainRewardsRegistry,
    bytes memory _initializationCalldata
) {
    BERACHAIN_REWARDS_REGISTRY = IBerachainRewardsRegistry(_berachainRewardsRegistry);

    // Validate function selector is initialize(address)
    require(
        _initializationCalldata.length == 36 &&
        bytes4(_initializationCalldata[0:4]) == bytes4(keccak256("initialize(address)")),
        "Invalid initialization function"
    );

     // Decode and validate the vaultFactory address is non-zero
    address vaultFactory = abi.decode(_initializationCalldata[4:], (address));
    require(vaultFactory != address(0), "Zero vault factory address");

    Address.functionDelegateCall(
        implementation(),
        _initializationCalldata,
        "POLIsolationModeWrapperProxy: Initialization failed"
    );
}
```

**Dolomite:**
Acknowledged.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Dolomite Polvaults |
| Report Date | N/A |
| Finders | 0kage, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

