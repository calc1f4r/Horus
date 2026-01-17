# Bridge & Cross-Chain Vulnerability Database

This directory contains comprehensive vulnerability patterns for cross-chain bridge integrations. Each subdirectory covers a specific bridge protocol with detailed vulnerability patterns, code examples, and secure implementations.

## Directory Structure

```
bridge/
├── README.md                    # This file
├── layerzero/                   # LayerZero protocol vulnerabilities
│   └── layerzero-integration-vulnerabilities.md
├── wormhole/                    # Wormhole protocol vulnerabilities
│   └── wormhole-integration-vulnerabilities.md
├── hyperlane/                   # Hyperlane protocol vulnerabilities
│   └── hyperlane-integration-vulnerabilities.md
├── axelar/                      # Axelar protocol (placeholder)
├── stargate/                    # Stargate protocol (placeholder)
├── ccip/                        # Chainlink CCIP (placeholder)
└── custom/                      # General cross-chain patterns
    └── cross-chain-general-vulnerabilities.md
```

## Protocol Coverage

### [LayerZero](layerzero/layerzero-integration-vulnerabilities.md)
**Reports Analyzed**: 175+

**Key Vulnerability Classes**:
- Channel Blocking Attacks
- Minimum Gas Validation
- Gas Estimation & Fee Calculation
- Fee Refund Handling
- Payload Size & Address Validation
- OFT/ONFT Specific Issues

**Critical Patterns**:
- `NonblockingLzApp` not properly implemented
- Missing `minDstGas` validation
- `adapterParams` gas manipulation
- `forceResumeReceive` not implemented

---

### [Wormhole](wormhole/wormhole-integration-vulnerabilities.md)
**Reports Analyzed**: 71+

**Key Vulnerability Classes**:
- VAA Parsing Vulnerabilities
- Guardian Set Transition Issues
- Message Replay Attacks
- Token Bridge Integration
- Gas Limit Configuration

**Critical Patterns**:
- Deprecated `parseAndVerifyVAA()` usage
- Missing emitter chain/address validation
- Guardian set index not tracked
- `transferTokensWithPayload` to EOA

---

### [Hyperlane](hyperlane/hyperlane-integration-vulnerabilities.md)
**Reports Analyzed**: 8+

**Key Vulnerability Classes**:
- ISM (Interchain Security Module) Bypass
- Message Replay for Unlimited Minting
- Router Configuration Issues
- Handle Function Vulnerabilities
- Gas Payment Issues

**Critical Patterns**:
- Missing ISM configuration
- Failed message can be replayed
- `handle()` without mailbox check
- No router enrollment validation

---

### [Custom/General Cross-Chain](custom/cross-chain-general-vulnerabilities.md)
**Reports Analyzed**: 100+

**Key Vulnerability Classes**:
- Cross-Chain Replay Attacks
- Signature Validation Issues
- Token Bridging Issues (fee-on-transfer, rebasing, decimals)
- Sequencer & L2 Specific Issues
- Access Control Vulnerabilities
- Slippage & MEV Issues
- Message Ordering & Timing

**Critical Patterns**:
- Missing chain ID in signatures (EIP-712)
- Global nonces instead of per-sender
- No decimal normalization
- Sequencer-dependent emergency functions

---

## Quick Reference: Common Bridge Vulnerabilities

### 1. Replay Attacks
| Protocol | Pattern | Fix |
|----------|---------|-----|
| All | Missing chain ID | Include `block.chainid` in signature/hash |
| All | Global nonces | Per-sender, per-chain nonces |
| All | No contract address | Include `address(this)` in message ID |

### 2. Channel/Message Blocking
| Protocol | Pattern | Fix |
|----------|---------|-----|
| LayerZero | Direct LzApp inheritance | Use `NonblockingLzApp` |
| LayerZero | External calls in receive | Move after try-catch |
| Hyperlane | Revert in handle | Track message ID before processing |

### 3. Access Control
| Protocol | Pattern | Fix |
|----------|---------|-----|
| Wormhole | Missing emitter validation | Verify emitter chain + address |
| Hyperlane | No ISM configured | Deploy with MultisigISM |
| LayerZero | No trusted remote check | Configure `setTrustedRemote()` |

### 4. Token Issues
| Protocol | Pattern | Fix |
|----------|---------|-----|
| All | Fee-on-transfer | Measure actual received amount |
| All | Decimal mismatch | Normalize to 18 decimals |
| All | Rebasing tokens | Use wrapped non-rebasing version |

---

## How to Use These Entries

### For Auditors
1. Identify which bridge protocol(s) the target uses
2. Review corresponding vulnerability database entry
3. Use the **Detection Patterns** section for code review
4. Follow the **Audit Checklist** for comprehensive coverage

### For Developers
1. Read the **Secure Implementation** sections
2. Compare your code against **Vulnerable Pattern Examples**
3. Ensure all items in **Audit Checklist** are addressed
4. Test edge cases mentioned in **Impact Analysis**

### For AI Agents
1. Reference file paths point to source audit reports
2. Use **Keywords for Search** for semantic matching
3. Code examples can be used for pattern matching
4. Each entry follows consistent YAML frontmatter schema

---

## Statistics

| Protocol | Vulnerability Classes | Code Examples | Secure Implementations |
|----------|----------------------|---------------|----------------------|
| LayerZero | 5+ | 10+ | 5+ |
| Wormhole | 5+ | 8+ | 5+ |
| Hyperlane | 5+ | 10+ | 6+ |
| Custom | 7+ | 15+ | 10+ |
| **Total** | **22+** | **43+** | **26+** |

---

## Contributing

To add new vulnerability patterns:
1. Analyze 5-10 reports for the pattern
2. Follow the TEMPLATE.md format
3. Include actual code from audit reports
4. Document severity consensus across sources
5. Provide secure implementation examples
6. Add to appropriate protocol subdirectory

---

## Related Categories

- [Chainlink Oracle Vulnerabilities](../oracle/chainlink/)
- [Pyth Oracle Vulnerabilities](../oracle/pyth/)
- [Slippage Protection Issues](../general/slippage-protection/)
- [Reentrancy Patterns](../general/reentrancy/)
