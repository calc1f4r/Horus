---
# Core Classification
protocol: Debita Finance V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44228
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/627
source_link: none
github_link: https://github.com/sherlock-audit/2024-10-debita-judging/issues/890

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
finders_count: 31
finders:
  - newspacexyz
  - shaflow01
  - DenTonylifer
  - nikhilx0111
  - xiaoming90
---

## Vulnerability Title

H-5: After the buyOrder is completed, the order creator does not receive the NFT

### Overview


This bug report is about an issue with a feature called buyOrder. After this feature is used, the person who created the order is supposed to receive a virtual item called NFT, but this is not happening. The cause of this issue is that the NFT is being sent to another contract instead of the order creator. This means that the order creator will lose the NFT. The report includes a test that shows how this can happen and suggests that the NFT should be transferred to the order creator after the buyOrder is completed.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-10-debita-judging/issues/890 

## Found by 
0x37, 0xPhantom2, 4lifemen, Audinarey, BengalCatBalu, CL001, Cybrid, DenTonylifer, Greed, Greese, IzuMan, KiroBrejka, KungFuPanda, Pro\_King, Valy001, alexbabits, araj, dhank, dimulski, durov, kazan, lanrebayode77, merlin, newspacexyz, nikhilx0111, pashap9990, shaflow01, t.aksoy, utsav, xiaoming90, ydlee
### Summary

After sellNFT is completed, the NFT should be transferred  to the order creator, but this is not done.

### Root Cause

After the buyOrder is completed, the order creator does not receive the NFT, and the NFT is sent directly to **[buyOrderContract](https://github.com/sherlock-audit/2024-11-debita-finance-v3/blob/1465ba6884c4cc44f7fc28e51f792db346ab1e33/Debita-V3-Contracts/contracts/buyOrders/buyOrder.sol#L99)**

The latter only emits an event and deletes the order, but does not transfer the NFT to  the order creator

### Internal pre-conditions



### External pre-conditions

1. User A  create buyOrder.
2. User B  **sellNFT**.

### Attack Path
1. User A  create buyOrder.
2. User B  **sellNFT**,and [receive](https://github.com/sherlock-audit/2024-11-debita-finance-v3/blob/1465ba6884c4cc44f7fc28e51f792db346ab1e33/Debita-V3-Contracts/contracts/buyOrders/buyOrder.sol#L122) **buyToken**
3.  But **order creator** will[ lose ](https://github.com/sherlock-audit/2024-11-debita-finance-v3/blob/1465ba6884c4cc44f7fc28e51f792db346ab1e33/Debita-V3-Contracts/contracts/buyOrders/buyOrder.sol#L99)the NFT


### Impact

The buyOrder creator will lose the NFT

### PoC

Path:
test/fork/BuyOrders/BuyOrder.t.sol

```solidity
function testpoc() public{
        vm.startPrank(seller);
        receiptContract.approve(address(buyOrderContract), receiptID);
        uint balanceBeforeAero = AEROContract.balanceOf(seller);
        address owner = receiptContract.ownerOf(receiptID);
       
        console.log("receipt owner before sell",owner);


        buyOrderContract.sellNFT(receiptID);
        address owner1 = receiptContract.ownerOf(receiptID);
        console.log("receipt owner after sell",owner1);
        //owner = buyOrderContract
        assertEq(owner1,address(buyOrderContract));
        
        
        vm.stopPrank();

    }

```
[PASS] testpoc() (gas: 242138)
Logs:
  receipt owner before sell 0x81B2c95353d69580875a7aFF5E8f018F1761b7D1
  receipt owner after sell 0xffD4505B3452Dc22f8473616d50503bA9E1710Ac
### Mitigation

After the buyOrder is completed,the NFT should be transferred  to the order creator

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Debita Finance V3 |
| Report Date | N/A |
| Finders | newspacexyz, shaflow01, DenTonylifer, nikhilx0111, xiaoming90, Greed, ydlee, Audinarey, KungFuPa, pashap9990, BengalCatBalu, IzuMan, CL001, 0x37, alexbabits, kazan, Pro\_King, 0xPhantom2, KiroBrejka, durov, 4lifemen, t.aksoy, dhank, Greese, utsav, Valy001, araj, dimulski, Cybrid, merlin, lanrebayode77 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-10-debita-judging/issues/890
- **Contest**: https://app.sherlock.xyz/audits/contests/627

### Keywords for Search

`vulnerability`

