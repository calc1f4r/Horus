---
# Core Classification (Required)
protocol: generic
chain: everychain
category: account_abstraction
vulnerability_type: erc7702_integration

# Attack Vector Details (Required)
attack_type: logical_error|data_manipulation|access_control|session_key_abuse
affected_component: signature_verification|address_handling|callback_implementation|reentrancy_guard|session_key_management|permit_function

# ERC-7702 Specific Fields
eip_standard: EIP-7702
related_standards: EIP-1271|EIP-4337|EIP-712|ERC-4494

# Technical Primitives (Required)
primitives:
  - isContract
  - extcodesize
  - tx.origin
  - msg.sender
  - ECDSA.recover
  - isValidSignature
  - ERC1271
  - delegatecall
  - fallback
  - receive
  - onERC721Received
  - onERC1155Received
  - sessionKey
  - validateUserOp
  - permit
  - ERC4494

# Impact Classification (Required)
severity: high
impact: signature_bypass|fund_loss|dos|reentrancy|address_mismatch|session_impersonation|token_theft
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - account_abstraction
  - smart_wallet
  - pectra_upgrade
  - eoa_delegation
  - signature_verification
  - cross_chain
  - session_keys
  - nft_permit
  - rental_protocol

# Version Info
language: solidity
version: ">=0.8.0"

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | signature_verification | erc7702_integration

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - ECDSA.recover
  - ERC1271
  - ERC4494
  - _is7702DelegatedWallet
  - _unwrapAndSendETH
  - _validateNFTForRental
  - _validateSingleCall
  - allowance
  - approve
  - block.timestamp
  - bridgeTokens
  - checkTransaction
  - claim
  - completeMission
  - create
  - delegatecall
  - deposit
  - emergencyWithdraw
  - execute
  - executeWithCallback
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### isContract/extcodesize Logic Broken
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| FactcheckDotFun - Signature Verification Broken | `reports/erc7702_findings/m-01-signatureverification-brokenundereip-7702duetorelianceoniscontractlogic.md` | MEDIUM | Kann |

### Reentrancy via EIP-7702 EOAs
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Across Protocol - Reentrancy via 7702 EOA | `reports/erc7702_findings/eip-7702-eoa-accounts-treatment-could-result-in-reentrancy.md` | MEDIUM | OpenZeppelin |

### Missing Token Callbacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Otim Smart Wallet - Lack of NFT Callbacks | `reports/erc7702_findings/lack-of-nft-callbacks.md` | MEDIUM | Trail of Bits |

### Cross-Chain Address Mismatch
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Securitize Bridge - Incorrect Address Handling | `reports/erc7702_findings/incorrect-address-handling-for-account-abstraction-wallets-in-securitizebridgebr.md` | MEDIUM | Cyfrin |

### tx.origin Exploitation with Smart Wallets
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Optimism - Theft of Bonds from Smart Wallet Users | `reports/erc7702_findings/m-3-theft-of-initial-bonds-from-proposers-who-are-using-smart-wallets.md` | MEDIUM | Sherlock |

### Session Key Impersonation in Smart Wallets
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Etherspot - SessionKey Owner Impersonation | `reports/bridge_crosschain_findings/h-01-sessionkey-owner-can-impersonate-another-session-key-owner-for-the-same-sma.md` | HIGH | Shieldify |

### NFT Permit Function Exploitation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| reNFT - NFT Permit Hijack Attack | `reports/erc7702_findings/m-02-a-malicious-borrower-can-hijack-any-nft-with-permit-function-he-rents.md` | MEDIUM | Code4rena |

### Cross-Chain AA Wallet Fund Loss (Extended)
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Nudge.xyz - Cross-Chain Reallocation Loss | `reports/bridge_crosschain_findings/m-03-all-reallocate-cross-chain-token-and-rewards-will-be-lost-for-the-users-usi.md` | MEDIUM | Code4rena |
| Reya Network - Deposit Fallback Bridging Loss | `reports/bridge_crosschain_findings/h-01-user-can-lose-tokens-during-deposit-fallback-bridging.md` | HIGH | Pashov Audit Group |
| Securitize - Smart Wallet Destination Address | `reports/bridge_crosschain_findings/investors-using-smart-contract-wallets-may-have-their-destination-chain-tokens-i.md` | MEDIUM | Cyfrin |

