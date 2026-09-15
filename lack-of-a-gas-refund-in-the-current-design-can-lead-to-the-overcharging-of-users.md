---
# Core Classification
protocol: Wormhole Evm Ntt
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31380
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
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

Lack of a gas refund in the current design can lead to the overcharging of users and misaligned relayer incentives that can choke message execution

### Overview


This bug report discusses a problem with gas handling in a system called Wormhole. The current design allows for transceivers to either attest to a message or both attest and execute it. However, this leads to some issues. Firstly, senders are being overcharged on the source chain without any way to get a refund. Secondly, relayers can manipulate the system by skipping message execution, which benefits them financially. To fix this, the report recommends implementing a mechanism to refund excess gas to the recipient address on the target chain. This has been addressed in a recent update by the Wormhole Foundation. 

### Original Finding Content

**Description:** To understand gas handling, it is important to highlight a few key aspects of the current design:

1. On the target chain, Transceivers can either attest to a message or attest and execute a message. Transceivers up to the threshold attest to a message, while the Transceiver who will cause the threshold to be reached attests and executes a message.

2. Each transceiver quotes a gas estimate on the source chain. When quoting a price, no Transceiver knows if its peer on the target chain will simply attest to a message or both attest and execute a message. This means that every Transceiver quotes a gas estimate that assumes its peer will be executing a message.

Based on the two above facts, the following can be deduced:

1. If the threshold has not yet been reached, a sender is paying a delivery fee for every Transceiver, even ones that are attesting a message after it was already executed.
2. The sender is paying for a scenario where every Transceiver is responsible for executing a message on the target chain. In reality, only one transceiver will execute, and all others will attest.
3. If a relayer consistently calls a Transceiver before the threshold is reached, a relayer will earn more than is spent in terms of gas.
4. The above point incentivizes relayers to always be the ones to attest and not to execute. A clever relayer can simply query `messageAttestations` off-chain and skip a delivery if `messageAttestations == threshold - 1`, since a relayer spends less gas than what they charged on the source chain if they deliver before OR after a threshold is met.

**Impact:**
1. Users are overcharged on the source chain without recourse due to the lack of a refund mechanism.
2. Relayers can choke message execution by skipping execution of the message that meets the attestation threshold. Current economic incentives benefit relayers if they skip this specific message.

**Recommended Mitigation:** In the case of standard relayers, consider a mechanism to refund excess gas to the recipient address on the target chain. `DeliveryProvider:: quoteEvmDeliveryPrice ` in the core Wormhole codebase returns a `targetChainRefundPerUnitGasUnused` parameter that is currently unused. Consider using this input to calculate the excess fee that can be refunded to the senders. Doing so will not only save costs for users but also remove any misaligned economic incentives for the relayers.

**Wormhole Foundation:** Fixed in [PR \#326](https://github.com/wormhole-foundation/example-native-token-transfers/pull/326).

**Cyfrin:** Verified. Transceivers now receive a refund address, and standard relaying for the `WormholeTransceiver` now issues refunds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Wormhole Evm Ntt |
| Report Date | N/A |
| Finders | Hans, 0kage, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

