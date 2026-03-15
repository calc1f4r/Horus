name: poc-writing
description: "Write honest, minimal, compilable exploit tests that prove smart contract vulnerabilities. Adapts to the target codebase's language and test framework (Foundry, Hardhat, Anchor, etc.). Enforces reachability-first methodology. Use when a vulnerability needs a PoC to prove impact, validate an audit finding, or demonstrate to a protocol team."
context: fork
agent: poc-writing
argument-hint: <finding-description-or-file>
---

Write a Proof-of-Concept exploit for `$ARGUMENTS`.

## Methodology

### Phase 0: Reachability Gate (MANDATORY)
Before writing any code, prove the vulnerability is reachable through the public API by an unprivileged user. If not reachable — refuse to write the PoC.

### Phase 1: Understand the vulnerability
Answer: What's the root cause? What's the impact? What preconditions are needed?

### Phase 2: Set up realistic state
Fork mainnet or set up minimal realistic protocol state. Never use phantom interfaces.

### Phase 3: Write exploit
Follow the SNAPSHOT → EXPLOIT → VERIFY pattern:
1. Record state before exploit
2. Execute the attack
3. Assert the exploited state proves the vulnerability

### Phase 4: Compile and run
Fix errors honestly — never mock away security checks to make tests pass.

### Phase 5: Pre-flight checklist
- [ ] No admin/owner roles used by attacker
- [ ] No phantom interfaces or fake contracts
- [ ] Assertions prove actual impact (value lost, state corrupted)
- [ ] Test passes on clean fork

## Related skills

- [/issue-writer](../issue-writer/SKILL.md) — Polishes findings that have PoCs
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 6)
