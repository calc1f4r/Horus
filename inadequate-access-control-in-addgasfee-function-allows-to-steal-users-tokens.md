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
solodit_id: 50216
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/biconomy/cross-chain-messaging-protocol-smart-contract-security-assessment-1
source_link: https://www.halborn.com/audits/biconomy/cross-chain-messaging-protocol-smart-contract-security-assessment-1
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
  - Halborn
---

## Vulnerability Title

INADEQUATE ACCESS CONTROL IN ADDGASFEE FUNCTION ALLOWS TO STEAL USERS' TOKENS

### Overview


The report describes a security issue where an attacker can use a function in the CCMPSendMessageFacet contract to steal ERC20 tokens from users who have approved the CCMPGateway to manage their tokens. This can happen in any chain where there is a gateway, and even if the tokens were expected to be used in later transactions. The attacker can also front-run the transaction if needed. The report includes a proof of concept showing how the attack can be carried out. The code location of the vulnerable function is also provided, along with a score of 5 for both impact and likelihood of the attack.

### Original Finding Content

##### Description

An attacker can use `addGasFee` function in **CCMPSendMessageFacet** contract and send a custom `GasFeePaymentArgs` to force the transfer of ERC20 tokens from all the users, who previously approved **CCMPGateway** to manage their tokens, to a fake relayer (i.e.: the attacker himself). The following situations increase the risk level of this issue:

* The attack can be replicated in all the chains where there is a gateway and allows stealing all the tokens approved, even if they were expected to be spent on later transactions yet.
* Even if the approval and the deposit of tokens is done together, this last transaction could be front-runned if necessary.

Here is a proof of concept showing how to exploit this security issue:

`Proof of Concept:`

1. A user approves that **CCMPGateway** manages `1_000_000 tokens`.
   ![](images/HAL-01/Step_1.png)
2. An attacker creates a custom `GasFeePaymentArgs` to steal all the tokens from the user.
   ![](images/HAL-01/Step_2.png)
3. The attacker calls the `addGasFee` function with the custom `GasFeePaymentArgs`. After this transaction, the balance of the attacker should have increased by `1_000_000` and the balance of the user should be `0`.
   ![](images/HAL-01/Step_3.png)
4. Finally, the attack is successful, as shown in the test.
   ![](images/HAL-01/Step_4.png)

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

Impact: 5  
Likelihood: 5

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

