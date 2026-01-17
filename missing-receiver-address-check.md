---
# Core Classification
protocol: Bridge Updates
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50979
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/chiliz/bridge-updates-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/chiliz/bridge-updates-smart-contract-security-assessment
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

MISSING RECEIVER ADDRESS CHECK

### Overview

See description below for full details.

### Original Finding Content

##### Description

In this system, the Solidity code does not include a check to prevent sending transactions to the zero address. The zero address is a special address that is reserved in Ethereum, and it represents the absence of an address. Sending a transaction to the zero address is equivalent to sending it to nowhere, and it will be lost and not executed. However, if the Solidity code does not check for the zero address, it is possible for a malicious actor to exploit this and send transactions to the zero address, potentially resulting in the loss of funds. It is important for the system to include a zero address check in the Solidity code, to prevent transactions from being sent to the zero address and to protect against potential loss of funds.

Code Location
-------------

[NativeHandler.sol#L104](https://gitlab.mediarex.com/mediarex/blockchain/bridge-contracts/-/blob/094856fd48bb4627842c72e914df09fe9689ad81/contracts/handlers/NativeHandler.sol#L104)

```
    function deposit(
        bytes32 resourceID,
        uint8   destinationChainID,
        uint64  depositNonce,
        address depositer,
        bytes   calldata data
    ) external override onlyBridge {
        bytes   memory recipientAddress;
        uint256        amount;
        uint256        lenRecipientAddress;

        assembly {
            amount := calldataload(0xC4)
            recipientAddress := mload(0x40)
            lenRecipientAddress := calldataload(0xE4)
            mstore(0x40, add(0x20, add(recipientAddress, lenRecipientAddress)))

            calldatacopy(
                recipientAddress, // copy to destinationRecipientAddress
                0xE4, // copy from calldata @ 0x104
                sub(calldatasize(), 0xE) // copy size (calldatasize - 0x104)
            )
        }

        address tokenAddress = _resourceIDToTokenContractAddress[resourceID];
        require(_contractWhitelist[tokenAddress], "provided tokenAddress is not whitelisted");

        uint256 bridgeFee = IBridge(_bridgeAddress)._fee();
        uint256 amountMinusFee = amount - bridgeFee;
        require(amountMinusFee > 0, "Invalid amount");

        _depositRecords[destinationChainID][depositNonce] = DepositRecord(
            tokenAddress,
            uint8(lenRecipientAddress),
            destinationChainID,
            resourceID,
            recipientAddress,
            depositer,
            amountMinusFee
        );
    }


```

##### Score

Impact: 3  
Likelihood: 1

##### Recommendation

**SOLVED**: The `Chiliz team` solved the issue by adding receiver address check.

`Commit ID:` [bf171d4028b5af946c091baa77a413b3927a44bc](https://gitlab.mediarex.com/mediarex/blockchain/bridge-contracts/-/commit/bf171d4028b5af946c091baa77a413b3927a44bc)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Bridge Updates |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/chiliz/bridge-updates-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/chiliz/bridge-updates-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

