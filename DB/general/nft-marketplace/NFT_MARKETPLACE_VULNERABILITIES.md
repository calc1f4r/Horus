---
# Core Classification
protocol: generic
chain: everychain
category: nft_marketplace
vulnerability_type: marketplace_protocol_logic

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_guard | marketplace_protocol | attacker_action | fund_loss_or_nft_lock

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Marketplace
  - NFT_Collection
  - GnosisSafe
  - PaymentEscrow
  - Auction
  - Bridge
  - Vault
path_keys:
  - missing_guard | marketplace_protocol | callback_reentrancy | fund_theft
  - missing_guard | marketplace_protocol | residual_allowance | asset_theft
  - missing_guard | marketplace_protocol | fee_bypass | protocol_revenue_loss
  - missing_guard | marketplace_protocol | rental_callback_revert | griefing
  - missing_guard | marketplace_protocol | fallback_handler_swap | nft_hijack
  - missing_guard | marketplace_protocol | auction_frontrun | nft_theft
  - missing_guard | marketplace_protocol | bridge_erc721 | permanent_lock
  - missing_guard | marketplace_protocol | merkle_criteria | wrong_tokenid

# Attack Vector Details
attack_type: multiple
affected_component: marketplace_contracts

# Technical Primitives
primitives:
  - onERC721Received
  - safeTransferFrom
  - safeMint
  - approve
  - setApprovalForAll
  - setFallbackHandler
  - flashLoan
  - royaltyInfo
  - bridgeToken
  - fulfillOrder
  - stopRent
  - reclaimRentedItems
  - offerPunkForSaleToAddress

# Grep / Hunt-Card Seeds
code_keywords:
  - onERC721Received
  - setFallbackHandler
  - safeTransferFrom
  - _safeMint
  - flashLoan
  - royaltyInfo
  - reclaimRentedItems
  - stopRent
  - addCollateral
  - batchDeposit
  - migrateVault
  - bridgeToken
  - _getRoyalty
  - settlePayment
  - reservedAddress
  - totalAmt
  - identifierOrCriteria

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.8
financial_impact: high

# Context Tags
tags:
  - nft
  - marketplace
  - erc721
  - erc1155
  - rental
  - auction
  - royalty
  - bridge
  - gnosis_safe
  - flashloan

# Version Info
language: solidity
version: ">=0.8.0"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [reentrancy-safemint] | reports/nft_marketplace_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md | HIGH | Code4rena | 1255 |
| [residual-allowance] | reports/nft_marketplace_findings/h-12-malicious-users-can-exploit-residual-allowance-to-steal-assets.md | HIGH | Code4rena | 2993 |
| [auction-bypass] | reports/nft_marketplace_findings/h-03-a-majority-attack-can-easily-bypass-zora-auction-stage-in-openseaproposal-a.md | HIGH | Code4rena | 3304 |
| [fee-bypass] | reports/nft_marketplace_findings/h-08-users-can-avoid-paying-fees-while-trading-trustlessly-using-goloms-network-.md | HIGH | Code4rena | 8734 |
| [deposit-frontrun] | reports/nft_marketplace_findings/h-3-cryptopunks-nfts-may-be-stolen-via-deposit-frontrunning.md | HIGH | Sherlock | 6289 |
| [royalty-accounting] | reports/nft_marketplace_findings/m-08-loss-of-funds-for-traders-due-to-accounting-error-in-royalty-calculations.md | MEDIUM | Code4rena | 16253 |
| [flashloan-theft] | reports/nft_marketplace_findings/m-15-pool-tokens-can-be-stolen-via-privatepoolflashloan-function-from-previous-o.md | MEDIUM | Code4rena | 43394 |
| [royalty-permyriad] | reports/nft_marketplace_findings/incorrect-distribution-of-royalties.md | HIGH | OtterSec | 48857 |
| [seller-break-lock] | reports/nft_marketplace_findings/h-11-malicious-seller-forced-break-lockcapital.md | HIGH | Sherlock | 6620 |
| [paused-erc721-stuck] | reports/nft_marketplace_findings/m-12-paused-erc721erc1155-could-cause-stoprent-to-revert-potentially-causing-iss.md | MEDIUM | Code4rena | 30539 |
| [swap-nft-airdrop] | reports/nft_marketplace_findings/m-04-its-possible-to-swap-nft-token-ids-without-fee-and-also-attacker-can-wrap-u.md | MEDIUM | Code4rena | 6102 |
| [quest-burn-other-nft] | reports/nft_marketplace_findings/users-can-start-a-quest-using-as-input-and-burning-an-nft-they-do-not-own.md | HIGH | Halborn | 50494 |
| [guard-fallback-hijack] | reports/nft_marketplace_findings/h-02-an-attacker-is-able-to-hijack-any-erc721-erc1155-he-borrows-because-guard-i.md | HIGH | Code4rena | 30522 |
| [rental-grief-callback] | reports/nft_marketplace_findings/m-14-lender-of-a-pay-order-lending-can-grief-renter-of-the-payment.md | MEDIUM | Code4rena | 30541 |
| [rental-blocklist-stuck] | reports/nft_marketplace_findings/m-15-blocklisting-in-payment-erc20-can-cause-rented-nft-to-be-stuck-in-safe.md | MEDIUM | Code4rena | 30542 |
| [migration-burn] | reports/nft_marketplace_findings/h-09-malicious-user-could-burn-the-assets-after-a-successful-migration.md | HIGH | Code4rena | 2990 |
| [bridge-one-way] | reports/nft_marketplace_findings/tokenbridgebridgetoken-allows-1-way-erc721-bridging-causing-users-to-permanently.md | HIGH | Cyfrin | 33298 |
| [merkle-criteria] | reports/nft_marketplace_findings/m-01-merkle-tree-criteria-can-be-resolved-by-wrong-tokenids.md | MEDIUM | Code4rena | 2623 |
| [auction-debt-shortfall] | reports/nft_marketplace_findings/h-01-borrowers-may-earn-auction-proceeds-without-filling-the-debt-shortfall.md | HIGH | Code4rena | 6202 |
| [transferfrom-lock] | reports/nft_marketplace_findings/m-02-use-safetransferfrom-instead-of-transferfrom-for-erc721.md | MEDIUM | Code4rena | 8739 |
| [safemint-lock] | reports/nft_marketplace_findings/m-1-tomo-m3-use-safemint-instead-of-mint-for-erc721.md | MEDIUM | Sherlock | 3593 |
| [unstake-lock] | reports/nft_marketplace_findings/m-3-using-erc721transferfrom-instead-of-safetransferfrom-may-cause-the-users-nft.md | MEDIUM | Sherlock | 3595 |
| [mint-lock-vault] | reports/nft_marketplace_findings/risk-of-locked-assets-due-to-use-of-_mint-instead-of-_safemint.md | MEDIUM | TrailOfBits | 26446 |
| [dual-standard-erc721-1155] | reports/nft_marketplace_findings/h-06-some-real-world-nft-tokens-may-support-both-erc721-and-erc1155-standards-wh.md | HIGH | Code4rena | N/A |
| [cryptokitty-pause] | reports/nft_marketplace_findings/m-20-cryptokitty-and-cryptofighter-nft-can-be-paused-which-block-borrowing-repay.md | MEDIUM | Code4rena | N/A |
| [bounty-brick-nft] | reports/nft_marketplace_findings/h-2-adversary-can-brick-bounty-payouts-by-calling-fundbountytoken-but-funding-it.md | HIGH | Code4rena | N/A |
| [royalty-unfair-share] | reports/nft_marketplace_findings/m-07-royalty-recipients-will-not-get-fair-share-of-royalties.md | MEDIUM | Code4rena | N/A |
| [burn-nft-lockcapital] | reports/nft_marketplace_findings/h-11-malicious-seller-forced-break-lockcapital.md | HIGH | Sherlock | 6620 |

