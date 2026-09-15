---
# Core Classification
protocol: Coinbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54656
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/deda323c-567b-40ca-a3da-23838d697595
source_link: https://cdn.cantina.xyz/reports/cantina_coinbase_july2023.pdf
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
  - luksgrin
---

## Vulnerability Title

If Optimism Wallet has expensive receive() function, their payments can be bypassed 

### Overview


This bug report discusses an issue with the `disburseFees()` function in the `FeeDisburser.sol` contract. The function calculates the fees to be sent to Optimism and then uses `SafeCall` to send the funds. However, the `SafeCall` does not check the return value, which means that if the call fails, the entire remaining balance of the contract is sent to another contract on L1. This could be a big problem, but the severity of the issue is considered medium as it is unlikely to happen. The report recommends checking the return value and setting aside the fees for Optimism if the call fails. A separate function would also be needed for withdrawing these fees.

### Original Finding Content

## FeeDisburser.sol #L57

## Description
When `disburseFees()` is called, the amount of fees to send to Optimism is calculated. Then, `SafeCall` is used to send those funds to Optimism. Finally, the remaining balance of the contract is bridged to L1.

Similar to the issue raised in "Vault's totalProcessed count can be inaccurately increased by any user", the `SafeCall` used to send these funds does not check the return value. This means that if the call fails, the function will continue executing and will send its full remaining balance to Base's contract on L1.

```solidity
SafeCall.send(OPTIMISM_WALLET, gasleft(), optimismRevenueShare);

// Send remaining funds to L1 wallet on L1
L2StandardBridge(payable(Predeploys.L2_STANDARD_BRIDGE)).bridgeETHTo{ value: address(this).balance }(
    L1_WALLET,
    WITHDRAWAL_MIN_GAS,
    bytes("")
);
```

While skipping Optimism's payments would be a big problem, I am considering this issue only a Medium Severity because it is quite unlikely. There are only two ways I can see the `SafeCall.send()` reverting:
1. Optimism deploys a contract to this address that reverts in the `receive()` function.
2. Optimism deploys a contract to this address where the `receive()` function uses so much gas that it can run out of gas, while the remaining 1/64th of the previous gas is sufficient to perform the bridge transaction. That would imply that the `receive()` function uses 63x as much gas as the bridge call, which is fairly unlikely.

## Recommendation
Unfortunately, it is not safe to simply `require(success);`, because this opens the door to a DOS if Optimism deploys a contract to the `OPTIMISM_WALLET` address that reverts on transfers. This could happen maliciously, or accidentally, and would lead to all funds being locked in the `FeeDisburser` contract.

Instead, the best solution seems to be to check this return success value and, if it returns false, set aside the fees for Optimism. This can be done by saving the value in a storage variable and, if the value is greater than zero, only sending `address(this).balance - optimismHoldings` on withdrawals.

Optimism would need a separate function to withdraw this `optimismHoldings` value directly, outside the regular fee disbursement process.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Coinbase |
| Report Date | N/A |
| Finders | Zach Obront, luksgrin |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_coinbase_july2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/deda323c-567b-40ca-a3da-23838d697595

### Keywords for Search

`vulnerability`

