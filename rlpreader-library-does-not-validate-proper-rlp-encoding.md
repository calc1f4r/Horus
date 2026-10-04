---
# Core Classification
protocol: Succinct Labs Telepathy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21292
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
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
finders_count: 3
finders:
  - Joe Doyle
  - Marc Ilunga
  - Tjaden Hess
---

## Vulnerability Title

RLPReader library does not validate proper RLP encoding

### Overview

See description below for full details.

### Original Finding Content

## Error Reporting

**Difficulty:** Low  
**Type:** Error Reporting  
**Target:** contracts/lib/Solidity-RLP/RLPReader.sol  

## Description

The TargetAMB uses the external RLPReader dependency to parse RLP-encoded nodes in the Ethereum state trie, including those provided by the user as part of a Merkle proof. When parsing a byte string as an `RLPItem`, the library does not check that the encoded payload length of the `RLPitem` matches the length of the underlying bytes.

```solidity
/*
* @param item RLP encoded bytes
*/
function toRlpItem (bytes memory item) internal pure returns (RLPItem memory) {
    uint256 memPtr;
    assembly {
        memPtr := add(item, 0x20)
    }
    return RLPItem(item.length, memPtr);
}
```

*Figure 11.1: Solidity-RLP/contracts/RLPReader.sol#51–61*

If the encoded byte length of the `RLPitem` is too long or too short, future operations on the `RLPItem` may access memory before or after the bounds of the underlying buffer. More generally, because the Merkle trie verifier assumes that all input is in the form of valid RLP-encoded data, it is important to check that potentially malicious data is properly encoded.

While we did not identify any way to convert improperly encoded proof data into a proof forgery, it is simple to give an example of an out-of-bounds read that could possibly lead in other contexts to unexpected behavior. In figure 11.2, the result of `items[0].toBytes()` contains many bytes read from memory beyond the bounds allocated in the initial byte string.

```solidity
RLPReader.RLPItem memory item = RLPReader.toRlpItem('\xc3\xd0');
RLPReader.RLPItem[] memory items = item.toList();
assert(items[0].toBytes().length == 16);
```

*Figure 11.2: Out-of-bounds read due to invalid RLP encoding*

In this example, `RLPReader.toRLPItem` should revert because the encoded length of three bytes is longer than the payload length of the string; similarly, the call to `toList()` should fail because the nested `RLPItem` encodes a length of 16, again more than the underlying buffer.

To prevent such ill-constructed nested `RLPItem`s, the internal `numItems` function should revert if `currPtr` is not exactly equal to `endPtr` at the end of the loop shown in figure 11.3.

```solidity
// @return number of payload items inside an encoded list.
function numItems (RLPItem memory item) private pure returns (uint256) {
    if (item.len == 0) return 0;
    uint256 count = 0;
    uint256 currPtr = item.memPtr + _payloadOffset(item.memPtr);
    uint256 endPtr = item.memPtr + item.len;
    while (currPtr < endPtr) {
        currPtr = currPtr + _itemLength(currPtr);  // skip over an item
        count++;
    }
    return count;
}
```

*Figure 11.3: Solidity-RLP/contracts/RLPReader.sol#256–269*

## Recommendations

**Short term:** Add a check in `RLPReader.toRLPItem` that validates that the length of the argument exactly matches the expected length of prefix + payload based on the encoded prefix. Similarly, add a check in `RLPReader.numItems`, checking that the sum of the encoded lengths of sub-objects matches the total length of the RLP list.

**Long term:** Treat any length values or pointers in untrusted data as potentially malicious and carefully check that they are within the expected bounds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Succinct Labs Telepathy |
| Report Date | N/A |
| Finders | Joe Doyle, Marc Ilunga, Tjaden Hess |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf

### Keywords for Search

`vulnerability`

