---
# Core Classification
protocol: Brink
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7274
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Brink-Spearbit-Security-Review-Engagement-1.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Brink-Spearbit-Security-Review-Engagement-1.pdf
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

protocol_categories:
  - dexes
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

The storage slots corresponding to _implementation and_owner could be accidentally overwritten

### Overview


This bug report is about a high risk issue related to ProxyStorage.sol. The problem is that the first two state variables declared in a verifier will overlap with the _implementation and _owner variables, which could result in funds being stolen or made inaccessible. 

To address the issue, three recommendations were made. The first was to store the variables at a quasi-random memory location determined by a Keccak-256 hash. The second was to let the verifiers inherit from ProxyStorage.sol so that the variables _implementation and _owner are mapped in storage and will not be overwritten accidentally. The third was to store the _implementation and the _owner as constants or immutable.

The bug was eventually fixed by using a Minimal Proxy with the owner address appended at the end of the deployed bytecode. This was followed up with a review to confirm that the issue was resolved.

### Original Finding Content

## Severity: High Risk

## Context
`ProxyStorage.sol#L7-L10`

```solidity
contract ProxyStorage {
    address internal _implementation;
    address internal _owner;
}
```

The state variables `_implementation` and `_owner` are at slots 0 and 1. The protocol architecture relies on executors calling `metaDelegateCall` to verifier contracts. Therefore, the storage slots are shared with the storage space of the verifiers.

## Risk
The first 2 state variables declared in a verifier will overlap with `_implementation` and `_owner`. Accidentally changing these variables will result in changing the implementation and changing the owner. Funds could be stolen or made inaccessible (accidentally or on purpose).

## Recommendations
1. Store the variables at a quasi-random memory location determined by a Keccak-256 hash. This pattern is used in `Bit.sol#L33`.
2. Let the verifiers inherit from `ProxyStorage.sol` so that the variables `_implementation` and `_owner` are mapped in storage and will not be overwritten accidentally. It is recommended to check the storage layout using `solc --storage-layout` or the equivalent standard-json flag to verify that this is indeed the case; we recommend building a small tool for doing this.
3. Store the `_implementation` and the `_owner` as constants or immutable. This allows for a smaller proxy that saves gas. However, this requires some architectural changes.

## Brink
We chose to fix, but took a slightly different approach than any of the recommended fixes. Our fix is closest to recommendation 3. While recommendations 1 and 2 would have been simpler to implement, and may prevent an accidental overwrite of the `_implementation` and `_owner` values, fixing in this way would not prevent an attacker from overwriting these values by tricking an account owner into signing permissions for the overwrite.

We wanted to make the values fully immutable after Proxy deployment. We updated `Proxy.sol` to include two constants: `ACCOUNT_IMPLEMENTATION`, which is the deterministic address for the `Account.sol` deployment and will be consistent across all chains, and `OWNER`, which is set as a placeholder address `0xfe-feFEFeFEFEFEFEFeFefefefefeFEfEfefefEfe`. 

We created `AccountFactory.sol` which dynamically creates Proxy init code, inserting the actual owner address at the same location as the `OWNER` placeholder. When Proxy makes a delegatecall to `Account`, the value of `OWNER` is read using `extcodecopy` (`ProxyGettable.sol`). Constant and immutable storage read from a contract executed via delegate will be read from the implementation contract (`Account.sol`), not the calling contract (`Proxy`). Using `extcodecopy` lets us read a constant value from the Proxy deployed bytecode.

**Note:** In order for us to compile `Proxy.sol` with the `OWNER` placeholder included in the deployed bytecode, we had to include a reference to it in the contract (outside of the constructor). We found `Proxy.sol#L40` to be the most gas-efficient way to accomplish this. We believe it has no security impact on the Proxy and only increases the gas for incoming ETH transfers by a negligible amount.

## Brink Update
We updated to use Minimal Proxy with the owner address appended at the end of the deployed bytecode commit `0ed725b`.

## Spearbit
We welcome this change and performed a follow-up review focused on the modification on the Minimal Proxy contract. Overall, we agree that the issues are resolved. Detailed comments can be found in the follow-up report.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Brink |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Brink-Spearbit-Security-Review-Engagement-1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Brink-Spearbit-Security-Review-Engagement-1.pdf

### Keywords for Search

`vulnerability`

