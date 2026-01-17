---
# Core Classification
protocol: Mantle Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19476
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/mantle/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/mantle/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Gas Exhaustion In resetRollupBatchData() Loop

### Overview

See description below for full details.

### Original Finding Content

## Code Review Summary

## MNT-23 Potential Gas Exhaustion in `resetRollupBatchData()`
**Asset:** `resetRollupBatchData` function  
**Status:** Resolved: See Resolution  
**Rating:** Severity: Low | Impact: Low | Likelihood: Medium  

### Description
The function `resetRollupBatchData()` lacks bounds on the for loop on line [198], which may lead to potential gas exhaustion. Without defining limits, the loop may iterate over many elements, causing excessive gas consumption and potential out-of-gas errors.

### Recommendations
- Determine a reasonable upper bound or limit for the loop based on the expected maximum value of `rollupBatchIndex`. This upper bound should ensure that the loop does not consume excessive gas or cause out-of-gas errors.
- Update the loop condition to enforce the defined upper bound or limit, ensuring that the loop terminates within a reasonable number of iterations.

### Resolution
The issue has been acknowledged by the development team with the following comment:
> We can specify the starting `_rollupBatchIndex` that needs to be reset, so that it can be reset from the latest `rollupBatchIndex` to the current specified `_rollupBatchIndex`. When many batches are required to be reset, it can be reset in batches, so that there is no out of gas error.

An event has been added on completion of `resetRollupBatchData()` at PR-1174.

---

## MNT-24 Unreachable Error Handling In `proxyd/cache.go`
**Asset:** `proxyd/cache.go`  
**Status:** Resolved: See Resolution  
**Rating:** Severity: Low | Impact: Low | Likelihood: Medium  

### Description
Cache misses may never be counted, leading to inaccurate logging. There is no way to reach the `RecordCacheMiss()` function on line [151] due to conflicting nested if statements.

```go
149 if res != nil {
if res == nil {
151 RecordCacheMiss(req.Method)
} else {
153 RecordCacheHit(req.Method)
}
155 }
```

This results in only `RecordCacheHit()` ever being processed, and cache misses would never be counted.

### Recommendations
Remove the outer `if res != nil` check on line [149].

### Resolution
The issue has been addressed at PR-1137.

---

## MNT-25 Mnemonic Cannot Be Used Without Supplying Private Key
**Asset:** `mt-batcher/mt_batcher.go`  
**Status:** Resolved: See Resolution  
**Rating:** Severity: Low | Impact: Low | Likelihood: Low  

### Description
Mnemonic cannot be used without a private key, defeating the purpose of supporting mnemonic phrases. The implementation requires `cfg.PrivateKey = ""` when a mnemonic phrase is set using `GetConfiguredPrivateKey()`, but `cfg.PrivateKey` also needs to be a valid private key in `mt-batcher/services/mt_batcher.go`.

### Recommendations
- Modify implementation to allow for use of either a mnemonic or a private key with `mtBatherPrivateKey` and `feePrivateKey` variables.
- Alternatively, if support for mnemonic is not required, remove the unused code.

### Resolution
The issue has been addressed at commit bb394d0.

---

## MNT-26 Nil Pointer Panic If DTL Returns Malformed Data
**Asset:** `mt-batcher/services/client/client.go`  
**Status:** Resolved: See Resolution  
**Rating:** Severity: Low | Impact: Low | Likelihood: Low  

### Description
An unhandled panic may occur if `enqueue.Origin` is nil since it is a pointer type.

### Recommendations
Ensure `enqueue.Origin` is not nil and return an error otherwise.

### Resolution
The issue has been addressed at PR-1163.

---

## MNT-27 Unhandled Panic If Metadata Is Set To Nil
**Asset:** `mt-batcher/services/restorer/handle.go`  
**Status:** Resolved: See Resolution  
**Rating:** Severity: Low | Impact: Low | Likelihood: Low  

### Description
Decoding a pointer with `json.Unmarshal()` may result in panic if `metadata` is set to nil.

### Recommendations
Ensure `txDecodeMetaData` is not nil before passing it to `json.Unmarshal`.

