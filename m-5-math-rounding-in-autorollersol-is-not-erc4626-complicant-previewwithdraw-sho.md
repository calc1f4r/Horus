---
# Core Classification
protocol: Sense
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3563
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/19
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-sense-judging/issues/30

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - rounding
  - erc4626

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ctf\_sec
---

## Vulnerability Title

M-5: Math rounding in AutoRoller.sol is not ERC4626-complicant: previewWithdraw should round up.

### Overview


This bug report is about an issue found in the AutoRoller.sol of the Sense Finance project. The issue is that the math rounding implemented in the previewWithdraw function is not compliant with ERC4626. According to the Ethereum Improvement Proposal (EIP) 4626, when calculating how many shares to issue to a user for a certain amount of the underlying tokens they provide, or when determining the amount of the underlying tokens to transfer to them for returning a certain amount of shares, it should round down. However, when calculating the amount of shares a user has to supply to receive a given amount of the underlying tokens, or when calculating the amount of underlying tokens a user has to provide to receive a certain amount of shares, it should round up.

The bug was found by ctf\_sec and the code snippet can be found at https://github.com/sherlock-audit/2022-11-sense/blob/main/contracts/src/AutoRoller.sol#L528-L567. The impact of this bug is that other protocols that integrate with Sense finance AutoRoller.sol might wrongly assume that the functions handle rounding as per ERC4626 expectation, which can lead to a wide range of issues for both parties.

The recommendation is to round up in previewWithdraw using mulDivUp and divWadUp. The fix was implemented and verified and can be found at https://github.com/sense-finance/auto-roller/pull/22. The severity of the issue was suggested to be medium.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-sense-judging/issues/30 

## Found by 
ctf\_sec

## Summary

Math rounding in AutoRoller.sol is not ERC4626-complicant: previewWithdraw should round up.

## Vulnerability Detail

Per EIP 4626's Security Considerations (https://eips.ethereum.org/EIPS/eip-4626)

> Finally, ERC-4626 Vault implementers should be aware of the need for specific, opposing rounding directions across the different mutable and view methods, as it is considered most secure to favor the Vault itself during calculations over its users:

> If (1) it’s calculating how many shares to issue to a user for a certain amount of the underlying tokens they provide or (2) it’s determining the amount of the underlying tokens to transfer to them for returning a certain amount of shares, it should round down.
If (1) it’s calculating the amount of shares a user has to supply to receive a given amount of the underlying tokens or (2) it’s calculating the amount of underlying tokens a user has to provide to receive a certain amount of shares, it should round up.

Then previewWithdraw in AutoRoller.sol should round up.

The original implementation for previewWithdraw in Solmate ERC4626 is:

```solidity
    function previewWithdraw(uint256 assets) public view virtual returns (uint256) {
        uint256 supply = totalSupply; // Saves an extra SLOAD if totalSupply is non-zero.

        return supply == 0 ? assets : assets.mulDivUp(supply, totalAssets());
    }
```

It is rounding up, however in the implementation of the AutoRoller.sol#previewWith is not round up.

```solidity
for (uint256 i = 0; i < 20;) { // 20 chosen as a safe bound for convergence from practical trials.
    if (guess > supply) {
        guess = supply;
    }

    int256 answer = previewRedeem(guess.safeCastToUint()).safeCastToInt() - assets.safeCastToInt();

    if (answer >= 0 && answer <= assets.mulWadDown(0.001e18).safeCastToInt() || (prevAnswer == answer)) { // Err on the side of overestimating shares needed. Could reduce precision for gas efficiency.
        break;
    }

    if (guess == supply && answer < 0) revert InsufficientLiquidity();

    int256 nextGuess = guess - (answer * (guess - prevGuess) / (answer - prevAnswer));
    prevGuess  = guess;
    prevAnswer = answer;
    guess      = nextGuess;

    unchecked { ++i; }
}

return guess.safeCastToUint() + maxError; // Buffer for pow discrepancies.
```

note the line:

```solidity
  int256 answer = previewRedeem(guess.safeCastToUint()).safeCastToInt() - assets.safeCastToInt();
```

previewRedeem is round down.

and later we update guess and return guess

```solidity
    int256 nextGuess = guess - (answer * (guess - prevGuess) / (answer - prevAnswer));
    prevGuess  = guess;
    prevAnswer = answer;
    guess      = nextGuess;
```

and

```solidity
 return guess.safeCastToUint() + maxError; // Buffer for pow discrepancies.
```

when calculating the the nextGuess, the code does not round up.

```solidity
int256 nextGuess = guess - (answer * (guess - prevGuess) / (answer - prevAnswer));
```

## Impact

Other protocols that integrate with Sense finance AutoRoller.sol might wrongly assume that the functions handle rounding as per ERC4626 expectation. Thus, it might cause some intergration problem in the future that can lead to wide range of issues for both parties.

## Code Snippet

https://github.com/sherlock-audit/2022-11-sense/blob/main/contracts/src/AutoRoller.sol#L528-L567

## Tool used

Manual Review

## Recommendation

Round up in previewWithdraw using mulDivUp and divWadUp

## Discussion

**jparklev**

Our understanding is that `nextGuess` does not need to be rounded up since it's just a "guess" that is confirmed or denied in how close the "answer" is to what we're looking for. So the rounding needs to be in the answer assessment stage.

In addition, as our comment in the answer inequality says, we do overestimate the shares needed, which is equivalent to rounding up. Perhaps one could make the case that the inequality should be `> 0` rather than `>= 0` so that exact matches from the rounded down `previewRedeem` don't make it through

Given the above, we're ok accepting this issue, but disagree with the severity

**jparklev**

Fix: https://github.com/sense-finance/auto-roller/pull/22

**Evert0x**

@jparklev What severity are you suggesting?

**jparklev**

> @jparklev What severity are you suggesting?

`medium` would be our suggestion

**aktech297**

Verified the fix. As @jparklev mentioned, `rounding needs to be in the answer assessment stage`, the fix is not related to rounding up. It is related to inequality. so, the fix is to check for `> 0` rather than `>= 0` so that exact matches from the rounded down `previewRedeem` don't make it through.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Sense |
| Report Date | N/A |
| Finders | ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-sense-judging/issues/30
- **Contest**: https://app.sherlock.xyz/audits/contests/19

### Keywords for Search

`Rounding, ERC4626`

