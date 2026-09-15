---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: overflow/underflow

# Attack Vector Details
attack_type: overflow/underflow
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7310
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - overflow/underflow

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

unchecked may cause under/overflows

### Overview


This bug report is about unchecked code in the LienToken.sol, PublicVault.sol, VaultImplementation.sol, and WithdrawProxy.sol files. Unchecked code should only be used when there is certainty that it will not cause underflows or overflows. In this report, a potential underflow is described in the _handleProtocolFee() block due to an error in setting the protocolFeeNumerator. It is recommended to reason about each unchecked code and remove them if there is not absolute certainty that it is safe to use. The Astaria and Spearbit teams have acknowledged the bug and will put checks in place to prevent unintended boundaries from being crossed.

### Original Finding Content

## Severity: Medium Risk

## Context
- `LienToken.sol#L424`
- `LienToken.sol#L482`
- `PublicVault.sol#L376`
- `PublicVault.sol#L422`
- `PublicVault.sol#L439`
- `PublicVault.sol#L490`
- `PublicVault.sol#L578`
- `PublicVault.sol#L611`
- `PublicVault.sol#L527`
- `PublicVault.sol#L544`
- `PublicVault.sol#L563`
- `PublicVault.sol#L640`
- `VaultImplementation.sol#L401`
- `WithdrawProxy.sol#L254`
- `WithdrawProxy.sol#L293`

## Description
Unchecked should only be used when there is a guarantee of no underflows or overflows, or when they are taken into account. In the absence of certainty, it's better to avoid unchecked to favor correctness over gas efficiency.

For instance, if by error, `protocolFeeNumerator` is set to be greater than `protocolFeeDenominator`, this block in `_handleProtocolFee()` will underflow:

```solidity
unchecked {
    amount -= fee;
}
```

However, later this reverts due to the ERC20 transfer of an unusually high amount. This is just to demonstrate that unknown bugs can lead to under/overflows.

## Recommendation
Reason about each unchecked and remove them in absence of absolute certainty of safety.

## Astaria
Acknowledged. We'll put checks on setting protocol values to not cross unintended boundaries.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

`Overflow/Underflow`

