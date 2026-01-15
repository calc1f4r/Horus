---
# Core Classification
protocol: Pyth
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48548
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/pyth-crosschain/tree/main/aptos

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
  - Harrison Green
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Pyth Deployment DOS

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Analysis

## Issue Overview

Similar to the issue we found in Wormhole, during the initialization of the `pyth` module, it attempts to register an `AptosCoin` account in order to be able to receive fees:

```rust
sources/pyth.move

module pyth::pyth {
    ...
    fun init_internal(...) {
        ...
        coin::register<AptosCoin>(&wormhole);
    }
    ...
}
```

However, `coin::register` is a one-time operation. If `coin::register` has previously been called on this address, this initialization code will abort, and the wormhole program will be unable to initialize.

While it is usually not possible to register coins for users you cannot sign for, the Aptos framework provides a special mechanism to register `AptosCoin` for any user via `aptos_account::create_account`:

```rust
aptos_account.move

public entry fun create_account(auth_key: address) {
    let signer = account::create_account(auth_key);
    coin::register<AptosCoin>(&signer);
}
```

Therefore, with this mechanism, an attacker could register `AptosCoin` for the wormhole program before deployment in order to prevent it from properly initializing.

## Remediation

Check if `AptosCoin` has been registered and conditionally invoke `coin::register` only if it hasn’t been registered.

## Patch

Resolved in commit `124589d`.

© 2022 OtterSec LLC. All Rights Reserved. 6 / 16

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth |
| Report Date | N/A |
| Finders | Harrison Green, Robert Chen, OtterSec |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/pyth-crosschain/tree/main/aptos
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