### Resolution
The issue has been addressed at PR-1142.

---

## MNT-28 Lack of Error Handling in `Hex2Bytes()`
**Asset:** `l2geth/common/bytes.go`  
**Status:** Closed: See Resolution  
**Rating:** Severity: Low | Impact: Low | Likelihood: Low  

### Description
Lack of error checks in `common.HexToAddress()` may result in an undefined return value for malformed input as no errors are handled or propagated from downstream `Hex2Bytes()`.

### Recommendations
Catch and propagate an error if one arises from `hex.DecodeString()` in `Hex2Bytes()`.

### Resolution
The issue has been acknowledged by the development team with the following comment:
> We have reviewed the code related to this function. It has no security implication if this err is not handled and it returns nil. Therefore we will leave it as pending until future releases.

---

## MNT-29 Incorrect Usage Of Context In `NewDriver()` & `NewDataService()`
**Assets:** `mt-batcher/services/sequencer/driver.go`, `mt-batcher/services/restorer/driver.go`  
**Status:** Closed: See Resolution  
**Rating:** Severity: Low | Impact: Low | Likelihood: Low  

### Description
The context is made `WithTimeout()` and then cancelled via `defer`, which will not terminate the original context, but its sub-context.

### Recommendations
Create a sub context with a cancel then pass that to the driver.

### Resolution
The issue has been acknowledged by the development team with the following comment:
> Thank you for your recommendation. Given its non-critical nature, we will include it as a pending task for future releases.

---

## MNT-30 Waitgroup Counter Not Incremented
**Asset:** `mt-batcher/services/sequencer/driver.go`  
**Status:** Resolved: See Resolution  
**Rating:** Severity: Low | Impact: Low | Likelihood: Low  

### Description
Wait group calls `Done()` in `CheckConfirmedWorker()` and `RollupFeeWorker()` functions but does not increment the wait group counter.

### Recommendations
Call `d.wg.Add(1)` before calling `RollupFeeWorker()` or `CheckConfirmedWorker()`.

### Resolution
The issue has been addressed at commit bb394d0.

---

## MNT-31 `hashAfterPops()` Uses Incorrect Length
**Asset:** `fraud-proof/proof/state/stack.go`  
**Status:** Resolved: See Resolution  
**Rating:** Informational  

### Description
The `HashAfterPops()` function uses incorrect length when referencing elements of the hash array.

### Recommendations
Change the function to reference size of the hash array instead.

### Resolution
The issue has been addressed at PR-1133.

---

## MNT-32 Compatibility Issues With Mantle L2 & Solidity Version ^0.8.20
**Asset:** Various files  
**Status:** Closed: See Resolution  
**Rating:** Informational  

### Description
Contracts deployed on Mantle face compatibility issues when using a Solidity version of 0.8.20 or greater due to the absence of the OP Code PUSH0.

### Recommendations
Amend instances of pragma versioning on files intended to be deployed to Mantle L2 to exclude versions greater or equal to 0.8.20.

### Resolution
The issue has been acknowledged by the development team with the following comment:
> Given the novelty of the current geth version, there is no support for the opcode PUSH0. Mantle network employs pre-compiled contracts from solc 0.8.9. The primary risk resides in executing user’s dApp contracts. Consequently, we will preliminarily highlight this in our documentation, with subsequent updates introducing pertinent restrictions.

---

## MNT-33 Proxy Inherited Solidity Contracts Should Contain A Storage Gap
**Asset:** Various files  
**Status:** Closed: See Resolution  
**Rating:** Informational  

### Description
If a contract is inherited by another contract that is intended to live behind a proxy, it is advisable to include a storage gap.

### Recommendations
Include an unused state variable array in this contract, such as `uint256[50] __gap;`. If additional state variables are needed, reduce the size of the unused state variable array to counteract their inclusion.

### Resolution
The issue has been acknowledged by the development team with the following comment:
> This issue is recognized, and we will subsequently implement a storage gap in all inherited Solidity contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Mantle Network |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/mantle/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/mantle/review.pdf

### Keywords for Search

`vulnerability`

