---
# Core Classification
protocol: Shiny
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64686
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Shiny-Security-Review.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-02] Hardcoded 6-decimal Stablecoin Assumptions Brick Protocol on 18-decimal Deployments

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

Note: this issue is valid if the protocol deploys in chains like BSC

1. In the BSC chain, a stable coin with $8B in circulation has 18 decimals: [address](https://bscscan.com/token/0x55d398326f99059ff775485246999027b3197955)
2. Search other stablecoins, here at https://bscscan.com/tokens. They are mostly of 18 decimals

Multiple core parameters are hardcoded as if the payment token ("USDC") always uses **6 decimals** (multiplying by `10**6`).
If the deployed payment token uses **18 decimals** (common for stables on some chains), these constants become off by 10^12,
causing critical functionality to revert or enforce meaningless limits.

Specifically:

- `PawnShop.MAX_LOAN_AMOUNT` is expressed in 6-decimal units, so any realistic 18-decimal loan amount becomes “too high” and reverts.
- `RWA.MIN_SELLBACK_AMOUNT` is intended to represent “1 USDC”, but on 18 decimals, it becomes dust, so the minimum sellback policy is not enforced.
- `Treasury.maxTransferPerCall` defaults to a 6-decimal unit limit, so `transferWithSignature()` reverts for normal 18-decimal amounts until an admin updates the value.

## Location of Affected Code

File: [Audit_Submission/src/Pawn.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Audit_Submission.zip)

```solidity
uint256 public constant MAX_LOAN_AMOUNT = 1_000_000 * 10**6;

if (offerAmount == 0 || offerAmount > MAX_LOAN_AMOUNT) revert InvalidAmount();
```

File: [Audit_Submission/src/sRWA.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Audit_Submission.zip)

```solidity
uint256 public constant MIN_SELLBACK_AMOUNT = 1 * 10**6;

if (usdcAmount < MIN_SELLBACK_AMOUNT) revert InvalidAmount();
```

File: [Audit_Submission/src/Treasury.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Audit_Submission.zip)

```solidity
uint256 public maxTransferPerCall = 100_000 * 10**6;

if (limit == type(uint256).max) limit = maxTransferPerCall;
if (amount > limit) revert AmountExceedsMaxTransfer();
```

## Impact

- **Protocol bricking on 18-decimals deployments**: borrowers cannot take “normal” loans because `pawn()` reverts with `InvalidAmount()` for realistic values.
- **Broken economic constraint**: `MIN_SELLBACK_AMOUNT` no longer enforces “minimum 1 token”; users can sell back for dust amounts if the backend signs it.
- **Operational failure risk**: Treasury payouts revert with `AmountExceedsMaxTransfer()` until `maxTransferPerCall` is manually updated.

## Proof of Concept

Run it in `test/System.t.sol`

```solidity
function test_POC_18DecimalsStable_Hardcoded1e6_Assumptions_BrickOrBreakLimits() public {
    /**
     * This POC demonstrates a real deployment hazard:
     * the protocol hardcodes several "USDC has 6 decimals" constants (x * 10**6),
     * but many chains/tokens (e.g. BSC stables) use 18 decimals.
     *
     * In THIS test suite, `MockUSDC` inherits OpenZeppelin `ERC20`, which uses 18 decimals by default.
     * So amounts like 1e18 represent "1 whole token", while 1e6 represents "0.000000000001 token".
     *
     * We prove all 3 issues in one flow:
     *  (1) PawnShop.MAX_LOAN_AMOUNT is set to 1_000_000 * 1e6 (6-decimal units).
     *      With an 18-decimal token, even a 1-token loan (1e18) is > MAX_LOAN_AMOUNT and reverts.
     *  (2) RWA.MIN_SELLBACK_AMOUNT is set to 1 * 1e6, intended to mean "1 USDC".
     *      With an 18-decimal token, this is dust (1e-12 token), so the "min 1 token" policy is not enforced.
     *  (3) Treasury.maxTransferPerCall defaults to 100_000 * 1e6, also 6-decimals units.
     *      With an 18-decimal token, even a 1-token payout exceeds the limit until the admin updates it.
     */
    assertEq(usdc.decimals(), 18);

    // 1 whole token in base units for an 18-decimal ERC20.
    uint256 oneToken = 1e18;

    /* =============================================================
     * (1) PawnShop MAX_LOAN_AMOUNT bricks normal loans on 18-decimals.
     * ============================================================= */
    {
        uint256 tokenId = 1;

        // MAX_LOAN_AMOUNT is 1_000_000 * 1e6 = 1e12 base units.
        // On an 18-decimal token, 1e12 base units is only 0.000001 token.
        assertEq(pawnShop.MAX_LOAN_AMOUNT(), 1_000_000 * 10**6);
        assertGt(oneToken, pawnShop.MAX_LOAN_AMOUNT());

        // Even with valid signatures, the call reverts before signature verification due to the hardcoded max amount.
        PawnCall memory c = _buildPawnCall(user, tokenId, 7, oneToken, block.timestamp + 1 hours);

        // Approve first (this should succeed). Then prove the pawn() itself is bricked by the hardcoded MAX_LOAN_AMOUNT.
        vm.prank(user);
        rwa.approve(address(pawnShop), tokenId);

        vm.expectRevert(PawnShop.InvalidAmount.selector);
        _pawnWithCall(user, c, false);

        // Sanity: pawn reverted, so the NFT was not transferred.
        assertEq(rwa.ownerOf(tokenId), user);
    }

    /* =============================================================
     * (2) RWA MIN_SELLBACK_AMOUNT becomes dust on 18-decimal tokens.
     * ============================================================= */
    uint256 userBalBeforeSell = usdc.balanceOf(user);
    {
        uint256 tokenId = 1;
        uint256 sellAmount = rwa.MIN_SELLBACK_AMOUNT(); // 1 * 1e6 base units
        assertEq(sellAmount, 1 * 10**6);

        // On 18 decimals, this is far less than 1 whole token, so the intended "min 1 token" policy is not enforced.
        assertLt(sellAmount, oneToken);

        uint256 validUntil = block.timestamp + 1 hours;
        uint256 nonce = rwa.nonces(user);
        bytes memory sellSig = _signSellback(backendPk, tokenId, sellAmount, validUntil, nonce);
        bytes32 opHash = keccak256(abi.encode("SELLBACK", tokenId, sellAmount, nonce, user));
        bytes memory treasSig = _signTreasury(backendPk, user, sellAmount, validUntil, opHash);

        // This succeeds because `sellAmount` >= MIN_SELLBACK_AMOUNT (even though it's dust in 18-decimal terms).
        vm.prank(user);
        rwa.burnForSellback(tokenId, sellAmount, validUntil, sellSig, treasSig);

        assertEq(usdc.balanceOf(user), userBalBeforeSell + sellAmount);
        vm.expectRevert();
        rwa.ownerOf(tokenId); // tokenId 1 is burned
    }

    /* =============================================================
     * (3) Treasury maxTransferPerCall is also 6-decimals by default.
     * ============================================================= */
    {
        // Create a new approved contract so we can call `transferWithSignature` from an authorized sender.
        TreasurySigReplayer replayer;
        vm.startPrank(owner);
        replayer = new TreasurySigReplayer(treasury);
        treasury.approveContractForTransfers(address(replayer));
        vm.stopPrank();

        // Try a "normal" 1-token payout.
        uint256 validUntil = block.timestamp + 1 hours;
        bytes32 opHash = keccak256("POC_TREASURY_LIMIT_18_DECIMALS");
        bytes memory sig = _signTreasury(backendPk, user, oneToken, validUntil, opHash);

        // This fails because Treasury defaults to maxTransferPerCall = 100_000 * 1e6 (6-decimals units).
        // In 18-decimal terms, that limit is tiny, so even 1 token exceeds it.
        assertEq(treasury.maxTransferPerCall(), 100_000 * 10**6);
        assertGt(oneToken, treasury.maxTransferPerCall());

        vm.expectRevert(Treasury.AmountExceedsMaxTransfer.selector);
        replayer.replayTreasurySignature(user, oneToken, validUntil, opHash, sig);

        // Admin can "fix" this after deployment by updating the limit to 18-decimal units,
        // e.g. 100_000 tokens = 100_000 * 1e18.
        vm.startPrank(owner);
        treasury.setMaxTransferPerCall(100_000 * oneToken);
        // Fund Treasury so the post-fix payout doesn't fail the balance check.
        usdc.mint(address(treasury), oneToken);
        vm.stopPrank();

        uint256 userBalBeforePayout = usdc.balanceOf(user);
        replayer.replayTreasurySignature(user, oneToken, validUntil, opHash, sig);
        assertEq(usdc.balanceOf(user), userBalBeforePayout + oneToken);
    }
}
```

## Recommendation

- Remove `10**6` hardcoding for the payment token.
- Make thresholds **decimals-aware** by :
  - **Passing `tokenDecimals` / `unit` as a constructor parameter**

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Shiny |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Shiny-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

