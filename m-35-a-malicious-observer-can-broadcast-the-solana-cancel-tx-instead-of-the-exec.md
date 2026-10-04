---
# Core Classification
protocol: ZetaChain Cross-Chain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58670
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/857
source_link: none
github_link: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/372

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
  - Al-Qa-qa
  - g
  - Laksmana
---

## Vulnerability Title

M-35: A Malicious Observer can broadcast the Solana cancel tx instead of the execute tx

### Overview


The bug report discusses an issue with the Solana Observers in the Zetachain Cross-Chain protocol. The Observers are responsible for signing instructions for executing transactions, but a malicious Observer can manipulate the process and prevent transactions from being executed. This can be done by broadcasting an increment nonce transaction instead of the intended execute transaction. This can be repeated multiple times, causing a significant impact on the protocol. The bug has been fixed by the protocol team in the latest PRs/commits.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/372 

## Found by 
Al-Qa-qa, Laksmana, g

### Summary

Solana Observers will [sign](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/node/zetaclient/chains/solana/signer/signer.go#L450-L455) both the execute and increment nonce instructions when preparing an execute SPL transaction. Since all Observers will sign both instructions, a malicious Observer can broadcast the fallback transaction (increment nonce) instead of the execute transaction. A single Observer can prevent Solana `execute` instructions indefinitely. 

### Root Cause

When preparing the `execute` or `execute SPL` transactions, all the observers TSS-sign both the execute and increment nonce instructions. Since the TSS signature for the increment nonce transaction is available, a malicious Observer can use this to broadcast the increment nonce transaction instead of the execute transaction.

```golang
// in `prepareExecuteTx()` and `prepareExecuteSPLTx()`

tx, err := signer.signTx(ctx, inst, params.CallOptions.GasLimit)
// ... snip ...

fallbackTx, err := signer.signTx(ctx, fallbackInst, 0)
```

### Internal Pre-conditions

None

### External Pre-conditions

None

### Attack Path

1. A malicious Observer modifies their Solana Observer code to broadcast the increment nonce transaction instead of the execute transaction.
2. Once an [`execute`](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/node/zetaclient/chains/solana/signer/signer.go#L165-L173) outbound is processed, the malicious Observer can broadcast the increment nonce without [delay](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/node/zetaclient/chains/solana/signer/signer.go#L298), so they can be the first to broadcast and consume the nonce.
3. The nonce will be incremented, and the execute Outbound is effectively cancelled. 
4. This attack can be done repeatedly to prevent most execute Outbounds from getting broadcasted.

### Impact

A single Observer can prevent Solana `execute` Outbounds indefinitely. 

### PoC

_No response_

### Mitigation

_No response_

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/zeta-chain/node/pull/3914






### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | ZetaChain Cross-Chain |
| Report Date | N/A |
| Finders | Al-Qa-qa, g, Laksmana |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/372
- **Contest**: https://app.sherlock.xyz/audits/contests/857

### Keywords for Search

`vulnerability`

