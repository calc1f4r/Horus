---
# Core Classification
protocol: EulerEarn_2025-07-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62184
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/EulerEarn-security-review_2025-07-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-11] Flash loan attack reallocates liquidity to riskier strategy vaults

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

In `EulerEarn`, user deposits are distributed across the underlying `supplyQueue` strategy vaults according to their remaining capacity. The `_supplyStrategy()` function iterates through this queue and deposits funds into the first supply strategy vault with available capacity. If a supply strategy vault hits its cap, the `EulerEarn` vault proceeds to the next one until the entire deposit is allocated:

```solidity
function _supplyStrategy(uint256 assets) internal {
        for (uint256 i; i < supplyQueue.length; ++i) {
            IERC4626 id = supplyQueue[i];

            uint256 supplyCap = config[id].cap;
            if (supplyCap == 0) continue;

            uint256 supplyAssets = _expectedSupplyAssets(id);

            uint256 toSupply =
                UtilsLib.min(UtilsLib.min(supplyCap.zeroFloorSub(supplyAssets), id.maxDeposit(address(this))), assets);

            if (toSupply > 0) {
                // Using try/catch to skip vaults that revert.
                try id.deposit(toSupply, address(this)) returns (uint256 suppliedShares) {
                    config[id].balance = (config[id].balance + suppliedShares).toUint112();
                    assets -= toSupply;
                } catch {}
            }

            if (assets == 0) return;
        }

        if (assets != 0) revert ErrorsLib.AllCapsReached();
    }
```

However, this design introduces a risk of **manipulative reallocation of liquidity**, where a malicious actor can perform a flash-loan attack: deposit a large amount of assets into `EulerEarn`, trigger redistribution across the `supplyQueue`, and then withdraw those assets in the same transaction. This causes the liquidity to be shifted away from larger, safer supply strategy vaults and into smaller or riskier ones.

For instance:

- Assume there are two strategy vaults (A and B) in the `supplyQueue` with caps of 100M and 20M, respectively. Supply strategy vault A currently holds 20M, and supply strategy vault B holds 1M.
- An attacker can deposit 99M into `EulerEarn`, causing funds to overflow from A into B. Then they immediately withdraw the 99M, leaving B with a disproportionate amount of the vault’s total liquidity.

This exploit allows attackers to manipulate portfolio allocation in `EulerEarn`, degrading performance and increasing risk exposure. Moreover, withdrawing a large share from one strategy vault could cause liquidity shortages and negatively impact users of that strategy vault.

**Recommendations**

Consider increasing the supply cap of the first strategy vault in the `supplyQueue` to a high value to make it act as a buffer to absorb temporary surges and protect smaller strategy vaults.


### Euler comments

We acknowledge the finding, will keep as is. Behaviour is the same in the original codebase.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | EulerEarn_2025-07-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/EulerEarn-security-review_2025-07-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