## Vulnerability Title

**NFT Marketplace & Protocol-Level Security Vulnerabilities** — Marketplace fee bypass, rental griefing, auction manipulation, guard bypass, bridge lock, and vault exploitation patterns across NFT trading protocols.

### Overview

NFT marketplace and protocol-level vulnerabilities arise from the complex interactions between marketplace contracts, NFT token standards, payment escrows, rental safes, auction houses, and bridge infrastructure. Unlike basic ERC721 token-level bugs, these patterns exploit the business logic and trust boundaries of the marketplace protocol layer — where callbacks, approvals, and multi-contract flows create attack surfaces for fund theft, NFT lock-up, and fee evasion.

#### Agent Quick View

- Root cause statement: "These vulnerabilities exist because NFT marketplace protocols fail to properly validate trust boundaries at callback entry points, approval scopes, fee enforcement paths, and multi-contract settlement flows, allowing attackers to steal assets, bypass fees, grief rentals, or permanently lock NFTs."
- Pattern key: `missing_guard | marketplace_protocol | attacker_action | fund_loss_or_nft_lock`
- Interaction scope: `multi_contract`
- Primary affected component(s): `Marketplace, Auction, PaymentEscrow, GnosisSafe/Guard, Bridge, Vault`
- Contracts involved: `Marketplace, NFT Collection, GnosisSafe, Guard, PaymentEscrow, AuctionHouse, TokenBridge, Migration, PrivatePool`
- Path keys: `fee_bypass`, `residual_allowance`, `callback_reentrancy`, `rental_callback_revert`, `fallback_handler_swap`, `auction_frontrun`, `bridge_erc721`, `merkle_criteria`
- High-signal code keywords: `onERC721Received, setFallbackHandler, flashLoan, royaltyInfo, reclaimRentedItems, stopRent, bridgeToken, migrateVault, batchDeposit, reservedAddress, identifierOrCriteria`
- Typical sink / impact: `fund theft / NFT permanent lock / fee evasion / rental griefing / royalty loss`
- Validation strength: `strong` (28+ unique findings from 10+ auditors across 15+ protocols)

#### Contract / Boundary Map

- Entry surface(s): `buy()`, `sell()`, `lock()`, `stopRent()`, `flashLoan()`, `bridgeToken()`, `migrateVaultERC721()`, `addCollateral()`, `fulfillOrder()`
- Contract hop(s): `User -> Marketplace -> NFT.safeTransferFrom -> Attacker.onERC721Received callback`, `User -> GnosisSafe.setFallbackHandler -> NFT.transferFrom (via fallback)`, `User -> Marketplace -> PaymentEscrow.settlePayment (reverts on blocklist)`
- Trust boundary crossed: `callback (onERC721Received)`, `Gnosis Safe fallback handler`, `payment escrow settlement`, `bridge token detection`, `Merkle proof verification`
- Shared state or sync assumption: `NFT ownership must be consistent across marketplace + safe + escrow; rental state must settle atomically`

#### Valid Bug Signals

