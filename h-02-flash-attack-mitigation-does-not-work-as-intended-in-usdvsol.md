---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3905
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/138

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

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-02] Flash attack mitigation does not work as intended in USDV.sol

### Overview


This bug report is about a vulnerability in the USDV contract which is part of the Vader Protocol. The issue is that the blockDelay state variable is not initialized, which means it has a default uint value of 0. This allows multiple calls on the contract to be executed in the same transaction of a block, which enables flash attacks. The proof of concept can be found in the provided links. The recommended mitigation step is to initialize blockDelay to a value greater than or equal to 1 at declaration or in the constructor.

### Original Finding Content


One of the stated protocol (review) goals is to detect susceptibility to “Any attack vectors using flash loans on Anchor price, synths or lending.” As such, USDV contract aims to protect against flash attacks using `flashProof()` modifier which uses the following check in `isMature()` to determine if currently executing contract context is at least `blockDelay` duration ahead of the previous context: ```lastBlock[tx.origin] + blockDelay <= block.number```

However, `blockDelay` state variable is not initialized which means it has a default uint value of 0. So unless it is set to >= 1 by `setParams()` which can be called only by the DAO (which currently does not have the capability to call `setParams()` function), `blockDelay` will be 0, which allows current executing context (`block.number`) to be the same as the previous one (`lastBlock[tx.origin]`). This effectively allows multiple calls on this contract to be executed in the same transaction of a block which enables flash attacks as opposed to what is expected as commented on [L41](https://github.com/code-423n4/2021-04-vader/blob/3041f20c920821b89d01f652867d5207d18c8703/vader-protocol/contracts/USDV.sol#L140-L142): "// Stops an EOA from doing a flash attack in the same block"

Even if the DAO can call `setParams()` to change `blockDelay` to >= 1, there is a big window of opportunity for flash attacks until the DAO votes, finalizes and approves such a proposal. Moreover, such proposals can be cancelled by a DAO minority or replaced by a malicious DAO minority to launch flash attacks.

Recommend initalizing `blockDelay` to >= 1 at declaration or in constructor.

**[strictly-scarce (vader) confirmed](https://github.com/code-423n4/2021-04-vader-findings/issues/138#issuecomment-830606188):**

> The actual issue is simply:

> > `blockDelay` state variable is not initialized
>
> It is intended to be initialised to 1, so this is a bug. Severity: 2



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/138
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

