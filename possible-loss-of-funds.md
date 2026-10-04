---
# Core Classification
protocol: Multiplyr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50946
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/affine-defi/multiplyr-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/affine-defi/multiplyr-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

POSSIBLE LOSS OF FUNDS

### Overview


This bug report discusses an issue with the Wormhole protocol where transactions can be lost if the rebalancer bot calls a function with the wrong chain ID. This can happen because the Wormhole Chain IDs are different from the network chain ID and can be easily confused. The code location for this issue is in the WormholeRouter.sol file. The impact of this bug is rated as a 5 out of 10, with a likelihood of 1. The recommendation is to use the solution provided by the Affine DeFi team, which can be found in the commit 06d6bc37fa80f0fdf794a8cb93e8100288d065e0.

### Original Finding Content

##### Description

Wormhole does not fail if the destination chain ID is different from the one supposed to be. If the rebalancer bot calls this function directly with a different chain ID, it will not fail, so funds during the transactions can be lost.

You can check the [Wormhole Chain IDs](https://book.wormhole.com/reference/contracts.html#core-bridge) on each chain, which is not the same as the network chain ID and can be easily confused.

Code Location
-------------

#### WormholeRouter.sol

```
function _validateWormholeMessageEmitter(IWormhole.VM memory vm) internal view {
    require(vm.emitterAddress == bytes32(uint256(uint160(otherLayerRouter))), "Wrong emitter address");
    require(vm.emitterChainId == otherLayerChainId, "Wrong emitter chain");
    require(vm.nonce >= nextValidNonce, "Old transaction");
}


```

1. Confuse wormhole chain ID with network chain ID
2. Initialize the contract with a wrong wormhole chain ID
3. Execute transactions on the protocol
4. Validate wormhole message emitter does not work as intended

##### Score

Impact: 5  
Likelihood: 1

##### Recommendation

**SOLVED**: The `Affine DeFi team` solved the issue in commit:
[06d6bc37fa80f0fdf794a8cb93e8100288d065e0](https://github.com/Multiplyr/contracts/commit/06d6bc37fa80f0fdf794a8cb93e8100288d065e0)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Multiplyr |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/affine-defi/multiplyr-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/affine-defi/multiplyr-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

