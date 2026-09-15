---
# Core Classification
protocol: Tensor Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46762
audit_firm: OtterSec
contest_link: https://tensor.foundation/
source_link: https://tensor.foundation/
github_link: https://github.com/tensor-foundation

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Denial of Service Due to ATA Ownership Change

### Overview


This bug report discusses a potential issue with the WithdrawCollateral token account checks in WithdrawCollateralShared. This could result in a Denial of Service (DoS) attack if the maker (original creator of the lock) intentionally changes their Associated Token Account (ATA) ownership to prevent the taker (buyer) from claiming their collateral. A Proof of Concept is provided, along with a suggested remediation and patch.

### Original Finding Content

## Withdrawal Collateral Attack Risk

As a result of the `WithdrawCollateral` token account checks in `WithdrawCollateralShared` within `validate`, there is a possibility that a Denial of Service (DoS) attack may occur if the maker (the original creator of the lock) intentionally changes their Associated Token Account (ATA) ownership to prevent the taker (the buyer) from claiming their collateral.

## Code Snippet

```rust
// program/src/state.rs
pub fn validate(&mut self, collateral_type: CollateralType, to_maker: bool) -> Result<()> {
    [...]
    // If returning to maker: cannot
    if to_maker {
        require!(
            !order_state.collateral_returned,
            TLockError::CollateralAlreadyReturned
        );
    } else {
        require!(
            order_state.collateral_returned,
            TLockError::CollateralNotReturned
        );
    }
    
    if order_state.is_lock_closeable_by_anyone()? {
        // NB: anyone can permissionlessly return the collateral back to the maker.
    } else {
        require!(
            order_state.taker.unwrap() == self.signer.key(),
            TLockError::InvalidSigner
        );
    }
    [...]
    Ok(())
}
```

## Proof of Concept

1. The maker creates an NFT lock and deposits their NFT into the lock, which is held as collateral.
2. The taker buys the locked NFT from the maker, sending yield to the maker. As a result, the value of the NFT increases, which implies that the taker stands to benefit if they sell it.
3. The taker sells the NFT at a higher price. As a result, the price of the NFT drops, implying it is possible to buy back the NFT at a lower price.
4. The taker buys the NFT again at a lower price. Consequently, the NFT’s value drops drastically.
5. At this point, the maker changes the owner of their ATA (which holds the SOL collateral).
6. If the taker, now in possession of the NFT again, wishes to return the NFT to the maker and withdraw the SOL collateral, they will be unable to do so due to the change in the maker’s ATA ownership.

## Remediation

Create the ATA only if it does not already exist.

## Patch

Resolved in `d8df474`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tensor Foundation |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://tensor.foundation/
- **GitHub**: https://github.com/tensor-foundation
- **Contest**: https://tensor.foundation/

### Keywords for Search

`vulnerability`

