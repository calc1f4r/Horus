---
# Core Classification
protocol: Starknet Perpetual
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57701
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-03-starknet-perpetual
source_link: https://code4rena.com/reports/2025-03-starknet-perpetual
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-03] Owner Account Can Be Overwritten Due to Missing Validation

### Overview

See description below for full details.

### Original Finding Content


<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/components/positions/positions.cairo# L195>

<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/components/positions/positions.cairo# L228-L251>

The contract allows ownership assignment via two functions: `set_owner_account_request` and `set_owner_account`. While the former checks that `owner_account` is unset (`assert(position.get_owner_account().is_none())`), the latter **lacks this validation**.

As a result, multiple requests can be submitted and processed under specific conditions, potentially **overwriting a previously set owner**, violating the intended one-time assignment logic.

Requests are identified by a hash—not a public key—so altering the owner address and signature produces a new hash, enabling duplicate requests. Operators process requests sequentially, making double/triple submissions feasible.

This is critical because:

* Ownership should be immutable once set.
* `set_owner_account` does not enforce this constraint.

### Affected Code
```

  /// Sets the owner of a position to a new account owner.
        ///
        /// Validations:
        /// - The contract must not be paused.
        /// - The caller must be the operator.
        /// - The operator nonce must be valid.
        /// - The expiration time has not passed.
@here        /// - The position has no account owner.       // note not done
        /// - The signature is valid.
        fn set_owner_account(
            ref self: ComponentState<TContractState>,
            operator_nonce: u64,
            position_id: PositionId,
            new_owner_account: ContractAddress,
            expiration: Timestamp,
        ) {
            get_dep_component!(@self, Pausable).assert_not_paused();
            let mut operator_nonce_component = get_dep_component_mut!(ref self, OperatorNonce);
            operator_nonce_component.use_checked_nonce(:operator_nonce);
            validate_expiration(:expiration, err: SET_POSITION_OWNER_EXPIRED);                       // reset the registerapproval and return not revert. BUG? NOTE ...note possible failure becomes unsettable for life....... if i don deposit inside ko???
            let position = self.get_position_mut(:position_id);
            let public_key = position.get_owner_public_key();
            let mut request_approvals = get_dep_component_mut!(ref self, RequestApprovals);
            let hash = request_approvals
                .consume_approved_request(
                    args: SetOwnerAccountArgs {
                        position_id, public_key, new_owner_account, expiration,
                    },
                    :public_key,
                );
@here            position.owner_account.write(Option::Some(new_owner_account));
            self
                .emit(
                    events::SetOwnerAccount {
                        position_id, public_key, new_owner_account, set_owner_account_hash: hash,
                    },
                );
        }
```

In `set_owner_account_request`:
```

assert(position.get_owner_account().is_none(), POSITION_HAS_OWNER_ACCOUNT);
```

But in `set_owner_account`, the same check is **missing**:
```

// Missing:
// assert(position.get_owner_account().is_none(), POSITION_HAS_OWNER_ACCOUNT);
position.owner_account.write(Option::Some(new_owner_account));
```

Supporting logic shows requests are saved and validated using only their hash:
```

let request_hash = args.get_message_hash(:public_key);
// No check for pre-existing owner
```

### Recommendation

Add the following validation inside `set_owner_account`:
```

assert(position.get_owner_account().is_none(), POSITION_HAS_OWNER_ACCOUNT);
```

This ensures ownership is only set once, even if multiple valid requests exist.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Starknet Perpetual |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-03-starknet-perpetual
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-03-starknet-perpetual

### Keywords for Search

`vulnerability`

