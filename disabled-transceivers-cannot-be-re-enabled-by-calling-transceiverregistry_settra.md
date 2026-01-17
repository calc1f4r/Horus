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
solodit_id: 31375
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

Disabled Transceivers cannot be re-enabled by calling `TransceiverRegistry::_setTransceiver` after 64 have been registered

### Overview


The bug report is about a function called `TransceiverRegistry::_setTransceiver` that is used to register and enable transceivers. However, the function has a bug that prevents disabled transceivers from being re-enabled after the maximum number of 64 transceivers has been registered. This is because the validation for the maximum number of transceivers is placed in the wrong block of code. This bug has a medium severity and has been fixed by the Wormhole Foundation in their code. 

### Original Finding Content

**Description:** [`TransceiverRegistry::_setTransceiver`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/TransceiverRegistry.sol#L112-L153) handles the registering of Transceivers, but note that they cannot be re-registered as this has other downstream effects, so this function is also responsible for the re-enabling of previously registered but currently disabled Transceivers.
```solidity
function _setTransceiver(address transceiver) internal returns (uint8 index) {
    /* snip */
    if (transceiver == address(0)) {
        revert InvalidTransceiverZeroAddress();
    }

    if (_numTransceivers.registered >= MAX_TRANSCEIVERS) {
        revert TooManyTransceivers();
    }

    if (transceiverInfos[transceiver].registered) {
        transceiverInfos[transceiver].enabled = true;
    } else {
    /* snip */
}
```

This function reverts if the passed transceiver address is `address(0)` or the number of registered transceivers is already at its defined maximum of 64. Assuming a total of 64 registered Transceivers, with some of these Transceivers having been previously disabled, the placement of this latter validation will prevent a disabled Transceiver from being re-enabled since the subsequent block in which the storage indicating its enabled state is set to `true` is not reachable. Consequently, it will not be possible to re-enable any disabled transceivers after having registered the maximum number of Transceivers, meaning that this function will never be callable without redeployment.

**Impact:** Under normal circumstances, this maximum number of registered Transceivers should never be reached, especially since the underlying Transceivers are upgradeable. However, while unlikely based on operational assumptions, this undefined behavior could have a high impact, and so this is classified as a **MEDIUM** severity finding.

**Recommended Mitigation:** Move the placement of the maximum Transceivers validation to within the `else` block that is responsible for handling the registration of new Transceivers.

**Wormhole Foundation:** Fixed in [PR \#253](https://github.com/wormhole-foundation/example-native-token-transfers/pull/253).

**Cyfrin:** Verified. The validation is now skipped for previously registered (but currently disabled) Transceivers.

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

