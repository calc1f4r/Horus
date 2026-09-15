---
# Core Classification
protocol: Pheasant Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60340
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
source_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
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
finders_count: 5
finders:
  - Danny Aksenov
  - Faycal Lalidji
  - Ruben Koch
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

Protocol Assumes Unlimited Relayer Liquidity on L2

### Overview


The client has acknowledged a risk in the PheasantNetworkBridgeChild.sol file, where there is currently no way for the relayer to control trade requests for L1->L2 trades. This can lead to the relayer being subject to slashing, as they are expected to have tokens readily available on the target network. This could become a problem if the bridge becomes heavily used, as the relayer may face liquidity issues. It is recommended to have an intermediate L1-contract in place to pause incoming requests to prevent this issue.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We are aware of the mentioned risk, but due to the high gas fees on L1, we have decided not to deploy the contract on L1 for now. However, we may consider consolidating the bonds on L1 in the future to address this issue.

**File(s) affected:**`PheasantNetworkBridgeChild.sol`

**Description:** For the relayer, there is currently no way to throttle the trade requests for L1->L2 trades. All valid direct L1 transfers make the relayer subject to slashing. As the relayer will be slashable starting after 30 minutes, the protocol seems to assume that the relayer has the tokens readily available on the target network. However, if this bridge were to become heavily used (and perhaps more for L1->L2 than L2->L1 trades), the relayer could quickly get liquidity problems. The relayer could attempt to swap for the desired token on a DEX, but that also requires some liquidity from other tokens accessible on L2. So the relayer might need to make use of a traditional "mint-and-burn" bridge for this. If L1->L2 would continue to be the dominant trade direction, the fees could even begin to exceed the ones of a traditional bridge, as the relayer would need to use such a bridge to bridge the funds with the additional overhead of performing the appropriate function calls in this protocol.

The liquidity problem is also amplified by the relayer theoretically needing to hold a bond for a trade for 14 days (though that is currently not enforced by the protocol).

This could be an attack vector for a malicious user, requesting a high quantity of upward trades that the relayer will struggle to handle on time, making them subject to slashing.

**Recommendation:** Have some intermediate L1-contract for L1->L2 requests in place where a relayer can (automatically) pause incoming requests.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Pheasant Network |
| Report Date | N/A |
| Finders | Danny Aksenov, Faycal Lalidji, Ruben Koch, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html

### Keywords for Search

`vulnerability`

