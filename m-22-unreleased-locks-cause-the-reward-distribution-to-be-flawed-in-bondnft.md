---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6352
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/630

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - HollaDieWaldfee
  - __141345__
  - Ermaniwe
  - Ruhum
  - wait
---

## Vulnerability Title

[M-22] Unreleased locks cause the reward distribution to be flawed in BondNFT

### Overview


This bug report is about a vulnerability that exists in the BondNFT contract code. It is found in lines 150 and 225 of the code. The issue is that after a lock has expired, it does not receive any rewards and other existing bonds also do not receive the full amount of tokens due to the unreleased locks. This causes bond owners to receive less rewards than they should. This vulnerability is rated as HIGH since it can cause a loss of funds for every bond holder. 

The vulnerability can be tested using the 09.Bonds.js code. The `totalShares` value is only updated after a lock is released. To mitigate this vulnerability, only shares belonging to an active bond should be used for the distribution logic.

### Original Finding Content


<https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/BondNFT.sol#L150> 

<https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/BondNFT.sol#L225>

### Impact

After a lock has expired, it doesn't get any rewards distributed to it. But, unreleased locks cause other existing bonds to not receive the full amount of tokens either. The issue is that as long as the bond is not released, the `totalShares` value isn't updated. Everybody receives a smaller cut of the distribution. Thus, bond owners receive less rewards than they should.

A bond can be released after it expired by the owner of it. If the owner doesn't release it for 7 days, anybody else can release it as well. As long as the owner doesn't release it, the issue will be in effect for at least 7 epochs.

Since this causes a loss of funds for every bond holder I rate it as HIGH. It's likely to be an issue since you can't guarantee that bonds will be released the day they expire.

### Proof of Concept

Here's a test showcasing the issue:

```js
// 09.Bonds.js

    it.only("test", async function () {
      await stabletoken.connect(owner).mintFor(owner.address, ethers.utils.parseEther("100"));
      await lock.connect(owner).lock(StableToken.address, ethers.utils.parseEther("100"), 100);
      await stabletoken.connect(owner).mintFor(user.address, ethers.utils.parseEther("1000"));
      await lock.connect(user).lock(StableToken.address, ethers.utils.parseEther("1000"), 10);
      await stabletoken.connect(owner).mintFor(owner.address, ethers.utils.parseEther("1000"));
      await bond.distribute(stabletoken.address, ethers.utils.parseEther("1000"));

      await network.provider.send("evm_increaseTime", [864000]); // Skip 10 days
      await network.provider.send("evm_mine");

      [,,,,,,,pending,,,] = await bond.idToBond(1);
      expect(pending).to.be.equals("499999999999999999986");
      [,,,,,,,pending,,,] = await bond.idToBond(2);
      expect(pending).to.be.equals("499999999999999999986");


      await stabletoken.connect(owner).mintFor(owner.address, ethers.utils.parseEther("1000"));
      await bond.distribute(stabletoken.address, ethers.utils.parseEther("1000"));

      await network.provider.send("evm_increaseTime", [86400 * 3]); // Skip 3 days
      await network.provider.send("evm_mine");

      // Bond 2 expired, so it doesn't receive any of the new tokens that were distributed
      [,,,,,,,pending,,,] = await bond.idToBond(2);
      expect(pending).to.be.equals("499999999999999999986");

      // Thus, Bond 1 should get all the tokens, increasing its pending value to 1499999999999999999960
      // But, because bond 2 wasn't released (`totalShares` wasn't updated), bond 1 receives less tokens than it should.
      // Thus, the following check below fails
      [,,,,,,,pending,,,] = await bond.idToBond(1);
      expect(pending).to.be.equals("1499999999999999999960");

      await lock.connect(user).release(2);

      expect(await stabletoken.balanceOf(user.address)).to.be.equals("1499999999999999999986");

    });
```

The `totalShares` value is only updated after a lock is released:

```sol
    function release(
        uint _id,
        address _releaser
    ) external onlyManager() returns(uint amount, uint lockAmount, address asset, address _owner) {
        Bond memory bond = idToBond(_id);
        require(bond.expired, "!expire");
        if (_releaser != bond.owner) {
            unchecked {
                require(bond.expireEpoch + 7 < epoch[bond.asset], "Bond owner priority");
            }
        }
        amount = bond.amount;
        unchecked {
            totalShares[bond.asset] -= bond.shares;
        // ... 
```

### Recommended Mitigation Steps

Only shares belonging to an active bond should be used for the distribution logic.

**[TriHaz (Tigris Trade) disputed and commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/630#issuecomment-1374438815):**
 > >Since this causes a loss of funds for every bond holder I rate it as HIGH. 
> 
> Funds are not lost, they will be redistributed when the bond is expired. 
> https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/BondNFT.sol#L180

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/630#issuecomment-1399439420):**
> I've asked the Warden for additional proof.  
> 
>*(Note: See [original submission](https://github.com/code-423n4/2022-12-tigris-findings/issues/630#issuecomment-1399439420) for proof.)*
>
> And believe that the finding is valid.
> 
> I have adapted the test to also claim after, and believe that the lost rewards cannot be received back (see POC and different values we get back).

**[Alex the Entreprenerd (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/630#issuecomment-1399439953):**
 > I have to agree with the Warden's warning, however, the `release` function is public, meaning anybody can break expired locks.
> 
> For this reason, I believe that Medium Severity is more appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | HollaDieWaldfee, __141345__, Ermaniwe, Ruhum, wait, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/630
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