### External Links
- [EIP-7702 Specification](https://eips.ethereum.org/EIPS/eip-7702)
- [EIP-1271: Standard Signature Validation](https://eips.ethereum.org/EIPS/eip-1271)
- [Pectra Upgrade Overview](https://ethereum.org/en/roadmap/pectra/)

---

# EIP-7702 Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for EIP-7702 Security Audits**

---

## Table of Contents

1. [Understanding EIP-7702](#understanding-eip-7702)
2. [isContract/extcodesize Logic Broken](#1-iscontractextcodesize-logic-broken)
3. [Reentrancy via EIP-7702 Delegated EOAs](#2-reentrancy-via-eip-7702-delegated-eoas)
4. [Missing Token Receiver Callbacks](#3-missing-token-receiver-callbacks)
5. [Cross-Chain Address Mismatch](#4-cross-chain-address-mismatch)
6. [tx.origin Exploitation with Smart Wallets](#5-txorigin-exploitation-with-smart-wallets)
7. [Fallback/Receive Function Issues](#6-fallbackreceive-function-issues)
8. [Session Key Impersonation in Smart Wallets](#7-session-key-impersonation-in-smart-wallets)
9. [NFT Permit Function Exploitation](#8-nft-permit-function-exploitation)

---

## Understanding EIP-7702

### Overview

EIP-7702, introduced with the Ethereum Pectra upgrade, fundamentally changes the EOA/contract distinction that many smart contracts rely upon. This EIP allows Externally Owned Accounts (EOAs) to temporarily delegate their execution to smart contract code during a transaction.

**Key Technical Changes:**
- EOAs can now have code attached during transaction execution
- `extcodesize(address)` may return non-zero for EOAs with delegated code
- `address.code.length > 0` checks become unreliable for EOA detection
- EOAs can execute complex logic in `receive`/`fallback` functions
- The boundary between EOA and contract becomes blurred

> **Root Cause Statement**: "EIP-7702 breaks the fundamental assumption that addresses with code are contracts and addresses without code are EOAs, causing signature verification, reentrancy guards, and callback implementations to fail or behave unexpectedly."

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | signature_verification | erc7702_integration`
- Interaction scope: `multi_contract`
- Primary affected component(s): `signature_verification|address_handling|callback_implementation|reentrancy_guard|session_key_management|permit_function`
- High-signal code keywords: `ECDSA.recover`, `ERC1271`, `ERC4494`, `_is7702DelegatedWallet`, `_unwrapAndSendETH`, `_validateNFTForRental`, `_validateSingleCall`, `allowance`
- Typical sink / impact: `signature_bypass|fund_loss|dos|reentrancy|address_mismatch|session_impersonation|token_theft`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `BrokenWalletImplementation.function -> DefaultAccountImplementation.function -> DisputeGame.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

## 1. isContract/extcodesize Logic Broken

### Overview

Protocols that distinguish between EOAs and contracts using `extcodesize`, `isContract()`, or `address.code.length` checks face critical vulnerabilities post-EIP-7702. When an EOA delegates to contract code via EIP-7702, these checks return non-zero values, causing the protocol to misidentify EOAs as contracts.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc7702_findings/m-01-signatureverification-brokenundereip-7702duetorelianceoniscontractlogic.md` (FactcheckDotFun - Kann)

### Vulnerability Description

#### Root Cause

Smart contracts commonly use `isContract()` checks to determine whether to verify signatures using ECDSA (for EOAs) or EIP-1271 `isValidSignature()` (for contracts). EIP-7702 allows EOAs to temporarily attach code, making them appear as contracts at runtime.

#### Attack Scenario

1. User has an EOA that uses EIP-7702 to delegate to a smart wallet implementation
2. User signs a valid ECDSA signature for an order/action
3. Protocol calls `isContract(user)` which returns `true` (due to delegated code)
4. Protocol attempts EIP-1271 `isValidSignature()` call instead of ECDSA verification
5. If the delegated code doesn't implement ERC-1271, the call reverts
6. User's legitimate ECDSA signature is rejected, causing denial of service or broken functionality

### Vulnerable Pattern Examples

**Example 1: Signature Verification with isContract Check** [MEDIUM]
> 📖 Reference: `reports/erc7702_findings/m-01-signatureverification-brokenundereip-7702duetorelianceoniscontractlogic.md`
```solidity
// ❌ VULNERABLE: Relies on isContract to choose verification method
function verifySignature(
    address signer,
    bytes32 hash,
    bytes memory signature
) internal view returns (bool) {
    if (isContract(signer)) {
        // Will fail for EIP-7702 EOAs that don't implement ERC-1271
        (bool success, bytes memory result) = signer.staticcall(
            abi.encodeWithSelector(IERC1271.isValidSignature.selector, hash, signature)
        );
        return success && abi.decode(result, (bytes4)) == IERC1271.isValidSignature.selector;
    } else {
        // Never reached for EIP-7702 EOAs
        return ECDSA.recover(hash, signature) == signer;
    }
}
```

**Example 2: Using extcodesize Directly** [MEDIUM]
```solidity
// ❌ VULNERABLE: Direct extcodesize check
function isContract(address account) internal view returns (bool) {
    uint256 size;
    assembly {
        size := extcodesize(account)
    }
    return size > 0;  // Returns true for EIP-7702 EOAs with delegated code!
}
```

**Example 3: OpenZeppelin's Address.isContract Pattern** [MEDIUM]
```solidity
// ❌ VULNERABLE: Common pattern that breaks with EIP-7702
function validateOrder(Order memory order, bytes memory signature) external {
    if (Address.isContract(order.maker)) {
        // EIP-1271 verification
        require(
            IERC1271(order.maker).isValidSignature(
                _hashOrder(order),
                signature
            ) == MAGIC_VALUE,
            "Invalid contract signature"
        );
    } else {
        // ECDSA verification - never reached for 7702 EOAs
        require(
            ECDSA.recover(_hashOrder(order), signature) == order.maker,
            "Invalid EOA signature"
        );
    }
}
```

### Impact Analysis

#### Technical Impact
- Signature verification logic breaks for EIP-7702 enabled accounts
- Legitimate ECDSA signatures are rejected
- EIP-1271 calls fail when delegated code doesn't implement the interface
- Protocol functions become inaccessible to EIP-7702 users

#### Business Impact
- Users unable to execute orders, trades, or other signed actions
- Protocol becomes incompatible with modern wallet standards
- User experience degradation post-Pectra upgrade
- Potential loss of market share to EIP-7702 compatible protocols

#### Affected Scenarios
- DEX order matching (0x, Seaport, CoW Protocol patterns)
- Permit-based token approvals
- Off-chain signed messages for gasless transactions
- Any protocol distinguishing EOA vs contract for signature handling

### Secure Implementation

**Fix 1: Try ECDSA First, Fall Back to EIP-1271**
```solidity
// ✅ SECURE: Try ECDSA recovery first, fall back to EIP-1271
function verifySignature(
    address signer,
    bytes32 hash,
    bytes memory signature
) internal view returns (bool) {
    // First, try ECDSA recovery (works for regular EOAs and 7702 EOAs)
    if (signature.length == 65) {
        address recovered = ECDSA.recover(hash, signature);
        if (recovered == signer) {
            return true;
        }
    }
    
    // Fall back to EIP-1271 for smart contract wallets
    if (signer.code.length > 0) {
        try IERC1271(signer).isValidSignature(hash, signature) returns (bytes4 magicValue) {
            return magicValue == IERC1271.isValidSignature.selector;
        } catch {
            return false;
        }
    }
    
    return false;
}
```

**Fix 2: Support Both Methods Simultaneously**
```solidity
// ✅ SECURE: Check both ECDSA and EIP-1271 regardless of code presence
function verifySignature(
    address signer,
    bytes32 hash,
    bytes memory signature
) internal view returns (bool) {
    // Try ECDSA first
    (address recovered, ECDSA.RecoverError error) = ECDSA.tryRecover(hash, signature);
    if (error == ECDSA.RecoverError.NoError && recovered == signer) {
        return true;
    }
    
    // Try EIP-1271 if signer has code (contract or 7702 EOA)
    if (signer.code.length > 0) {
        try IERC1271(signer).isValidSignature(hash, signature) returns (bytes4 result) {
            return result == IERC1271.isValidSignature.selector;
        } catch {}
    }
    
    return false;
}
```

**Fix 3: Use SignatureChecker Library**
```solidity
// ✅ SECURE: Use OpenZeppelin's updated SignatureChecker
import {SignatureChecker} from "@openzeppelin/contracts/utils/cryptography/SignatureChecker.sol";

function verifySignature(
    address signer,
    bytes32 hash,
    bytes memory signature
) internal view returns (bool) {
    // SignatureChecker handles both EOA and contract signatures correctly
    return SignatureChecker.isValidSignatureNow(signer, hash, signature);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- isContract(address) checks before signature verification
- extcodesize assembly usage for EOA/contract distinction
- address.code.length > 0 checks in signature paths
- Branching logic: if (isContract) { EIP-1271 } else { ECDSA }
- Exclusive ECDSA.recover without EIP-1271 fallback
```

#### Audit Checklist
- [ ] Verify signature verification handles both ECDSA and EIP-1271
- [ ] Check that isContract checks don't gate critical functionality
- [ ] Ensure ECDSA is attempted regardless of code presence
- [ ] Test with EIP-7702 enabled EOAs (delegated to various implementations)
- [ ] Verify graceful degradation when EIP-1271 call fails

---

## 2. Reentrancy via EIP-7702 Delegated EOAs

### Overview

When protocols send ETH or tokens to addresses identified as EOAs, they typically use limited gas stipends (2300 gas) assuming EOAs cannot execute complex logic. EIP-7702 breaks this assumption by allowing EOAs to execute arbitrary code in their `receive` or `fallback` functions via delegation.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc7702_findings/eip-7702-eoa-accounts-treatment-could-result-in-reentrancy.md` (Across Protocol - OpenZeppelin)

### Vulnerability Description

#### Root Cause

Protocols that detect EIP-7702 delegated wallets may use low-level `.call` with unlimited gas to send ETH, enabling complex operations in the recipient's `receive`/`fallback` functions. This opens reentrancy attack vectors that traditional EOA recipients couldn't exploit.

#### Attack Scenario

1. Attacker sets up an EIP-7702 EOA delegating to malicious contract code
2. Protocol detects the 7702 delegation and uses `.call` with unlimited gas to send ETH
3. Attacker's delegated `receive`/`fallback` function executes malicious logic
4. Attacker reenters the protocol during vulnerable state
5. Protocol state is corrupted or funds are drained

### Vulnerable Pattern Examples

**Example 1: Sending ETH to Detected 7702 Wallet** [MEDIUM]
> 📖 Reference: `reports/erc7702_findings/eip-7702-eoa-accounts-treatment-could-result-in-reentrancy.md`
```solidity
// ❌ VULNERABLE: Unlimited gas call to 7702 wallet enables reentrancy
function _unwrapAndSendETH(address to, uint256 amount) internal {
    WETH.withdraw(amount);
    
    if (_is7702DelegatedWallet(to)) {
        // Low-level call with unlimited gas - can execute complex operations
        (bool success, ) = to.call{value: amount}("");
        require(success, "ETH transfer failed");
    } else {
        // Standard transfer with 2300 gas stipend
        payable(to).transfer(amount);
    }
}

function _is7702DelegatedWallet(address account) internal view returns (bool) {
    // Check for EIP-7702 delegation prefix
    bytes memory code = account.code;
    return code.length >= 23 && 
           code[0] == 0xef && 
           code[1] == 0x01 && 
           code[2] == 0x00;
}
```

**Example 2: Callback Handler with Unlimited Gas** [MEDIUM]
```solidity
// ❌ VULNERABLE: Callback to 7702 EOA can reenter
function executeWithCallback(address recipient, uint256 amount, bytes calldata data) external {
    // Transfer tokens
    token.transfer(recipient, amount);
    
    // Execute callback with unlimited gas
    if (recipient.code.length > 0) {
        ICallback(recipient).onTokenReceived(msg.sender, amount, data);
    }
    
    // State update after external call - vulnerable to reentrancy
    userBalances[recipient] += amount;
}
```

### Impact Analysis

#### Technical Impact
- Reentrancy attacks possible from addresses that appear as EOAs
- State corruption through reentrant calls
- Breaks assumptions about EOA recipient behavior
- CEI pattern violations become exploitable

#### Business Impact
- Potential fund drainage through reentrancy
- Protocol security model compromised
- Increased attack surface post-Pectra

#### Affected Scenarios
- ETH/WETH unwrapping and sending flows
- Protocols with callback mechanisms
- Any code path that sends value to detected 7702 wallets

### Secure Implementation

**Fix 1: Use Reentrancy Guards**
```solidity
// ✅ SECURE: Always use reentrancy protection
import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureProtocol is ReentrancyGuard {
    function _unwrapAndSendETH(address to, uint256 amount) internal nonReentrant {
        WETH.withdraw(amount);
        (bool success, ) = to.call{value: amount}("");
        require(success, "ETH transfer failed");
    }
}
```

**Fix 2: Limit Gas for All External Calls**
```solidity
// ✅ SECURE: Limit gas regardless of recipient type
function _unwrapAndSendETH(address to, uint256 amount) internal {
    WETH.withdraw(amount);
    
    // Use limited gas stipend for all recipients
    (bool success, ) = to.call{value: amount, gas: 10000}("");
    require(success, "ETH transfer failed");
}
```

**Fix 3: Follow CEI Pattern Strictly**
```solidity
// ✅ SECURE: Checks-Effects-Interactions pattern
function withdraw(uint256 amount) external nonReentrant {
    // Checks
    require(balances[msg.sender] >= amount, "Insufficient balance");
    
    // Effects - update state BEFORE external call
    balances[msg.sender] -= amount;
    
    // Interactions - external call last
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- .call{value: amount}("") without reentrancy guard
- State changes after external calls to user addresses
- Special handling for detected 7702 wallets with unlimited gas
- Missing nonReentrant modifiers on functions with external calls
```

#### Audit Checklist
- [ ] Verify all external calls are protected by reentrancy guards
- [ ] Check that CEI pattern is followed consistently
- [ ] Ensure gas limits are appropriate for external calls
- [ ] Test reentrancy scenarios with 7702 delegated EOAs

---

## 3. Missing Token Receiver Callbacks

### Overview

When an EOA upgrades to an EIP-7702 smart wallet, it transforms from an EOA to a smart contract in the eyes of token standards like ERC-721 and ERC-1155. These standards require smart contracts to implement specific receiver callbacks (`onERC721Received`, `onERC1155Received`) for safe transfers to succeed.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc7702_findings/lack-of-nft-callbacks.md` (Otim Smart Wallet - Trail of Bits)

### Vulnerability Description

#### Root Cause

EIP-7702 smart wallet implementations that don't implement `IERC721Receiver` and `IERC1155Receiver` interfaces will fail to receive NFTs via `safeTransfer` functions. Since the delegated code makes the EOA appear as a contract, token standards enforce callback checks.

#### Attack Scenario

1. User upgrades their EOA to use an EIP-7702 smart wallet delegation
2. User attempts to receive an NFT via `safeTransferFrom`
3. The token contract checks if recipient is a contract (returns true for 7702)
4. Token contract calls `onERC721Received` on the recipient
5. If the delegated implementation doesn't have this callback, the call reverts
6. User cannot receive NFTs, causing DoS for their wallet

### Vulnerable Pattern Examples

**Example 1: Smart Wallet Missing ERC-721 Receiver** [MEDIUM]
> 📖 Reference: `reports/erc7702_findings/lack-of-nft-callbacks.md`
```solidity
// ❌ VULNERABLE: No ERC-721 receiver callback
contract SmartWalletImplementation {
    address public owner;
    
    function execute(
        address target,
        uint256 value,
        bytes calldata data
    ) external returns (bytes memory) {
        require(msg.sender == owner, "Not owner");
        (bool success, bytes memory result) = target.call{value: value}(data);
        require(success, "Execution failed");
        return result;
    }
    
    receive() external payable {}
    
    // Missing: onERC721Received
    // Missing: onERC1155Received
    // Missing: onERC1155BatchReceived
}
```

**Example 2: Incomplete Interface Implementation** [MEDIUM]
```solidity
// ❌ VULNERABLE: Only implements ERC-721, not ERC-1155
contract PartialWalletImplementation is IERC721Receiver {
    function onERC721Received(
        address,
        address,
        uint256,
        bytes calldata
    ) external pure returns (bytes4) {
        return IERC721Receiver.onERC721Received.selector;
    }
    
    // Missing: onERC1155Received
    // Missing: onERC1155BatchReceived
}
```

### Impact Analysis

#### Technical Impact
- EIP-7702 enabled wallets cannot receive NFTs via safeTransfer
- Transaction reverts on NFT marketplaces and transfers
- Incompatibility with major NFT ecosystems

#### Business Impact
- Users locked out of NFT marketplaces
- Breaking change when upgrading EOA to smart wallet
- Poor user experience with EIP-7702 adoption

#### Affected Scenarios
- NFT marketplace purchases (OpenSea, Blur, etc.)
- NFT airdrops using safeTransfer
- Gaming NFT rewards and transfers
- Any ERC-721/ERC-1155 safeTransfer operations

### Secure Implementation

**Fix 1: Implement All Required Callbacks**
```solidity
// ✅ SECURE: Full token receiver support
import {IERC721Receiver} from "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import {IERC1155Receiver} from "@openzeppelin/contracts/token/ERC1155/IERC1155Receiver.sol";
import {IERC165} from "@openzeppelin/contracts/utils/introspection/IERC165.sol";

contract SecureSmartWallet is IERC721Receiver, IERC1155Receiver, IERC165 {
    function onERC721Received(
        address,
        address,
        uint256,
        bytes calldata
    ) external pure override returns (bytes4) {
        return IERC721Receiver.onERC721Received.selector;
    }
    
    function onERC1155Received(
        address,
        address,
        uint256,
        uint256,
        bytes calldata
    ) external pure override returns (bytes4) {
        return IERC1155Receiver.onERC1155Received.selector;
    }
    
    function onERC1155BatchReceived(
        address,
        address,
        uint256[] calldata,
        uint256[] calldata,
        bytes calldata
    ) external pure override returns (bytes4) {
        return IERC1155Receiver.onERC1155BatchReceived.selector;
    }
    
    function supportsInterface(bytes4 interfaceId) external pure override returns (bool) {
        return interfaceId == type(IERC721Receiver).interfaceId ||
               interfaceId == type(IERC1155Receiver).interfaceId ||
               interfaceId == type(IERC165).interfaceId;
    }
}
```

**Fix 2: Use TokenCallbackHandler Base Contract**
```solidity
// ✅ SECURE: Inherit from comprehensive handler
import {TokenCallbackHandler} from "@safe-global/safe-contracts/contracts/handler/TokenCallbackHandler.sol";

contract SecureSmartWallet is TokenCallbackHandler {
    // TokenCallbackHandler implements all ERC-721, ERC-1155, and ERC-777 callbacks
    
    function execute(
        address target,
        uint256 value,
        bytes calldata data
    ) external returns (bytes memory) {
        // Wallet logic
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Smart wallet implementations without IERC721Receiver
- Missing onERC721Received function
- Missing onERC1155Received and onERC1155BatchReceived
- Incomplete supportsInterface implementation
```

#### Audit Checklist
- [ ] Verify EIP-7702 delegate contracts implement IERC721Receiver
- [ ] Check for IERC1155Receiver implementation
- [ ] Ensure supportsInterface returns correct values
- [ ] Test NFT transfers to EIP-7702 enabled wallets

---

## 4. Cross-Chain Address Mismatch

### Overview

Account Abstraction wallets (including those using EIP-7702 or EIP-4337) can have different addresses across different chains for the same logical user. This breaks the common assumption that `msg.sender` on one chain equals the user's address on another chain.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc7702_findings/incorrect-address-handling-for-account-abstraction-wallets-in-securitizebridgebr.md` (Securitize Bridge - Cyfrin)

### Vulnerability Description

#### Root Cause

Smart contract wallets are deployed using factory contracts with chain-specific parameters (deployment salts, nonces, factory addresses). The same user's wallet logic results in different contract addresses on different chains. Bridge protocols that assume `msg.sender` on source chain equals recipient on destination chain will send funds to uncontrolled addresses.

#### Attack Scenario

1. User Alice uses a Safe wallet at address `0xAAA...111` on Ethereum
2. Alice bridges tokens to Polygon via a protocol that uses `msg.sender` as destination
3. The bridge encodes `0xAAA...111` as the destination address on Polygon
4. On Polygon, Alice's Safe wallet is deployed at `0xBBB...222` (different factory)
5. Tokens are minted to `0xAAA...111` on Polygon, which Alice cannot access
6. Funds are permanently lost

### Vulnerable Pattern Examples

**Example 1: Using msg.sender as Destination** [MEDIUM]
> 📖 Reference: `reports/erc7702_findings/incorrect-address-handling-for-account-abstraction-wallets-in-securitizebridgebr.md`
```solidity
// ❌ VULNERABLE: Assumes msg.sender is same on destination chain
function bridgeTokens(
    uint16 targetChain,
    uint256 amount
) external payable {
    token.burnFrom(msg.sender, amount);
    
    // Sends to msg.sender address on target chain
    // WRONG for smart contract wallets!
    wormholeRelayer.sendPayloadToEvm(
        targetChain,
        targetAddress,
        abi.encode(msg.sender, amount),  // Using msg.sender as recipient
        0,
        gasLimit
    );
}
```

**Example 2: Cross-Chain Registration** [MEDIUM]
```solidity
// ❌ VULNERABLE: Registers user with same address on all chains
function registerCrossChain(uint256[] calldata chainIds) external {
    for (uint i = 0; i < chainIds.length; i++) {
        // Sends registration to msg.sender on all chains
        // Smart wallet may not exist at this address on other chains
        crossChainMessenger.send(
            chainIds[i],
            abi.encodeWithSelector(
                IRegistry.register.selector,
                msg.sender  // Wrong assumption!
            )
        );
    }
}
```

### Impact Analysis

#### Technical Impact
- Tokens/assets sent to wrong addresses on destination chains
- User registrations tied to inaccessible addresses
- Cross-chain state synchronization fails

#### Business Impact
- Permanent loss of bridged funds
- KYC/AML registrations broken
- User trust erosion
- Regulatory compliance issues

#### Affected Scenarios
- Token bridges (Wormhole, LayerZero, Axelar integrations)
- Cross-chain governance
- Multi-chain identity/registration systems
- Any protocol assuming address consistency across chains

### Secure Implementation

**Fix 1: Explicit Destination Address Parameter**
```solidity
// ✅ SECURE: User specifies destination address explicitly
function bridgeTokens(
    uint16 targetChain,
    uint256 amount,
    address destinationWallet
) external payable {
    require(destinationWallet != address(0), "Invalid destination");
    
    token.burnFrom(msg.sender, amount);
    
    wormholeRelayer.sendPayloadToEvm(
        targetChain,
        targetAddress,
        abi.encode(destinationWallet, amount),  // User-specified destination
        0,
        gasLimit
    );
    
    emit TokensBridged(msg.sender, destinationWallet, targetChain, amount);
}
```

**Fix 2: Cross-Chain Address Registry**
```solidity
// ✅ SECURE: Maintain address registry across chains
mapping(address => mapping(uint256 => address)) public crossChainAddresses;

function registerCrossChainAddress(
    uint256 chainId,
    address addressOnChain
) external {
    crossChainAddresses[msg.sender][chainId] = addressOnChain;
    emit CrossChainAddressRegistered(msg.sender, chainId, addressOnChain);
}

function bridgeTokens(uint16 targetChain, uint256 amount) external payable {
    address destination = crossChainAddresses[msg.sender][targetChain];
    require(destination != address(0), "Register cross-chain address first");
    
    // Use registered destination
    _bridge(targetChain, destination, amount);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- msg.sender used directly as cross-chain recipient
- No explicit destinationAddress parameter in bridge functions
- Assuming address portability across chains
- Cross-chain messages encoding msg.sender without user confirmation
```

#### Audit Checklist
- [ ] Verify bridge functions allow explicit destination addresses
- [ ] Check that users can specify different addresses per chain
- [ ] Ensure proper validation of destination addresses
- [ ] Test with smart contract wallets on different chains

---

## 5. tx.origin Exploitation with Smart Wallets

### Overview

The use of `tx.origin` to identify users is dangerous with smart wallets (including EIP-7702, Safe, EIP-4337). An attacker can front-run transactions to smart wallets and execute them from their own EOA, causing `tx.origin` to be the attacker's address instead of the legitimate user's.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc7702_findings/m-3-theft-of-initial-bonds-from-proposers-who-are-using-smart-wallets.md` (Optimism - Sherlock)

### Vulnerability Description

#### Root Cause

Smart wallets like Gnosis Safe accept signed transactions via `execTransaction()` and execute them on behalf of signers. The function is agnostic to who calls it, as long as signatures are valid. When protocols use `tx.origin` to assign ownership or benefits, attackers can front-run the transaction and receive those benefits.

#### Attack Scenario

1. User with Smart Wallet signs a transaction to create a dispute game with bond
2. Transaction is submitted to mempool calling Safe's `execTransaction()`
3. Attacker monitors mempool, copies the transaction data
4. Attacker calls `execTransaction()` from their own EOA
5. Smart Wallet validates signatures and executes the action
6. Protocol uses `tx.origin` (attacker's EOA) as the claimant
7. Attacker receives the bond when claim is resolved

### Vulnerable Pattern Examples

**Example 1: Using tx.origin for Claimant Registration** [MEDIUM]
> 📖 Reference: `reports/erc7702_findings/m-3-theft-of-initial-bonds-from-proposers-who-are-using-smart-wallets.md`
```solidity
// ❌ VULNERABLE: tx.origin used for critical identification
function initialize() public payable {
    claimData.push(
        ClaimData({
            parentIndex: type(uint32).max,
            counteredBy: address(0),
            claimant: tx.origin,  // WRONG: Should be msg.sender
            bond: uint128(msg.value),
            claim: rootClaim(),
            position: ROOT_POSITION,
            clock: LibClock.wrap(Duration.wrap(0), Timestamp.wrap(uint64(block.timestamp)))
        })
    );
}
```

**Example 2: tx.origin for Reward Distribution** [MEDIUM]
```solidity
// ❌ VULNERABLE: Rewards go to tx.origin instead of actual caller
function completeMission(uint256 missionId) external {
    require(missions[missionId].completed == false, "Already completed");
    missions[missionId].completed = true;
    
    // Attacker can front-run and receive rewards
    rewards[tx.origin] += missions[missionId].reward;
}
```

**Example 3: tx.origin for Access Control** [HIGH]
```solidity
// ❌ VULNERABLE: Authorization based on tx.origin
function emergencyWithdraw() external {
    require(tx.origin == owner, "Not owner");  // Can be bypassed
    payable(tx.origin).transfer(address(this).balance);
}
```

### Impact Analysis

#### Technical Impact
- Rewards/bonds assigned to attackers instead of legitimate users
- Access control bypasses for smart wallet users
- State corruption in beneficiary records

#### Business Impact
- Theft of user funds (bonds, rewards)
- Smart wallet users effectively excluded from protocols
- Security model broken for significant user segment

#### Affected Scenarios
- Dispute resolution systems with bonds
- Reward/incentive distribution
- Any protocol using tx.origin for user identification

### Secure Implementation

**Fix 1: Use msg.sender Instead of tx.origin**
```solidity
// ✅ SECURE: Use msg.sender for identification
function initialize() public payable {
    claimData.push(
        ClaimData({
            parentIndex: type(uint32).max,
            counteredBy: address(0),
            claimant: msg.sender,  // Correct: actual caller
            bond: uint128(msg.value),
            claim: rootClaim(),
            position: ROOT_POSITION,
            clock: LibClock.wrap(Duration.wrap(0), Timestamp.wrap(uint64(block.timestamp)))
        })
    );
}
```

**Fix 2: Pass Caller Through Factory**
```solidity
// ✅ SECURE: Factory passes the actual sender
contract DisputeGameFactory {
    function create(bytes32 claim) external payable returns (IDisputeGame) {
        IDisputeGame game = IDisputeGame(address(new DisputeGame()));
        game.initialize{value: msg.value}(claim, msg.sender);  // Pass sender explicitly
        return game;
    }
}

contract DisputeGame {
    function initialize(bytes32 claim, address claimant) external payable {
        claimData.push(
            ClaimData({
                claimant: claimant,  // Use passed address
                bond: uint128(msg.value),
                claim: claim
            })
        );
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- tx.origin usage for user identification
- tx.origin in reward/bond distribution
- tx.origin for access control
- tx.origin stored in state variables
```

#### Audit Checklist
- [ ] Search for all tx.origin usages in codebase
- [ ] Verify tx.origin is never used for authorization
- [ ] Check that benefits/rewards use msg.sender
- [ ] Test with transactions submitted through smart wallets

---

## 6. Fallback/Receive Function Issues

### Overview

When EOAs upgrade to EIP-7702 smart wallets, the delegated implementation must properly handle ETH transfers. Missing `payable` modifiers on `fallback` functions or improper implementations can cause ETH transfers to fail, breaking compatibility with protocols expecting EOA-like behavior.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc7702_findings/m-03-defaultaccountfallback-lack-payable.md` (zkSync - Code4rena)

### Vulnerability Description

#### Root Cause

EIP-7702 transforms an EOA into what appears to be a smart contract. If the delegated contract's `fallback` function lacks the `payable` modifier, ETH transfers using `.call{value: x}("")` will fail, even though they would succeed for a regular EOA.

#### Attack Scenario

1. Protocol sends ETH to an address using `.call{value: amount}("")`
2. Address is an EIP-7702 EOA delegating to implementation without payable fallback
3. The call reverts because fallback cannot receive ETH
4. User cannot receive ETH from protocols, breaking expected EOA behavior

### Vulnerable Pattern Examples

**Example 1: Fallback Without Payable** [MEDIUM]
> 📖 Reference: `reports/erc7702_findings/m-03-defaultaccountfallback-lack-payable.md`
```solidity
// ❌ VULNERABLE: fallback cannot receive ETH
contract DefaultAccountImplementation {
    fallback() external {  // Missing payable!
        // Behave like EOA
    }
    
    receive() external payable {
        // Can receive direct ETH
    }
}
```

**Example 2: Missing Both Fallback and Receive** [MEDIUM]
```solidity
// ❌ VULNERABLE: No way to receive ETH
contract BrokenWalletImplementation {
    function execute(address target, bytes calldata data) external {
        (bool success, ) = target.call(data);
        require(success);
    }
    
    // Missing: receive() external payable {}
    // Missing: fallback() external payable {}
}
```

### Impact Analysis

#### Technical Impact
- EIP-7702 wallets cannot receive ETH through standard call patterns
- Breaks compatibility with many existing protocols
- Reverts on legitimate ETH transfers

#### Business Impact
- Users locked out of ETH-based interactions
- Protocol incompatibility with modern wallet standards
- User funds stuck in sending contracts

#### Affected Scenarios
- Direct ETH transfers via call
- Protocol withdrawals to user addresses
- Refund mechanisms

### Secure Implementation

**Fix 1: Implement Both Receive and Payable Fallback**
```solidity
// ✅ SECURE: Both functions handle ETH properly
contract SecureWalletImplementation {
    receive() external payable {
        // Handle direct ETH transfers
    }
    
    fallback() external payable {
        // Handle ETH with data
    }
}
```

**Fix 2: Comprehensive Implementation**
```solidity
// ✅ SECURE: Full EOA-compatible behavior
contract EOACompatibleWallet {
    address public owner;
    
    receive() external payable {
        emit Received(msg.sender, msg.value);
    }
    
    fallback() external payable {
        // For 7702 compatibility, behave like EOA for unknown calls
        if (msg.sender == address(0)) {
            // Bootloader/system call handling if needed
        }
        // Accept ETH with arbitrary data
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- fallback() without payable modifier
- Missing receive() function
- Incomplete ETH handling in delegate contracts
- revert() in fallback for unknown calls
```

#### Audit Checklist
- [ ] Verify EIP-7702 implementations have payable fallback
- [ ] Check receive() function exists and is payable
- [ ] Test ETH transfers to delegated accounts
- [ ] Ensure behavior matches EOA expectations

---

## 7. Session Key Impersonation in Smart Wallets

### Overview

Smart wallets implementing session key functionality (common in EIP-4337 and EIP-7702 contexts) may allow one session key owner to impersonate another session key owner for the same wallet. This occurs when the validation logic fails to verify that the session key used to sign a message matches the session key being consumed in the function call.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-01-sessionkey-owner-can-impersonate-another-session-key-owner-for-the-same-sma.md` (Etherspot - Shieldify)

### Vulnerability Description

#### Root Cause

When a smart wallet allows multiple active sessions concurrently, the signature validation must ensure that the session key that signed the transaction is the same one being used for the operation. Without this binding, session key owners can sign messages that consume other session keys belonging to the same wallet.

#### Attack Scenario

1. Smart Wallet (SCW) has multiple active session keys (SK1, SK2)
2. SK2 signs a message for the `claim()` function, but passes SK1 as the `sessionKey` parameter
3. Validation checks pass because:
   - The `msg.sender` is the SCW ✓
   - SK2 (the signer) is owned by the SCW ✓
   - The function being called is allowed ✓
4. However, SK1's session gets consumed without SK1's authorization
5. This leads to unauthorized claims using another session key's allowance

### Vulnerable Pattern Examples

**Example 1: Missing Session Key Binding** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-01-sessionkey-owner-can-impersonate-another-session-key-owner-for-the-same-sma.md`
```solidity
// ❌ VULNERABLE: No check that signer's sessionKey matches parameter
function _validateSingleCall(bytes calldata _callData) internal view returns (bool) {
    (address target,, bytes calldata execData) = ExecutionLib.decodeSingle(_callData[EXEC_OFFSET:]);
    bytes4 selector = _validateSelector(bytes4(execData[0:4]));
    if (selector == bytes4(0)) return false;
    if (selector == IERC20.approve.selector) return true;
    if (target != address(this)) return false; // If not approve call must call this contract
    return true;
    // Missing: verify sessionKey parameter matches the signing sessionKey!
}

function validateUserOp(UserOperation calldata userOp, bytes32 userOpHash) external returns (uint256) {
    // Validates that signer owns A sessionKey, but not THE sessionKey
    address sessionKeySigner = _recoverSigner(userOpHash, userOp.signature);
    require(isSessionKeyOwner[sessionKeySigner], "Invalid session key");
    // Does NOT verify that sessionKeySigner == sessionKey in the calldata!
}
```

**Example 2: Session Key Parameter Not Validated Against Signer** [HIGH]
```solidity
// ❌ VULNERABLE: claim() uses sessionKey from parameter, not from signer
function claim(
    address sessionKey,  // This can be any valid session key!
    uint256 amount
) external onlySmartWallet {
    // Uses sessionKey from parameter, which may be different from who signed
    SessionData storage session = sessions[sessionKey];
    require(session.active, "Session not active");
    require(session.allowance >= amount, "Insufficient allowance");
    
    session.allowance -= amount;
    _transfer(msg.sender, amount);
}
```

### Impact Analysis

#### Technical Impact
- Unauthorized consumption of session key allowances
- Session key functionality bypass
- State corruption in session management

#### Business Impact
- Token theft through unauthorized claims
- Loss of user trust in session key security
- Potential for complete session key system compromise

#### Affected Scenarios
- Multi-session smart wallet implementations
- Delegated execution patterns
- Gasless transaction systems using session keys

### Secure Implementation

**Fix 1: Bind Session Key to Signature**
```solidity
// ✅ SECURE: Extract sessionKey from calldata and verify against signer
function _validateSingleCall(
    bytes calldata _callData,
    address sessionKeySigner
) internal view returns (bool) {
    (address target,, bytes calldata execData) = ExecutionLib.decodeSingle(_callData[EXEC_OFFSET:]);
    bytes4 selector = _validateSelector(bytes4(execData[0:4]));
    
    if (selector == bytes4(0)) return false;
    if (selector == IERC20.approve.selector) return true;
    if (target != address(this)) return false;
    
    // For claim(), verify sessionKey parameter matches signer
    if (selector == this.claim.selector) {
        address sessionKeyParam = abi.decode(execData[4:36], (address));
        require(sessionKeyParam == sessionKeySigner, "Session key mismatch");
    }
    
    return true;
}
```

**Fix 2: Use Signer as Session Key Directly**
```solidity
// ✅ SECURE: Use recovered signer address as the session key
function claim(uint256 amount) external {
    // The session key IS the signer - extracted during validation
    address sessionKey = _currentSessionKey; // Set during validateUserOp
    
    SessionData storage session = sessions[sessionKey];
    require(session.active, "Session not active");
    require(session.allowance >= amount, "Insufficient allowance");
    
    session.allowance -= amount;
    _transfer(msg.sender, amount);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Session key passed as parameter without verification against signer
- validateUserOp that doesn't bind sessionKey to the operation
- Multiple session keys per wallet with shared validation
- Separation between signature verification and session key consumption
```

#### Audit Checklist
- [ ] Verify session key in calldata matches the signing session key
- [ ] Check that validateUserOp binds the signer to the operation
- [ ] Test with multiple session keys attempting cross-consumption
- [ ] Ensure session key cannot be specified independently of signer

---

## 8. NFT Permit Function Exploitation

### Overview

Smart wallets and rental protocols that hold NFTs implementing ERC-4494 (Permit for ERC-721) are vulnerable to token hijacking. A malicious user can produce a signature for the `permit()` function to approve themselves as a spender, bypassing traditional transfer restrictions.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc7702_findings/m-02-a-malicious-borrower-can-hijack-any-nft-with-permit-function-he-rents.md` (reNFT - Code4rena)

### Vulnerability Description

#### Root Cause

ERC-4494 adds a `permit()` function to ERC-721, allowing off-chain signed approvals. When an NFT is held by a smart contract wallet (like a Gnosis Safe or rental safe), the wallet's signature verification (EIP-1271) will validate signatures from the wallet owner. This allows the owner to approve themselves as a spender, even when the protocol intends to restrict transfers.

#### Attack Scenario

1. Attacker rents an NFT, which is held in their rental safe
2. Attacker creates a permit signature to approve themselves as spender
3. Attacker calls `permit()` on the NFT contract with the signature
4. NFT contract calls `isValidSignature()` on the rental safe
5. Rental safe verifies the signature is from the attacker (safe owner) - valid!
6. NFT approves attacker as spender
7. Attacker transfers NFT out of the rental safe, stealing it

### Vulnerable Pattern Examples

**Example 1: Rental Protocol Without Permit Restrictions** [MEDIUM]
> 📖 Reference: `reports/erc7702_findings/m-02-a-malicious-borrower-can-hijack-any-nft-with-permit-function-he-rents.md`
```solidity
// ❌ VULNERABLE: No guard against permit() calls
contract RentalSafe is Safe {
    // Inherits EIP-1271 signature validation from Safe
    // Any signature from owner is valid, including permit signatures!
    
    function isValidSignature(
        bytes32 hash,
        bytes memory signature
    ) public view override returns (bytes4) {
        // Validates signature is from owner - but owner can sign permit!
        if (isValidOwnerSignature(hash, signature)) {
            return EIP1271_MAGIC_VALUE;
        }
        return bytes4(0);
    }
}

// ERC-721 with Permit (ERC-4494)
contract NFTWithPermit is ERC721, IERC4494 {
    function permit(
        address spender,
        uint256 tokenId,
        uint256 deadline,
        bytes memory signature
    ) external {
        address owner = ownerOf(tokenId);
        
        // If owner is a contract, uses EIP-1271
        if (owner.code.length > 0) {
            // Safe validates signature from its owner - attacker!
            require(
                IERC1271(owner).isValidSignature(hash, signature) == 0x1626ba7e,
                "Invalid signature"
            );
        }
        
        _approve(spender, tokenId);  // Approves attacker!
    }
}
```

**Example 2: Smart Wallet Vulnerable to Self-Approval** [MEDIUM]
```solidity
// ❌ VULNERABLE: Wallet owner can sign permit for tokens held by wallet
contract VulnerableSmartWallet {
    address public owner;
    
    function isValidSignature(
        bytes32 hash,
        bytes calldata signature
    ) external view returns (bytes4) {
        address signer = ECDSA.recover(hash, signature);
        
        // Any signature from owner is valid
        if (signer == owner) {
            return IERC1271.isValidSignature.selector;
        }
        return bytes4(0);
    }
    
    // No restrictions on what the owner can sign!
    // Owner can sign permit() to approve themselves on any held NFT
}
```

### Impact Analysis

#### Technical Impact
- Bypass of transfer restrictions on held tokens
- Unauthorized token approvals
- EIP-1271 signature verification exploited

#### Business Impact
- NFT theft from rental protocols
- Loss of escrowed/locked tokens
- Protocol trust completely undermined

#### Affected Scenarios
- NFT rental platforms
- Escrow contracts holding NFTs
- Any smart wallet holding ERC-4494 tokens
- Collateralized NFT lending

### Secure Implementation

**Fix 1: Guard Against Permit Calls**
```solidity
// ✅ SECURE: Block permit() signatures in smart wallet
contract SecureRentalSafe is Safe {
    // Blocklist of function selectors that shouldn't be signed
    bytes4 constant PERMIT_SELECTOR = 0x8c5be1e5;  // permit signature
    
    function isValidSignature(
        bytes32 hash,
        bytes memory signature
    ) public view override returns (bytes4) {
        // Decode and check if this is a permit-related signature
        // Block any signatures that could approve token transfers
        
        if (isValidOwnerSignature(hash, signature)) {
            // Additional check: is this for a dangerous operation?
            if (_isDangerousSignature(hash)) {
                return bytes4(0);  // Reject!
            }
            return EIP1271_MAGIC_VALUE;
        }
        return bytes4(0);
    }
}
```

**Fix 2: Restrict Token Operations at Guard Level**
```solidity
// ✅ SECURE: Transaction guard prevents permit calls
contract PermitGuard is ITransactionGuard {
    bytes4 constant PERMIT_SELECTOR = bytes4(keccak256("permit(address,uint256,uint256,bytes)"));
    bytes4 constant PERMIT2_SELECTOR = bytes4(keccak256("permit(address,address,uint256,uint256,bytes)"));
    
    function checkTransaction(
        address to,
        uint256 value,
        bytes memory data,
        Enum.Operation operation,
        uint256 safeTxGas,
        uint256 baseGas,
        uint256 gasPrice,
        address gasToken,
        address payable refundReceiver,
        bytes memory signatures,
        address msgSender
    ) external view {
        if (data.length >= 4) {
            bytes4 selector = bytes4(data);
            require(
                selector != PERMIT_SELECTOR && selector != PERMIT2_SELECTOR,
                "Permit calls blocked"
            );
        }
    }
}
```

**Fix 3: Rental Protocol Specific Fix**
```solidity
// ✅ SECURE: Check for permit support before accepting NFT
function _validateNFTForRental(address nftContract, uint256 tokenId) internal {
    // Check if NFT supports permit - warn or reject if risky
    try IERC165(nftContract).supportsInterface(type(IERC4494).interfaceId) returns (bool supported) {
        if (supported) {
            // NFT supports permit - additional safeguards needed
            _applyPermitRestrictions(nftContract, tokenId);
        }
    } catch {}
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Smart wallets implementing EIP-1271 without signature filtering
- NFT rental/escrow without permit() call restrictions
- isValidSignature() that accepts any owner signature
- No transaction guards against token approval functions
```

#### Audit Checklist
- [ ] Check if held NFTs support ERC-4494 (permit)
- [ ] Verify isValidSignature blocks dangerous operations
- [ ] Test permit() calls from wallet owners on held tokens
- [ ] Ensure transaction guards filter permit-related calls
- [ ] Review rental protocols for permit attack surface

---

## Prevention Guidelines

### Development Best Practices

1. **Never rely on isContract() for security decisions** - EIP-7702 breaks this check
2. **Always try ECDSA recovery before falling back to EIP-1271** - Works for both EOAs and 7702
3. **Use reentrancy guards on ALL external call paths** - Even for "EOA" recipients
4. **Implement all token receiver callbacks** - Required for smart contract behavior
5. **Never use tx.origin for user identification** - Easily manipulated with smart wallets
6. **Allow explicit destination addresses for cross-chain operations** - Don't assume address consistency
7. **Ensure payable fallback/receive in wallet implementations** - Maintain EOA compatibility
8. **Bind session keys to signatures** - Always verify the session key in calldata matches the signing key
9. **Guard against permit() in signature validation** - Block dangerous EIP-1271 signatures for held tokens
10. **Filter dangerous function selectors in transaction guards** - Prevent permit/approval bypass attacks

### Testing Requirements

- Unit tests for: Signature verification with 7702 delegated EOAs
- Integration tests for: NFT transfers to 7702 wallets
- Cross-chain tests for: Smart wallet address differences
- Reentrancy tests for: External calls to 7702 recipients
- Session key tests for: Cross-consumption between multiple session keys
- Permit attack tests for: Self-approval on held ERC-4494 tokens
- Fuzzing targets: Signature verification logic, callback implementations, session key binding

---

## Keywords for Search

> These keywords enhance vector search retrieval - include comprehensive terms:

### Primary Terms
`EIP-7702`, `ERC-7702`, `account_abstraction`, `smart_wallet`, `pectra_upgrade`, `eoa_delegation`, `delegate_code`

### Signature Verification Terms
`isContract`, `extcodesize`, `EIP-1271`, `isValidSignature`, `ECDSA.recover`, `signature_verification`, `SignatureChecker`

### Account Abstraction Terms
`EIP-4337`, `smart_contract_wallet`, `Safe_wallet`, `Gnosis_Safe`, `account_abstraction_wallet`, `AA_wallet`, `session_key`, `userOp`, `bundler`

### Attack Vector Terms
`reentrancy_via_eoa`, `tx.origin_exploitation`, `cross_chain_address_mismatch`, `front_running_smart_wallet`, `callback_missing`, `session_key_impersonation`, `permit_hijack`, `nft_permit_exploit`

### Token Standard Terms
`onERC721Received`, `onERC1155Received`, `safeTransfer_revert`, `token_callback`, `IERC721Receiver`, `ERC-4494`, `ERC721_permit`, `NFT_permit`

### Impact Terms
`signature_bypass`, `fund_loss`, `denial_of_service`, `address_inconsistency`, `wallet_incompatibility`, `token_theft`, `session_consumption`

### Code Pattern Terms
`address.code.length`, `extcodesize_check`, `payable_fallback`, `receive_function`, `tx.origin_usage`, `validateUserOp`, `session_binding`

### Protocol Examples
`Across_Protocol`, `Optimism_FaultDisputeGame`, `Securitize_Bridge`, `Otim_SmartWallet`, `FactcheckDotFun`, `Etherspot`, `reNFT`, `Nudge_Protocol`

---

## Related Vulnerabilities

### Compounds With
- [Reentrancy Vulnerabilities](../reentrancy/) - EIP-7702 expands attack surface
- [Signature Replay](../missing-validations/) - Combined with isContract check failures
- [NFT Token Vulnerabilities](../../tokens/erc721/) - ERC-4494 permit exploitation

### Enables
- Cross-chain fund theft via address mismatch
- Front-running attacks on smart wallet transactions
- DoS attacks on upgraded EOAs
- Session key impersonation attacks
- NFT theft via permit signature exploitation

### Pattern Variants
This vulnerability is part of the **Account Abstraction Security** family:
- EIP-7702 Integration Issues (this document)
- EIP-4337 Bundler Vulnerabilities
- Safe Multisig Security Patterns
- Smart Wallet Signature Handling
- Session Key Management Vulnerabilities

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`ECDSA.recover`, `ERC1271`, `ERC4494`, `_is7702DelegatedWallet`, `_unwrapAndSendETH`, `_validateNFTForRental`, `_validateSingleCall`, `account_abstraction`, `allowance`, `approve`, `block.timestamp`, `bridgeTokens`, `checkTransaction`, `claim`, `completeMission`, `create`, `cross_chain`, `defi`, `delegatecall`, `deposit`, `emergencyWithdraw`, `eoa_delegation`, `erc7702_integration`, `execute`, `executeWithCallback`, `extcodesize`, `fallback`, `isContract`, `isValidSignature`, `msg.sender`, `nft_permit`, `onERC1155Received`, `onERC721Received`, `pectra_upgrade`, `permit`, `receive`, `rental_protocol`, `sessionKey`, `session_keys`, `signature_verification`, `smart_wallet`, `tx.origin`, `validateUserOp`