- Signal 1: A `_safeMint` or `safeTransferFrom` call is followed by state-changing logic that reads/writes balances or reward accumulators — reentrancy via `onERC721Received` is possible
- Signal 2: Marketplace deposit/vault functions accept a user-supplied `from` parameter instead of enforcing `msg.sender` — residual allowance theft
- Signal 3: Fee/royalty calculation and distribution use different recipient validation (collect from zero-address royalty but don't distribute) — user overpays
- Signal 4: Rental `stopRent()` uses `safeTransferFrom` with no fallback for callback revert — lender can grief renter
- Signal 5: Gnosis Safe guard does not check `setFallbackHandler` — attacker can redirect NFT via fallback

#### False Positive Guards

- Not this bug when: Marketplace only accepts `msg.sender` as the depositor/from address (no residual allowance)
- Safe if: Guard blocks ALL state-modifying Safe functions including `setFallbackHandler`, `enableModule`, `setGuard`
- Safe if: Rental settlement splits NFT reclaim and payment transfer into separate claimable steps (pull pattern)
- Safe if: Bridge validates token type using `ERC165.supportsInterface(0x80ac58cd)` before accepting
- Requires attacker control of: callback contract (onERC721Received), Safe ownership, approved token, or frontrun timing

---

## 1. Reentrancy via onERC721Received / safeMint Callbacks

**Root Cause:** `_safeMint` and `safeTransferFrom` invoke `onERC721Received` on the recipient before completing state updates. If reward distribution, balance, or accounting logic executes before or after the callback without reentrancy protection, an attacker contract can re-enter and manipulate state.

**Unique Evidence:** 6+ findings from 6+ auditors across XDEFI, Carapace, and others.
**Severity consensus:** HIGH (lowest across sources)

### Attack Scenario

**Path A: safeMint reentrancy steals rewards**
Path key: `missing_reentrancy_guard | lock+safeMint | callback_reenter_updateDistribution | reward_theft`
Entry surface: `lock(amount)` → `_safeMint(to, tokenId)`
Contracts touched: `XDEFIDistribution → ERC721._safeMint → Attacker.onERC721Received → XDEFIDistribution.updateDistribution`
1. Attacker calls `lock()` to deposit tokens and trigger `_safeMint`
2. `_safeMint` calls `onERC721Received` on attacker contract
3. Inside callback, attacker calls `updateDistribution()` which lacks `noReenter` modifier
4. `_pointsPerUnit` becomes abnormally large due to stale `totalDepositedXDEFI`
5. Attacker calls `unlock()` to drain inflated rewards

**Path B: Burned NFT reverts lockCapital()**
Path key: `missing_try_catch | ownerOf_revert_on_burn | lockCapital_revert | buyer_compensation_loss`
Entry surface: `lockCapital(lendingPoolAddress)`
Contracts touched: `ProtectionPool.lockCapital → GoldfinchAdapter.calculateRemainingPrincipal → PoolTokens.ownerOf`
1. Lending pool status changes from Active to Late
2. Protocol calls `lockCapital()` to lock protection amounts
3. Loop calls `calculateRemainingPrincipal()` which calls `ownerOf()` on NFT ID
4. Malicious seller has burned the NFT, causing `ownerOf()` to revert
5. Entire `lockCapital()` reverts — status cannot transition, buyer loses compensation

### Vulnerable Pattern Example

**Example 1: safeMint reentrancy** [HIGH]
```solidity
// ❌ VULNERABLE: updateDistribution lacks noReenter modifier
// Source: XDEFI (Code4rena, solodit 1255)
function lock(uint256 amount, uint256 duration, address destination) external {
    totalDepositedXDEFI += amount;
    // State update to _pointsPerUnit happens BEFORE minting
    _safeMint(destination, _generateNewTokenId(amount));
    // Attacker re-enters updateDistribution() from onERC721Received
}

function updateDistribution() external {
    // No noReenter modifier!
    _pointsPerUnit += (newTokens * POINTS_MULTIPLIER) / totalDepositedXDEFI;
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Add reentrancy guard to all state-modifying functions
function updateDistribution() external noReenter {
    _pointsPerUnit += (newTokens * POINTS_MULTIPLIER) / totalDepositedXDEFI;
}

// ✅ SECURE: Use try-catch for external ownerOf calls
function calculateRemainingPrincipal(uint256 tokenId) external view returns (uint256) {
    try poolTokens.ownerOf(tokenId) returns (address owner) {
        // normal logic
    } catch {
        return 0; // treat burned NFT as zero principal
    }
}
```

---

## 2. Residual Allowance & Vault Deposit Exploitation

**Root Cause:** Vault or marketplace deposit functions accept a caller-specified `from` address, allowing anyone to pull tokens from users who granted approval to the contract. After a legitimate deposit, residual allowance remains, enabling theft by third parties.

**Unique Evidence:** 8+ findings from 8+ auditors across Fractional v2, Caviar, and others.
**Severity consensus:** HIGH

### Attack Scenario

**Path A: Residual ERC20/ERC721/ERC1155 allowance theft**
Path key: `missing_msg_sender_check | batchDeposit(from) | third_party_calls | asset_theft`
Entry surface: `batchDepositERC20(from, ...) / batchDepositERC721(from, ...) / batchDepositERC1155(from, ...)`
Contracts touched: `Attacker → BaseVault.batchDepositERC721(alice, ...) → ERC721.transferFrom(alice, vault, tokenId)`
1. Alice approves BaseVault to transfer her tokens and deposits
2. After deposit, residual allowance remains on the BaseVault contract
3. Attacker calls `batchDepositERC721(alice, ...)` pointing the `from` to Alice
4. Vault pulls Alice's remaining tokens and deposits them under attacker's account
5. Attacker withdraws the stolen tokens

### Vulnerable Pattern Example

**Example 2: Unchecked from parameter** [HIGH]
```solidity
// ❌ VULNERABLE: 'from' can be any address with residual allowance
// Source: Fractional v2 (Code4rena, solodit 2993)
function batchDepositERC721(
    address _from,
    address[] calldata _tokens,
    uint256[] calldata _ids
) external {
    for (uint256 i; i < _tokens.length; ) {
        IERC721(_tokens[i]).transferFrom(_from, address(this), _ids[i]);
        unchecked { ++i; }
    }
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Force from to be msg.sender
function batchDepositERC721(
    address[] calldata _tokens,
    uint256[] calldata _ids
) external {
    for (uint256 i; i < _tokens.length; ) {
        IERC721(_tokens[i]).transferFrom(msg.sender, address(this), _ids[i]);
        unchecked { ++i; }
    }
}
```

---

## 3. Marketplace Fee Bypass & Royalty Calculation Errors

**Root Cause:** Marketplace fee and royalty logic contains inconsistencies: royalty amounts collected from buyers but not distributed when recipient is `address(0)`, royalty permyriad sent instead of calculated amount, or fee calculation done on a user-controlled value that can be set to zero.

**Unique Evidence:** 5+ unique findings from 5+ auditors across Golom, Caviar, Monument, and others.
**Severity consensus:** MEDIUM (lowest across sources)

### Attack Scenario

**Path A: Zero-amount fee bypass**
Path key: `missing_totalAmt_validation | order.totalAmt=0 | reservedAddress_payment | fee_evasion`
Entry surface: `fillAsk(order, ...)`
Contracts touched: `Attacker → GolomTrader.fillAsk → AvoidsFeesContract (reservedAddress)`
1. Maker sets `o.totalAmt = 0` in the order struct
2. Exchange amount and `prePaymentAmt` are calculated as percentage of `totalAmt`, yielding 0
3. Maker hides actual payment info in `order.root` field
4. `reservedAddress` (attacker's contract) handles direct payment outside fee logic
5. Trade executes at full value but 0 fees collected by protocol

**Path B: Royalty collected but not distributed (zero-address recipient)**
Path key: `inconsistent_royalty_validation | _getRoyalty_returns_zero_address | royaltyFeeAmount_still_added | buyer_loss`
Entry surface: `PrivatePool.buy(tokenIds)`
Contracts touched: `Buyer → PrivatePool.buy → _getRoyalty → (recipient = address(0), royaltyFee = 10 ETH)`
1. Buyer calls `buy()` for an NFT
2. `_getRoyalty()` returns royalty of 10 WETH but `address(0)` as recipient
3. 10 WETH added to `royaltyFeeAmount` — collected from buyer
4. Distribution loop skips transfer because `recipient == address(0)`
5. Buyer loses 10 WETH that is neither distributed nor returned

**Path C: Permyriad sent instead of royalty amount**
Path key: `royalty_permyriad_vs_amount | getRoyaltyInfoByArtifactId | wrong_value_sent | underpayment`
Entry surface: `buyEditions(orderId)`
Contracts touched: `Buyer → MonumentMarketplace.buyEditions → Splits (royalty receiver)`
1. Marketplace queries `getRoyaltyInfoByArtifactId` returning permyriad (e.g., 500 = 5%)
2. Code sends `royaltyAmount` directly to splitter, but the value IS the permyriad, not the calculated percentage of price
3. Royalty receivers get e.g. 500 wei instead of 5% of sale price

### Vulnerable Pattern Example

**Example 3: Inconsistent royalty validation** [MEDIUM]
```solidity
// ❌ VULNERABLE: Royalty collected even when recipient is address(0)
// Source: Caviar (Code4rena, solodit 16253)
for (uint256 i = 0; i < tokenIds.length; i++) {
    (address recipient, uint256 royaltyFee) = _getRoyalty(tokenIds[i], salePrice);
    // Bug: adds fee regardless of recipient validity
    royaltyFeeAmount += royaltyFee;
}
// Later: skips transfer when recipient == address(0)
if (royaltyFee > 0 && recipient != address(0)) {
    // transfer royalty
}
// Buyer overpaid by royaltyFee for zero-address recipients
```

### Secure Implementation
```solidity
// ✅ SECURE: Only collect royalty when recipient is valid
for (uint256 i = 0; i < tokenIds.length; i++) {
    (address recipient, uint256 royaltyFee) = _getRoyalty(tokenIds[i], salePrice);
    if (royaltyFee > 0 && recipient != address(0)) {
        royaltyFeeAmount += royaltyFee;
    }
}
```

---

## 4. NFT Rental Griefing via Callback Revert & Blocklist

**Root Cause:** Rental protocols (e.g., reNFT) use `safeTransferFrom` to return NFTs to lenders during `stopRent()`. If the lender's wallet reverts in `onERC721Received` or if the payment ERC20 blocklists a participant, the entire settlement reverts — locking both the NFT in the renter's safe and the payment in escrow.

**Unique Evidence:** 17+ findings across Code4rena reNFT contest (30+ independent finders).
**Severity consensus:** MEDIUM

### Attack Scenario

**Path A: Lender callback revert griefs renter payment**
Path key: `safeTransferFrom_callback | onERC721Received_revert | stopRent_revert | payment_hostage`
Entry surface: `stopRent(rentalOrder)`
Contracts touched: `Renter → Stop.stopRent → Safe.execTransactionFromModule → Reclaimer.reclaimRentalOrder → ERC721.safeTransferFrom → MaliciousLender.onERC721Received (reverts)`
1. Lender creates PAY order rental with malicious wallet as recipient
2. Renter fulfills the order; NFT goes to renter's Safe, payment to escrow
3. Rental expires; renter calls `stopRent()`
4. `_reclaimRentedItems()` calls `safeTransferFrom()` to return NFT to lender
5. Lender's `onERC721Received()` reverts, blocking entire `stopRent` transaction
6. Payment stays in escrow; NFT stays in renter's safe — lender holds payment hostage

**Path B: ERC20 blocklist prevents rental settlement**
Path key: `blocklisted_address | settlePayment_revert | stopRent_revert | nft_stuck_in_safe`
Entry surface: `stopRent(rentalOrder)`
Contracts touched: `Renter → Stop.stopRent → PaymentEscrow.settlePayment → ERC20.transfer (reverts on blocklist)`
1. Renter is blocklisted by payment ERC20 (e.g., USDC/USDT)
2. Rental expires; lender calls `stopRent()`
3. `settlePayment()` tries to transfer ERC20 to blocklisted renter — reverts
4. NFT remains in renter's Safe; payment stuck in escrow

**Path C: Paused ERC721/ERC1155 blocks stopRent**
Path key: `paused_token_transfer | safeTransferFrom_revert | stopRent_revert | nft_stuck`
Entry surface: `stopRent(rentalOrder)`
Contracts touched: `Caller → Stop.stopRent → Reclaimer → ERC721(paused).safeTransferFrom (reverts)`
1. NFT collection (e.g., Axie Infinity) has a `pause` function
2. Token transfers are paused by the NFT contract owner
3. `stopRent()` → `reclaimRentedItems()` → `safeTransferFrom()` reverts
4. Rental cannot be stopped; NFT and payments locked

### Vulnerable Pattern Example

**Example 4: safeTransferFrom enables lender griefing** [MEDIUM]
```solidity
// ❌ VULNERABLE: safeTransferFrom allows lender callback to revert entire settlement
// Source: reNFT (Code4rena, solodit 30541)
function reclaimRentalOrder(RentalOrder calldata rentalOrder) external {
    for (uint256 i = 0; i < rentalOrder.items.length; ++i) {
        Item memory item = rentalOrder.items[i];
        if (item.itemType == ItemType.ERC721) {
            // Lender's onERC721Received can revert, blocking stopRent
            IERC721(item.token).safeTransferFrom(
                address(this), rentalOrder.lender, item.identifier
            );
        }
    }
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Use transferFrom (no callback) or pull-based pattern
// Option A: Use transferFrom without callback
IERC721(item.token).transferFrom(address(this), rentalOrder.lender, item.identifier);

// Option B: Split into separate claims
function stopRent(RentalOrder calldata order) external {
    _markRentalStopped(order); // update state
    // Assets claimable via separate pull calls
}

function claimNFT(bytes32 orderHash) external {
    // Lender claims their NFT independently
}
```

---

## 5. Gnosis Safe Guard Bypass via Fallback Handler

**Root Cause:** Gnosis Safe rental guards check common function signatures (`transferFrom`, `approve`, `setApprovalForAll`, etc.) but miss `setFallbackHandler`. An attacker can set the fallback handler to the rented NFT contract's address, then call `transferFrom` on the Safe — which the Safe doesn't recognize, so it delegates to the fallback handler (= NFT contract), executing the transfer as the Safe.

**Unique Evidence:** 15+ finders in Code4rena reNFT contest.
**Severity consensus:** HIGH

### Attack Scenario

**Path A: Fallback handler set to rented NFT contract**
Path key: `missing_setFallbackHandler_check | Guard.checkTransaction | fallback_delegates_to_nft | nft_hijack`
Entry surface: `execTransaction(setFallbackHandler(nftAddress))` → `execTransaction(transferFrom(safe, attacker, tokenId))`
Contracts touched: `Attacker → GnosisSafe.execTransaction(setFallbackHandler) → Guard.checkTransaction (passes) → GnosisSafe.setFallbackHandler(nftContract)` → Then: `Attacker → GnosisSafe(transferFrom) → FallbackManager.fallback → NFT.transferFrom(safe, attacker, tokenId)`
1. Attacker rents ERC721 NFT; it's held in their Gnosis rental Safe
2. Attacker calls `execTransaction` to set fallback handler to the NFT contract address
3. Guard's `checkTransaction` does NOT block `setFallbackHandler` — only checks `transferFrom`, `approve`, etc.
4. Attacker sends `transferFrom(safe, attacker, tokenId)` to the Safe
5. Safe doesn't have `transferFrom`, delegates to fallback handler = NFT contract
6. NFT contract executes `transferFrom(safe, attacker, tokenId)` — Safe is the `msg.sender` and owner
7. NFT is stolen; lender cannot recover it

### Vulnerable Pattern Example

**Example 5: Guard missing setFallbackHandler check** [HIGH]
```solidity
// ❌ VULNERABLE: Guard doesn't check setFallbackHandler
// Source: reNFT (Code4rena, solodit 30522)
function checkTransaction(
    address to,
    uint256 value,
    bytes memory data,
    // ...
) external override {
    // Checks: approve, transferFrom, setApprovalForAll, enableModule, setGuard
    // MISSING: setFallbackHandler is NOT checked!
    if (selector == IERC721.approve.selector) { revert(); }
    if (selector == IERC721.transferFrom.selector) { revert(); }
    if (selector == IERC721.setApprovalForAll.selector) { revert(); }
    // No check for setFallbackHandler(address)!
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Block setFallbackHandler in guard
bytes4 constant SET_FALLBACK_HANDLER = bytes4(keccak256("setFallbackHandler(address)"));

function checkTransaction(address to, uint256, bytes memory data, ...) external override {
    bytes4 selector = bytes4(data);
    if (selector == SET_FALLBACK_HANDLER) revert GuardPolicy_UnauthorizedCall();
    // ... existing checks ...
}
```

---

## 6. Auction Manipulation, Frontrunning & Debt Shortfall

**Root Cause:** NFT auction systems allow majority holders to manipulate auction outcomes (e.g., forcing auction failure by bidding from non-ERC721-compatible contracts), or fail to track debt shortfall across sequential liquidation auctions, allowing borrowers to pocket auction proceeds that should repay protocol debt.

**Unique Evidence:** 5+ unique findings from 4+ auditors across PartyDAO, Backed Protocol (Papr), and others.
**Severity consensus:** HIGH

### Attack Scenario

**Path A: Force Zora auction failure, steal NFT on Opensea**
Path key: `settlable_auction_returns_false | non_erc721_bidder | opensea_stage_bypass | nft_theft`
Entry surface: `execute(listOnOpenseaProposal)`
Contracts touched: `Attacker → PartyGovernance.execute → ListOnOpenseaProposal._settleZoraAuction → ZORA.endAuction (fails) → Seaport (negligible price)`
1. Attacker passes proposal listing NFT on Opensea with tiny price
2. `_settleZoraAuction()` is called — auction settlement is attempted
3. Attacker's bid contract doesn't implement `onERC721Received`, causing transfer failure
4. `settleZoraAuction()` returns `false` — moves to Opensea stage
5. Attacker immediately buys NFT from Seaport at negligible price

**Path B: Debt shortfall not tracked across sequential auctions**
Path key: `missing_shortfall_tracking | isLastCollateral_clears_debt | second_auction_pays_borrower | protocol_loss`
Entry surface: `purchaseLiquidationAuctionNFT(auction2)`
Contracts touched: `Liquidator → PaprController.purchaseLiquidationAuctionNFT → _handleExcess → borrower.transfer`
1. Borrower has 2 NFT collaterals and max debt
2. First collateral auctioned but at low price — debt shortfall burned via `_reduceDebtWithoutBurn`
3. `isLastCollateral` check triggers because vault has no more collaterals (second auction is separate)
4. Debt set to 0 including shortfall
5. Second auction proceeds transferred entirely to borrower as "excess", bypassing debt repayment

### Vulnerable Pattern Example

**Example 6: Debt shortfall not tracked** [HIGH]
```solidity
// ❌ VULNERABLE: Shortfall burned without tracking for future auctions
// Source: Backed Protocol / Papr (Code4rena, solodit 6202)
if (isLastCollateral && remaining != 0) {
    // Debt cleared entirely — no record of shortfall
    _reduceDebtWithoutBurn(auction.nftOwner, auction.auctionAssetContract, remaining);
}
// Second auction: debt is 0, so all excess goes to borrower
if (excess > 0) {
    remaining = _handleExcess(excess, neededToSaveVault, debtCached, auction);
    // debtCached == 0, so everything is "excess" → sent to borrower
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Track shortfall and fill it from future auction proceeds
mapping(address => mapping(ERC721 => uint256)) private _shortfall;

if (isLastCollateral && remaining != 0) {
    _shortfall[auction.nftOwner][auction.auctionAssetContract] += remaining;
    _reduceDebtWithoutBurn(auction.nftOwner, auction.auctionAssetContract, remaining);
}

// In _handleExcess:
uint256 payout = totalOwed - debtCached;
uint256 burnShortfall = _shortfall[owner][asset];
if (burnShortfall > 0) {
    uint256 toFill = burnShortfall > payout ? payout : burnShortfall;
    PaprToken(address(papr)).burn(address(this), toFill);
    _shortfall[owner][asset] -= toFill;
    payout -= toFill;
}
if (payout > 0) papr.transfer(owner, payout);
```

---

## 7. NFT Bridge One-Way Lock & Migration Burn

**Root Cause:** Token bridge contracts intended only for ERC20 don't properly reject ERC721 tokens (which lack `decimals()`), allowing NFTs to be bridged one-way. Similarly, vault migration functions don't validate proposal IDs, enabling transfers to `address(0)` which burns NFTs.

**Unique Evidence:** 10+ findings from 9+ auditors across Linea (Cyfrin), Fractional v2.
**Severity consensus:** HIGH

### Attack Scenario

**Path A: ERC721 bridged via ERC20 bridge — permanent lock**
Path key: `missing_token_type_check | _safeDecimals_doesnt_revert | bridgeToken_accepts_erc721 | permanent_nft_lock`
Entry surface: `bridgeToken(nftAddress, amount, recipient)`
Contracts touched: `User → TokenBridge.bridgeToken(ERC721) → L2 (deploys ERC20 wrapper) → User tries bridgeBack → always reverts`
1. User calls `bridgeToken()` with ERC721 contract address
2. `_safeDecimals()` doesn't revert for non-ERC20 tokens (returns 0)
3. NFT is locked in bridge contract on L1, ERC20 token deployed on L2
4. On L2, user has ERC20 representation — but bridging back to L1 always reverts
5. NFT permanently stuck in bridge contract

**Path B: Migration with invalid proposalId burns NFT**
Path key: `missing_proposalId_validation | migrationInfo_returns_zero | withdraw_to_address0 | nft_burned`
Entry surface: `migrateVaultERC721(vault, invalidProposalId, tokenAddr, tokenId, proof)`
Contracts touched: `Attacker → Migration.migrateVaultERC721 → IBuyout.withdrawERC721(vault, token, address(0), tokenId, proof)`
1. Vault migration succeeds; `settleVault` and `settleFractions` called
2. Attacker calls `migrateVaultERC721` with a non-existent `_proposalId`
3. `migrationInfo[_vault][_proposalId].newVault` returns `address(0)` (uninitialized)
4. `withdrawERC721` transfers NFT to `address(0)`, effectively burning it
5. All vault assets destroyed

### Vulnerable Pattern Example

**Example 7: No proposalId validation** [HIGH]
```solidity
// ❌ VULNERABLE: newVault can be address(0) with invalid proposalId
// Source: Fractional v2 (Code4rena, solodit 2990)
function migrateVaultERC721(
    address _vault,
    uint256 _proposalId,
    address _token,
    uint256 _tokenId,
    bytes32[] calldata _erc721TransferProof
) external {
    address newVault = migrationInfo[_vault][_proposalId].newVault;
    // newVault is address(0) for invalid _proposalId!
    IBuyout(buyout).withdrawERC721(_vault, _token, newVault, _tokenId, _erc721TransferProof);
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Validate newVault is not zero address
function migrateVaultERC721(...) external {
    address newVault = migrationInfo[_vault][_proposalId].newVault;
    require(newVault != address(0), "Invalid proposal ID");
    IBuyout(buyout).withdrawERC721(_vault, _token, newVault, _tokenId, _erc721TransferProof);
}
```

---

## 8. Merkle Criteria Resolution & Order Matching Bypass

**Root Cause:** Seaport-style merkle tree criteria resolution uses raw `tokenId` as leaf values. Since intermediate merkle hashes are 32-byte values that could also be valid tokenIds (per ERC721 spec, tokenIds are arbitrary uint256), an attacker can submit an intermediate hash as the `tokenId` and an empty proof, passing verification.

**Unique Evidence:** 2 finders (cmichel, frangio/Spearbit) in OpenSea Seaport contest.
**Severity consensus:** MEDIUM

### Attack Scenario

**Path A: Intermediate merkle hash used as tokenId**
Path key: `leaf_vs_interior_hash_collision | raw_tokenId_as_leaf | empty_proof | wrong_nft_traded`
Entry surface: `fulfillAdvancedOrder(order, criteriaResolvers, ...)`
Contracts touched: `Attacker → Seaport.fulfillAdvancedOrder → CriteriaResolution._verifyProof`
1. Alice creates an offer for NFTs with tokenId 1 or 2 using merkle criteria
2. Merkle root = `hash(1 || 2) = 0xe90b7b...`
3. Attacker acquires NFT with tokenId = `0xe90b7b...` (the merkle root value)
4. Attacker fulfills Alice's order with tokenId = `merkleRoot` and empty proof
5. Proof verification: `computedHash = merkleRoot` (leaf) == `root` (stored) → passes with empty proof
6. Alice receives unwanted NFT; attacker receives Alice's payment

### Vulnerable Pattern Example

**Example 8: Raw tokenId as merkle leaf** [MEDIUM]
```solidity
// ❌ VULNERABLE: tokenId used directly as leaf — collides with intermediate hashes
// Source: OpenSea Seaport (Code4rena, solodit 2623)
function _verifyProof(uint256 leaf, uint256 root, bytes32[] memory proof) internal pure {
    assembly {
        let computedHash := leaf  // raw tokenId used as hash!
        // ... standard proof walking ...
    }
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Hash the tokenId before using as leaf
function _verifyProof(uint256 leaf, uint256 root, bytes32[] memory proof) internal pure {
    bytes32 computedHash = keccak256(abi.encodePacked(leaf));
    // Now leaf hash (32 bytes input) can't collide with internal hash (64 bytes input)
    // ... standard proof walking ...
}
```

---

## 9. Flash Loan & Pool Token Theft

**Root Cause:** NFT pool/marketplace flash loan functions allow the caller to specify an arbitrary token address rather than restricting to the pool's NFT. A previous pool owner who set approvals via `execute()` can exploit `flashLoan()` to steal tokens after ownership transfer.

**Unique Evidence:** 3+ findings from 3 auditors across Caviar.
**Severity consensus:** MEDIUM

### Attack Scenario

**Path A: Previous owner steals via flashLoan with arbitrary token**
Path key: `caller_chosen_token_in_flashloan | residual_approval_from_execute | ownership_transfer | fund_theft`
Entry surface: `PrivatePool.flashLoan(receiver, token, tokenId, data)`
Contracts touched: `Attacker (previous owner) → PrivatePool.flashLoan(ExploitContract, anyToken, ...) → ExploitContract.onFlashLoan → steal tokens`
1. Bob creates PrivatePool with 5 NFTs and 500 USDC
2. Bob calls `execute()` to approve USDC spending and NFT transfers to his exploit contract
3. Bob sells PrivatePool ownership to Alice (ERC721 transfer via Factory)
4. Bob calls `flashLoan()` specifying his exploit contract as the token address
5. Exploit contract's `transferFrom` is called during flash loan, draining approved tokens
6. All NFTs and USDC stolen from Alice's pool

### Vulnerable Pattern Example

**Example 9: Arbitrary token in flashLoan** [MEDIUM]
```solidity
// ❌ VULNERABLE: Caller chooses token address — can be exploit contract
// Source: Caviar (Code4rena, solodit 43394)
function flashLoan(
    IERC3156FlashBorrower receiver,
    address token,        // ← attacker-controlled!
    uint256 tokenId,
    bytes calldata data
) external returns (bool) {
    // Calls token.transferFrom — if token is attacker contract, it can steal
    IERC721(token).transferFrom(address(this), address(receiver), tokenId);
    // ... callback ...
    IERC721(token).transferFrom(address(receiver), address(this), tokenId);
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Restrict flash loan to pool's own NFT
function flashLoan(...) external returns (bool) {
    require(token == address(nft), "Only pool NFT");
    // ... rest of logic ...
}
```

---

## 10. NFT Wrap/Unwrap Airdrop & ID Swap Exploitation

**Root Cause:** NFT wrapping/fractionalization protocols allow wrapping one NFT and immediately unwrapping a different NFT (same collection, whitelisted ID), enabling fee-free ID swapping and airdrop theft by temporarily holding each NFT in the pool.

**Unique Evidence:** 2+ findings across Caviar.
**Severity consensus:** MEDIUM

### Attack Scenario

**Path A: Wrap-unwrap cycle steals airdrops**
Path key: `no_unwrap_delay | wrap_unwrap_same_tx | attacker_temporary_owner | airdrop_theft`
Entry surface: `wrap(tokenIds) → unwrap(tokenIds)` in a loop
Contracts touched: `Attacker → Pair.wrap(attackerNFT) → Pair.unwrap(poolNFT) → NFT.getAirDrop(poolNFT) → repeat`
1. Pool holds 100 NFTs from collection with upcoming airdrop
2. Attacker owns 1 whitelisted NFT and wraps it for `1e18` fractional tokens
3. In same tx: unwrap a different pool NFT, call `getAirDrop()`, wrap it back
4. Repeat for all 100 pool NFTs in a single transaction
5. Attacker steals airdrops for all 100 NFTs that belong to fractional token holders

### Vulnerable Pattern Example

**Example 10: No lock period on wrap/unwrap** [MEDIUM]
```solidity
// ❌ VULNERABLE: Immediate unwrap allows NFT ID swapping and airdrop theft
// Source: Caviar (Code4rena, solodit 6102)
function wrap(uint256[] calldata tokenIds, bytes32[][] calldata proofs) public returns (uint256) {
    _validateTokenIds(tokenIds, proofs);
    uint256 fractionalTokenAmount = tokenIds.length * ONE;
    _mint(msg.sender, fractionalTokenAmount);
    for (uint256 i = 0; i < tokenIds.length; i++) {
        ERC721(nft).safeTransferFrom(msg.sender, address(this), tokenIds[i]);
    }
}

function unwrap(uint256[] calldata tokenIds) public returns (uint256) {
    uint256 fractionalTokenAmount = tokenIds.length * ONE;
    _burn(msg.sender, fractionalTokenAmount);
    for (uint256 i = 0; i < tokenIds.length; i++) {
        ERC721(nft).safeTransferFrom(address(this), msg.sender, tokenIds[i]);
    }
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Add unwrap delay or fee
mapping(uint256 => uint256) public wrapTimestamp;

function wrap(uint256[] calldata tokenIds, ...) public {
    for (uint256 i = 0; i < tokenIds.length; i++) {
        wrapTimestamp[tokenIds[i]] = block.timestamp;
        // ... existing logic
    }
}

function unwrap(uint256[] calldata tokenIds) public {
    for (uint256 i = 0; i < tokenIds.length; i++) {
        require(block.timestamp >= wrapTimestamp[tokenIds[i]] + LOCK_PERIOD, "Too early");
        // ... existing logic
    }
}
```

---

## Impact Analysis

### Technical Impact
- **Fund theft:** Direct asset theft via residual allowance, flash loan exploitation, or guard bypass (Patterns 2, 5, 9)
- **NFT permanent lock:** One-way bridging, paused token transfers, or settlement revert traps (Patterns 4, 7)
- **Protocol revenue loss:** Fee bypass through zero-amount tricks or direct contract payment (Pattern 3)
- **Royalty underpayment:** Calculation errors cause royalty receivers to get wrong amounts (Pattern 3)
- **Accounting corruption:** Debt shortfall not tracked across sequential auctions (Pattern 6)
- **State transition DoS:** Burned NFT reverts ownerOf, blocking liquidation state changes (Pattern 1B)

### Business Impact
- NFT marketplace trust: Fee bypass undermines protocol economics
- NFT rental adoption: Griefing attacks make PAY orders risky for renters
- NFT-backed DeFi: Liquidation bugs threaten protocol solvency
- Cross-chain NFT: Bridge acceptance of ERC721 causes permanent loss

### Impact Frequency
- Callback reentrancy via safeMint/safeTransferFrom: Common (6/28 unique findings)
- Residual allowance exploitation: Common (8/28)
- Fee bypass/royalty errors: Common (5/28)
- Rental griefing via callback: Very Common (17+ finders)
- Guard bypass (fallback handler): Very Common (15+ finders)
- Auction manipulation: Moderate (5/28)
- Bridge/migration permanent loss: Moderate (10/28)
- Merkle criteria bypass: Rare (2/28)

---

## Detection Patterns

### Grep Seeds
```bash
# Pattern 1: Reentrancy via callbacks
grep -rn "_safeMint\|safeTransferFrom" --include="*.sol" | grep -v "test/"

# Pattern 2: Residual allowance
grep -rn "batchDeposit\|depositERC721\|depositERC1155" --include="*.sol" | grep -v "msg.sender"

# Pattern 3: Royalty/fee issues
grep -rn "royaltyInfo\|_getRoyalty\|royaltyFee\|permyriad" --include="*.sol"

# Pattern 4: Rental settlement
grep -rn "stopRent\|reclaimRentedItems\|settlePayment\|safeTransferFrom.*lender" --include="*.sol"

# Pattern 5: Guard bypass
grep -rn "setFallbackHandler\|checkTransaction\|Guard" --include="*.sol"

# Pattern 6: Auction manipulation
grep -rn "settleAuction\|isLastCollateral\|_reduceDebtWithoutBurn\|shortfall" --include="*.sol"

# Pattern 7: Bridge/migration
grep -rn "bridgeToken\|migrateVault\|_safeDecimals" --include="*.sol"

# Pattern 8: Merkle criteria
grep -rn "identifierOrCriteria\|_verifyProof\|CriteriaResolution" --include="*.sol"
```

### Call Graph Signals
- `lock() → _safeMint() → onERC721Received` (Pattern 1)
- `batchDeposit(from, ...) → transferFrom(from, ...)` where `from != msg.sender` (Pattern 2)
- `stopRent() → reclaimRentedItems() → safeTransferFrom()` (Pattern 4)
- `execTransaction() → checkTransaction() → setFallbackHandler()` (Pattern 5)
- `purchaseLiquidationAuctionNFT() → _handleExcess() → transfer(borrower)` after `_reduceDebtWithoutBurn` (Pattern 6)

---

## Keywords for Vector Search

NFT marketplace, ERC721, ERC1155, safeTransferFrom, safeMint, onERC721Received, reentrancy callback, residual allowance, vault deposit, batchDeposit, fee bypass, royalty calculation, royaltyInfo, permyriad, rental griefing, stopRent, reclaimRentedItems, PaymentEscrow, settlePayment, blocklist, Gnosis Safe, setFallbackHandler, Guard bypass, auction manipulation, Zora, Seaport, debt shortfall, isLastCollateral, NFT bridge, bridgeToken, one-way lock, migration burn, migrateVaultERC721, address(0), Merkle criteria, identifierOrCriteria, intermediate hash, flash loan, PrivatePool, wrap unwrap, airdrop theft, CryptoPunks, frontrunning, deposit frontrun, offerPunkForSaleToAddress

---

## Cross-References

- **ERC721 Token-Level Bugs:** See `DB/tokens/erc721/ERC721_NFT_VULNERABILITIES.md` for transfer safety, approval, and standard compliance patterns
- **Reentrancy Patterns:** See `DB/general/reentrancy/` for callback reentrancy patterns
- **Access Control:** See `DB/general/access-control/` for approval and authorization patterns
- **Bridge Vulnerabilities:** See `DB/bridge/` for cross-chain bridge patterns
