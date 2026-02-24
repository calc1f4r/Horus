---
# Core Classification
protocol: Eigenlayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53494
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-16-EigenLayer.md
github_link: none

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
  - Hexens
---

## Vulnerability Title

[EIG-14] M1 EigenPods can restake and withdraw without proving and burning shares

### Overview


This bug report is about a critical issue in the EigenPod.sol code. The EigenPod has two functions for withdrawing ETH, but they do not work well together. This can be exploited to restake and withdraw ETH without burning shares, allowing for free minting of shares. The report suggests that the function `_processWithdrawalBeforeRestaking` should be fixed by zeroing out the `nonBeaconChainETHBalanceWei` to prevent this exploit. The status of the bug is currently fixed.

### Original Finding Content

**Severity:** Critical

**Path:** EigenPod.sol:withdrawNonBeaconChainETHBalanceWei#L393-L404

**Description:**  

The EigenPod offers 2 functions to withdraw ETH directly without proving a withdrawal. The first one is `withdrawBeforeRestaking`, which requires `hasRestaked` to be `false`. The second one is  `withdrawNonBeaconChainETHBalanceWei`, which is introduced in M2 and takes from a balance counter that is increased upon execution of `receive`. 

The former is to allow for depositing and withdrawing before restaking (and so without proofs) and the latter is to withdraw any ETH that was mistakenly sent to the EigenPod. However, they do not work well together. 

Most M1 EigenPods will still have `hasRestaked` be set to `false`, as proving is not enabled for M1 EigenPods. Once they are upgraded to the M2 implementation, they will have access to both functions.

This can then be exploited to restake and withdraw the stake without proving the withdrawal and consequently without burning the shares, effectively allowing for free minting of shares.

Consider the following scenario:

1. An M1 EigenPod with `hasRestaked` is `false` is upgraded to the M2 implementation.

2. The owner sends 32 ETH to the EigenPod, the `nonBeaconChainETHBalanceWei` increases with 32 ETH.

3. The owner calls `withdrawBeforeRestaking`, which will simply send the entire ETH balance (32 ETH) to the owner.

4. The owner activates restaking, creates a validator and verifies the withdrawal credentials, receiving 32 ETH in shares.

5. The owner exits the validator and the EigenPod receives the 32 ETH principal.

6. The owner can now call `withdrawNonBeaconChainETHBalanceWei` to withdraw the 32 ETH, because `nonBeaconChainETHBalanceWei` is still equal to 32 ETH, bypassing the withdrawal proof and keeping the 32 ETH shares.

7. Repeat (or use multiple validators) for more free shares.

```
receive() external payable {
    nonBeaconChainETHBalanceWei += msg.value;
    emit NonBeaconChainETHReceived(msg.value);
}

function withdrawNonBeaconChainETHBalanceWei(
    address recipient,
    uint256 amountToWithdraw
) external onlyEigenPodOwner {
    require(
        amountToWithdraw <= nonBeaconChainETHBalanceWei,
        "EigenPod.withdrawnonBeaconChainETHBalanceWei: amountToWithdraw is greater than nonBeaconChainETHBalanceWei"
    );
    nonBeaconChainETHBalanceWei -= amountToWithdraw;
    emit NonBeaconChainETHWithdrawn(recipient, amountToWithdraw);
    _sendETH_AsDelayedWithdrawal(recipient, amountToWithdraw);
}

function withdrawBeforeRestaking() external onlyEigenPodOwner hasNeverRestaked {
    _processWithdrawalBeforeRestaking(podOwner);
}

function _processWithdrawalBeforeRestaking(address _podOwner) internal {
    mostRecentWithdrawalTimestamp = uint32(block.timestamp);
    _sendETH_AsDelayedWithdrawal(_podOwner, address(this).balance);
}
```

**Remediation:**  The function `_processWithdrawalBeforeRestaking` should also zero out `nonBeaconChainETHBalanceWei`, as the entire balance will be withdrawn anyway.

**Status:**   Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Eigenlayer |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-16-EigenLayer.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

