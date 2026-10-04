---
# Core Classification
protocol: MegaETH
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47161
audit_firm: OtterSec
contest_link: https://megaeth.systems/
source_link: https://megaeth.systems/
github_link: https://github.com/Troublor/launch-pool

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Robert Chen
---

## Vulnerability Title

LOF Due to Incorrect Tracking of Received Ether

### Overview


The report discusses a bug in LaunchBridge where the claim function triggers a process to claim Ether from Lido. However, during the transfer of the claimed Ether, LaunchBridge mistakenly records it as a new deposit instead of claimed Ether. This can lead to a deficit in the system and result in a direct loss of user funds. The bug has been resolved in the latest patch. To fix this issue, the developers need to ensure that Ether received from Lido during the claim process is treated differently from new user deposits.

### Original Finding Content

## LaunchBridge Claim Process

In **LaunchBridge**, when `claim` is called, it triggers a process to claim Ether that was unstaked and withdrawn from Lido. The function checks the status of withdrawal requests to identify which ones are claimable (finalized and not yet claimed). If claimable withdrawals are found, it calculates the expected amount of Ether (`expected`) and then proceeds to claim these withdrawals. The claimed Ether is transferred from the Lido contract to LaunchBridge. During this transfer, LaunchBridge receives Ether, which triggers the `receive` function in the contract. In this case, `receive` calls `depositETH`, which in turn records a new deposit of Ether.

## Code Snippet

> _ src/LaunchBridge.sol rust

```rust
/// @notice Mint new ETH shares from new deposit
/// @param depositedAmount Amount deposited in ETH (wad)
/// @param alreadyDeposited The amount has already been deposited to the contract
function _recordDepositETH(uint256 depositedAmount, bool alreadyDeposited) internal {
    uint256 _totalETHBalance = totalETHBalance();
    if (alreadyDeposited) {
        _totalETHBalance = _totalETHBalance - depositedAmount;
    }
    uint256 sharesToIssue = depositedAmount * totalETHShares / _totalETHBalance;
    require(sharesToIssue > 0, ZeroSharesIssued());
    _mintETHShares(msg.sender, sharesToIssue);
    emit ETHDeposited(msg.sender, sharesToIssue, depositedAmount);
}
```

`depositETH` adds the received Ether as a new deposit into the system, treating it as if it were a fresh deposit from a user. This deposit increases the total ETH balance tracked by the system. Since the Ether from Lido is mistakenly treated as a new deposit rather than recording it as claimed Ether, the `ethAmountToMove` value becomes inaccurate. The incorrect recording of claimed Ether as a new deposit may result in scenarios where the system allocates more Ether than it has, resulting in a deficit when fulfilling user withdrawals. This deficit represents a direct loss of user funds.

## Remediation

Ensure that Ether received from Lido during the claim process is treated differently from genuine new user deposits.

## Patch

Resolved in commit **6867123**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | MegaETH |
| Report Date | N/A |
| Finders | Robert Chen |

### Source Links

- **Source**: https://megaeth.systems/
- **GitHub**: https://github.com/Troublor/launch-pool
- **Contest**: https://megaeth.systems/

### Keywords for Search

`vulnerability`

