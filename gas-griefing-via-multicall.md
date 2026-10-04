---
# Core Classification
protocol: Pyth Network Per
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47179
audit_firm: OtterSec
contest_link: https://www.pyth.network/
source_link: https://www.pyth.network/
github_link: https://github.com/pyth-network/per

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
finders_count: 2
finders:
  - Robert Chen
  - Nicholas R.Putra
---

## Vulnerability Title

Gas Griefing Via Multicall

### Overview


The report discusses a potential vulnerability in the ExpressRelay contract that could be exploited by a malicious actor. The issue occurs when processing a multicall transaction, where the data returned after each call is stored in memory. This can result in a significant increase in gas costs, especially if the returned data is excessively large. This vulnerability can lead to the failure of the entire transaction, disrupting its execution. The suggested solution is to implement the ExcessivelySafeCall library and use it instead of the current callWithBid function, which will restrict the amount of data that can be copied from the external call's return value. The issue has been fixed in the latest version of the contract. 

### Original Finding Content

## Potential Gas Griefing Vulnerability in Multicall within ExpressRelay

There is a potential gas griefing vulnerability in multicall within ExpressRelay. When processing multicall, the returned data after each call to `callWithBid` is stored in memory within `result`. A large result size significantly increases the gas cost of the entire multicall transaction. This issue is particularly concerning since multicall does not limit the size of `result` that stores the data returned by external calls.

```solidity
// ExpressRelay.sol solidity
function multicall(
    bytes calldata permissionKey,
    MulticallData[] calldata multicallData
)[...]
{
    [...]
    for (uint256 i = 0; i < multicallData.length; i++) {
        try
            // callWithBid will revert if call to external contract fails or if bid conditions
            // not met
            this.callWithBid(multicallData[i])
            returns (bool success, bytes memory result) {
                multicallStatuses[i].externalSuccess = success;
                multicallStatuses[i].externalResult = result;
            } catch Error(string memory reason) {
                multicallStatuses[i].multicallRevertReason = reason;
            }
        [...]
    }
    [...]
}
```

A malicious actor may exploit this by including a single call in multicall that returns an excessively large result. Processing this large result will consume a significant portion of the transaction’s gas budget. If the gas cost of processing the large result exceeds the available gas budget, the entire multicall transaction may fail, disrupting the execution.

## Remediation

Implement the `ExcessivelySafeCall` library and invoke `excessivelySafeCall` instead of within `callWithBid`. This will restrict the amount of data that may be copied from the external call’s return value.

© 2024 Otter Audits LLC. All Rights Reserved. 8/18

## Pyth ExpressRelay Audit 04 — Vulnerabilities Patch

Fixed in f0a9a7b.

© 2024 Otter Audits LLC. All Rights Reserved. 9/18

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Network Per |
| Report Date | N/A |
| Finders | Robert Chen, Nicholas R.Putra |

### Source Links

- **Source**: https://www.pyth.network/
- **GitHub**: https://github.com/pyth-network/per
- **Contest**: https://www.pyth.network/

### Keywords for Search

`vulnerability`

