---
# Core Classification
protocol: Reyanetwork
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31743
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] User can lose tokens during deposit fallback bridging

### Overview


This bug report discusses an issue with the DepositsFallbackModule, which is responsible for handling situations where a deposit fails and needs to be bridged back to the user's account. The module uses the address of the deposit on the Reya chain to bridge back the funds on the source chain. However, it incorrectly assumes that the address on the source chain is owned by the same person on the Reya chain, which may not always be the case. This can happen with certain types of wallets and with older versions of multisig accounts. The recommendation is to add an argument to the FallbackData struct and use it instead of the current address to ensure the correct user receives the bridged funds. 

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Medium

**Description**

DepositsFallbackModule handles situations where a deposit reverts and initiates bridging back of users' funds. Note that it uses the address `receiver` of the deposit on the Reya chain to bridge back funds on the source chain:

```solidity
        try DepositsModule(address(this)).depositPassivePool(inputs) { }
        catch {
            BridgingUtils.executeBridging({
                withdrawToken: usdc,
                socketConnector: fallbackData.socketConnector,
                socketMsgGasLimit: fallbackData.socketMsgGasLimit,
                tokenAmount: inputs.amount,
@>              receiver: inputs.owner,
                socketPayloadSize: fallbackData.socketPayloadSize
            });
        }
```

It incorrectly assumes that the address `inputs.owner` on the source chain is owned by the same person on Reya chain. There are 2 cases when the assumption is not guaranteed:

1.  Account Abstraction wallet implementations
2.  old version of Safe multisigs https://rekt.news/wintermute-rekt/

**Recommendations**

Add argument `receiver` to FallbackData struct and use it instead of `inputs.accountOwner` in DepositsFallbackModule.sol

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Reyanetwork |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

