---
# Core Classification
protocol: Optimism
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36607
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-optimism
source_link: https://code4rena.com/reports/2024-07-optimism
github_link: https://github.com/code-423n4/2024-07-optimism-findings/issues/54

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - n4nika
  - Femboys
  - Zubat
---

## Vulnerability Title

[M-05] Panic in MIPS VM could lead to unchallengeable L2 output root claim

### Overview


This bug report discusses an issue with the execution bisection game system in the code-423n4/2024-07-optimism repository. The bug allows for the possibility of a malicious actor to hijack the state of the L2 output root, making it unrecoverable. The bug is caused by the current configuration setting the `SPLIT_DEPTH` to 30, which allows for the root claim at depth 0 to be denied in any dispute. The report recommends setting the `split_depth` to an odd number as a mitigation step. The assessed type of this bug is DoS (denial of service). Inphi (Optimism) has confirmed and commented on the bug, acknowledging that it is valid and that there are other problems introduced by adjusting the split depth to fix it. They suggest implementing a multi-proof architecture to mitigate against a single faulty program taking down the system. 

### Original Finding Content


<https://github.com/code-423n4/2024-07-optimism/blob/70556044e5e080930f686c4e5acde420104bb2c4/packages/contracts-bedrock/src/dispute/FaultDisputeGame.sol#L883-L895>

### Impact

Suppose we have a situation where the MIPS geth goes wrong and always panics. The vmStatus can only be either `UNFINISHED` or `PANIC`.

In the current execution bisection game system, the `UNFINISHED` state can not be used as the root claim; the `PANIC` state can always be attacked. So we can counter every bisection game at `SPLIT_DEPTH + 1`; none of the claims at `SPLIT_DEPTH` are challenged. Inductively, claims agreeing with `SPLIT_DEPTH` are not challengable.

In the current configuration, `SPLIT_DEPTH` is set to 30, so we can deny any dispute against the root claim at depth 0. If that were to happen, the state of the L2 output root could be hijacked and unrecoverable.

It's unclear if there are easy methods to trigger panic in the MIPS VM.

One possible way is to leverage the privilege, as the batcher is currently controlled by a centralized trusted entity. Ordinary users cannot construct the batches and channels for the rollup, but the batcher can freely set the payload blob to L1.

<https://github.com/code-423n4/2024-07-optimism/blob/main/op-node/rollup/derive/channel.go#L169-L205>

A malicious batcher could compress a huge amount of zero blobs, upload them to L1, and force the MIPS VM to decompress them. Considering the limited memory resources of the MIPS VM and the absence of garbage collection in the MIPS go-ethereum, the VM could be very easily corrupted.

### Recommended Mitigation Steps

Set the `split_depth` to an odd number.

### Assessed type

DoS

**[Inphi (Optimism) confirmed and commented](https://github.com/code-423n4/2024-07-optimism-findings/issues/54#issuecomment-2263227608):**
 > This is valid. Note that an implicit assumption of the `FaultDisputeGame` is that the program being verified must be not contain bugs or panic unexpectedly. But we have not documented this assumption clearly, so we would still like to acknowledge this report.
> 
> Also note that there are other problems introduced by adjusting the split depth to fix this. Really fixing this will require a multi-proof architecture, to mitigate against a single faulty program taking down the system, rather than tweaks to a dispute game.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Optimism |
| Report Date | N/A |
| Finders | n4nika, Femboys, Zubat |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-optimism
- **GitHub**: https://github.com/code-423n4/2024-07-optimism-findings/issues/54
- **Contest**: https://code4rena.com/reports/2024-07-optimism

### Keywords for Search

`vulnerability`

