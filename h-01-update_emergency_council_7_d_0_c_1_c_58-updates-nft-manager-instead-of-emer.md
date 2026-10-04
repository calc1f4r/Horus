---
# Core Classification
protocol: Superposition
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41512
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-superposition
source_link: https://code4rena.com/reports/2024-08-superposition
github_link: https://github.com/code-423n4/2024-08-superposition-findings/issues/162

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - d4r3d3v1l
  - ZanyBonzy
  - Nikki
  - oakcobalt
  - zhaojohnson
---

## Vulnerability Title

[H-01] `update_emergency_council_7_D_0_C_1_C_58()` updates nft manager instead of emergency council

### Overview


The bug report is about a function called `update_emergency_council_7_D_0_C_1_C_58()` in the `lib.rs` file that is supposed to update the emergency council. However, it is currently updating another contract called `nft_manager`. This is a problem because the `emergency_council` is needed to handle emergency situations, but the function is not updating it correctly. The recommended solution is to change the function to update the `emergency_council` instead. The severity of this bug is considered high because it could have significant consequences for the system.

### Original Finding Content


Inside of `lib.rs`, there is a function `update_emergency_council_7_D_0_C_1_C_58()` that is needed to update the emergency council that can disable the pools. However, in the current implementation, `nft_manager` is updated instead.

### Proof of Concept

This is the current functionality of `update_emergency_council_7_D_0_C_1_C_58()`:

<https://github.com/code-423n4/2024-08-superposition/blob/main/pkg/seawater/src/lib.rs#L1111-1124>

```
    pub fn update_emergency_council_7_D_0_C_1_C_58(
            &mut self,
            manager: Address,
        ) -> Result<(), Revert> {
            assert_eq_or!(
                msg::sender(),
                self.seawater_admin.get(),
                Error::SeawaterAdminOnly
            );

            self.nft_manager.set(manager);

            Ok(())
        }
```

As you can see, the function updates `nft_manager` contract instead of `emergency_council` that is needed to be updated. Above this function there is another function that updates `nft_manager`:

<https://github.com/code-423n4/2024-08-superposition/blob/main/pkg/seawater/src/lib.rs#L1097-1107>

```
  pub fn update_nft_manager_9_B_D_F_41_F_6(&mut self, manager: Address) -> Result<(), Revert> {
        assert_eq_or!(
            msg::sender(),
            self.seawater_admin.get(),
            Error::SeawaterAdminOnly
        );

        self.nft_manager.set(manager);

        Ok(())
    }
```

As you can see here, in both of the functions `nft_manager` is updated which is an unexpected behavior and the contract cannot update the `emergency_council` that handles emergency situations:

<https://github.com/code-423n4/2024-08-superposition/blob/main/pkg/seawater/src/lib.rs#L117-118>

```
     // address that's able to activate and disable emergency mode functionality
        emergency_council: StorageAddress,
```

### Recommended Mitigation Steps

Change `update_emergency_council_7_D_0_C_1_C_58()` to update `emergency_council`.

**[af-afk (Superposition) confirmed via duplicate issue #64](https://github.com/code-423n4/2024-08-superposition-findings/issues/64#event-14265172686)** 

**[0xsomeone (judge) commented](https://github.com/code-423n4/2024-08-superposition-findings/issues/162#issuecomment-2369609895):**
 > The Warden and its duplicates have correctly identified that the mechanism exposed for updating the `emergency_council` will incorrectly update the `nft_manager` instead. 
> 
> I initially wished to retain a medium risk severity rating for this vulnerability due to how the `emergency_council` is configured during the contract's initialization and its value changing being considered a rare event; however, a different highly sensitive variable is altered instead incorrectly (`nft_manager`) which would have significant consequences to the system temporarily.
> 
> Based on the above, I believe that a high-risk rating is appropriate due to the unexpected effects invocation of the function would result in.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Superposition |
| Report Date | N/A |
| Finders | d4r3d3v1l, ZanyBonzy, Nikki, oakcobalt, zhaojohnson, eta, nslavchev, ABAIKUNANBAEV, wasm\_it, Testerbot, shaflow2, DadeKuma, prapandey031, Rhaydden, Q7 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-superposition
- **GitHub**: https://github.com/code-423n4/2024-08-superposition-findings/issues/162
- **Contest**: https://code4rena.com/reports/2024-08-superposition

### Keywords for Search

`vulnerability`

