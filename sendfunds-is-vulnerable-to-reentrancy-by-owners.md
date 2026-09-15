---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17684
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
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
finders_count: 3
finders:
  - Troy Sargent
  - Anish Naik
  - Nat Chin
---

## Vulnerability Title

sendFunds is vulnerable to reentrancy by owners

### Overview


This bug report is about a vulnerability in the sendFunds function of the FundKeeper smart contract. The function is vulnerable to reentrancy, which means that the owner of a token contract can use the function to drain the contract of its funds. This is because fundsTransfered[user] is written to after a call to an external contract. Furthermore, the owner can send funds to any user by calling setAmountToSend and then sendFunds, but amountToSend is not changed after a successful transfer. 

To exploit this vulnerability, the owner of the FundKeeper contract can reenter the sendFunds function to drain the contract of its funds. For example, if the contract is set to transfer 1 ETH to the owner, the owner can reenter the function and drain all ETH from the contract. 

To fix this vulnerability, the developers should set fundsTransfered[user] to true prior to making external calls. In the long term, they should store each user's balance in a mapping to ensure that users cannot make withdrawals that exceed their balances. Additionally, they should follow the checks-effects-interactions pattern.

### Original Finding Content

## Vulnerability Report

## Difficulty: High

## Type: Access Controls

## Target: CrosslayerPortal/contracts/PolygonReward/FundKeeper.sol

### Description
The `sendFunds` function is vulnerable to reentrancy and can be used by the owner of a token contract to drain the contract of its funds. Specifically, because `fundsTransfered[user]` is written to after a call to an external contract, the contract’s owner could input his or her own address and reenter the `sendFunds` function to drain the contract’s funds. An owner could send funds to him- or herself without using the reentrancy, but there is no reason to leave this vulnerability in the code.

Additionally, the `FundKeeper` contract can send funds to any user by calling `setAmountToSend` and then `sendFunds`. It is unclear why `amountToSend` is not changed (set to zero) after a successful transfer. It would make more sense to call `setAmountToSend` after each transfer and to store users’ balances in a mapping.

```solidity
function setAmountToSend(uint256 amount) external onlyOwner {
    amountToSend = amount;
    emit NewAmountToSend(amount);
}

function sendFunds(address user) external onlyOwner {
    require(!fundsTransfered[user], "reward already sent");
    require(address(this).balance >= amountToSend, "Contract balance low");
    // solhint-disable-next-line avoid-low-level-calls
    (bool sent, ) = user.call{value: amountToSend}("");
    require(sent, "Failed to send Polygon");
    fundsTransfered[user] = true;
    emit FundSent(amountToSend, user);
}
```

*Figure 9.1: Part of the `sendFunds` function in `FundKeeper.sol`:23-38*

### Exploit Scenario
Eve’s smart contract is the owner of the `FundKeeper` contract. Eve’s contract executes a transfer for which Eve should receive only 1 ETH. Instead, because the user address is a contract with a fallback function, Eve can reenter the `sendFunds` function and drain all ETH from the contract.

### Recommendations
- **Short term:** Set `fundsTransfered[user]` to `true` prior to making external calls.
- **Long term:** Store each user’s balance in a mapping to ensure that users cannot make withdrawals that exceed their balances. Additionally, follow the checks-effects-interactions pattern.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Troy Sargent, Anish Naik, Nat Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf

### Keywords for Search

`vulnerability`

