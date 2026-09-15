---
# Core Classification
protocol: Casimir
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35014
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
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
  - Hans
  - 0kage
---

## Vulnerability Title

Incorrect test setup leads to false test outcomes

### Overview

See description below for full details.

### Original Finding Content

**Description:** `IntegrationTest.t.sol` includes an integrated test that verifies the entire staking lifecycle. However, the current test setup, in several places, advances the blocks using foundry's `vm.roll` but neglects to adjust the timestamp using `vm.warp`.

This allows the test setup to claim rewards without any time delay.

_IntegrationTest.t.sol Line 151_
```solidity
>       vm.roll(block.number + eigenWithdrawals.withdrawalDelayBlocks() + 1); //@audit changing block without changing timestamp
        vm.prank(reporterAddress);
>       manager.claimRewards(); //@audit claiming at the same timestamp

        // Reporter runs after the heartbeat duration
        vm.warp(block.timestamp + 24 hours);
        timeMachine.setProofGenStartTime(0.5 hours);
        beaconChain.setNextTimestamp(timeMachine.proofGenStartTime());
        vm.startPrank(reporterAddress);
        manager.startReport();
        manager.syncValidators(abi.encode(beaconChain.getActiveBalanceSum(), 0));
        manager.finalizeReport();
        vm.stopPrank();
````

Moving blocks without updating the timestamp is an unrealistic simulation of the blockchain. As of EigenLayer M2, `WithdrawDelayBlocks` are 50400, which is approximately 7 days. By advancing 50400 blocks without changing the timestamp, tests overlook several accounting edge cases related to delayed rewards. This is especially true because each reporting period lasts for 24 hours - this means there are 7 reporting periods before a pending reward can actually be claimed.

**Impact:** An incorrect setup can provide false assurance to the protocol that all edge cases are covered.

**Recommended Mitigation:** Consider modifying the test setup as follows:

- Run reports without instantly claiming rewards. This accurately reflects events on the real blockchain.
- Consider adjusting time whenever blocks are advanced.

**Casimir:**
Fixed in [290d8e1](https://github.com/casimirlabs/casimir-contracts/commit/290d8e11846c5d20ed6a059e32864c8227fb582d)

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Casimir |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

