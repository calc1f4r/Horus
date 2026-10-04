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
solodit_id: 19477
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

Missing Zero Address Checks In Checkpoint Oracle

### Overview

See description below for full details.

### Original Finding Content

## Security Findings Report

## MNT-35 TSS Node Clients Have Unreachable Max Connection Attempts Logic
**Asset:** `tss/ws/client/tm/client.go`  
**Status:** Resolved: See Resolution  
**Rating:** Informational  

### Description
The WebSocket client of a TSS node employs an exponentially increasing time delay for reconnect attempts. When attempting to reconnect the WebSocket client of a TSS node, there is an exponentially increasing time delay to prevent accidental DoS attacks on the server being connected to. If the max number of reconnect attempts is reached then the program should return an error on line [308] of `tss/ws/client/tm/client.go`. However, because the time delay increases exponentially, and the max amount of tries is 25, this will lead to unrealistic waiting periods and over 2 years prior to the error message on line [308] being reached. This effectively makes line [308] unreachable.

### Recommendations
Reduce the exponential time gaps between reconnect attempts. Currently this is calculated by `(1 << uint(attempt)) * time.Second`. There is no realistic need to have over 1 year between reconnect attempts and, as such, a linear equation for the time delay seems more fitting.

### Resolution
The issue has been addressed at PR-1257.

---

## MNT-36 Irregular Size Of The First Signature In Sequence Will Trigger Panic
**Asset:** `datalayr-mantle/dl-disperser/aggregator.go`  
**Status:** Closed: See Resolution  
**Rating:** Informational  

### Description
In `flattenSigs()`, if the first signature is of incorrect size, the resulting `sigBytes` array will be created with an incorrect length and may panic with out of bounds error:

```go
410 func flattenSigs(sigs [][]byte) []byte {
412  sigLen := len(sigs[0])
414  sigBytes := make([]byte, len(sigs)*sigLen)
416  copy(sigBytes[i*sigLen:], sigs[i])
for i := 0; i < len(sigs); i++ {
418 }
return sigBytes
420 }
```

Note, this function is used by `datalayr-mantle/dl-disperser/utils.go genRandomSigs()`, which did not appear to be used in the reviewed codebase.

### Recommendations
Use the fixed `crypto.SignatureLength` from the `package crypto` instead of `sigLen := len(sig[0])` on line [412].

### Resolution
The issue has been acknowledged by the development team with the following comment: The code of the old version of Eigenlayr, which is currently obsolete. `flattenSigs()` has been removed.

---

## MNT-37 Unused Items in Structures
**Asset:** `mt-batcher/services/sequencer/driver.go`, `mt-batcher/services/restorer/service.go`  
**Status:** Resolved: See Resolution  
**Rating:** Informational  

### Description
Unused items in structures:
1. **Driver**
   - GraphqlClient
2. **DriverConfig**
   - EigenABI
   - EigenFeeABI
   - RollupMinSize
   - ChainID
   - EigenLogConfig
   - CheckerBatchIndex
3. **DaService**
   - GraphClient
4. **DaServiceConfig**
   - EigenABI
   - Timeout
   - Debug

### Recommendations
Remove all unused elements from the struct.

### Resolution
The issue has been addressed at PR-1202.

---

## MNT-38 Miscellaneous General Comments
**Asset:** Various files  
**Status:** Closed  
**Rating:** Informational  

### Description
This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Semantic overloaded variables**  
   On line [215] of the smart contract `TssGroupManager` an active member’s existence is determined by checking the length of their public key. It is best to avoid adding silent extra meanings to variables as when later changes are made it may not be obvious of their impact to such checks. See the OpenZeppelin forums for more details.

2. **Stale code**  
   In various places of the code there is code that is commented out and no longer used; this code should be removed to avoid mistakes in the future. Likewise, some contracts were confirmed to no longer be used and so should be removed from the project. Examples are:
   - Line [65] of `TssGroupManager`
   - The `WETH9` contract
   - Lines [127-138] of `tss/node/tsslib/p2p/communication.go`

3. **Lack of zero address checks**  
   In the smart contract function `TssStakingSlashing.setAddress()` there are no zero address checks on the argument inputs. This could result in one or both contracts being set to the default state if care is not taken whilst calling this function. It is suggested to verify both arguments are set prior to overwriting `bitToken` and `tssGroupContract` in storage.

4. **Use of SafeMath library with wrong Solidity version**  
   `TssRewardContract`, `BVM_EigenDataLayrFee`, `BVM_EigenDataLayrChain`, and `TssGroupManager` all import the `SafeMath` library or its upgradable variant despite using the versioning pragma `^ 0.8.0` or `pragma ^ 0.8.9` in which SafeMath behavior is included by default.

