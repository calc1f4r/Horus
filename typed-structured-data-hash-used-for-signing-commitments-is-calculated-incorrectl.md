---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: type_casting

# Attack Vector Details
attack_type: type_casting
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7291
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - type_casting

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

Typed structured data hash used for signing commitments is calculated incorrectly

### Overview


This bug report concerns the VaultImplementation.sol and IVaultImplementation.sol files. It has been identified that the STRATEGY_TYPEHASH is incorrect according to EIP-712. This is due to the fact that the s.strategistNonce type is a uint32, but the type used in the type hash is a uint256. Additionally, the struct name used in the type hash collides with the StrategyDetails struct name which is defined as a uint8 version, uint256 deadline, and an address vault. 

The recommendation is to update the STRATEGY_TYPEHASH to reflect the correct type uint32 for thenonce. It is also suggested to keep the STRATEGY_TYPEHASH using the non-inlined version and to avoid name collision for the two structs, one should be renamed.

### Original Finding Content

## Severity: High Risk

## Context
- `VaultImplementation.sol#L150-L151`
- `VaultImplementation.sol#L172-L176`
- `IVaultImplementation.sol#L41`

## Description
Since  
`STRATEGY_TYPEHASH == keccak256("StrategyDetails(uint256 nonce,uint256 deadline,bytes32 root)")`  
The hash calculated in `_encodeStrategyData` is incorrect according to EIP-712. `s.strategistNonce` is of type `uint32` and the nonce type used in the type hash is `uint256`.

Also, the struct name used in the typehash collides with the `StrategyDetails` struct name defined as:
```solidity
struct StrategyDetails {
    uint8 version;
    uint256 deadline;
    address vault;
}
```

## Recommendation
We suggest the following:
1. Update the `STRATEGY_TYPEHASH` to reflect the correct type `uint32` for the nonce.
2. Keep the `STRATEGY_TYPEHASH` using the non-inlined version below since the compiler would inline the value off-chain:
   ```solidity
   bytes32 public constant STRATEGY_TYPEHASH = keccak256("StrategyDetails(uint32 nonce,uint256 deadline,bytes32 root)");
   ```
3. To avoid name collision for the two structs, rename one of the `StrategyDetails` (even though one is not defined directly).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Type casting`

