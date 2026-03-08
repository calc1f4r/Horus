---
# Core Classification (Required)
protocol: generic
chain: sui
category: wallet_snap_security
vulnerability_type: injection|forced_signing|input_validation|information_disclosure|build_configuration

# Attack Vector Details (Required)
attack_type: injection|social_engineering|information_disclosure|privilege_escalation
affected_component: snap_rpc|transaction_rendering|key_derivation|dapp_origin|build_config

# Technical Primitives (Required)
primitives:
  - snap_rpc
  - sui_signTransaction
  - sui_signMessage
  - renderSignTransaction
  - renderSignMessage
  - deriveKeyPair
  - snap_dialog
  - confirmation_dialog
  - alert_dialog
  - markdown_rendering
  - control_characters
  - dapp_origin
  - ed25519
  - bip44_derivation
  - metamask_snap

# Impact Classification (Required)
severity: high
impact: fund_loss|unauthorized_signing|information_disclosure|phishing
exploitability: 0.8
financial_impact: high

# Context Tags
tags:
  - sui
  - metamask
  - snap
  - wallet
  - injection
  - xss
  - signing
  - key_derivation
  - dapp
  - browser_extension
  - javascript
  - typescript

# Version Info
language: javascript|typescript
version: all
---

## References & Source Reports

> **For Agents**: Read the full report for each finding at the referenced path.

### Injection Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Ctrl-Char Markdown Injection in renderSignTransaction | `reports/sui_move_findings/ctrlcharmarkdown-injection-in-rendersigntransaction-can-confuse-users.md` | HIGH | ConsenSys | Solflare Sui Snap |
| Ctrl-Char Markdown Injection in renderSignMessage | `reports/sui_move_findings/ctrlcharmarkdown-injection-via-rendersignmessage-can-confuse-users-into.md` | HIGH | ConsenSys | Solflare Sui Snap |

### Forced Signing / Approval Bypass
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Dapp May Force Sign Approval Dialog | `reports/sui_move_findings/dapp-may-force-a-sign-approval-dialog-on-a-user-resulting-in-loss-of-f.md` | HIGH | ConsenSys | Solflare Sui Snap |
| Dapp May Retrieve Public Key Without Confirmation | `reports/sui_move_findings/dapp-may-force-a-sign-approval-dialog-on-a-user-resulting-in-loss-of-f-fbb8.md` | HIGH | ConsenSys | Solflare Sui Snap |

### User Confirmation Suppression
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Dapp May Suppress User Confirmation | `reports/sui_move_findings/dapp-may-suppress-user-confirmation-for-getpublickey-getaccount-reques.md` | MEDIUM | ConsenSys | Solflare Sui Snap |

### Input Validation
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Insufficient Input Validation for deriveKeyPair | `reports/sui_move_findings/insufficient-input-validation-derivekeypair-schema-allows-extraction-o.md` | MEDIUM | ConsenSys | Solflare Sui Snap |

### Build Configuration
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Production Builds Allow Development Config | `reports/sui_move_findings/production-builds-allow-development-origins-to-connect-to-the-snap.md` | MEDIUM | ConsenSys | Solflare Sui Snap |

### Artifacts Index
| Artifact | Source | Type |
|----------|--------|------|
| `artifacts/14-consensys.io-diligence-audits-2023-07-solfl.html` | ConsenSys Diligence Audit | HTML |

---

# Sui Wallet / MetaMask Snap Vulnerabilities — Comprehensive Database

**A Complete Pattern-Matching Guide for Sui Wallet Extension and MetaMask Snap Security**

---

## Table of Contents

