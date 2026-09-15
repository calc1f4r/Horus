---
# Core Classification
protocol: Sablier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42012
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0e86d73a-3c3b-4b2b-9be5-9cecd4c7a5ac
source_link: https://cdn.cantina.xyz/reports/cantina_sablier_october2024.pdf
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
finders_count: 2
finders:
  - Zach Obront
  - RustyRabbit
---

## Vulnerability Title

New protocol fee applies retroactively on debt before fee change 

### Overview


Bug Report Summary:

The _withdraw() function in SablierFlow.sol is applying the protocol fee on the withdrawn amount, regardless of when the debt was accumulated. This means that the admin can potentially steal 10% from all users at any time, and users cannot have confidence in the fee that will be applied. A proof of concept has been provided, and a recommendation has been made to consider storing the fee as part of the stream parameters. However, the Sablier team has decided to keep the current version due to strategic business decisions. Cantina Managed has acknowledged the bug report.

### Original Finding Content

## SablierFlow.sol Analysis

## Context
SablierFlow.sol#L811-L820

## Description
The `_withdraw()` function applies the protocol fee on the withdrawn amount regardless of whether the debt was accumulated before or after the fee change. 

As such, users may be reluctant to use the protocol since:
- The admin can potentially steal 10% from all users at any time
- Even if the admin is not malicious, users cannot have confidence in the fee that will be applied up front.

## Proof of Concept
Add the following to `withdraw.t.sol`:
```solidity
function test_withdrawAfterFeeUpdate() external {
    uint256 fee = flow.protocolFee(usdc).unwrap();
    assertEq(fee, 0);
    uint256 streamId = createDefaultStream(usdc);
    resetPrank({ msgSender: users.sender });
    deposit(streamId, DEPOSIT_AMOUNT_6D);
    vm.warp({ newTimestamp: flow.depletionTimeOf(defaultStreamId)});
    resetPrank({ msgSender: users.admin });
    flow.setProtocolFee(usdc, PROTOCOL_FEE);
    fee = flow.protocolFee(usdc).unwrap();
    assertEq(fee, PROTOCOL_FEE);
    expectCallToTransfer({ token: usdc, to: users.recipient, amount: WITHDRAW_AMOUNT_6D - PROTOCOL_FEE_AMOUNT_6D });
    flow.withdraw({ streamId: streamId, to: users.recipient, amount: WITHDRAW_AMOUNT_6D });
}
```

## Recommendation
Consider storing the fee in effect as part of the stream parameters when created.

## Sablier Response
We appreciate your input. While we agree with your valid points, this is a strategic business decision to facilitate monetization via all pending withdrawals, including streamed tokens pre-activation of the protocol fee. Therefore, we have decided to keep the current version.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sablier |
| Report Date | N/A |
| Finders | Zach Obront, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sablier_october2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0e86d73a-3c3b-4b2b-9be5-9cecd4c7a5ac

### Keywords for Search

`vulnerability`

