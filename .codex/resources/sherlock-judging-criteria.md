# Sherlock Judging Criteria Reference

This document contains the complete Sherlock judging standards for validating security findings.

## Severity Definitions

### HIGH Severity
Direct loss of funds without (extensive) limitations of external conditions. The loss of the affected party must be significant.

**Guidelines for Significant Loss:**
- Users lose more than 1% and more than $10 of their principal
- Users lose more than 1% and more than $10 of their yield
- The protocol loses more than 1% and more than $10 of the fees

### MEDIUM Severity
- Causes a loss of funds but requires certain external conditions or specific states, or a loss is highly constrained. The loss must be relevant to the affected party.
- Breaks core contract functionality, rendering the contract useless or leading to loss of funds that's relevant to the affected party.

**Guidelines for Relevant Loss:**
- Users lose more than 0.01% and more than $10 of their principal
- Users lose more than 0.01% and more than $10 of their yield
- The protocol loses more than 0.01% and more than $10 of the fees

**Note:** If a single attack can cause a 0.01% loss but can be replayed indefinitely, it will be considered a 100% loss and can be medium or high, depending on the constraints.

**Note:** Likelihood is NOT considered when identifying the severity and the validity of the report.

## Denial-of-Service (DOS) Severity Assessment

Could DOS, griefing, or locking of contracts count as Medium or High severity?

**Criteria:**
1. The issue causes funds to be locked for more than a week
2. The issue impacts the availability of time-sensitive functions (cutoff functions are not considered time-sensitive)

**Severity Guidelines:**
- If at least one criterion applies → Medium
- If both criteria apply → High (additional constraints may decrease severity)
- If single occurrence causes DOS for less than a week → evaluate based on single occurrence (Medium only if disrupts time-sensitive function)
- Exception: If single occurrence is relatively long (>2 days) and takes only 2-3 iterations to cause 7-day DOS → may be valid

## Hierarchy of Truth

**Order of precedence:**
1. Default guidelines (always apply unless overridden)
2. README information (can override defaults)
3. Code comments (may provide context, but README takes precedence in conflicts)
4. Judge can decide code comments are outdated (defaults then apply)
5. Public statements up to 24h before contest ends (can override chosen source of truth)

**Protocol Invariants:**
- Protocol teams can define invariants/properties in README using the question: "What properties/invariants do you want to hold even if breaking them has a low/unknown impact?"
- Breaking these invariants can be Medium severity if it doesn't conflict with common sense
- High severity only if issue falls into High category per judging guidelines

**Examples:**
- Valid Medium: README states "Admin can only call XYZ function once" but code allows twice
- Invalid: README states "Variable X must always match USDC amount" but user can donate USDC to break invariant without causing protocol issues

## Admin Trust Assumptions

**External Admin:**
- If protocol defines restrictions on owner/admin, issues bypassing restrictions may be valid
- Restrictions must be explicitly stated and assessed case by case
- Admin functions assumed to be used correctly and not harm users/protocol
- Valid if admin unknowingly causes issues

**Internal Protocol Roles:**
- Trusted by default
- Can be untrusted only if: 
  - Specifically claimed untrusted in contest README, OR
  - User can get role without admin/owner permission (e.g., paying specific fee)

