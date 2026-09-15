---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27600
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
finders_count: 8
finders:
  - Maroutis
  - marqymarq10
  - hash
  - dipp
  - ZedBlockchain
---

## Vulnerability Title

The transfer of ERC-20 tokens with blacklist functionality in process functions can lead to stuck vaults

### Overview


This bug report is about the potential of a DoS (Denial of Service) of the entire strategy vault when transferring ERC-20 tokens with blacklist functionality. The system is not in an Open state when a keeper bot interacts with such a process function, and if the call to such a function reverts, the status can not be updated back to Open. This could lead to a situation where the vault is stuck in a given status and all users experience a DoS.

The attack flow could for example look like this: a blacklisted user calls withdraw with the wish to withdraw USDC, the withdraw function passes and status is updated to GMXTypes.Status.Withdraw, Keeper calls the processWithdraw function, transferring USDC tokens to blacklisted user reverts, and therefore the vault is stuck inside GMXTypes.Status.Withdraw status and all users experience a DoS.

The impact of this bug is a DoS of the entire strategy vault, as the status can no longer be updated to Open until the user is no longer blacklisted. This could potentially take forever and force the owners to take emergency action.

The bug was identified through manual review. The recommended solution is to use a two-step process instead of transferring the ERC-20 tokens directly to a user in the process functions. This means creating another contract whose only purpose is to hold assets and store the information about which address is allowed to withdraw how many of the specified tokens. In the process functions, send the funds to this new contract along with this information instead. This way, if a user has been blacklisted, the DoS only exists for that specific user and for the rest of the users the system continues to function normally.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXDeposit.sol#L212-L217">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXDeposit.sol#L212-L217</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXDeposit.sol#L348-L349">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXDeposit.sol#L348-L349</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXWithdraw.sol#L193-L194">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXWithdraw.sol#L193-L194</a>


## Summary

Inside a few process functions are ERC-20 tokens transfered which could potentially have a blacklist functionality. This can lead to a DoS of the strategy vault. If for example, a blacklisted user withdraws funds.

## Vulnerability Details

Some ERC-20 tokens like for example USDC (which is used by the system) have the functionality to blacklist specific addresses, so that they are no longer able to transfer and receive tokens. Sending funds to these addresses will lead to a revert.
A few of the process functions inside the deposit and withdraw contracts transfer ERC-20 tokens to addresses which could potentially be blacklisted. The system is not in an Open state when a keeper bot interacts with such a process function, and if the call to such a function reverts, the status can not be updated back to Open. Therefore, it will remain in the given status and a DoS for all users occurs. The only possibility that DoS stops would be when the user is no longer blacklisted, which can potentially last forever.

The attack flow (could be accidental) would for example look like this:

- USDC Blacklisted user calls withdraw with the wish to withdraw USDC
- withdraw function passes and status is updated to GMXTypes.Status.Withdraw
- Keeper calls the processWithdraw function
- Transferring USDC tokens to blacklisted user reverts
- Therefore vault is stuck inside GMXTypes.Status.Withdraw status and all users experience a DoS

Here are the code snippets of these dangerous transfers inside process functions:

```jsx
function processDepositCancellation(
  GMXTypes.Store storage self
) external {
  GMXChecks.beforeProcessDepositCancellationChecks(self);
	...
	// Transfer requested withdraw asset to user
	IERC20(self.depositCache.depositParams.token).safeTransfer(
		self.depositCache.user,
		self.depositCache.depositParams.amt
	);
  ...
  self.status = GMXTypes.Status.Open;

  emit DepositCancelled(self.depositCache.user);
}
```

```jsx
function processDepositFailureLiquidityWithdrawal(
  GMXTypes.Store storage self
) public {
  GMXChecks.beforeProcessAfterDepositFailureLiquidityWithdrawal(self);
	...
  // Refund user the rest of the remaining withdrawn LP assets
  // Will be in tokenA/tokenB only; so if user deposited LP tokens
  // they will still be refunded in tokenA/tokenB
  self.tokenA.safeTransfer(self.depositCache.user, self.tokenA.balanceOf(address(this)));
  self.tokenB.safeTransfer(self.depositCache.user, self.tokenB.balanceOf(address(this)));
	...
  self.status = GMXTypes.Status.Open;
}
```

```jsx
function processWithdraw(
  GMXTypes.Store storage self
) external {
  GMXChecks.beforeProcessWithdrawChecks(self);

  try GMXProcessWithdraw.processWithdraw(self) {
    if (self.withdrawCache.withdrawParams.token == address(self.WNT)) {
			...
    } else {
      // Transfer requested withdraw asset to user
      IERC20(self.withdrawCache.withdrawParams.token).safeTransfer(
        self.withdrawCache.user,
        self.withdrawCache.tokensToUser
      );
    }

    // Transfer any remaining tokenA/B that was unused (due to slippage) to user as well
    self.tokenA.safeTransfer(self.withdrawCache.user, self.tokenA.balanceOf(address(this)));
    self.tokenB.safeTransfer(self.withdrawCache.user, self.tokenB.balanceOf(address(this)));
		
		...

    self.status = GMXTypes.Status.Open;
  }
	...
}
```

## Impact

DoS of the entire strategy vault, as the status can no longer be updated to Open until the user is no longer blacklisted. This can potentially take forever and forces the owners to take emergency action.

## Tools Used

Manual Review

## Recommendations

Instead of transferring the ERC-20 tokens directly to a user in the process functions, use a two-step process instead. For example, create another contract whose only purpose is to hold assets and store the information about which address is allowed to withdraw how many of the specified tokens. In the process functions, send the funds to this new contract along with this information instead. So if a user has been blacklisted, the DoS only exists for that specific user and for the rest of the users the system continues to function normally.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | Maroutis, marqymarq10, hash, dipp, ZedBlockchain, Cosine, tychaios |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

