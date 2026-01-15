---
# Core Classification
protocol: Wormhole Evm Cctp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31359
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
github_link: none

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
  - Hans
  - 0kage
  - Giovanni Di Siena
---

## Vulnerability Title

Redemptions are blocked when L2 sequencers are down

### Overview


The report describes a bug in a code that prevents the execution of valid transactions on a specific chain when a sequencer is down. This can have a high impact on cross-chain transfers, such as urgent liquidity infusion. The bug can be mitigated by validating the sender's address against the "mintRecipient" alias. The Wormhole Foundation, responsible for the code, does not consider this aliasing, but another party has acknowledged the issue.

### Original Finding Content

**Description:** Given that rollups such as [Optimism](https://docs.optimism.io/chain/differences#address-aliasing) and [Arbitrum](https://docs.arbitrum.io/arbos/l1-to-l2-messaging#address-aliasing) offer methods for forced transaction inclusion, it is important that the aliased sender address is also [checked](https://solodit.xyz/issues/m-8-operator-is-blocked-when-sequencer-is-down-on-arbitrum-sherlock-none-index-git) within [`Logic::redeemTokensWithPayload`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/CircleIntegration/Logic.sol#L88-L91) when verifying the sender is the specified `mintRecipient` to allow for maximum uptime in the event of sequencer downtime.

```solidity
// Confirm that the caller is the `mintRecipient` to ensure atomic execution.
require(
    msg.sender.toUniversalAddress() == deposit.mintRecipient, "caller must be mintRecipient"
);
```

**Impact:** Failure to consider the aliased `mintRecipient` address prevents the execution of valid VAAs on a target CCTP domain where transactions are batched by a centralized L2 sequencer. Since this VAA could carry a time-sensitive payload, such as the urgent cross-chain liquidity infusion to a protocol, this issue has the potential to have a high impact with reasonable likelihood.

**Proof of Concept:**
1. Protocol X attempts to transfer 10,000 USDC from CCTP Domain A to CCTP Domain B.
2. CCTP Domain B is an L2 rollup that batches transactions for publishing onto the L1 chain via a centralized sequencer.
3. The L2 sequencer goes down; however, transactions can still be executed via forced inclusion on the L1 chain.
4. Protocol X implements the relevant functionality and attempts to redeem 10,000 USDC via forced inclusion.
5. The Wormhole CCTP integration does not consider the contract's aliased address when validating the `mintRecipient`, so the redemption fails.
6. Cross-chain transfer of this liquidity will remain blocked so long as the sequencer is down.

**Recommended Mitigation:** Validation of the sender address against the `mintRecipient` should also consider the aliased `mintRecipient` address to allow for maximum uptime when [`Logic::redeemTokensWithPayload`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/CircleIntegration/Logic.sol#L88-L91) is called via forced inclusion.

**Wormhole Foundation:** Since CCTP [doesn’t deal with this aliasing](https://github.com/circlefin/evm-cctp-contracts/blob/adb2a382b09ea574f4d18d8af5b6706e8ed9b8f2/src/MessageTransmitter.sol#L270-L277), we don’t feel strongly that we should either.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Wormhole Evm Cctp |
| Report Date | N/A |
| Finders | Hans, 0kage, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