1. [Markdown/Control Character Injection in Transaction Rendering](#1-markdowncontrol-character-injection-in-transaction-rendering)
2. [Markdown Injection in Message Signing](#2-markdown-injection-in-message-signing)
3. [Forced Transaction Signing via RPC](#3-forced-transaction-signing-via-rpc)
4. [Public Key Extraction Without User Consent](#4-public-key-extraction-without-user-consent)
5. [User Confirmation Suppression](#5-user-confirmation-suppression)
6. [Key Derivation Path Manipulation](#6-key-derivation-path-manipulation)
7. [Development Origins in Production Builds](#7-development-origins-in-production-builds)

---

## 1. Markdown/Control Character Injection in Transaction Rendering

### Overview

MetaMask Snap dialog boxes render text using a subset of Markdown. When transaction data (recipient addresses, amounts, metadata) is rendered without sanitization, control characters and Markdown formatting can be injected to mislead users about what they're signing.

> **Validation strength**: Strong — 2 HIGH reports from ConsenSys Diligence on Solflare Sui Snap
> **Frequency**: 2/69 reports (all from same audit, critical wallet vulnerability class)

### Vulnerability Description

#### Root Cause

The `renderSignTransaction` function interpolates raw transaction data into dialog text without escaping Markdown characters or filtering control characters. Attackers craft transactions with metadata containing `**`, `#`, `---`, `\n`, or special Unicode characters to alter the dialog appearance.

#### Attack Scenario

1. Malicious dApp constructs a transaction with crafted metadata/comments containing Markdown
2. When user is prompted to sign, the dialog renders attacker-controlled formatted text
3. The injected text can mimic trusted UI elements, hide the actual transaction details, or add fake "verified" labels
4. User signs thinking they're approving a different, benign transaction

### Vulnerable Pattern Examples

**Example 1: Transaction Rendering Without Sanitization** [HIGH]
> 📖 Reference: `reports/sui_move_findings/ctrlcharmarkdown-injection-in-rendersigntransaction-can-confuse-users.md`
```typescript
// ❌ VULNERABLE: Raw transaction data rendered in Markdown dialog
async function renderSignTransaction(tx: SuiTransaction): Promise<string> {
    const recipient = tx.recipient;  // Attacker-controlled
    const amount = tx.amount;
    const metadata = tx.metadata;    // Attacker-controlled
    
    return `
# Sign Transaction

**To:** ${recipient}
**Amount:** ${amount} SUI
**Note:** ${metadata}
    `;
    // If metadata = "Safe transfer\n---\n# ✅ Verified by Sui Foundation\n**Amount:** 0.001 SUI"
    // User sees fake "Verified" badge and wrong amount
}
```

**Example 2: Control Characters in Address Display** [HIGH]
> 📖 Reference: `reports/sui_move_findings/ctrlcharmarkdown-injection-in-rendersigntransaction-can-confuse-users.md`
```typescript
// ❌ VULNERABLE: Unicode/control chars can override displayed text
const dialogContent = `
Sending ${amount} to ${recipientAddress}
`;
// If recipientAddress contains RTL override (U+202E) or other control chars:
// "0x1234...abcd" appears as "dcba...4321x0" — user copies wrong address
```

### Impact Analysis

#### Technical Impact
- Transaction details misrepresented to user
- Fake "verified" or "safe" badges injected into signing dialogs
- Real transaction amounts/recipients hidden behind fake UI elements
- Control characters can reverse or hide address display

#### Financial Impact
- Users sign malicious transactions believing them to be safe (HIGH, 2/69 reports)
- Address confusion leads to funds sent to attacker addresses
- Phishing attacks appear as legitimate wallet prompts

### Secure Implementation

**Fix: Sanitize All User-Controllable Text**
```typescript
// ✅ SECURE: Strip Markdown and control characters before rendering
function sanitizeForDialog(input: string): string {
    // Remove control characters (except basic whitespace)
    let cleaned = input.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]/g, '');
    // Escape Markdown special characters
    cleaned = cleaned.replace(/([*_~`#\[\](){}|\\>!-])/g, '\\$1');
    // Remove Unicode directional overrides
    cleaned = cleaned.replace(/[\u200E\u200F\u202A-\u202E\u2066-\u2069]/g, '');
    return cleaned;
}

async function renderSignTransaction(tx: SuiTransaction): Promise<string> {
    const recipient = sanitizeForDialog(tx.recipient);
    const metadata = sanitizeForDialog(tx.metadata || '');
    return `
# Sign Transaction

**To:** ${recipient}
**Amount:** ${tx.amount} SUI
${metadata ? `**Note:** ${metadata}` : ''}
    `;
}
```

### Detection Patterns

```
- Template literal interpolation of user/dApp-controlled data in dialog text
- Missing sanitization functions for Markdown rendering
- Any snap_dialog content including raw transaction fields
- String interpolation in confirmation/alert dialogs
```

---

## 2. Markdown Injection in Message Signing

### Overview

Same as transaction rendering, but for arbitrary message signing. The `renderSignMessage` handler is equally vulnerable to Markdown injection, allowing attackers to craft messages that display misleading content in the signing dialog.

> **Validation strength**: Strong — 1 HIGH report from ConsenSys Diligence
> **Frequency**: 1/69 reports (same root cause as Section 1)

### Vulnerable Pattern Examples

**Example 1: Message Signing Injection** [HIGH]
> 📖 Reference: `reports/sui_move_findings/ctrlcharmarkdown-injection-via-rendersignmessage-can-confuse-users-into.md`
```typescript
// ❌ VULNERABLE: Raw message content shown in signing dialog
async function renderSignMessage(message: string): Promise<boolean> {
    const result = await snap.request({
        method: 'snap_dialog',
        params: {
            type: 'confirmation',
            content: panel([
                heading('Sign Message'),
                text(`Message: ${message}`),  // Unsanitized — Markdown injection
            ]),
        },
    });
    return result === true;
}
```

### Secure Implementation

```typescript
// ✅ SECURE: Sanitize message content and use copyable for addresses
async function renderSignMessage(message: string): Promise<boolean> {
    const sanitized = sanitizeForDialog(message);
    const result = await snap.request({
        method: 'snap_dialog',
        params: {
            type: 'confirmation',
            content: panel([
                heading('Sign Message'),
                text('Please review the message below:'),
                copyable(sanitized),  // Uses copyable component — no Markdown rendering
            ]),
        },
    });
    return result === true;
}
```

---

## 3. Forced Transaction Signing via RPC

### Overview

A malicious dApp can chain RPC calls to force a signing dialog on the user without a clear opportunity to review the transaction. By combining `getPublicKey` (which may bypass confirmation) with immediate `signTransaction`, the user is rushed into signing.

> **Validation strength**: Strong — 2 HIGH reports from ConsenSys Diligence
> **Frequency**: 2/69 reports

### Vulnerable Pattern Examples

**Example 1: Immediate Sign After Key Extraction** [HIGH]
> 📖 Reference: `reports/sui_move_findings/dapp-may-force-a-sign-approval-dialog-on-a-user-resulting-in-loss-of-f.md`
```typescript
// ❌ VULNERABLE: dApp can call signTransaction immediately without prior context
// Snap RPC handler processes requests sequentially
async function onRpcRequest({ origin, request }: { origin: string; request: any }) {
    switch (request.method) {
        case 'sui_signTransaction':
            // No rate limiting, no origin trust verification
            // No mandatory delay after key extraction
            return await signTransaction(request.params);
        case 'getPublicKey':
            // Returns public key without user confirmation
            return await getPublicKey();
    }
}

// Attack: dApp calls getPublicKey -> immediately calls sui_signTransaction
// User sees signing dialog without understanding what dApp wants
```

**Example 2: Public Key Extraction Enables Targeted Attacks** [HIGH]
> 📖 Reference: `reports/sui_move_findings/dapp-may-force-a-sign-approval-dialog-on-a-user-resulting-in-loss-of-f-fbb8.md`
```typescript
// ❌ VULNERABLE: Public key returned without user awareness
async function getPublicKey(): Promise<string> {
    const keyPair = await deriveKeyPair();
    return keyPair.publicKey;  // No confirmation dialog — user doesn't know dApp has their pubkey
}
```

### Impact Analysis

- Attacker obtains user's public key (and therefore Sui address) silently
- Constructs a targeted malicious transaction using the known address
- Immediately pushes signing dialog — user may approve reflexively
- Fund loss from signing attacker-crafted transaction (HIGH, 2/69 reports)

### Secure Implementation

```typescript
// ✅ SECURE: Require confirmation for key extraction, rate limit sign requests
async function onRpcRequest({ origin, request }: { origin: string; request: any }) {
    // Verify origin is in allowed list
    if (!isAllowedOrigin(origin)) {
        throw new Error('Origin not authorized');
    }
    
    switch (request.method) {
        case 'sui_signTransaction':
            // Rate limit: max 1 sign request per 3 seconds per origin
            if (!checkRateLimit(origin, 'sign', 3000)) {
                throw new Error('Rate limited');
            }
            return await signTransaction(request.params);
            
        case 'getPublicKey':
            // Require user confirmation before revealing public key
            const approved = await snap.request({
                method: 'snap_dialog',
                params: {
                    type: 'confirmation',
                    content: panel([
                        heading('Share Public Key'),
                        text(`**${origin}** wants to access your Sui public key.`),
                        text('This will reveal your wallet address to this site.'),
                    ]),
                },
            });
            if (!approved) throw new Error('User rejected');
            return await getPublicKey();
    }
}
```

---

## 4. Public Key Extraction Without User Consent

### Overview

The `getPublicKey` and `getAccount` RPC methods return the user's public key and Sui address without displaying a confirmation dialog. This leaks the user's blockchain identity to any connected dApp silently.

> **Validation strength**: Moderate — 1 MEDIUM report from ConsenSys Diligence
> **Frequency**: 1/69 reports (covered in more detail in Section 3)

See Section 3 above for secure implementation.

---

## 5. User Confirmation Suppression

### Overview

Certain RPC methods that should require user confirmation (like `getPublicKey` or `getAccount`) don't show any dialog, allowing dApps to silently extract wallet information.

> **Validation strength**: Moderate — 1 MEDIUM report from ConsenSys Diligence
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: No Dialog for Account Access** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/dapp-may-suppress-user-confirmation-for-getpublickey-getaccount-reques.md`
```typescript
// ❌ VULNERABLE: Account info returned without any user interaction
case 'getAccount':
    const keyPair = await deriveKeyPair();
    return {
        publicKey: keyPair.publicKey,
        address: computeSuiAddress(keyPair.publicKey),
    };
    // User never knows dApp accessed their account info
```

### Secure Implementation

```typescript
// ✅ SECURE: Show confirmation for account access with origin info
case 'getAccount':
    const confirmed = await snap.request({
        method: 'snap_dialog',
        params: {
            type: 'confirmation',
            content: panel([
                heading('Connect Account'),
                text(`**${origin}** wants to view your Sui account.`),
            ]),
        },
    });
    if (!confirmed) throw new Error('User rejected');
    const keyPair = await deriveKeyPair();
    return {
        publicKey: keyPair.publicKey,
        address: computeSuiAddress(keyPair.publicKey),
    };
```

---

## 6. Key Derivation Path Manipulation

### Overview

The `deriveKeyPair` function accepts user-specified derivation paths. Without proper validation, an attacker can provide paths that derive unintended keys, potentially extracting keys from other accounts or applications.

> **Validation strength**: Moderate — 1 MEDIUM report from ConsenSys Diligence
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Unrestricted Derivation Path** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/insufficient-input-validation-derivekeypair-schema-allows-extraction-o.md`
```typescript
// ❌ VULNERABLE: Derivation path not constrained to Sui BIP44 coin type
async function deriveKeyPair(path?: string): Promise<KeyPair> {
    const derivationPath = path || "m/44'/784'/0'/0'/0'";
    // No validation that path uses Sui coin type (784)
    // dApp could request: "m/44'/60'/0'/0'/0'" (Ethereum coin type)
    // This would derive the user's Ethereum key pair!
    const node = await snap.request({
        method: 'snap_getBip44Entropy',
        params: { coinType: parseInt(derivationPath.split("'")[1]) },
    });
    return ed25519.keyFromSeed(node.privateKey);
}
```

### Secure Implementation

```typescript
// ✅ SECURE: Restrict to Sui BIP44 coin type only
const SUI_COIN_TYPE = 784;

async function deriveKeyPair(accountIndex: number = 0): Promise<KeyPair> {
    // Only allow Sui coin type — ignore user-specified paths
    const node = await snap.request({
        method: 'snap_getBip44Entropy',
        params: { coinType: SUI_COIN_TYPE },
    });
    // Derive using standard Sui path
    const child = deriveChild(node, accountIndex);
    return ed25519.keyFromSeed(child.privateKey);
}
```

---

## 7. Development Origins in Production Builds

### Overview

Production builds of the snap allow development/localhost origins to connect, enabling attackers who can reach the user's localhost (via DNS rebinding, XSS on localhost, etc.) to interact with the snap.

> **Validation strength**: Moderate — 1 MEDIUM report from ConsenSys Diligence
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Localhost Allowed in Production** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/production-builds-allow-development-origins-to-connect-to-the-snap.md`
```typescript
// ❌ VULNERABLE: Development origins included in production build
const ALLOWED_ORIGINS = [
    'https://solflare.com',
    'https://app.solflare.com',
    'http://localhost:3000',     // Development origin — should not be in production
    'http://localhost:8080',     // Development origin
    'http://127.0.0.1:3000',    // Development origin
];
```

### Secure Implementation

```typescript
// ✅ SECURE: Environment-based origin configuration
const ALLOWED_ORIGINS = process.env.NODE_ENV === 'production'
    ? [
        'https://solflare.com',
        'https://app.solflare.com',
      ]
    : [
        'https://solflare.com',
        'https://app.solflare.com',
        'http://localhost:3000',
        'http://localhost:8080',
      ];
```

---

## Prevention Guidelines

### Wallet / Snap Security Best Practices
1. **Sanitize ALL text** rendered in snap dialogs — strip Markdown, control chars, Unicode overrides
2. **Require confirmation** for every RPC method that reveals user information
3. **Rate limit** signing requests to prevent rapid-fire approval fatigue
4. **Restrict derivation paths** to the snap's designated coin type (784 for Sui)
5. **Use `copyable` component** instead of `text` for addresses and amounts
6. **Remove dev origins** from production builds — use environment-based configuration
7. **Show origin** in every dialog so users know which dApp is requesting action
8. **Never auto-approve** any operation that involves keys, signing, or account info

### Testing Requirements
- Test dialogs with Markdown injection payloads: `**bold**`, `# heading`, `---`, `[link](url)`
- Test with Unicode control characters: RTL override (U+202E), zero-width joiner
- Test rapid-fire RPC calls to verify rate limiting
- Test derivation with non-Sui coin types (60 for ETH, 501 for SOL)
- Verify production builds don't include localhost origins
- Test confirmation dialogs show correct origin information

---

### Keywords for Search

`metamask_snap`, `snap_dialog`, `snap_rpc`, `sui_signTransaction`, `sui_signMessage`, `renderSignTransaction`, `renderSignMessage`, `confirmation_dialog`, `alert_dialog`, `markdown_injection`, `control_character`, `unicode_override`, `RTL`, `getPublicKey`, `getAccount`, `deriveKeyPair`, `bip44`, `coin_type_784`, `ed25519`, `dapp_origin`, `localhost`, `development_build`, `rate_limit`, `sanitize`, `copyable`, `solflare`, `wallet_security`, `signing_approval`, `phishing`

### Related Vulnerabilities
- `DB/general/signatures/` — Signature validation patterns
- `DB/general/access-control/` — Access control patterns
