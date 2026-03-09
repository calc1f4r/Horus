---
# Core Classification
protocol: generic
chain: everychain
category: token_standard
vulnerability_type: erc721_nft

# Attack Vector Details
attack_type: multiple
affected_component: nft_contracts

# Technical Primitives
primitives:
  - safeMint
  - safeTransferFrom
  - onERC721Received
  - approve
  - setApprovalForAll
  - tokenURI
  - balanceOf
  - ownerOf
  - delegation
  - voting_power

# Impact Classification
severity: high
impact: fund_loss, locked_tokens, governance_manipulation
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - erc721
  - nft
  - token_standard
  - reentrancy
  - access_control
  - voting
  - delegation
  - approval
  - royalty
  - metadata
---

# ERC721/NFT Security Vulnerabilities Database

## Overview

ERC721 (Non-Fungible Token) vulnerabilities represent a critical class of smart contract security issues that affect NFT implementations across DeFi protocols, marketplaces, governance systems, and gaming platforms. This comprehensive database documents vulnerability patterns discovered across 1,730+ audit findings, categorized by root cause, attack vector, and severity.

NFT security vulnerabilities manifest across multiple dimensions: transfer safety issues, reentrancy via callbacks, approval management flaws, voting/delegation bugs, royalty manipulation, and ERC-721 standard non-compliance. Understanding these patterns is essential for secure NFT protocol development and auditing.

---

## Table of Contents

