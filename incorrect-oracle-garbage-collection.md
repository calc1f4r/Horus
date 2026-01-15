---
# Core Classification
protocol: Switchboard_evm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47982
audit_firm: OtterSec
contest_link: https://switchboard.xyz/
source_link: https://switchboard.xyz/
github_link: https://github.com/switchboard-xyz/switchboard-evm

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
finders_count: 4
finders:
  - Woosun Song
  - Matteo Oliva
  - OtterSec
  - Nicholas Putra
---

## Vulnerability Title

Incorrect Oracle Garbage Collection

### Overview


The oracleHeartbeat function in the Switchboard contract has a bug where it sets the numRows of the wrong oracle during garbage collection. This can lead to a situation where an oracle exists in multiple queues at the same time, causing issues with other parts of the code that assume an oracle only exists in one queue. To fix this, the setNumRows function should be changed to use the correct oracleId. This bug has been patched in the latest version of the contract.

### Original Finding Content

## Oracle Heartbeat Vulnerability

`oracleHeartbeat` performs garbage collection on a valid oracle instead of an expired one. Each oracle has a field named `numRows`, which indicates the number of queues associated with it. An oracle may only be added to a queue if its `numRows` value is zero. Therefore, setting `numRows` of an oracle back to zero should always be accompanied by queue removal to prevent the oracle from existing in multiple queues simultaneously.

However, `oracleHeartbeat` erroneously performs `setNumRows` on `oracleId` instead of `gcOracleId` during garbage collection.

### Code Snippet
```solidity
// contracts/src/Switchboard/oracle/Oracle.sol
function oracleHeartbeat(address oracleId) external {
    /* ... */
    // get gcIdx - guaranteed to have at least 1 element here
    uint256 gcIdx = queue.gcIdx;
    address gcOracleId = queue.oracles[gcIdx];
    // increment gcIdx
    OracleQueueLib.incrementGC(oracle.queueId);
    // handle expired oracles if gcIdx is expired
    if (
        (OracleLib.oracles(gcOracleId).lastHeartbeat + queue.oracleTimeout) < block.timestamp
    ) {
        // log the garbage collection
        emit OracleGC(gcOracleId, oracle.queueId);
        // swap remove queue.oracles[gcIdx]
        OracleLib.setNumRows(oracleId, 0);
        OracleQueueLib.swapRemove(oracle.queueId, gcIdx);
    }
}
```

### Vulnerability Explanation
By exploiting this vulnerability, an attacker may create an oracle that exists in two queues simultaneously, violating crucial assumptions made by other parts of the code. For example, `saveResults` assumes that an oracle exists in only one queue and that an oracle’s effective heartbeat indicates it is not expired. However, if an oracle is present in multiple queues, it may continue to perform heartbeats even when it is already expired.

### Remediation
Change `setNumRows(oracleId, 0)` to `setNumRows(gcOracleId, 0)`.

### Patch
Fixed in commit `e833e48`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Switchboard_evm |
| Report Date | N/A |
| Finders | Woosun Song, Matteo Oliva, OtterSec, Nicholas Putra |

### Source Links

- **Source**: https://switchboard.xyz/
- **GitHub**: https://github.com/switchboard-xyz/switchboard-evm
- **Contest**: https://switchboard.xyz/

### Keywords for Search

`vulnerability`

