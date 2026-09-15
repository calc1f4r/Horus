# DAO Governance Vulnerabilities Database

This directory contains comprehensive vulnerability patterns for DAO and governance smart contract security auditing.

## Entry Overview

| Entry | Description | Key Patterns | Severity Range |
|-------|-------------|--------------|----------------|
| [Voting Power Manipulation](./voting-power-manipulation.md) | Double voting, flash loans, delegation bugs, snapshot issues | 5 patterns, 25+ examples | MEDIUM-HIGH |
| [Timelock Bypass](./timelock-bypass.md) | Privileged function bypass, zero delay, canceled execution | 5 patterns, 10+ examples | MEDIUM-CRITICAL |
| [Quorum Manipulation](./quorum-manipulation.md) | Dynamic quorum abuse, threshold miscalculation, tie handling | 5 patterns, 15+ examples | MEDIUM-HIGH |
| [Proposal Lifecycle Manipulation](./proposal-lifecycle-manipulation.md) | Cancellation bugs, threshold bypass, expiration errors | 5 patterns, 12+ examples | MEDIUM-HIGH |
| [Governance Takeover](./governance-takeover.md) | 51% attacks, centralization, veto loss, emergency abuse | 5 patterns, 15+ examples | HIGH-CRITICAL |

## Quick Reference by Attack Vector

### Voting Power Attacks
- Flash loan voting manipulation → [voting-power-manipulation.md#1](./voting-power-manipulation.md#1-double-voting-via-delegation)
- Unlimited vote minting → [voting-power-manipulation.md#3](./voting-power-manipulation.md#3-unlimited-vote-minting-via-checkpoint-bugs)
- Missing snapshots → [voting-power-manipulation.md#4](./voting-power-manipulation.md#4-voting-power-snapshot-missing)

### Timelock Attacks
- Admin functions not timelocked → [timelock-bypass.md#1](./timelock-bypass.md#1-timelock-bypass-via-privileged-functions)
- Zero delay in constructor → [timelock-bypass.md#2](./timelock-bypass.md#2-zerominimal-delay-vulnerabilities)
- Storage collision attacks → [timelock-bypass.md#5](./timelock-bypass.md#5-storage-collision-attacks)

### Quorum Attacks
- Delegation lowers quorum → [quorum-manipulation.md#1](./quorum-manipulation.md#1-quorum-lowering-via-delegation-abuse)
- Wrong threshold calculation → [quorum-manipulation.md#3](./quorum-manipulation.md#3-quorum-threshold-miscalculation)
- Ties incorrectly approved → [quorum-manipulation.md#5](./quorum-manipulation.md#5-tie-handling-vulnerabilities)

### Proposal Attacks
- Anyone can cancel proposals → [proposal-lifecycle-manipulation.md#1](./proposal-lifecycle-manipulation.md#1-unrestricted-proposal-cancellation)
- Flash loan proposal spam → [proposal-lifecycle-manipulation.md#2](./proposal-lifecycle-manipulation.md#2-proposal-threshold-bypass-for-griefing)
- Wrong expiration logic → [proposal-lifecycle-manipulation.md#3](./proposal-lifecycle-manipulation.md#3-proposal-expiration-logic-errors)

### Takeover Attacks
- 51% arbitrary execution → [governance-takeover.md#1](./governance-takeover.md#1-51-attack-via-arbitrary-execution)
- Veto power removal → [governance-takeover.md#2](./governance-takeover.md#2-loss-of-veto-power-enabling-takeover)
- Single admin control → [governance-takeover.md#3](./governance-takeover.md#3-centralized-governance-control)

## Source Reports Analyzed

These entries are synthesized from **30+ audit reports** across multiple security firms:

- **Code4rena**: Nouns DAO, GMX, Venus, Y2K Finance, NFTX, Party DAO, Farcaster, Usual Money
- **Sherlock**: DAOSol, Apollon, Velar, Multiple DeFi protocols
- **Codehawks**: RAAC, VeToken, Autonomint
- **Spearbit**: Coinbase Solady, Various DeFi
- **Halborn**: Moonwell

## Usage for Security Auditors

1. **Pre-Audit Review**: Read relevant entries before auditing governance contracts
2. **Pattern Matching**: Use code patterns and detection guidelines during review
3. **Checklist Validation**: Apply audit checklists from each entry
4. **Deep Dive**: Follow report references for detailed context

## Usage for AI Agents

Each entry is optimized for vector search with:
- Rich semantic descriptions
- Domain-specific terminology
- Comprehensive keyword lists
- Report references for additional context

When querying this database, use governance-specific terms like:
- `voting power`, `delegation`, `checkpoint`, `snapshot`
- `timelock`, `delay`, `governor`, `admin`
- `quorum`, `threshold`, `majority`
- `proposal`, `cancel`, `execute`
- `51% attack`, `veto`, `guardian`, `centralization`

## Contributing

To add new vulnerability patterns:
1. Analyze 5+ audit reports with the pattern
2. Follow the structure in existing entries
3. Include vulnerable and secure code examples
4. Add report references (verified file paths only)
5. Update this README with the new entry
