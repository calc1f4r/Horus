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
solodit_id: 31740
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

[C-01] Users can't bridge funds back from the app chain

### Overview


This bug report is about a problem in a protocol that requires a fee in the native coin to bridge funds back from the app chain. The severity and impact of this bug are high, and the likelihood of it occurring is also high. The issue is that the contracts involved in this process do not have a function to receive ETH, which is causing the problem. The recommendation is to make sure that the contract responsible for this process inherits a module with a function that can receive ETH.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** High

**Description**

The protocol must pay a fee in native coin to bridge funds back from the app chain:

```solidity
        (uint256 tokenFees, uint256 nativeFees) =
            getFees(withdrawToken, socketController, socketConnector, socketMsgGasLimit, socketPayloadSize);
        if (tokenAmount > tokenFees) {
            uint256 tokensToWithdraw = tokenAmount - tokenFees;
@>          socketController.bridge{ value: nativeFees }({
                receiver_: receiver,
                amount_: tokensToWithdraw,
                msgGasLimit_: socketMsgGasLimit,
                connector_: socketConnector,
                execPayload_: abi.encode(),
                options_: abi.encode()
            });
```

Periphery is the module that interacts with the bridge. The problem is that none of these contracts has `payable` function to receive ETH

```solidity
contract PeripheryRouter is
    ConfigurationModule,
    DepositsModule,
    DepositsFallbackModule,
    OrderModule,
    TransfersModule,
    WithdrawalsModule,
    OwnerUpgradeModule,
    ERC721ReceiverModule,
    FeatureFlagModule
{ }

contract PeripheryProxy is UUPSProxyWithOwner, PeripheryRouter {
    constructor(
        address firstImplementation,
        address initialOwner
    )
        UUPSProxyWithOwner(firstImplementation, initialOwner)
    { }
}
```

**Recommendations**

Make sure that PeripheryRouter.sol inherits the module with the function `receive() payable`

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

