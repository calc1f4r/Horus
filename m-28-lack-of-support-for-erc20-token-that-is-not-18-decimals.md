---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25844
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/129

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - rvierdiiev
  - ladboy233
---

## Vulnerability Title

[M-28] Lack of support for ERC20 token that is not 18 decimals

### Overview


This bug report is about the lack of support for ERC20 tokens with decimals other than 18 in the PublicVault.sol implementation. The code in the PublicVault.sol is hardcoded to 18 decimals, which means that tokens with a different decimal precision will not function correctly. This is an issue because it can cause confusion and complicate integration across front-ends and other off-chain users. 

To illustrate this, the example of USDC is used, which is a token with 6 decimals. If this token is used, the convertToAssets() function will be broken. This is because the totalSupply is in 18 deimals, but the totalAssets is in 6 decimals, but the totalSupply should be 6 decimals as well to match the underlying token precision. In addition, the logic for liquidation ratio calculation is also broken because the hardcoded 1e18 is used.

The recommended mitigation steps for this bug are for the protocol to make the PublicVault.sol decimal match the underlying token decimals. This has been confirmed by SantiagoGregory (Astaria).

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L66><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L73>

Lack of support for ERC20 token that is not 18 decimals in PublicVault.sol.

### Proof of Concept

We need to look into the PublicVault.sol implementation

```solidity
contract PublicVault is VaultImplementation, IPublicVault, ERC4626Cloned {
```

the issue that is the decimal precision in the PublicVault is hardcoded to 18

```solidity
function decimals()
	public
	pure
	virtual
	override(IERC20Metadata)
returns (uint8)
{
	return 18;
}
```

According to

<https://eips.ethereum.org/EIPS/eip-4626>

> Although the convertTo functions should eliminate the need for any use of an EIP-4626 Vault’s decimals variable, it is still strongly recommended to mirror the underlying token’s decimals if at all possible, to eliminate possible sources of confusion and simplify integration across front-ends and for other off-chain users.

The solmate ERC4626 implementation did mirror the underlying token decimals

<https://github.com/transmissions11/solmate/blob/3998897acb502fa7b480f505138a6ae1842e8d10/src/mixins/ERC4626.sol#L38>

```solidity
constructor(
	ERC20 _asset,
	string memory _name,
	string memory _symbol
) ERC20(_name, _symbol, _asset.decimals()) {
	asset = _asset;
}
```

but the token decimals is over-written to 18 decimals.

<https://github.com/d-xo/weird-erc20#low-decimals>

Some tokens have low decimals (e.g. USDC has 6). Even more extreme, some tokens like Gemini USD only have 2 decimals.

For example, if the underlying token is USDC and has 6 decimals, the convertToAssets() function will be broken.

<https://github.com/transmissions11/solmate/blob/3998897acb502fa7b480f505138a6ae1842e8d10/src/mixins/ERC4626.sol#L130>

```solidity
function convertToAssets(uint256 shares) public view virtual returns (uint256) {
	uint256 supply = totalSupply; // Saves an extra SLOAD if totalSupply is non-zero.

	return supply == 0 ? shares : shares.mulDivDown(totalAssets(), supply);
}
```

The totalSupply is in 18 deimals, but the totalAssets is in 6 deciimals, but the totalSupply should be 6 decimals as well to match the underlying token precision.

There are place that the code assume the token is 18 decimals, if the token is not 18 decimals, the logic for liquidatoin ratio calculation is broken as well because the hardcoded 1e18 is used.

```solidity
s.liquidationWithdrawRatio = proxySupply
.mulDivDown(1e18, totalSupply())
.safeCastTo88();

currentWithdrawProxy.setWithdrawRatio(s.liquidationWithdrawRatio);
uint256 expected = currentWithdrawProxy.getExpected();

unchecked {
if (totalAssets() > expected) {
  s.withdrawReserve = (totalAssets() - expected)
	.mulWadDown(s.liquidationWithdrawRatio)
	.safeCastTo88();
} else {
  s.withdrawReserve = 0;
}
}
_setYIntercept(
s,
s.yIntercept -
  totalAssets().mulDivDown(s.liquidationWithdrawRatio, 1e18)
);
```

And in the claim function for WithdrawProxy.sol

```solidity
if (balance < s.expected) {
  PublicVault(VAULT()).decreaseYIntercept(
	(s.expected - balance).mulWadDown(1e18 - s.withdrawRatio)
  );
} else {
  PublicVault(VAULT()).increaseYIntercept(
	(balance - s.expected).mulWadDown(1e18 - s.withdrawRatio)
  );
}
```

### Recommended Mitigation Steps

We recommend the protocol make the PublicVault.sol decimal match the underlying token decimals.

**[SantiagoGregory (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/129)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | rvierdiiev, ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/129
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

