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
solodit_id: 58668
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/857
source_link: none
github_link: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/367

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
finders_count: 2
finders:
  - 0x73696d616f
  - g
---

## Vulnerability Title

M-33: TON Gateway withdrawals can be DOS'd with an invalid withdrawal recipient

### Overview


The bug report discusses an issue with the TON Gateway contract in the Zetachain cross-chain protocol. The problem is that there is only one way to increment the nonce (a unique identifier) in the contract, which can cause failures in withdrawals and prevent future withdrawals from being executed. This is because the nonce is only incremented in one specific function, and if that function fails, the nonce will not be updated. This can lead to a denial of service attack, where withdrawals to the TON Gateway contract are indefinitely blocked. The report includes a proposed solution and a discussion of how the issue was fixed in the protocol.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/367 

## Found by 
0x73696d616f, g

### Summary

Unlike in Gateway contracts in other chains, there is only one way to increment the nonce in the Ton Gateway contract. The nonce is only [incremented](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/protocol-contracts-ton/contracts/gateway.fc#L312) in `handle_withdrawal()`. 

Any failure in `handle_withdrawal` before the nonce is incremented and committed will [prevent withdrawals](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/protocol-contracts-ton/contracts/gateway.fc#L301) with higher nonces from getting executed. 

### Root Cause

There is no way to increment the nonce other than through [`handle_withdrawal()`](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/protocol-contracts-ton/contracts/gateway.fc#L312-L315).

```funC
    state::total_locked -= (amount + tx_fee);
    state::seqno += 1;

    mutate_state();
    commit();
```

### Internal Pre-conditions

None

### External Pre-conditions

None

### Attack Path

1. A user withdraws TON coins from Zetachain, triggering an Outbound Withdrawal to TON. The Outbound Withdrawal has a nonce of 5 and a receiver of `{workchain: 1, recipient_addr: 0xted}`.
2. An Observer executes the Outbound Withdrawal and it fails with a [wrong workchain error](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/protocol-contracts-ton/contracts/gateway.fc#L297). 
3. The nonce in the TON Gateway contract stays at nonce 5 because it does not get incremented and committed.
4. Outbound Withdrawals with nonce greater than 5 will fail because of [this check](https://github.com/sherlock-audit/2025-04-zetachain-cross-chain/blob/main/protocol-contracts-ton/contracts/gateway.fc#L301).

### Impact

Withdrawals to the TON Gateway contract are DOS'd indefinitely.

### PoC

_No response_

### Mitigation

Consider applying the same `increment_nonce` approach that is applied to the Solana Gateway contract.

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/zeta-chain/node/pull/3977


**gjaldon**

The issue is [fixed](https://github.com/zeta-chain/node/pull/3977/files\#diff-465c1d777ce2840091a6424b19070a06fd488910fe61ce099807a20a81bf3180R72-R93) by calling IncreaseSeqno in the Gateway when an invalid workchain is used.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | ZetaChain Cross-Chain |
| Report Date | N/A |
| Finders | 0x73696d616f, g |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/367
- **Contest**: https://app.sherlock.xyz/audits/contests/857

### Keywords for Search

`vulnerability`

