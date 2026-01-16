---
# Core Classification
protocol: Megapot
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49318
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/3677c4f9-3739-4b83-9d5e-4cd16280ad70
source_link: https://cdn.cantina.xyz/reports/cantina_megapot_february2024.pdf
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
finders_count: 2
finders:
  - Anurag Jain
  - Blockdev
---

## Vulnerability Title

Token transfer logic is incorrect for some tokens 

### Overview


The current transfer funds logic in a contract called BaseJackpot has multiple issues. One issue is that certain tokens, like USDT, do not return a bool value when using the transfer or transferFrom function. This causes a require check to fail. Another issue is that in the case of a fee on transfer tokens, the contract will actually receive a lesser amount than expected. To fix this, the report recommends moving the token transfer outside of an if-else block and using safeTransfer/safeTransferFrom functions instead. It also suggests implementing a method to ensure the correct balance is obtained for fee-on-transfer tokens. Additionally, the report advises verifying that any new ERC20 tokens integrated with the contract follow certain specifications to avoid potential issues. The report notes that the issues have been fixed in a pull request (PR) for two specific tokens called Megapot and Cantina Managed. The risk level of these issues is considered low. 

### Original Finding Content

## Current Transfer Funds Logic Issues in BaseJackpot.sol

## Context
- BaseJackpot.sol#L490-L508
- BaseJackpot.sol#L544-L564
- BaseJackpot.sol#L607
- BaseJackpot.sol#L622
- BaseJackpot.sol#L640-L644
- BaseJackpot.sol#L689-L690
- BaseJackpot.sol#L810-L811

## Description
The current transfer funds logic has multiple issues:

1. Tokens like USDT do not return a bool value on the `transfer`/`transferFrom` function. This means the below require check will fail.
   ```solidity
   require(
       token.transferFrom(msg.sender, address(this), value),
       "ERC20: transfer failed"
   );
   ```
   
2. In the case of fee-on-transfer tokens, the contract will actually receive a lesser amount. Since the contract code does not check if the amount received is the expected amount, it will lack the expected funds.

## Recommendation
1. Since token transfer is required in all conditions, we can move the token transfer outside the if-else block in both `purchaseTickets` and `lpDeposit` functions.
   
2. Use `safeTransfer`/`safeTransferFrom`, which can handle tokens like USDT (which has no return value) at all places where ERC20 `transfer`/`transferFrom` is used.
   
3. Since the project wants to support fee-on-transfer tokens:
   - Determine the pre-balance of the token.
   - Transfer the token to the contract.
   - Compute the current token balance.
   - Subtract current balance - pre-balance.
   - Check if the resulting amount equals the value to be transferred. This will ensure that the correct balance is obtained for fee-on-transfer tokens.

Finally, since the team may integrate new ERC20 tokens with the BaseJackpot contract, it's important to verify that the token largely satisfies the ERC20 specification. For example:
- It shouldn't be a rebasing token.
- If it is a fee-on-transfer token, the fee should be taken from the transfer amount. Although unexpected, a weird ERC20 token may take a fee from the sender balance instead of the transfer amount. This will lead to improper accounting when the contract transfers some amount out of the contract. In this case, the contract's balance reduces by more than the transfer amount and users may not be able to withdraw the expected amounts later.

## Reference
Check OpenZeppelin's `SafeERC20.sol`.

## Status
- **Megapot**: Fixed in PR 11.
- **Cantina Managed**: Fixed as recommended in PR 11.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Megapot |
| Report Date | N/A |
| Finders | Anurag Jain, Blockdev |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_megapot_february2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/3677c4f9-3739-4b83-9d5e-4cd16280ad70

### Keywords for Search

`vulnerability`

