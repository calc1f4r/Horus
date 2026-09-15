---
# Core Classification
protocol: Parallel Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18232
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
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
  - Artur Cygan Will Song Fredrik Dahlgren
---

## Vulnerability Title

Missing validation of referral code size

### Overview

See description below for full details.

### Original Finding Content

## Security Assessment Report

## Difficulty: High

## Type: Patching

## Target: 
`pallets/crowdloans/src/lib.rs`

## Description
The length of the referral code is not validated by the `contribute` extrinsic defined by the crowdloans pallet. Since the referral code is stored by the node, a malicious user could call `contribute` multiple times with a very large referral code. This would increase the memory pressure on the node, potentially leading to memory exhaustion.

```rust
fn do_contribute (
    who: &AccountIdOf<T>,
    crowdloan: ParaId,
    vault_id: VaultId,
    amount: BalanceOf<T>,
    referral_code: Vec<u8>,
) -> Result<(), DispatchError> {
    // ... <redacted>
    XcmRequests::<T>::insert(
        query_id,
        XcmRequest::Contribute {
            crowdloan,
            vault_id,
            who: who.clone(),
            amount,
            referral_code: referral_code.clone(),
        },
    );
    // ... <redacted>
    Ok(())
}
```

*Figure 10.1: pallets/crowdloans/src/lib.rs: 1429-1464*

## Exploit Scenario
A malicious user calls the `contribute` extrinsic multiple times with a very large referral code. This increases the memory pressure on the validator nodes and eventually causes all parachain nodes to run out of memory and crash.

## Recommendations
In the short term, add validation that limits the size of the referral code argument to the `contribute` extrinsic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Parallel Finance |
| Report Date | N/A |
| Finders | Artur Cygan Will Song Fredrik Dahlgren |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf

### Keywords for Search

`vulnerability`

