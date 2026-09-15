---
# Core Classification
protocol: Venus Multichain Support
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60186
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
source_link: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
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
finders_count: 4
finders:
  - Shih-Hung Wang
  - Julio Aguilar
  - Ibrahim Abouzied
  - Cameron Biniamow
---

## Vulnerability Title

Potential of Locked Funds in XVS Bridges

### Overview


The report discusses two fixes that were made to the XVSProxyOFTSrc and XVSProxyOFTDest contracts. The first fix added a function to release locked funds in the source bridge, but it did not account for failed callback functions. The second fix added a function to recover locked tokens, but it also increased the risks of the protocol. The issue was caused by the design of the OFTCoreV2 contract, which could potentially lock funds in the bridge. The report recommends introducing a mechanism to return locked funds in the source chain to avoid this issue.

### Original Finding Content

**Update**
**1st Fix Review**: Both `XVSProxyOFTSrc` and `XVSProxyOFTDest` contracts include a `dropFailedMessage()` function to drop any failed cross-chain messages. A `fallbackWithdraw()` function is added to `XVSProxyOFTSrc` to release the locked funds in the source bridge after the failed message in the destination bridge is dropped. However, if the `sendAndCall()` function is used, and the callback function fails, the newly minted XVS will be locked in the destination bridge.

**2nd Fix Review**: A `sweepToken()` function is added to recover locked tokens (not limited to only XVS) in the bridge contracts. An admin-controlled flag is added to allow the admin to activate or deactivate the `sendAndCall()` function. Although the issue of the potential of locked funds is resolved, it should be noted that the mitigation increases the centralization and operational risks of the protocol. See [VMC-30](https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html#findings-qs30) for more details.

![Image 42: Alert icon](https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the Venus team. Addressed in: `264109ce597e95b4ea1a630e7c68dada143968fe` (isolated-pools repo), `6229b5e6082608fef2215cb7cc5f5f6588d79df9` (token-bridge repo), `06c6009e01411182d738b2249cbbb06019926b54` (token-bridge repo).

**File(s) affected:**`isolated-pools/contracts/Bridge/BaseXVSProxyOFT.sol`

**Description:** The function `BaseOFTV2.sendAndCall()` burns or locks XVS tokens from users with the intention of bridging them over to another chain to an address provided by the user. However, the recipient, `_toAddress`, **must** be a contract on the destination chain. Otherwise, the function `OFTCoreV2._sendAndCallAck()` will mint or release tokens through `_creditTo()` without transferring them to the designated address, essentially locking the XVS tokens in the bridge contract.

Additionally, if for some reason a failed transaction is unable to be retried through `retryMessage()`, tokens might be unable to be sent to the destination address even though they might have been burned in the source chain.

**Recommendation:** This issue originates from the design of LayerZero's `OFTCoreV2` contract. Funds locked in the bridge should be avoided. Since the source bridge cannot verify that the destination address is a contract, we recommend introducing a mechanism that can return the locked funds in the source chain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus Multichain Support |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Julio Aguilar, Ibrahim Abouzied, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html

### Keywords for Search

`vulnerability`

