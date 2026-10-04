---
# Core Classification
protocol: CodeHawks Escrow Contract - Competition Details
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34669
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cljyfxlc40003jq082s0wemya
source_link: none
github_link: https://github.com/Cyfrin/2023-07-escrow

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
finders_count: 15
finders:
  - 0xJuda
  - 0xdeadbeef
  - chainNue
  - nervouspika
  - golanger85
---

## Vulnerability Title

Fixed `i_arbiterFee` can prevent payment

### Overview


This bug report is about a fixed value called `i_arbiterFee` that can cause problems when trying to resolve disputes in a payment system. This can be a big issue if the payment token has a rebasing balance, which is a common feature in many projects. The problem occurs when the fixed value is bigger than the current balance of the contract, which can result in funds being locked in the system. To avoid this issue, it is recommended to either calculate the percentage of the fee at the beginning or set the percentage directly. This will also require changes in the code to send a percentage of the balance to the arbiter instead of a fixed amount.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-escrow/blob/fa9f20a273f1e004c1b11985ef0518b2b8ae1b10/src/Escrow.sol#L112">https://github.com/Cyfrin/2023-07-escrow/blob/fa9f20a273f1e004c1b11985ef0518b2b8ae1b10/src/Escrow.sol#L112</a>


## Summary

`i_arbiterFee` is a fixed value and can brick payment in resolution of disputes if the payment token has a rebasing balance. 
Instead, `i_arbiterFee` should be a percentage and should the actual fee should be based on the current balance of the contract.

## Vulnerability Details

```solidity
function resolveDispute(uint256 buyerAward) external onlyArbiter nonReentrant inState(State.Disputed) {
        uint256 tokenBalance = i_tokenContract.balanceOf(address(this));
        uint256 totalFee = buyerAward + i_arbiterFee; // Reverts on overflow
        if (totalFee > tokenBalance) {
            revert Escrow__TotalFeeExceedsBalance(tokenBalance, totalFee);
        }

        s_state = State.Resolved;
        emit Resolved(i_buyer, i_seller);

        if (buyerAward > 0) {
            i_tokenContract.safeTransfer(i_buyer, buyerAward); 
        }
        if (i_arbiterFee > 0) {
            i_tokenContract.safeTransfer(i_arbiter, i_arbiterFee);
        }
        tokenBalance = i_tokenContract.balanceOf(address(this));
        if (tokenBalance > 0) {
            i_tokenContract.safeTransfer(i_seller, tokenBalance);
        }
    }
```

As can be seen above, there are three values that are sent:
1. `buyerAward`- controlled by the arbiter, the refund that the `buyer` will receive 
2. `i_arbiterFee` - predefined fixed value that the arbiter will receive
3. `tokenBalance` - the remaining of the the contract will be sent to the `seller`

in case `i_tokenContract` is a token that has a rebasing balance. `i_arbiterFee` can be bigger then the current balance and `resolveDispute` will revert in the following statement
```solidity
if (totalFee > tokenBalance) {
            revert Escrow__TotalFeeExceedsBalance(tokenBalance, totalFee);
        }
```

Note that it is popular to use rebasing tokens. Additionally, it is common that projects (`buyer`s) will request the payouts in their own token (which can be rebasing). 

## Impact

Funds can be locked in the Escrow contract due to rebasing

## Tools Used

Manual

## Recommendations

Instead of setting a fixed `i_arbiterFee` either calculate the percentage at the escrow deployment or set the percentage directly.
This will also require to change `resolveDispute` to send a percentage of the balance to `arbiter` instead of a fixed payment

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | CodeHawks Escrow Contract - Competition Details |
| Report Date | N/A |
| Finders | 0xJuda, 0xdeadbeef, chainNue, nervouspika, golanger85, cccz, pontifex, ptsanev, mahdiRostami, 0xNiloy, aviggiano, 0xPinto, ZedBlockchain, guhu95, Shogoki |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-escrow
- **Contest**: https://codehawks.cyfrin.io/c/cljyfxlc40003jq082s0wemya

### Keywords for Search

`vulnerability`

