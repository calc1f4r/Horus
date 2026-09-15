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
solodit_id: 64690
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

[L-05] Unbounded Fee Parameters Allow Abusive Fees and Redemption DoS

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

`PawnShop` charges a fee (in basis points) on top of the borrowed principal when a borrower redeems their NFT via `redeem(...)` (context).

However, `setFees(...)` allows `MANAGER_ROLE` to set `fee7Days` and `fee30Days` to any `uint16` value, with no upper bound (e.g., `<= BASIS_POINTS`) and no sanity checks (problem).

This means a manager can set fees to values that make redemption economically impossible (or unexpectedly expensive), effectively trapping users or extracting arbitrary value at repayment time (impact).

## Location of Affected Code

File: [Pawn.sol#L111-L115](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Pawn.sol#L111-L115)

```solidity
function setFees(uint16 _fee7Days, uint16 _fee30Days) external onlyRole(MANAGER_ROLE) {
    // @audit No bounds checks (e.g., <= BASIS_POINTS)
    fee7Days = _fee7Days;
    fee30Days = _fee30Days;
    emit FeesUpdated(_fee7Days, _fee30Days);
}
```

## Impact

- **Redemption DoS**: Fees can be set so high that borrowers cannot (or will not) repay.
- **Unexpected user loss**: Borrowers who expected fixed or bounded fees can be forced into paying excessive fees to redeem collateral.

## Proof of Concept

1. User pawns an NFT.
2. Manager calls `setFees(65_535, 65_535)`.
3. `redeem(...)` now requires paying principal + ~655.35% fee, which will likely be infeasible for most borrowers.

## Recommendation

Enforce bounds (example):

- `require(_fee7Days <= BASIS_POINTS && _fee30Days <= BASIS_POINTS)`

## Team Response

Fixed.

## [I-01] Burned UUIDs Can Be Re-Minted

## Severity

Informational Risk

## Description

The `RWA.mint(...)` assigns a `uuid` to each token and enforces uniqueness by tracking `_usedUUIDs[uuid]` (context).

However, all burn paths (`burn(...)`, `burnForRedemption(...)`, `burnForSellback(...)`) delete `_usedUUIDs[uuid]`, making the UUID available for reuse (problem).

This means the on-chain guarantee is “no two _currently existing_ tokens share a UUID”, not “a UUID is unique forever”. If off-chain systems treat `uuid` as a permanent physical-asset identifier, UUID reuse can lead to confusion or allow re-issuance of previously redeemed assets without an explicit re-deposit workflow (impact).

## Location of Affected Code

File: [sRWA.sol#L140-L152](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/sRWA.sol#L140-L152)

```solidity
function mint(address to, string calldata uuid) external onlyRole(MINTER_ROLE) nonReentrant whenNotPaused {
    // code
    if (_usedUUIDs[uuid]) revert UUIDAlreadyExists();
    // code
    _tokenUUID[tokenId] = uuid;
    _usedUUIDs[uuid] = true;
    _safeMint(to, tokenId);
}
```

File: [sRWA.sol#L200-L207](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/sRWA.sol#L200-L207)

```solidity
function burnForRedemption(uint256 tokenId) external onlyTokenOwner(tokenId) whenNotPaused {
    string memory uuid = _tokenUUID[tokenId];
    // @audit UUID becomes reusable after burn
    delete _usedUUIDs[uuid];
    delete _tokenUUID[tokenId];
    _burn(tokenId);
}
```

## Impact

UUID uniqueness is not permanent.

## Proof of Concept

1. Admin mints a token with `uuid = "UUID-123"`.
2. Owner calls `burnForRedemption(tokenId)`.
3. Admin mints a new token again with `uuid = "UUID-123"`; the mint succeeds because `_usedUUIDs["UUID-123"]` was deleted.

## Recommendation

Decide which uniqueness guarantee is required:

- If UUID must be globally unique forever, **do not delete** `_usedUUIDs[uuid]` on burn.

## Team Response

Acknowledged.

## [I-02] Redundant `usedSignatures` Tracking Alongside Nonce-Based Replay Protection

## Severity

Informational Risk

## Description

`PawnShop` and `RWA` apply two replay protections to EIP-712 signatures:

- Per-user `nonces[user]` included in the signed payload and incremented on success.
- A global `usedSignatures[digest]` mapping.

For these flows, the nonce already prevents replay for the same sender: after a successful call, the contract computes the digest using `nonce + 1`, so the old signature no longer verifies. As a result, `usedSignatures` is largely redundant and adds an extra storage write.

Note: `Treasury.transferWithSignature(...)` does not include a nonce, so `usedSignatures` (or adding a nonce/salt) is required there to prevent replay until `validUntil`.

## Location of Affected Code

File: [Pawn.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Pawn.sol)

File: [sRWA.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/sRWA.sol)

- `usedSignatures[digest]` check + write in signature validation paths
- `nonces[msg.sender]++` performed after successful validation

File: [Treasury.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Treasure.sol)

- Signature payload lacks a nonce; `usedSignatures` provides replay protection until `validUntil`

## Impact

Each successful signature-based call in `PawnShop`/`RWA` incurs an extra `SSTORE` for `usedSignatures[digest]`.

## Recommendation

In `PawnShop` and `RWA`, remove `usedSignatures` and rely on nonces for replay protection.

## Team Response

Fixed.

## [I-03] Configuration Mismatch Risk Across `backendSigner` and `treasury` Addresses

## Severity

Informational Risk

## Description

The system relies on coordinated configuration across three separate contracts:

- `PawnShop` validates a backend signature (`pawnSignature`) using its own `backendSigner`.
- `RWA` validates a backend signature (`sellbackSignature`) using its own `backendSigner`.
- `Treasury` validates a backend signature (`treasurySignature`) using _its_ `backendSigner`, and also requires the caller to be allowlisted.

These settings are each managed independently via admin setters (context).

However, there is no on-chain enforcement that these configuration values remain consistent (problem).

This means a simple operational misconfiguration (e.g., updating `PawnShop.backendSigner` but not `Treasury.backendSigner`, or pointing `PawnShop.treasury` at the wrong address) can halt core flows like `pawn(...)` and `burnForSellback(...)` (impact).

## Location of Affected Code

File: [Pawn.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Pawn.sol)

```solidity
address public treasury;
address public backendSigner;

function setTreasury(address _treasury) external onlyRole(DEFAULT_ADMIN_ROLE) {
    // code
    treasury = _treasury;
}

function setBackendSigner(address _signer) external onlyRole(DEFAULT_ADMIN_ROLE) {
    // code
    backendSigner = _signer;
}
```

File: [Treasure.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Treasure.sol)

```solidity
address public backendSigner;

function setBackendSigner(address _signer) external onlyRole(DEFAULT_ADMIN_ROLE) {
    // code
    backendSigner = _signer;
}
```

File: [sRWA.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/sRWA.sol)

```solidity
address public treasury;
address public backendSigner;

function setTreasury(address _treasury) external onlyRole(DEFAULT_ADMIN_ROLE) {
    // code
    treasury = _treasury;
}

function setBackendSigner(address _signer) external onlyRole(DEFAULT_ADMIN_ROLE) {
    // code
    backendSigner = _signer;
}
```

## Impact

Mismatched signers or wrong treasury addresses cause signature checks or external calls to revert, halting user actions.

## Proof of Concept

1. Admin updates `PawnShop.backendSigner` to a new key.
2. Admin forgets to update `Treasury.backendSigner`.
3. Users can no longer successfully call `pawn(...)` because the pawn signature and treasury signature are validated against different signer keys across contracts.

## Recommendation

Use a **single configuration source of truth**, e.g. a registry contract that stores `backendSigner`/`treasury` addresses read by all modules.

## Team Response

Acknowledged.

## [I-04] PawnShop `MAX_LOAN_AMOUNT` Can Exceed Treasury

## Severity

Informational Risk

## Description

`PawnShop` validates offers up to its hard cap `MAX_LOAN_AMOUNT = 1_000_000 * 10**6`, but the funding path `Treasury.transferWithSignature(...)` applies a per-call limit from `contractTransferLimits[msg.sender]` (defaulting to `maxTransferPerCall = 100_000 * 10**6` when unset).

As a result, `PawnShop` can accept and sign offers up to 1,000,000 USDC that will deterministically revert in Treasury for amounts above 100,000 USDC unless the transfer limit is explicitly raised.

## Location of Affected Code

File: [Pawn.sol#L62](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Pawn.sol#L62)

```solidity
// max loan is 1 million usdc
uint256 public constant MAX_LOAN_AMOUNT = 1_000_000 * 10**6;
```

File: [Treasure.sol](https://github.com/ShinyUrban/SmartContracts/blob/f49b5db73b297552666783ed587cf0818ef86b75/Treasure.sol)

```solidity
mapping(address => uint256) public contractTransferLimits;
uint256 public maxTransferPerCall = 100_000 * 10**6;

function transferWithSignature(address recipient, uint256 amount, uint256 validUntil, bytes32 operationHash, bytes calldata signature) external nonReentrant whenNotPaused {
    // code
    uint256 limit = contractTransferLimits[msg.sender];
    if (limit == type(uint256).max) limit = maxTransferPerCall;

    if (amount > limit) revert AmountExceedsMaxTransfer();
    if (amount > usdc.balanceOf(address(this))) revert InsufficientBalance();
    // code
}
```

## Impact

Users can waste gas on offers that pass `PawnShop` checks but fail funding.

## Recommendation

Align the constraints:

- Either lower `PawnShop.MAX_LOAN_AMOUNT` to match the effective Treasury limit, or
- Raise/configure `Treasury.maxTransferPerCall` / `contractTransferLimits[PawnShop]` to support the intended max loan.

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

