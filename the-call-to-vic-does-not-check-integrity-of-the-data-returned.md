---
# Core Classification
protocol: Morpho Vaults v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62927
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-Spearbit-Security-Review-May-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-Spearbit-Security-Review-May-2025.pdf
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
finders_count: 4
finders:
  - Saw-mon and Natalie
  - Om Parikh
  - Jonatas Martins
  - Emmanuele Ricci
---

## Vulnerability Title

The call to vic does not check integrity of the data returned

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
VaultV2.sol#L428-L436

## Description
When the codebase performs a `staticcall` to `vic`, the integrity of the returned data is not checked. There are two possible bad scenarios:

1. The returned data is empty. In this case, the code wrongfully assumes that data should always be non-empty and thus reads the output from the `add(data, 32)` memory slot which could hold bytes totally unrelated to the `staticcall`. We will examine this issue in the PoC in the next section.
   
2. The data returned might hold more bytes than one expects (more than 32 bytes).
   
3. The data type returned by the `vic` might have been meant to be of a different type than the one expected.

## Proof of Concept

**Case 1:**
```solidity
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;
import 'forge-std/Test.sol';
import 'forge-std/console.sol';

contract TestContract {
    function callMe(uint256 a, uint256 b) external returns (uint256) {
        return 1;
    }
}

contract SGeneralTest is Test {
    function testAss() public {
        scall(address(100), 100, 200);
    }

    function scall(address vic, uint256 a, uint256 b) private {
        (bool success, bytes memory data) =
            address(vic).staticcall(abi.encodeCall(TestContract.callMe, (a, b)));
        uint256 output = 0;
        assembly ("memory-safe") {
            output := mload(add(data, 32))
        }
        // interestPerSecond will be equal to output!
        assertEq(output, 68);
    }
}
```
In this case, `data` is empty and `solc` points empty arrays to the zero slot in memory `0x60` (Layout in Memory):

- The zero slot is used as the initial value for dynamic memory arrays and should never be written to ...

Let's examine the memory during the call to `scall`. Before encoding the `_calldata` (`abi.encodeCall(IVic.interestPerSecond, (_totalAssets, elapsed)))` for the `staticcall`, the memory looks like:

```
0x000 0000000000000000000000000000000000000000000000000000000000000000    scratch space slot 1
0x020 0000000000000000000000000000000000000000000000000000000000000000    scratch space slot 2
0x040 0000000000000000000000000000000000000000000000000000000000000080    free memory pointer
```

After encoding, the memory looks like:

```
0x000 0000000000000000000000000000000000000000000000000000000000000000    scratch space slot 1
0x020 0000000000000000000000000000000000000000000000000000000000000000    scratch space slot 2
0x040 00000000000000000000000000000000000000000000000000000000000000e4    free memory pointer (updated)
0x060 0000000000000000000000000000000000000000000000000000000000000000    zero slot **
0x080 0000000000000000000000000000000000000000000000000000000000000044    _calldata.length
```

This next chunk is the `abi-encoding`, !

```
0x0a0 e444521000000000000000000000000000000000000000000000000000000000
interestPerSecond.selector 100 200, !
0x0c0 0000006400000000000000000000000000000000000000000000000000000000
0x0e0 000000c8
```

fmp -> 00000000000000000000000000000000000000000000000000000000 padded 00 bytes

After the `staticcall`:

```
0x000 0000000000000000000000000000000000000000000000000000000000000000    scratch space slot 1
0x020 0000000000000000000000000000000000000000000000000000000000000000    scratch space slot 2
0x040 00000000000000000000000000000000000000000000000000000000000000e4    free memory pointer
0x060 0000000000000000000000000000000000000000000000000000000000000000    zero slot ** <-- data
0x080 0000000000000000000000000000000000000000000000000000000000000044    _calldata.length
```

You can examine and see that `data` points to `0x60` which is the zero slot in memory, and the next slot after is `add(data, 32)` which is the slot at `0x80` holding the length of the call data `abi-encoding` which is `0x44` (4 bytes for the selector and 0x40 for the two arguments, which is 68 in decimal representation). So even though `data` is empty, we try to read from out-of-bound memory. Aka checking that `data.length` might be 0 is missing.

## Recommendations
1. If `data.length` is 0, do not read out of bound memory and just set `output` to 0.
2. Contracts like `vic` in general can return more data than expected. But if a strict check is required, one can check that `data.length` is exactly 32 bytes and if not set `output` to 0.
3. EVM does not have the semantics for the types defined by Solidity (`bool`, `bytes32`, ...) only `uint256` B256. So it is up to the caller, in this case the VaultV2, to interpret the returned values correctly. So as long as `vic` returns at least 32 bytes of return data, one can decode that as the output.

## Morpho
Because of the try-catch gas bug, we decided that it was better if the VIC was handled as a trusted component for the liveness.

## Spearbit
Verified in the recent commit `4bba94`, changes were made enabling the VIC to revert.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho Vaults v2 |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Om Parikh, Jonatas Martins, Emmanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-Spearbit-Security-Review-May-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-Spearbit-Security-Review-May-2025.pdf

### Keywords for Search

`vulnerability`

