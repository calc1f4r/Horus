---
# Core Classification
protocol: Wormhole Evm Ntt
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31374
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
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
finders_count: 3
finders:
  - Hans
  - 0kage
  - Giovanni Di Siena
---

## Vulnerability Title

Silent overflow in `TrimmedAmount::shift` could result in rate limiter being bypassed

### Overview


This bug report discusses a potential issue in the `TrimmedAmount` code, specifically in the `shift` function. This function does not have a check to ensure that the scaled amount does not exceed the maximum `uint64` value, which could result in a silent overflow. This could potentially bypass the rate limiter and has been classified as a medium severity finding. The recommended solution is to add an explicit check to prevent this issue. The Wormhole Foundation has already fixed this issue in their code and it has been verified by Cyfrin.

### Original Finding Content

**Description:** Within [`TrimmedAmount::trim`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/libraries/TrimmedAmount.sol#L136-L158), there is an explicit check that ensures the scaled amount does not exceed the maximum `uint64`:
```solidity
// NOTE: amt after trimming must fit into uint64 (that's the point of
// trimming, as Solana only supports uint64 for token amts)
if (amountScaled > type(uint64).max) {
    revert AmountTooLarge(amt);
}
```
However, no such check exists within [`TrimmedAmount::shift`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/libraries/TrimmedAmount.sol#L121-L129) which means there is potential for silent overflow when casting to `uint64` here:
```solidity
function shift(
    TrimmedAmount memory amount,
    uint8 toDecimals
) internal pure returns (TrimmedAmount memory) {
    uint8 actualToDecimals = minUint8(TRIMMED_DECIMALS, toDecimals);
    return TrimmedAmount(
        uint64(scale(amount.amount, amount.decimals, actualToDecimals)), actualToDecimals
    );
}
```

**Impact:** A silent overflow in `TrimmedAmount::shift` could result in the rate limiter being bypassed, considering its usage in [`NttManager::_transferEntryPoint`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/NttManager.sol#L300). Given the high impact and reasonable likelihood of this issue occurring, it is classified a **MEDIUM** severity finding.

**Recommended Mitigation:** Explicitly check the scaled amount in `TrimmedAmount::shift` does not exceed the maximum `uint64`.

**Wormhole Foundation:** Fixed in [PR \#262](https://github.com/wormhole-foundation/example-native-token-transfers/pull/262).

**Cyfrin:** Verified. OpenZeppelin `SafeCast` library is now used when casting to `uint64`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Wormhole Evm Ntt |
| Report Date | N/A |
| Finders | Hans, 0kage, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

