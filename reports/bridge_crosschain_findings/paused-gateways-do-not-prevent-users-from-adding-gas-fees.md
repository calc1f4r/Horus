---
# Core Classification
protocol: Cross Chain Messaging Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50219
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/biconomy/cross-chain-messaging-protocol-smart-contract-security-assessment-1
source_link: https://www.halborn.com/audits/biconomy/cross-chain-messaging-protocol-smart-contract-security-assessment-1
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
  - Halborn
---

## Vulnerability Title

PAUSED GATEWAYS DO NOT PREVENT USERS FROM ADDING GAS FEES

### Overview


The bug report describes an issue with the `addGasFee` function in the CCMPSendMessageFacet contract. This function allows users to add gas fees even when a gateway is paused, which goes against the intended purpose of the protocol. This could result in users losing their tokens if a gateway is paused due to cyberattacks, market conditions, or other security issues. The code responsible for this issue can be found in the CCMPSendMessageFacet.sol file, and the likelihood of this bug occurring is rated at 3 out of 10, with an impact score of 4 out of 10.

### Original Finding Content

##### Description

`addGasFee` function in **CCMPSendMessageFacet** contract allows users to add gas fee `even if a gateway is paused`, which would go against the business logic of the protocol.

As a consequence, users could lose their recently deposited tokens if a gateway has been paused because of an unexpected scenario: cyberattacks, market adverse conditions, security issues with the adaptors, etc.

Code Location
-------------

#### gateway/facets/CCMPSendMessageFacet.sol

```
function addGasFee(
  GasFeePaymentArgs memory _args,
  bytes32 _messageHash,
  address _sender
) public payable {
  uint256 feeAmount = _args.feeAmount;
  address relayer = _args.relayer;
  address tokenAddress = _args.feeTokenAddress;

  LibDiamond.CCMPDiamondStorage storage ds = LibDiamond._diamondStorage();

  if (feeAmount > 0) {
    ds.gasFeePaidByToken[_messageHash][tokenAddress][
      relayer
    ] += feeAmount;

    if (tokenAddress == NATIVE_ADDRESS) {
      if (msg.value != feeAmount) {
        revert NativeAmountMismatch();
      }
      (bool success, bytes memory returndata) = relayer.call{
        value: msg.value
      }("");
      if (!success) {
        revert NativeTransferFailed(relayer, returndata);
      }
    } else {
      if (msg.value != 0) {
        revert NativeAmountMismatch();
      }
      IERC20(tokenAddress).safeTransferFrom(
        _sender,
        relayer,
        feeAmount
      );
    }

    emit FeePaid(tokenAddress, feeAmount, relayer);
  }
}

```

##### Score

Impact: 4  
Likelihood: 3

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Cross Chain Messaging Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/biconomy/cross-chain-messaging-protocol-smart-contract-security-assessment-1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/biconomy/cross-chain-messaging-protocol-smart-contract-security-assessment-1

### Keywords for Search

`vulnerability`

