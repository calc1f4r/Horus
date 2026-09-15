---
# Core Classification
protocol: Symbiotic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64341
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
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
finders_count: 4
finders:
  - 0kage
  - Aleph-v
  - ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3
  - Farouk
---

## Vulnerability Title

Missing bounds check on weight values in `WeightedTokensVPCalc` and `WeightedVaultsVPCalc`

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `WeightedTokensVPCalc` and `WeightedVaultsVPCalc` contracts lack proper bounds checking when setting weight values, which could lead to integer overflow during voting power calculations or complete elimination of voting power through zero weights.

The weight-setting functions in both contracts accept any `uint208` value without validation:

```solidity
// WeightedTokensVPCalc.sol
function setTokenWeight(address token, uint208 weight) public virtual checkPermission {
    _setTokenWeight(token, weight);  // No bounds checking
}

// WeightedVaultsVPCalc.sol
function setVaultWeight(address vault, uint208 weight) public virtual checkPermission {
    _setVaultWeight(vault, weight);  // No bounds checking
}
```

The voting power calculation multiplies stake amounts by these weights without overflow protection:

```solidity
// WeightedTokensVPCalc.sol
function stakeToVotingPower(address vault, uint256 stake, bytes memory extraData)
    public view virtual override returns (uint256) {
    return super.stakeToVotingPower(vault, stake, extraData) * getTokenWeight(_getCollateral(vault)); //@audit could go to 0 or overflow based on weight set
 }
```

**Impact:** Cause an integer overflow (extremely large weight) or total domination of one token over the rest or complete voting power elimination (0 weight).

While the weight-setting functions are protected by the `checkPermission` modifier and controlled by network governance in production deployments, technical safeguards remain important.

**Recommended Mitigation:** Consider implementing a min and max weight that are either constants or immutable.

```solidity
contract WeightedTokensVPCalc is NormalizedTokenDecimalsVPCalc, PermissionManager {
    uint208 public constant MIN_WEIGHT = 1e6;     // Minimum non-zero weight
    uint208 public constant MAX_WEIGHT = 1e18;    // Maximum reasonable weight

    function setTokenWeight(address token, uint208 weight) public virtual checkPermission {
        require(weight <= MAX_WEIGHT, "Weight exceeds maximum");
        require(weight <= MAX_SAFE_WEIGHT, "Weight risks overflow");

        _setTokenWeight(token, weight);
    }
}
```

**Symbiotic:** Fixed in [2a8b18d](https://github.com/symbioticfi/relay-contracts/pull/36/commits/2a8b18d8d6bb8b487b8eecf4485758f1d6fe93a5).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Symbiotic |
| Report Date | N/A |
| Finders | 0kage, Aleph-v, ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

