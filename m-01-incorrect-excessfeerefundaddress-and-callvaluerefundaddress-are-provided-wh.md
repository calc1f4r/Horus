---
# Core Classification
protocol: Hytopia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31595
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hytopia-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Incorrect `excessFeeRefundAddress` and `callValueRefundAddress` are provided when bridging tokens to the L2

### Overview


The report discusses a bug in the HYCHAIN blockchain that uses the same technology as Arbitrum Nova. The bug relates to the `createRetryableTicket` function, which is used for L1 -> L2 bridging for the minted node key token. The `excessFeeRefundAddress` and `callValueRefundAddress` parameters are set to `address(this)`, which could result in a loss of excess fee and the ability to cancel the ticket. The severity of this bug is medium, and the likelihood is also medium. The report recommends considering a configurable L2 address for these parameters to prevent any potential issues.

### Original Finding Content

**Severity**

**Impact:** Medium, `address(this)` is provided for the `excessFeeRefundAddress` and `callValueRefundAddress` parameters when calling `createRetryableTicket`, which could lead to a loss of excess fee and the ability to cancel the L1 -> L2 ticket.

**Likelihood:** Medium, The ability to cancel a ticket might needed when there is potentially malicious behavior that needs to be prevented when `_mintAndBridge` is triggered.

**Description**

HYCHAIN's blockchain uses the same technology that powers Arbitrum Nova (L2). One of the capabilities that is available and used is L1 -> L2 bridging for the minted node key token. According to the docs, `excessFeeRefundAddress` is L2 address to which the excess fee is credited and `callValueRefundAddress` is address that has the capability to cancel the bridging ticket if needed.

```solidity
    function _mintAndBridge(address _to, uint256 _qty) internal {
        uint256 _startingTokenId = _nextTokenId();
        _mint(_to, _qty);
        HychainNodeKeyStorage.Layout storage $ = HychainNodeKeyStorage.layout();
        // require enough nativeToken to bridge
        if ($._topia != address(0)) {
            // TODO: figure out the exact amount
            require(IERC20($._topia).balanceOf(address(this)) >= $._transferCost, "Not enough $TOPIA to mint");
        }
        // approve inbox to transfer token
        IERC20($._topia).approve($._inbox, $._transferCost);
        // register ownership via retryable ticket
        uint256 ticketID = IERC20Inbox($._inbox).createRetryableTicket(
            $._l2NodeKeyAddress, // to
            0, // l2CallValue
            $._maxSubmissionCost, // maxSubmissionCost
>>>         address(this), // excessFeeRefundAddress
>>>         address(this), // callValueRefundAddress
            $._l2GasLimit, // gasLimit
            $._l2GasPrice, // maxGasPrice
            4e15, // tokenTotalFeeAmount
            abi.encodeWithSignature("mint(address,uint256,uint256)", msg.sender, _startingTokenId, _qty)
        );

        emit InboxTicketCreated(msg.sender, ticketID, _startingTokenId, _qty);
    }
```

However, `address(this)` is provided for those two parameters, which could become an issue when the excess fee is non-zero or when the cancel action is required to prevent unexpected behavior.

**Recommendations**

Consider putting a configurable L2 address for `excessFeeRefundAddress` and `callValueRefundAddress`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hytopia |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hytopia-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