1. [Transfer Safety Vulnerabilities](#1-transfer-safety-vulnerabilities)
2. [Reentrancy via NFT Callbacks](#2-reentrancy-via-nft-callbacks)
3. [Approval and Access Control Issues](#3-approval-and-access-control-issues)
4. [Voting and Delegation Vulnerabilities](#4-voting-and-delegation-vulnerabilities)
5. [Royalty Manipulation](#5-royalty-manipulation)
6. [ERC-721 Standard Compliance Issues](#6-erc-721-standard-compliance-issues)
7. [NFT Liquidation and Collateral Issues](#7-nft-liquidation-and-collateral-issues)
8. [Self-Transfer Edge Cases](#8-self-transfer-edge-cases)

---

## 1. Transfer Safety Vulnerabilities

### 1.1 Using `transferFrom` Instead of `safeTransferFrom`

**Root Cause:** Using the basic `transferFrom` function instead of `safeTransferFrom` for ERC721 transfers does not verify whether the recipient can handle NFTs.

**Attack Scenario:**
1. Protocol transfers NFT to a recipient address using `transferFrom()`
2. Recipient is a contract without `onERC721Received` implementation
3. NFT becomes permanently locked in the recipient contract

**Observed Frequency:** 54+ reports across different protocols
**Consensus Severity:** MEDIUM

**Example 1: Direct transferFrom Usage** [MEDIUM]
```solidity
// ❌ VULNERABLE: No check if receiver can handle ERC721
function transferNFT(address collection, address to, uint256 tokenId) external {
    ERC721(collection).transferFrom(msg.sender, to, tokenId);
}
```
> 📖 Reference: [reports/erc721_nft_findings/m-02-use-safetransferfrom-instead-of-transferfrom-for-erc721.md](../../../reports/erc721_nft_findings/m-02-use-safetransferfrom-instead-of-transferfrom-for-erc721.md)

**Example 2: Marketplace Transfer** [MEDIUM]
```solidity
// ❌ VULNERABLE: NFT sent to buyer without safety check
function fillOrder(Order memory o, address receiver) external {
    // If receiver is a contract without onERC721Received, NFT is lost
    ERC721(o.collection).transferFrom(o.signer, receiver, o.tokenId);
}
```

**✅ SECURE: Using safeTransferFrom**
```solidity
// ✅ SECURE: Validates receiver can handle ERC721
function transferNFT(address collection, address to, uint256 tokenId) external {
    ERC721(collection).safeTransferFrom(msg.sender, to, tokenId);
}
```

### 1.2 Using `_mint` Instead of `_safeMint`

**Root Cause:** Minting NFTs with `_mint()` does not invoke the `onERC721Received` callback, potentially sending tokens to contracts that cannot handle them.

**Attack Scenario:**
1. User calls mint function with a smart contract wallet as recipient
2. Smart contract wallet lacks ERC721Receiver implementation
3. NFT and any associated assets become permanently locked

**Observed Frequency:** 30+ reports
**Consensus Severity:** MEDIUM

**Example 1: Direct Mint Without Safety Check** [MEDIUM]
```solidity
// ❌ VULNERABLE: No receiver validation
function mint(address to) external {
    uint256 tokenId = _tokenIdCounter.current();
    _mint(to, tokenId);  // Does not check receiver
    _tokenIdCounter.increment();
}
```
> 📖 Reference: [reports/erc721_nft_findings/risk-of-locked-assets-due-to-use-of-_mint-instead-of-_safemint.md](../../../reports/erc721_nft_findings/risk-of-locked-assets-due-to-use-of-_mint-instead-of-_safemint.md)

**Example 2: Vault Factory Creating Asset Vaults** [MEDIUM]
```solidity
// ❌ VULNERABLE: Vault token minted without safety check
function initializeBundle(address to) external payable returns (uint256) {
    address vault = _create();
    _mint(to, uint256(uint160(vault)));  // If `to` can't handle ERC721, vault token is lost
    return uint256(uint160(vault));
}
```

**✅ SECURE: Using _safeMint**
```solidity
// ✅ SECURE: Validates receiver before minting
function mint(address to) external {
    uint256 tokenId = _tokenIdCounter.current();
    _safeMint(to, tokenId);  // Checks onERC721Received
    _tokenIdCounter.increment();
}
```

---

## 2. Reentrancy via NFT Callbacks

### 2.1 Reentrancy Through `onERC721Received` Callback

**Root Cause:** The `safeTransferFrom` and `_safeMint` functions invoke `onERC721Received` on the recipient, creating a callback opportunity. If state updates occur after this callback, attackers can reenter.

**Attack Scenario:**
1. Attacker deploys contract implementing `onERC721Received`
2. Protocol calls `safeTransferFrom` or `_safeMint` to attacker's contract
3. Attacker's `onERC721Received` reenters vulnerable function
4. State variables are manipulated before being updated

**Observed Frequency:** 40+ reports
**Consensus Severity:** HIGH to CRITICAL

**Example 1: Unlimited Minting via Reentrancy** [CRITICAL]
```solidity
// ❌ VULNERABLE: State updated after callback
function whitelistMint(bytes memory _signature) external payable {
    require(verifySignature(_signature), "Invalid signature");
    require(mintedCount[msg.sender] < maxPerWallet, "Max minted");
    
    // Callback happens BEFORE state update
    _safeMint(msg.sender, _tokenIdCounter.current());
    
    // Attacker reenters in onERC721Received, mintedCount still 0
    _tokenIdCounter.increment();
    mintedCount[msg.sender]++;
}
```
> 📖 Reference: [reports/erc721_nft_findings/h-01-malicious-user-can-mint-unlimited-amount-of-nfts-due-to-reentrancy-in-white.md](../../../reports/erc721_nft_findings/h-01-malicious-user-can-mint-unlimited-amount-of-nfts-due-to-reentrancy-in-white.md)

**Example 2: Fee Stealing via ERC777/ERC721 Callback** [HIGH]
```solidity
// ❌ VULNERABLE: ERC1155 minted before fee accounting updated
function mintPosition(uint256 amount) external {
    // 1. Mint ERC1155 position token (callback to attacker)
    _mint(msg.sender, tokenId, positionSize);
    
    // 2. Update liquidity (attacker can transfer token before this)
    s_accountLiquidity[positionKey] = liquidity;
    
    // 3. Transfer tokens from user
    token.transferFrom(msg.sender, address(this), amount);
    
    // 4. Update fee base - TOO LATE if attacker transferred position
    s_accountFeesBase[positionKey] = _getFeesBase();
}
```
> 📖 Reference: [reports/erc721_nft_findings/h-01-attacker-can-steal-all-fees-from-sfpm-in-pools-with-erc777-tokens.md](../../../reports/erc721_nft_findings/h-01-attacker-can-steal-all-fees-from-sfpm-in-pools-with-erc777-tokens.md)

**Example 3: ERC777 Token Reentrancy in NFT Protocol** [HIGH]
```solidity
// ❌ VULNERABLE: Base token transfer before fractional balance update
function buy(uint256 outputAmount, uint256 maxInputAmount) public payable {
    inputAmount = buyQuote(outputAmount);  // Uses current balance
    
    // Transfer fractional tokens (updates one balance)
    _transferFrom(address(this), msg.sender, outputAmount);
    
    // Transfer base tokens - if ERC777, triggers tokensReceived hook
    // Attacker reenters, buys more with stale quote
    ERC20(baseToken).safeTransferFrom(msg.sender, address(this), inputAmount);
}
```
> 📖 Reference: [reports/erc721_nft_findings/h-01-reentrancy-in-buy-function-for-erc777-tokens-allows-buying-funds-with-consi.md](../../../reports/erc721_nft_findings/h-01-reentrancy-in-buy-function-for-erc777-tokens-allows-buying-funds-with-consi.md)

**✅ SECURE: Reentrancy Guard + CEI Pattern**
```solidity
// ✅ SECURE: State updated before external call + reentrancy guard
function whitelistMint(bytes memory _signature) external payable nonReentrant {
    require(verifySignature(_signature), "Invalid signature");
    require(mintedCount[msg.sender] < maxPerWallet, "Max minted");
    
    // Update state FIRST (Checks-Effects-Interactions)
    uint256 tokenId = _tokenIdCounter.current();
    _tokenIdCounter.increment();
    mintedCount[msg.sender]++;
    
    // External call LAST
    _safeMint(msg.sender, tokenId);
}
```

### 2.2 Liquidation DoS via `onERC721Received` Callback

**Root Cause:** When liquidating positions that hold NFTs, the protocol transfers the NFT back to the owner using `safeTransferFrom`. A malicious owner can implement `onERC721Received` to revert, preventing liquidation.

**Attack Scenario:**
1. Borrower opens position with NFT collateral using a malicious contract
2. Position becomes undercollateralized and should be liquidated
3. Liquidation calls `safeTransferFrom` to return NFT to borrower
4. Borrower's contract reverts in `onERC721Received`, blocking liquidation
5. Bad debt accrues, potentially causing protocol insolvency

**Observed Frequency:** 23+ reports
**Consensus Severity:** HIGH

**Example 1: Blocking Liquidation** [HIGH]
```solidity
// Attacker's contract
contract MaliciousBorrower {
    address public vault;
    
    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external returns (bytes4) {
        // Block NFT transfers from vault (liquidation)
        if (from == vault) return bytes4(0xdeadbeef);  // Invalid selector
        return this.onERC721Received.selector;
    }
}

// Vulnerable liquidation in protocol
function liquidate(uint256 tokenId) external {
    // ... liquidation logic ...
    
    // ❌ VULNERABLE: Owner can block this
    nonfungiblePositionManager.safeTransferFrom(
        address(this), 
        owner,  // Malicious contract 
        tokenId
    );
}
```
> 📖 Reference: [reports/erc721_nft_findings/h-06-owner-of-a-position-can-prevent-liquidation-due-to-the-onerc721received-cal.md](../../../reports/erc721_nft_findings/h-06-owner-of-a-position-can-prevent-liquidation-due-to-the-onerc721received-cal.md)

**✅ SECURE: Escrow Pattern for Liquidation**
```solidity
// ✅ SECURE: Don't transfer directly, use claimable escrow
function liquidate(uint256 tokenId) external {
    // ... liquidation logic ...
    
    // Store NFT for later claim instead of direct transfer
    pendingClaims[owner][tokenId] = true;
    emit NFTReadyToClaim(owner, tokenId);
}

function claimNFT(uint256 tokenId) external {
    require(pendingClaims[msg.sender][tokenId], "Nothing to claim");
    delete pendingClaims[msg.sender][tokenId];
    
    // If this reverts, it's the user's problem
    nonfungiblePositionManager.safeTransferFrom(
        address(this), 
        msg.sender, 
        tokenId
    );
}
```

---

## 3. Approval and Access Control Issues

### 3.1 Approval Not Cleared on Transfer

**Root Cause:** NFT approvals (single token or operator) are not revoked when the NFT is transferred, allowing previous approved addresses to reclaim the token.

**Attack Scenario:**
1. Alice approves Eve to transfer her NFT
2. Eve transfers NFT to Bob
3. Bob sells/transfers NFT back to Alice
4. Eve (still approved) can steal the NFT again without new approval

**Observed Frequency:** 15+ reports
**Consensus Severity:** HIGH

**Example 1: Persistent Approval After Transfer** [HIGH]
```solidity
// ❌ VULNERABLE: Approval persists across transfers
contract VulnerableNFT {
    mapping(address => mapping(uint256 => address)) public nftApprovals;
    
    function approveTransferERC721(uint256 tokenId, address delegate) external {
        require(msg.sender == ownerOf(tokenId));
        nftApprovals[msg.sender][tokenId] = delegate;  // Sets approval
    }
    
    function transferERC721(address to, uint256 tokenId) external {
        address owner = ownerOf(tokenId);
        require(msg.sender == owner || nftApprovals[owner][tokenId] == msg.sender);
        
        _transfer(owner, to, tokenId);
        // ❌ MISSING: Clear approval after transfer
        // nftApprovals[owner][tokenId] = address(0);
    }
}
```
> 📖 Reference: [reports/erc721_nft_findings/h-02-nft-transfer-approvals-are-not-removed-and-cannot-be-revoked-thus-leading-t.md](../../../reports/erc721_nft_findings/h-02-nft-transfer-approvals-are-not-removed-and-cannot-be-revoked-thus-leading-t.md)

**Example 2: Key Transfer Without Clearing Approvals** [HIGH]
```solidity
// ❌ VULNERABLE: Trading keys retain old approvals
function transferKey(address to, uint256 tokenId) external {
    require(ownerOf(tokenId) == msg.sender);
    _transfer(msg.sender, to, tokenId);
    // ❌ MISSING: tokenApprovals[tokenId] = address(0);
}
```

**✅ SECURE: Clear Approvals on Transfer**
```solidity
// ✅ SECURE: Approvals cleared during transfer
function _transfer(address from, address to, uint256 tokenId) internal override {
    super._transfer(from, to, tokenId);
    
    // Clear single-token approval
    _approve(address(0), tokenId);
    
    // Note: setApprovalForAll is per-owner, automatically doesn't apply to new owner
}
```

### 3.2 Missing Approval Revocation Mechanism

**Root Cause:** Protocol lacks a way to revoke previously granted approvals, leaving users vulnerable if delegates become compromised.

**Observed Frequency:** 10+ reports
**Consensus Severity:** MEDIUM to HIGH

**Example: No Revoke Function** [MEDIUM]
```solidity
// ❌ VULNERABLE: Can only set approval, not revoke
function approveTransferERC721(uint256 tokenId, address delegate) external {
    require(msg.sender == ownerOf(tokenId));
    nftApprovals[tokenId] = delegate;  // Can only set, not unset
}
```

**✅ SECURE: Parameterized Approval**
```solidity
// ✅ SECURE: Boolean parameter allows revocation
function approveTransferERC721(uint256 tokenId, address delegate, bool approved) external {
    require(msg.sender == ownerOf(tokenId));
    if (approved) {
        nftApprovals[tokenId] = delegate;
    } else {
        delete nftApprovals[tokenId];
    }
}
```

---

## 4. Voting and Delegation Vulnerabilities

### 4.1 Double Voting Through Self-Delegation

**Root Cause:** When NFT holders first self-delegate, incorrect checkpoint logic allows them to double their voting power.

**Attack Scenario:**
1. Alice owns tokens and has never delegated
2. Alice calls `delegate(Alice)` to self-delegate
3. Due to bug, voting power is not properly transferred from default
4. Alice now has 2x voting power

**Observed Frequency:** 10+ reports
**Consensus Severity:** HIGH

**Example 1: Default Delegation Bug** [HIGH]
```solidity
// ❌ VULNERABLE: Self-delegation doubles voting power
function _delegate(address _from, address _to) internal {
    // Get previous delegate (address(0) if never delegated)
    address prevDelegate = delegation[_from];  // Returns address(0)
    
    delegation[_from] = _to;
    
    // Move votes from prevDelegate to _to
    // BUG: If prevDelegate == address(0), votes are created, not moved
    _moveDelegateVotes(prevDelegate, _to, balanceOf(_from));
}

function _moveDelegateVotes(address _from, address _to, uint256 _amount) internal {
    if (_from != address(0)) {
        // Never executes if user self-delegates first time
        _writeCheckpoint(_from, numCheckpoints[_from], -int256(_amount));
    }
    if (_to != address(0)) {
        // Always adds votes - effectively doubling if self-delegating first
        _writeCheckpoint(_to, numCheckpoints[_to], int256(_amount));
    }
}
```
> 📖 Reference: [reports/erc721_nft_findings/h-04-erc721votes-token-owners-can-double-voting-power-through-self-delegation.md](../../../reports/erc721_nft_findings/h-04-erc721votes-token-owners-can-double-voting-power-through-self-delegation.md)

**✅ SECURE: Proper Default Delegate Handling**
```solidity
// ✅ SECURE: Use delegates() function for actual delegate
function _delegate(address _from, address _to) internal {
    address prevDelegate = delegates(_from);  // Returns _from if not delegated
    delegation[_from] = _to;
    _moveDelegateVotes(prevDelegate, _to, balanceOf(_from));
}

function delegates(address account) public view returns (address) {
    address delegate = delegation[account];
    return delegate == address(0) ? account : delegate;  // Self-delegate by default
}
```

### 4.2 Delegation Disables NFT Transfers

**Root Cause:** After delegating votes away, the `_afterTokenTransfer` hook attempts to move votes from the token owner (who has 0 votes) instead of the delegate, causing underflow.

**Attack Scenario:**
1. Alice self-delegates, accumulating voting power
2. Alice delegates to Bob, transferring all voting power
3. Alice tries to transfer her NFT
4. `_afterTokenTransfer` tries to subtract from Alice's (now 0) balance
5. Transaction reverts, NFT is stuck

**Observed Frequency:** 5+ reports
**Consensus Severity:** HIGH

**Example: Transfer After Delegation** [HIGH]
```solidity
// ❌ VULNERABLE: Uses owner instead of delegate
function _afterTokenTransfer(address _from, address _to, uint256) internal override {
    // BUG: Should use delegates(_from), not _from directly
    // If _from delegated away their votes, their checkpoint is 0
    _moveDelegateVotes(_from, _to, 1);  // Reverts on underflow
}
```
> 📖 Reference: [reports/erc721_nft_findings/h-02-erc721votess-delegation-disables-nft-transfers-and-burning.md](../../../reports/erc721_nft_findings/h-02-erc721votess-delegation-disables-nft-transfers-and-burning.md)

**✅ SECURE: Use Delegates in Transfer Hook**
```solidity
// ✅ SECURE: Move votes between actual delegates
function _afterTokenTransfer(address _from, address _to, uint256) internal override {
    // delegates(address(0)) == address(0) for mint/burn
    _moveDelegateVotes(delegates(_from), delegates(_to), 1);
}
```

### 4.3 Double Voting via Managed NFTs

**Root Cause:** Protocols with managed NFTs (holding multiple users' stakes) may allow voting power to be used twice when users withdraw from managed positions.

**Attack Scenario:**
1. Alice's managed NFT votes with 1000 power
2. Bob withdraws his stake from Alice's managed NFT
3. Bob's individual NFT now has 1000 voting power
4. Bob votes again in the same epoch
5. Total votes: 2000 from 1000 actual power

**Observed Frequency:** 6+ reports
**Consensus Severity:** MEDIUM to HIGH

**Example: Managed NFT Vote Shifting** [MEDIUM]
```solidity
// ❌ VULNERABLE: Vote power transferable within epoch
function withdrawManaged(uint256 managedTokenId) external {
    // Transfer voting power from managed to normal NFT
    _checkpoint(managedTokenId);  // Reduces managed NFT votes
    _checkpoint(msg.sender);       // Increases user's votes
    
    // ❌ MISSING: Check if managed NFT already voted this epoch
}
```
> 📖 Reference: [reports/erc721_nft_findings/double-voting-by-shifting-the-voting-power-between-managed-and-normal-nfts.md](../../../reports/erc721_nft_findings/double-voting-by-shifting-the-voting-power-between-managed-and-normal-nfts.md)

**✅ SECURE: Poke Managed NFT on Withdraw**
```solidity
// ✅ SECURE: Update managed NFT vote state on withdrawal
function withdrawManaged(uint256 managedTokenId) external {
    // Poke the voter to update the managed NFT's vote
    Voter.poke(managedTokenId);
    
    // Now safe to transfer voting power
    _checkpoint(managedTokenId);
    _checkpoint(msg.sender);
}
```

---

## 5. Royalty Manipulation

### 5.1 Royalty Fee Manipulation via Reentrancy

**Root Cause:** When royalties are calculated twice (once for validation, once for payment), an attacker controlling the royalty recipient can change the fee between calls.

**Attack Scenario:**
1. Buyer calls `buy()` function
2. Protocol calculates royalty fee (e.g., 0%) for validation
3. Protocol makes external call (e.g., checking stolen NFT oracle)
4. Attacker's callback changes royalty to 100%
5. Protocol pays royalty based on new 100% value
6. Entire purchase price goes to attacker as "royalty"

**Observed Frequency:** 5+ reports
**Consensus Severity:** HIGH to CRITICAL

**Example: Double Royalty Call Manipulation** [CRITICAL]
```solidity
// ❌ VULNERABLE: Royalty queried twice, can change between calls
function buy(uint256[] calldata tokenIds) external payable {
    uint256 totalRoyalty = 0;
    
    // First loop: Calculate expected royalties (attacker sets to 0%)
    for (uint i = 0; i < tokenIds.length; i++) {
        (uint256 royaltyFee,) = _getRoyalty(tokenIds[i], salePrice);
        totalRoyalty += royaltyFee;
    }
    
    require(msg.value >= netCost + totalRoyalty, "Insufficient payment");
    
    // External call - attacker can change royalty here
    _checkStolenNFT(tokenIds);  // Untrusted external call
    
    // Second loop: Pay royalties (attacker changed to 100%)
    for (uint i = 0; i < tokenIds.length; i++) {
        (uint256 royaltyFee, address recipient) = _getRoyalty(tokenIds[i], salePrice);
        // ❌ Now royaltyFee is the entire salePrice!
        recipient.safeTransferETH(royaltyFee);  // Drains pool
    }
}
```
> 📖 Reference: [reports/erc721_nft_findings/h-01-royalty-receiver-can-drain-a-private-pool.md](../../../reports/erc721_nft_findings/h-01-royalty-receiver-can-drain-a-private-pool.md)

**✅ SECURE: Cache Royalty Values**
```solidity
// ✅ SECURE: Calculate and pay royalties in single pass
function buy(uint256[] calldata tokenIds) external payable {
    // Single loop: Calculate AND pay immediately
    for (uint i = 0; i < tokenIds.length; i++) {
        (uint256 royaltyFee, address recipient) = _getRoyalty(tokenIds[i], salePrice);
        
        // Pay immediately with cached value
        if (royaltyFee > 0 && recipient != address(0)) {
            recipient.safeTransferETH(royaltyFee);
        }
    }
}
```

---

## 6. ERC-721 Standard Compliance Issues

### 6.1 tokenURI Not Reverting for Non-Existent Tokens

**Root Cause:** ERC-721 standard requires `tokenURI` to revert for non-existent tokens. Implementations that return empty strings or default values violate the standard.

**Impact:** Breaks composability with other protocols expecting standard behavior.

**Observed Frequency:** 9+ reports
**Consensus Severity:** MEDIUM

**Example: Non-Compliant tokenURI** [MEDIUM]
```solidity
// ❌ VULNERABLE: Returns value for non-existent tokens
function tokenURI(uint256 tokenId) public view override returns (string memory) {
    // Missing: require(_exists(tokenId), "Nonexistent token");
    return descriptor.tokenURI(tokenId, artPieces[tokenId].metadata);
}
```
> 📖 Reference: [reports/erc721_nft_findings/m-02-violation-of-erc-721-standard-in-verbstokentokenuri-implementation.md](../../../reports/erc721_nft_findings/m-02-violation-of-erc-721-standard-in-verbstokentokenuri-implementation.md)

**✅ SECURE: Standard-Compliant tokenURI**
```solidity
// ✅ SECURE: Reverts for non-existent tokens per EIP-721
function tokenURI(uint256 tokenId) public view override returns (string memory) {
    require(_exists(tokenId), "ERC721: URI query for nonexistent token");
    return descriptor.tokenURI(tokenId, artPieces[tokenId].metadata);
}
```

### 6.2 Incorrect `onERC721Received` Implementation

**Root Cause:** Custom implementations of `onERC721Received` may have incorrect access control, wrong return values, or logic errors.

**Observed Frequency:** 10+ reports
**Consensus Severity:** MEDIUM to HIGH

**Example: DoS via Callback Logic** [MEDIUM]
```solidity
// ❌ VULNERABLE: Can be exploited to DoS admin
function onERC721Received(
    address operator,
    address from,
    uint256 tokenId,
    bytes calldata data
) external override returns (bytes4) {
    // Attacker can front-run with same tokenId
    require(hasRole(DEFAULT_ADMIN_ROLE, from), "Only admin");
    require(_uniV3NftByToken0Token1[nft.token0][nft.token1] == 0, "Exists");
    
    // ... registration logic
    return this.onERC721Received.selector;
}
```
> 📖 Reference: [reports/erc721_nft_findings/m-01-the-onerc721received-is-not-implemented-correctly.md](../../../reports/erc721_nft_findings/m-01-the-onerc721received-is-not-implemented-correctly.md)

### 6.3 balanceOf Overflow

**Root Cause:** Some optimized ERC721 implementations pack balanceOf with auxiliary data, potentially causing overflow in extreme edge cases.

**Observed Frequency:** 4+ reports
**Consensus Severity:** MEDIUM

**Example: Packed Storage Overflow** [MEDIUM]
```solidity
// ❌ VULNERABLE: Overflow protection fails in edge case
function _mint(address to, uint256 id) internal {
    let toBalanceSlot := keccak256(0x0c, 0x1c)
    let toBalanceSlotPacked := add(sload(toBalanceSlot), 1)
    
    // If auxiliary bits are all 1 AND balanceOf is max,
    // overflow wraps to 1, clearing auxiliary data
    if iszero(mul(to, and(toBalanceSlotPacked, _MAX_ACCOUNT_BALANCE))) {
        mstore(shl(2, iszero(to)), 0xea553b3401336cea)
        revert(0x1c, 0x04)
    }
}
```
> 📖 Reference: [reports/erc721_nft_findings/erc721-balanceof-overflow-possible.md](../../../reports/erc721_nft_findings/erc721-balanceof-overflow-possible.md)

---

## 7. NFT Liquidation and Collateral Issues

### 7.1 NFTs Locked in Contracts

**Root Cause:** NFTs used as collateral may become permanently locked if liquidation or withdrawal mechanisms have bugs.

**Observed Frequency:** 20+ reports
**Consensus Severity:** HIGH

**Example: Locked NFT After Liquidation** [HIGH]
```solidity
// ❌ VULNERABLE: NFT stuck if owner blocks transfer
function liquidatePosition(uint256 tokenId) external {
    // Liquidation logic...
    
    // If this fails (owner reverts), NFT is stuck
    nft.safeTransferFrom(address(this), owner, tokenId);
    
    // No fallback mechanism
}
```

**✅ SECURE: Pull Pattern for NFT Retrieval**
```solidity
// ✅ SECURE: Users pull NFTs instead of automatic push
function liquidatePosition(uint256 tokenId) external {
    // Liquidation logic...
    
    // Mark NFT as claimable instead of transferring
    claimableNFTs[owner][tokenId] = true;
    emit NFTClaimable(owner, tokenId);
}

function claimNFT(uint256 tokenId) external {
    require(claimableNFTs[msg.sender][tokenId], "Not claimable");
    delete claimableNFTs[msg.sender][tokenId];
    nft.safeTransferFrom(address(this), msg.sender, tokenId);
}
```

---

## 8. Self-Transfer Edge Cases

### 8.1 Self-Transfer Corrupts State

**Root Cause:** Self-transfers (from == to) may not be properly handled, causing state corruption in hooks or balance tracking.

**Attack Scenario:**
1. User transfers NFT to themselves
2. `afterUpdate` hook pushes new entry then pops last entry
3. Due to self-transfer, the newly pushed entry is popped
4. NFT's associated data (fees, liquidity) is cleared
5. NFT becomes worthless; can grief buyers

**Observed Frequency:** 11+ reports
**Consensus Severity:** MEDIUM to HIGH

**Example: Self-Transfer Clears Fee Data** [MEDIUM]
```solidity
// ❌ VULNERABLE: Self-transfer corrupts state
function afterUpdate(address _from, address _to, uint256 _tokenID) public {
    // Push new entry for recipient
    poolsFeeData[poolAddress][_to].push(feeDataArray[tokenIdIndex]);
    // feeDataArrayLength is now increased
    
    if (_from != address(0)) {
        // Delete and pop old entry
        delete feeDataArray[feeDataArrayLength - 1];
        feeDataArray.pop();
        // ❌ BUG: If _from == _to, this pops the entry we just pushed!
    }
}
```
> 📖 Reference: [reports/erc721_nft_findings/incorrect-handling-of-nft-self-transfer-in-afterupdate-hook-allows-the-owner-to-.md](../../../reports/erc721_nft_findings/incorrect-handling-of-nft-self-transfer-in-afterupdate-hook-allows-the-owner-to-.md)

**✅ SECURE: Disallow or Handle Self-Transfers**
```solidity
// ✅ SECURE Option 1: Disallow self-transfers
function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override {
    require(from != to, "Self-transfer not allowed");
    super._beforeTokenTransfer(from, to, tokenId);
}

// ✅ SECURE Option 2: Handle self-transfer properly
function afterUpdate(address _from, address _to, uint256 _tokenID) public {
    if (_from == _to) return;  // No-op for self-transfers
    
    // Normal transfer logic...
}
```

---

## Detection Patterns

### Code Patterns to Search For

```
// Transfer safety issues
- `transferFrom(` without `safe` prefix
- `_mint(` instead of `_safeMint(`
- Missing `onERC721Received` implementation

// Reentrancy vulnerabilities  
- `_safeMint` or `safeTransferFrom` before state updates
- External calls before state modifications
- Missing `nonReentrant` modifier on mint/transfer functions

// Approval issues
- Missing approval clearing in `_transfer`
- No revoke mechanism for approvals
- Approval checked against wrong address

// Voting/Delegation bugs
- `delegation[` mapping accessed directly instead of `delegates()` function
- Missing checkpoint updates on delegation
- Vote moves using owner instead of delegate

// Self-transfer issues
- Missing `from != to` check in transfer hooks
- Push/pop operations in transfer callbacks
```

### Audit Checklist

- [ ] All ERC721 transfers use `safeTransferFrom`
- [ ] All mints use `_safeMint` or validate receiver
- [ ] Reentrancy guards on functions with callbacks
- [ ] Checks-Effects-Interactions pattern followed
- [ ] Approvals cleared on transfer
- [ ] Revocation mechanism exists for approvals
- [ ] Delegation functions properly track actual delegates
- [ ] Self-transfers handled or disallowed
- [ ] `tokenURI` reverts for non-existent tokens
- [ ] `onERC721Received` returns correct selector
- [ ] Liquidation has fallback if transfer blocked

---

## Real-World Examples

### Known Exploits and Protocols

| Protocol | Vulnerability | Impact | Reference |
|----------|---------------|--------|-----------|
| Caviar | Reentrancy via ERC777 | Pool drain | [h-01-reentrancy-in-buy](../../../reports/erc721_nft_findings/h-01-reentrancy-in-buy-function-for-erc777-tokens-allows-buying-funds-with-consi.md) |
| Caviar Private Pools | Royalty manipulation | Pool drain | [h-01-royalty-receiver](../../../reports/erc721_nft_findings/h-01-royalty-receiver-can-drain-a-private-pool.md) |
| Nouns Builder | Self-delegation double voting | Governance manipulation | [h-04-erc721votes](../../../reports/erc721_nft_findings/h-04-erc721votes-token-owners-can-double-voting-power-through-self-delegation.md) |
| Visor Finance | Approval not cleared | NFT theft | [h-02-nft-transfer-approvals](../../../reports/erc721_nft_findings/h-02-nft-transfer-approvals-are-not-removed-and-cannot-be-revoked-thus-leading-t.md) |
| Revert Lend | Liquidation DoS | Bad debt | [h-06-owner-of-position](../../../reports/erc721_nft_findings/h-06-owner-of-a-position-can-prevent-liquidation-due-to-the-onerc721received-cal.md) |
| Panoptic | ERC777 reentrancy | Fee theft | [h-01-attacker-steal-fees](../../../reports/erc721_nft_findings/h-01-attacker-can-steal-all-fees-from-sfpm-in-pools-with-erc777-tokens.md) |

---

## Prevention Guidelines

### Development Best Practices

1. **Always use safe transfers**: Use `safeTransferFrom` and `_safeMint`
2. **Follow CEI pattern**: Update state before external calls
3. **Add reentrancy guards**: Use `nonReentrant` on functions with callbacks
4. **Clear approvals**: Reset approvals in `_transfer` override
5. **Handle edge cases**: Validate self-transfers, zero addresses
6. **Use delegates() function**: Don't access delegation mapping directly
7. **Cache external values**: Don't query same value twice with external calls between
8. **Implement pull patterns**: For liquidation, let users claim NFTs

### Testing Requirements

- Unit tests for self-transfer scenarios
- Reentrancy tests with malicious `onERC721Received`
- Fuzz testing for approval/delegation state
- Integration tests with ERC777 tokens
- Liquidation tests with reverting recipients

---

## Keywords for Search

`ERC721`, `NFT`, `safeTransferFrom`, `transferFrom`, `_safeMint`, `_mint`, `onERC721Received`, `approve`, `setApprovalForAll`, `approval`, `delegation`, `delegate`, `voting power`, `double voting`, `reentrancy`, `callback`, `royalty`, `EIP-2981`, `tokenURI`, `ownerOf`, `balanceOf`, `ERC1155`, `position NFT`, `collateral`, `liquidation`, `self-transfer`, `transfer hook`, `checkpoint`, `voting escrow`, `veNFT`, `managed NFT`, `marketplace`, `auction`, `mint`, `burn`, `token standard`, `non-fungible`, `NFT security`, `NFT vulnerability`, `ERC721 exploit`, `CEI pattern`, `checks effects interactions`, `pull pattern`, `escrow`, `ERC777 reentrancy`

---

## Related Vulnerabilities

- [Chainlink Oracle Vulnerabilities](../oracle/chainlink/) - Oracle integration with NFT protocols
- [Pyth Oracle Vulnerabilities](../oracle/pyth/) - Price feed issues affecting NFT collateral
- General reentrancy patterns (cross-reference with reentrancy database)
- Access control vulnerabilities (cross-reference with access control database)

---

## References

### Standards
- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [EIP-2981: NFT Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981)
- [EIP-1155: Multi Token Standard](https://eips.ethereum.org/EIPS/eip-1155)

### Security Research
- [OpenZeppelin ERC721 Documentation](https://docs.openzeppelin.com/contracts/4.x/erc721)
- [SWC Registry: Reentrancy](https://swcregistry.io/docs/SWC-107)

---

*This database was generated from analysis of 1,730+ vulnerability reports from Solodit/Cyfrin audit database. Last updated: 2026-01-15.*
