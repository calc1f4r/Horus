---
# Core Classification
protocol: Foundry DeFi Stablecoin CodeHawks Audit Contest
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34427
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0
source_link: none
github_link: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin

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
  - HollaDieWaldfee
  - ljj
  - Rotcivegaf
  - TheSchnilch
  - Bughunter101
---

## Vulnerability Title

Anyone can burn **DecentralizedStableCoin** tokens with `burnFrom` function

### Overview


This bug report is about a vulnerability in the DecentralizedStableCoin (DSC) contract. The issue is that anyone can burn DSC tokens using the burnFrom function, which is inherited from the OZ ERC20Burnable contract. This bypasses the onlyOwner modifier, which means that anyone can burn tokens without permission. The impact of this bug is that it allows for unauthorized burning of tokens. The recommendation is to block the burnFrom function in the OZ ERC20Burnable contract to prevent this vulnerability.

### Original Finding Content

## Summary

Anyone can burn `DSC` tokens with [`burnFrom`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/0a25c1940ca220686588c4af3ec526f725fe2582/contracts/token/ERC20/extensions/ERC20Burnable.sol#L35-L38) function inherited of **OZ ERC20Burnable** contract

## Vulnerability Details

In the **DecentralizedStableCoin** contract the `burn` function is `onlyOwner` and is used by **DSCEngine** contract, which is the owner of **DecentralizedStableCoin** contract

## Impact

The tokens can be burned with `burnFrom` function bypassing the `onlyOwner` modifier of the `burn` functions

## Recommendations

Block the `burnFrom` function of **OZ ERC20Burnable** contract

```solidity
@@ -40,6 +40,7 @@ contract DecentralizedStableCoin is ERC20Burnable, Ownable {
     error DecentralizedStableCoin__MustBeMoreThanZero();
     error DecentralizedStableCoin__BurnAmountExceedsBalance();
     error DecentralizedStableCoin__NotZeroAddress();
+    error DecentralizedStableCoin__BlockFunction();

     constructor() ERC20("DecentralizedStableCoin", "DSC") {}

@@ -54,6 +55,10 @@ contract DecentralizedStableCoin is ERC20Burnable, Ownable {
         super.burn(_amount);
     }

+    function burnFrom(address, uint256) public pure override {
+        revert DecentralizedStableCoin__BlockFunction();
+    }
+
     function mint(address _to, uint256 _amount) external onlyOwner returns (bool) {
         if (_to == address(0)) {
             revert DecentralizedStableCoin__NotZeroAddress();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Foundry DeFi Stablecoin CodeHawks Audit Contest |
| Report Date | N/A |
| Finders | HollaDieWaldfee, ljj, Rotcivegaf, TheSchnilch, Bughunter101, ABA, klaus, lwltea, BAHOZ, hoshiyari, TorpedopistolIxc41, alexzoid, Qiezie, 0x4non, Tripathi |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin
- **Contest**: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0

### Keywords for Search

`vulnerability`

