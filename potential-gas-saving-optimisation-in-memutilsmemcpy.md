---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19488
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
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

Potential Gas Saving Optimisation in Memutils.memcpy

### Overview

See description below for full details.

### Original Finding Content

## Description

The `Memutils.memcpy()` function uses a gas-expensive `EXP` operation, which can be easily replaced by using the much cheaper `SHL`. 

The current `memcpy` implementation has the following line:

```
let mask := sub ( exp (256 , sub (32 , _len )), 1) // 2 ** (8 * (32 - _len )) - 1
```

Which can be replaced as follows:

```
let mask := sub ( shl (1 , mul (8 , sub (32 , _len ))), 1) // 2 ** (8 * (32 - _len )) - 1
```

`MUL` and `SHL` cost 5 and 3 gas respectively, while `EXP` is at least 10 gas.

While `SHL` was introduced more recently in the Constantinople hard fork, the current contracts are compiled for the Constantinople EVM. Because these operations are written in inline assembly, the Solidity compiler will not perform any optimizations.

## Recommendations

Consider modifying `Memutils.sol:36`, as described above, including relevant tests to confirm equivalent functionality.

## Resolution

This issue was tracked in Issue #242 and resolved in PR #239.  
Refer to: [EIP-145](https://eips.ethereum.org/EIPS/eip-145), [EIP-160](https://eips.ethereum.org/EIPS/eip-160)

---

## LID-17 Miscellaneous Observations on Lido-DAO Codebase

**Asset:** lidofinance/lido-dao  
**Status:** Closed: See Resolution  
**Rating:** Informational  

## Description

This section details miscellaneous findings discovered by the testing team on the codebase associated with the Lido-DAO contracts that do not have direct security implications:

1. The `stETH.burn()` and `StETH.burnShares()` methods are unused. Although protected by `BURN_ROLE`, there is no reason for this method to exist until stETH withdrawal is possible.
2. We recommend avoiding the use of pre and post-increment operators (`++`) within other expressions, such that the pre vs post-increment results in different outcomes. Although they make the code concise, this can be more difficult to understand or easily missed by less familiar readers. e.g., Lido.sol:518,776 LidoOracle.sol:311
3. Note that the `Lido.stop()` function is shadowed in inline assembly by the `stop()` instruction. This would, however, only be an issue if some inline assembly tried to call the function.
4. Gas savings in `NodeOperatorRegistry.assignNextSigningKeys()`: The loop at line [336] iterates through the entire cache when it could break when `numLoadedKeys == numAssignedKeys`. This is likely a very minimal improvement though, when considering all the looping earlier in the function.
5. In the `getBit()` and `setBit()` functions defined in `BitOps.sol`, consider asserting (using a require statement) that the parameter `_bitIndex < 256`, or pass it as a `uint8`.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The comments have been understood and acknowledged by the Lido team, with fixes implemented where deemed useful/relevant. In particular, items 4 and 5 were fixed in PR #239. The Lido team also made a note regarding item 1, clarifying that `StETH.burn()` will be used prior to withdrawal as part of the insurance fund implementation.

---

## LID-18 Miscellaneous Observations on DC4BC Codebase

**Asset:** dc4bc  
**Status:** Closed: See Resolution  
**Rating:** Informational  

## Description

This section details miscellaneous findings discovered by the testing team on the dc4bc codebase that do not have direct security implications:

- In `airgapped/encryption.go`, key derivation is performed in every call to encrypt and decrypt, rather than just after reading the password from stdin (in `SetEncryptionKey` roughly every 10 min). This offers no meaningful security improvements compared to saving the derived key in memory. By deriving the encryption key only once every 10 min, a much stronger parameterization is possible.
- `client/http_server.go:263` sets content type to "image/jpeg" but should be "image/png".

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The comments have been understood and acknowledged by the Lido team, with some relevant fixes implemented in PR #74.  
Refer to: [https://godoc.org/github.com/skip2/go-qrcode#Encode](https://godoc.org/github.com/skip2/go-qrcode#Encode)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf

### Keywords for Search

`vulnerability`

