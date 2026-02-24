---
# Core Classification
protocol: Ethos Network Financial Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44325
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/675
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-ethos-network-ii-judging/issues/660

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
finders_count: 68
finders:
  - volodya
  - Ch\_301
  - tobi0x18
  - DenTonylifer
  - Artur
---

## Vulnerability Title

H-3: Market funds cannot be withdrawn because of incorrect calculation of `fundsPaid`

### Overview


This bug report is about a problem with the calculation of `fundsPaid` in the `ReputationMarket` contract. This calculation error is causing issues with withdrawing funds from the market. The issue was found by multiple users and the root cause is that fees are not being deducted correctly when votes are bought. This leads to the protocol fees and donation fees being counted twice, resulting in insufficient funds for withdrawal. The team has provided a proof of concept and recommendations for fixing the issue. The bug has been fixed in the latest update of the contract. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-ethos-network-ii-judging/issues/660 

## Found by 
0rpse, 0x486776, 0xEkko, 0xPhantom2, 0xProf, 0xaxaxa, 0xgremlincat, 0xlucky, 0xmujahid002, 0xpiken, 4th05, Abhan1041, AestheticBhai, Al-Qa-qa, Artur, BengalCatBalu, Bozho, Ch\_301, Cybrid, DenTonylifer, DharkArtz, HOM1T, John44, JohnTPark24, KingNFT, KlosMitSoss, Limbooo, Nave765, NickAuditor2, Pablo, Waydou, Weed0607, X0sauce, X12, ami, blutorque, bube, bughuntoor, cryptic, debugging3, dobrevaleri, farismaulana, future2\_22, hals, iamnmt, ke1caM, kenzo123, mahdikarimi, nikhilx0111, novaman33, parzival, pashap9990, qandisa, rudhra1749, shui, smbv-1923, t.aksoy, tjonair, tmotfl, tobi0x18, udo, vatsal, volodya, wellbyt3, whitehair0330, y4y, ydlee, zxriptor
### Summary
Funds withdrawal is blocked as fees are not deducted from fundsPaid when already being applied.

## Root Cause

When votes are bought in `ReputationMarket` market, user has to pay fees to:
- donation fees going to owner of the market
- protocol fees going to treasury

This is seen in `applyFees` function below:

```solidity
  function applyFees(
    uint256 protocolFee,
    uint256 donation,
    uint256 marketOwnerProfileId
  ) private returns (uint256 fees) {
@>    donationEscrow[donationRecipient[marketOwnerProfileId]] += donation; // donation fees are updated for market owner
    if (protocolFee > 0) {
@>      (bool success, ) = protocolFeeAddress.call{ value: protocolFee }(""); // protocolFees paid to treasury
      if (!success) revert FeeTransferFailed("Protocol fee deposit failed");
    }
    fees = protocolFee + donation;
  }
```

Next, the total amount a user pays when votes are bought is managed by the `fundsPaid` variable. The amount consists of:
`cost of votes + protocol fees + donation fees`

The vulnerability exists in the execution here:
1. send protocol fees to the treasury
2. add donations to market owner's escrow
3. marketOwner is able to withdraw donations via `withdrawDonations()`

In the `buyVotes` function, protocolFee and donation are paid first as seen below:

```solidity
 applyFees(protocolFee, donation, profileId);
```

Then, when tallying the market funds, `marketFunds` is updated with `fundsPaid`. This `fundsPaid` still includes the protocolFee and donation and has not been deducted.

```solidity
 marketFunds[profileId] += fundsPaid; 
```

Hence, the protocolFee and donation has been counted twice.

When a market graduates, because of the incorrect counting of `marketFunds`, the contract may not have enough funds to be withdrawn via `ReputationMarket.withdrawGraduatedMarketFunds` and results in transaction reverting.


## Proof of Concept

Assume this scenario:

A market exists with 2 trust votes and 2 distrust votes, each costing 0.03 ETH. Protocol and donation fees are both set at 5%.
Alice buys 2 trust votes for 0.07 ETH:

Fees (5% each):
Protocol: 0.0015 ETH per vote → 0.003 ETH total.
Donations: 0.0015 ETH per vote → 0.003 ETH total.
Vote Cost: 0.03 ETH × 2 = 0.06 ETH.
Refund: 0.07 ETH - (0.06 ETH + 0.006 ETH fees) = 0.004 ETH.
The contract incorrectly records 0.066 ETH (votes + fees) as market funds.

Market owner withdraws the 0.06 ETH correctly available.

After market graduation, the contract attempts to withdraw the recorded 0.066 ETH, but only 0.06 ETH exists.

## Impact:

The withdrawal fails due to insufficient funds.
Funds are stuck, or other markets' funds are misallocated.
If a withdrawal succeeds, it might wrongly pull ETH allocated to other markets, leading to losses for other users.

## Line(s) of Code
https://github.com/sherlock-audit/2024-11-ethos-network-ii/blob/main/ethos/packages/contracts/contracts/ReputationMarket.sol#L442

https://github.com/sherlock-audit/2024-11-ethos-network-ii/blob/main/ethos/packages/contracts/contracts/ReputationMarket.sol#L920

https://github.com/sherlock-audit/2024-11-ethos-network-ii/blob/main/ethos/packages/contracts/contracts/ReputationMarket.sol#L660

https://github.com/sherlock-audit/2024-11-ethos-network-ii/blob/main/ethos/packages/contracts/contracts/ReputationMarket.sol#L1116

## Recommendations

Update logic to deduct protocol fees and donations before updating `marketFunds`.





## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/trust-ethos/ethos/pull/2216

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Ethos Network Financial Contracts |
| Report Date | N/A |
| Finders | volodya, Ch\_301, tobi0x18, DenTonylifer, Artur, X0sauce, nikhilx0111, 4th05, tmotfl, whitehair0330, DharkArtz, udo, zxriptor, future2\_22, novaman33, iamnmt, ami, tjonair, ydlee, 0xmujahid002, ke1caM, 0xaxaxa, debugging3, farismaulana, pashap9990, BengalCatBalu, mahdikarimi, KingNFT, KlosMitSoss, John44, Waydou, cryptic, vatsal, dobrevaleri, blutorque, 0xPhantom2, 0xpiken, y4y, Abhan1041, Pablo, smbv-1923, 0xEkko, 0rpse, 0x486776, 0xProf, 0xgremlincat, AestheticBhai, NickAuditor2, t.aksoy, HOM1T, bube, parzival, Weed0607, rudhra1749, JohnTPark24, kenzo123, Al-Qa-qa, Nave765, Bozho, bughuntoor, Limbooo, wellbyt3, Cybrid, shui, qisa, hals, 0xlucky, X12 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-ethos-network-ii-judging/issues/660
- **Contest**: https://app.sherlock.xyz/audits/contests/675

### Keywords for Search

`vulnerability`

