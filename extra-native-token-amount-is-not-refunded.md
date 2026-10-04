---
# Core Classification
protocol: Omni Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53663
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
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

Extra Native Token Amount Is Not Refunded

### Overview

See description below for full details.

### Original Finding Content

## Security and Development Issues Documentation

## OMP-18 Excess Token Payment Not Refunded
### Asset
`*`

### Status
Resolved: See Resolution

### Rating
- Severity: Medium
- Impact: Medium
- Likelihood: Low

### Description
When a user initiates an `XCall` using the function `xcall()`, they pay for fees in native token. However, any excess amount paid beyond the required fee is not refunded to the user.

The function `xcall()` checks using the require statement on line [140] that the user pays enough fees. This amount depends on the `destChainId`, the data used in the `xcall()`, and the `gasLimit`. While a user may accidentally or intentionally pay more than this required amount, any excess payment will not be refunded.

### Recommendations
Refund the extra native token amount to the user. Ensure that the refund occurs after the event emission to avoid reentrancy.

### Resolution
The development team has decided to not address this issue for now.

## OMP-19 Usage of Deprecated Dependency Functions
### Asset
`lib/k1util/k1util.go`, `halo/evmstaking/evmstaking.go`

### Status
Resolved: See Resolution

### Rating
- Severity: Low
- Impact: Medium
- Likelihood: Low

### Description
Multiple functions end up calling deprecated functions from `go-ethereum/crypto v1.13.15` that could panic under certain conditions, such as points not being on the curve.

### Recommendations
Update `go-ethereum` dependency to version `>=1.14.0`.

### Resolution
Dependency has been updated in the main branch during testing.

## OMP-20 Lack Of stateJSON Validation When Loading From File
### Asset
`halo/attest/voter/voter.go`

### Status
Resolved: See Resolution

### Rating
- Severity: Low
- Impact: Low
- Likelihood: Low

### Description
When loading state from file, there is no validation of loaded `stateJSON` data to ensure it has not been corrupted or malformed. If any of the `types.Vote` values in the `stateJSON` have any of their parameter values set to `nil`, it may lead to unexpected panics elsewhere in the code.

### Recommendations
Implement sanity checks to verify that `stateJSON` data loaded from file is not malformed and that all of its values, including their parameters, are set correctly and not `nil`.

### Resolution
This issue has been addressed in PR #1320.

## OMP-21 nil Pointer Deference Panics In AddVotes(), Add() and addOne()
### Asset
`halo/attest/keeper/msg_server.go`, `halo/attest/keeper/keeper.go`

### Status
Resolved: See Resolution

### Rating
Informational

### Description
There is no validation of `Votes` values in the `msg` parameter of `MsgAddVotes` type in the `Add()` function. This could result in a nil dereference panic on line [114] if a `BlockHeader` parameter was `nil`.

There are also no nil checks on `agg` parameter values in the `addOne()` function, which may lead to a nil dereference panic on lines [145] and lines [150-153]. `addOne()` is called via `Add()` by `AddVotes()` function of `halo/attest/keeper/msg_server.go`, which does not perform validation of `msg` parameter of `MsgAddVotes` type. As a result, it is possible that a `MsgAddVotes` with invalid votes will be processed.

If `Votes` array elements provided as part of `MsgAddVotes` type have their JSON values set to `null`, or omitted completely, they will be interpreted as `nil`, and unexpected panics may occur during dereferencing.

### Recommendations
Implement verification of `Votes` values in the higher-level `AddVotes()` function to ensure they are not set to `nil`, particularly `BlockHeader`. This would prevent invalid values flowing into `Add()` and `addOne()` functions.

### Resolution
This issue has been addressed in PR #1252.

## OMP-22 Unaddressed TODO Comments
### Asset
`*.go`, `halo/attest/keeper/keeper.go`

### Status
Resolved: See Resolution

### Rating
Informational

### Description
A number of `//TODO` style comments have been found throughout the codebase. These are marked as known issues, and therefore raised as informational; however, many of them have security considerations. Some examples of those identified which have security considerations and are not yet fixed:
- `halo/evmengine/keeper/abci.go` on line [86]: `// TODO(corver): Figure out what to use here.` - currently the zero hash is used as the beacon block hash.
- `halo/evmengine/keeper/abci.go` on line [83]: `// TODO(corver): implement proper randao.` - the randomness passed to the execution client is currently the previous block hash and unsafe for use.

Note, the list above is not exhaustive.

### Recommendations
Address all `//TODO` comments throughout the codebase, verify and ensure they have all been addressed where relevant, or clear assumptions and design decisions have been made and documented.

### Resolution
This issue has been addressed in PR #1332.

## OMP-23 Additional Chain Height And Header Checks Required
### Asset
`lib/xchain/provider/fetch.go`

### Status
Closed: See Resolution

### Rating
Informational

### Description
Inside `finalisedInCache()` function on line [143], there are no checks for a scenario where the latest fetched head is larger than the chain's height. Although an unlikely condition, it could indicate something has gone fundamentally wrong and, as such, should be handled and managed.

### Recommendations
Consider implementing additional checks to cater for an unlikely situation where the latest fetched head is larger than the chain's height.

### Resolution
The issue has been acknowledged by the development team and closed with the following comment: "We trust the RPC endpoints to return valid data."

## OMP-24 No Linear Search Data Set Restrictions
### Asset
`lib/xchain/merkle.go`

### Status
Resolved: See Resolution

### Rating
Informational

### Description
Linear search is utilized to find Merkle tree's leaf indices, but no restrictions on the overall data set size have been implemented. As Merkle trees grow, so will the time to search through them to find relevant indices, potentially leading to poor performance or creating a DoS (denial-of-service) condition.

### Recommendations
Consider implementing checks and restrictions on sizes of data sets being searched through.

### Resolution
This issue has been addressed in PR #1319.

## OMP-25 Lack Of Validators Array Size Checks
### Asset
`halo/evmengine/keeper/keeper.go`

### Status
Resolved: See Resolution

### Rating
Informational

### Description
If the validators list is empty or all validators have power of 0, a division by zero panic may occur on line [116] at `halo/evmengine/keeper/keeper.go`. In `newABCIValsetFunc()` function of `lib/cchain/provider/abci.go`, an array of validators is created based on the `ValidatorSetResponse` type response from a call to `ValidatorSet()`. If no validators existed or all of them had power of 0, they would not be included in the returned array as per check on line [128] of `halo/valsync/keeper/query.go`. As such, `valSetResponse` would be set with an empty Validators array. Subsequently, a call on line [116] at `halo/evmengine/keeper/keeper.go` would result in a division by zero panic due to `len(valset.Validators)` being zero:
```go
nextIdx := int(idx+1) % len(valset.Validators)
```

### Recommendations
Implement checks to ensure `valset.Validators` array is not empty before performing any operations on it, or using its size (which could be zero) in calculations.

### Resolution
This issue has been addressed in PR #1318.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Omni Network |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf

### Keywords for Search

`vulnerability`