**Examples:**
- Invalid: "Admin can break deposit by setting fee to 100%+" (common sense: fees can't exceed 100%)
- Valid Medium: "Admin sets fee to 20%, causing liquidations to fail when utilization ratio below 10%" (admin unaware of consequences)

## Contract Scope

- If contract is in contest scope, all parent contracts included by default
- Vulnerability in library used by in-scope contract → valid
- Vulnerability in contract from repo but not in scope → invalid
- Design decisions are not valid (even if suboptimal, unless implying loss of funds)

## VALID Issue Categories

### 1. Slippage Issues
Showing direct loss of funds with detailed explanation → Valid High

### 2. EIP Compliance
Valid only if:
- Protocol/codebase shows important external integrations requiring strong EIP compliance
- EIP must be in regular use or final state

### 3. Out of Gas (OOG)
Valid Medium (or High if blocking all user funds) if:
- Malicious user fills arrays causing OOG, OR
- Practical call flow results in OOG

Invalid (considered Low) if:
- Array length controlled by trusted admin/owner, OR
- Issue describes impractical parameter usage to reach OOG

### 4. Chainlink Price Checks
Valid Medium only if report:
- Explicitly mentions price feeds (e.g., USDC/ETH) for in-scope tokens on in-scope chains
- Includes proper attack path
- Demonstrates at least Medium severity impact
- Check if min/maxAnswer deprecated on the price feed

## INVALID Issue Categories

### 1. Gas Optimizations
User/protocol pays little extra gas → Invalid

### 2. Incorrect Event Values
Incorrectly calculated/wrong values in emitted events → Invalid

### 3. Zero Address Checks
Checks to prevent zero addresses → Invalid

### 4. User Input Validation
Prevention of user mistakes → Invalid
Exception: If user input causes major protocol malfunction or significant loss for others (protocol/users) → Valid High

### 5. Admin Input/Call Validation
- Incorrect call order → Invalid
- Admin action breaking assumptions about code functioning → Invalid
- Exception: See Admin Trust Assumptions section

### 6. Contract/Admin Blacklisting
Protocol contracts/admin addresses blacklisted → Invalid
Exception: Attacker uses blacklisted address to harm protocol → Valid

### 7. Front-running Initializers
Front-running where protocol can redeploy and reinitialize without irreversible damage → Invalid

### 8. User Experience Issues
Minor inconvenience without fund loss (e.g., temporarily inaccessible funds recoverable by admin) → Invalid

### 9. User Blacklist
User blacklisted by token/contract, harming only themselves → Invalid

### 10. Future Opcode Gas Repricing
Not considered Medium/High severity
Use of call vs transfer = protocol design choice (unless good reason call may consume >2300 gas without repricing)

### 11. Accidental Direct Token Transfers
Users accidentally/intentionally transferring tokens directly into contracts (not part of expected operations, no retrieval method) → Invalid (user mistake)
Exception: If leads to harming protocol and/or other users → Valid

### 12. Loss of Airdrops/Rewards
Not part of original protocol design → Invalid

### 13. Storage Gaps
Simple contracts with parent not implementing storage gaps → Low/Informational
Exception: Highly complex branched inheritance with inconsistent storage gaps + clear necessity description → Valid Medium

### 14. Incorrect View Function Values
Default → Low
Exception: If incorrect values used in larger function causing loss of funds → Valid Medium/High depending on impact

### 15. Stale Prices and Chainlink Round Completeness
Recommendations to implement round completeness/stale price checks → Invalid
Exception: Valid if oracle (e.g., Pyth) requires requesting price before use and lack of staleness check could use very old price

### 16. Previous Contest/Audit Issues
Issues from previous contests with "won't fix" labels (in update contests) → Invalid
Issues from previous audits (in README) marked "acknowledged" (not fixed) → Invalid

### 17. Chain Re-org and Network Liveness
Not valid

### 18. ERC721 Unsafe Mint
Users unable to safemint ERC721 due to unsupported implementation → Invalid

### 19. Future Issues
Issues from future integration/implementation not in docs/README or from future code changes → Invalid

### 20. Non-Standard Tokens
Issues with weird-tokens not considered valid unless explicitly mentioned in README
Exception: Tokens with decimals 6-18 are not considered weird

### 21. Solidity Version EVM Compatibility
Using Solidity versions supporting opcodes not working on deployment networks → Invalid (can manage compilation flags)

### 22. Sequencer Reliability
Sequencers assumed reliable. Vulnerabilities relying on sequencer offline/malfunctioning → Invalid

## Recommendations for Report Quality

### PoC (Proof of Concept) Recommended For:
- Non-obvious issues with complex vulnerabilities/attack paths
- Issues with non-trivial input constraints
- Precision loss issues
- Reentrancy attacks
- Gas consumption or reverting message call attacks

**Important:** Original report without PoC considered invalid if issue cannot be clearly understood without one.

### Specifying Conditions
Watsons encouraged to:
- Specify all conditions required to trigger issue
- Clarify scenarios where constraints may apply

### Front-running and Private Mempool
Issues depending on front-running get severity downgraded on chains with private mempool:
- High → Medium
- Medium → Invalid

Reports must explain how issue happens with unintentional front-running. Saying "attacker monitors mempool" → Invalid on private mempool chains.

## Duplication Guidelines

For "potential duplicate" to be duplicated with "target issue", must meet ALL requirements:
1. Identify the root cause
2. Identify at least Medium impact
3. Identify valid attack path or vulnerability path

Otherwise, "potential duplicate" not duplicated but could be judged separately.

### Root Cause Groupings

Issues appearing in multiple places/contracts may have same root cause if:
- Same logic mistake (e.g., uint256 cast to uint128 unsafely)
- Same conceptual mistake (e.g., different untrusted external admins can steal funds)

**Categories:**
- Slippage protection
- Reentrancy
- Access control
- Front-run / sandwich (front-run and sandwich can be duplicated)

If underlying implementations, impact, or fixes are different → may be treated separately.

### Reentrancy Duplication Groups:
- Reenter in same function
- Cross function reentrancy (different function in contract)
- Cross contract reentrancy (different contract in codebase)
- Read-only reentrancy
- Cross-chain reentrancy

Different scenarios of same reentrancy type within codebase → same root cause.

### Front-running/Sandwich/Slippage Duplication Groups:
- Can be fixed by slippage protection
- Can be fixed by commit-reveal mechanism

## Best Practices

1. Read contest readme and documents thoroughly
2. Submit issues valid according to Sherlock guidelines based on discretion
3. Do NOT submit multiple issues in single submission (even if on same line, submit separately)
   - Exception: Multiple obvious repetitions can be combined (see example for guidance)
4. Be specific and sufficiently descriptive about impact
   - Bad: "Loss of funds for the user"
   - Good: "Loss of funds for users as there is no access control for the 'withdraw' function"
5. Do NOT add unnecessarily long code snippets (limit to impact scope, be descriptive in Vulnerability Details)
6. Do NOT copy-paste issues from other contests/reports/past audits (extremely unlikely to be valid)

## Glossary

- **Attack Path:** Sequence of steps malicious actor takes to cause losses/grief to protocol/users and/or gain value/profit
- **Front-run:** Operation A (typically no losses) followed by operation B before A, causing loss for protocol/user(s)
- **Root Cause:** Primary factor or fundamental reason imposing unwanted outcome
- **Sandwich:** Front-run followed by operation C (controlled by attacker who executed B) to revert contract to initial state
- **Vulnerability Path:** Sequence of steps showing how issue causes losses/grief through well-intended protocol usage