5. **Incorrect comments in codebase**  
   There are several instances of incorrect comments in the code:
   - In `BVM_EigenDataLayrChain` on line [197] there is an incorrect revert message for function `restRollupBatchData()`.
   - In `BVM_EigenDataLayrChain` on line [120] there is an incorrect revert message for function `setFraudProofAddress()`, as this function adds an address to the fraud proof whitelist, it does not remove it.
   - In `BVM_EigenDataLayrChain` on line [319] the NatSpec comment is incorrect as currently the challenger role has whitelisted access only.

6. **Magic numbers**  
   When constant values are used, these should be set as named constant variables rather than hardcoded values within the code body. This aids readability and makes future alterations easier for developers. One Golang example is the maximum batch size in `mt-batcher/services/restorer/handle.go` on line [97]. For Solidity examples, on line [75] of `TssRewardContract` both `10 ** 18` and `365 * 24 * 60 * 60` should be stored in named variables. Both could also make use of built-in Solidity number aliases, `1 ether == 10 ** 18` and `52 weeks == 365 * 24 * 60 * 60`.

7. **Numerous TODO comments to address**  
   Numerous TODO comments exist throughout the Solidity and Golang code outlining outstanding design decisions and feature implementation. Go through all TODO comments to ensure all key design decisions have been made, verified, and there are no outstanding items that could be considered critical.

8. **Explicit panic() calls throughout the codebase**  
   A number of explicit panic() calls exist throughout the Golang code. Investigate each occurrence individually to determine if the error conditions should be handled gracefully, or whether exiting with a panic is appropriate.

9. **Use of deprecated library ioutil**  
   The `io/ioutil` package has turned out to be a poorly defined and hard to understand collection of things. All functionality provided by the package has been moved to other packages and so should not be used. A non-exhaustive list of uses in the codebase is as follows:
   - `node/tsslib/storage/localstate_mgr.go` uses `ioutil.ReadFile` and `ioutil.WriteFile`.
   - `ws/client/tm/http_json_client.go` uses `ioutil.ReadAll`.
   - `proxyd/backend.go` uses `ioutil.ReadAll`.
   - `proxyd/rpc.go` uses `ioutil.ReadAll`.
   - `proxyd/server.go` uses `ioutil.ReadAll`.
   - `proxyd/tls.go` uses `ioutil.ReadFile`.
   - `subsidy/cache-file/cache.go` uses `ioutil.ReadFile`.
   - `tss/node/tsslib/storage/localstate_mgr.go` uses `ioutil.ReadFile` and `ioutil.WriteFile`.

10. **Use of deprecated error checking method**  
    The following files all make use of `os.IsNotExist()` for error detection; this only supports errors returned by the os package and so new code should use `errors.Is(err, fs.ErrNotExist)` to detect errors instead:
   - `tss/node/tsslib/storage/localstate_mgr.go`
   - `tss/node/tsslib/tss.go`
   - `subsidy/cache-file/cache.go`

11. **Gas Optimizations**  
    Some areas of code can be optimized further; this is important particularly for code intended to run on the Ethereum mainnet due to the transaction cost being generally higher there. Some examples are:
   - Calling a length in a loop, one such example is on line [67] of `TssGroupManager`: To save gas, this length should be called once and stored in a local variable rather than called every iteration of the loop.
   - Checks against booleans. Rather than checking if boolean == true, it is better to just check the boolean condition itself. Examples are line [95] and line [98] of `TssGroupManager`.
   - Accessing storage variables repeatedly. If a variable is needed multiple times in the same function it is better to write the value to a local variable and access that repeatedly. An example of this is `memberGroupKey[_publicKey]` in `TssGroupManager.setGroupPublicKey()` that is accessed 3 times.
   - Redundant checks. Some sections of code are unnecessary as shown below:
     - Line [127] of `TssStakingSlashing` is not needed as if `slashAmount[0] > 0` then `exIncome[0] > 0` as well. This is because the values of these variables can only be set via calling `setSlashingParams()` only and line [103] and line [104] enforce this relationship between `slashAmount[i]` and `exIncome[i]`.
     - `TssGroupManager.removeActiveTssMembers()` validates that the index given is less than the length of the array. However, this function is only ever called by `TssGroupManager.removeMember()` which bounds the input `i` by the array length already, making the check in `removeActiveTssMembers()` redundant.

### Recommendations
Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

### Resolution
The comments above have been acknowledged by the development team, and relevant changes actioned in PR-1140 and commit `bb394d0`.

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

