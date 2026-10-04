# Code4rena Judging Criteria Reference

Source: https://docs.code4rena.com/competitions/severity-categorization  
        https://docs.code4rena.com/competitions/judging-criteria

---

## Severity Classifications

### 3 — HIGH
Assets can be stolen/lost/compromised directly OR indirectly through a valid attack path that does not rely on hand-wavy hypotheticals.

- Direct loss of funds, NFTs, data, authorization, or private/confidential information.
- Loss of matured yield (treated like any other capital loss) — real amounts depend on specific conditions and likelihood.
- **Loss of unmatured yield / yield in motion is capped at MEDIUM**.

### 2 — MEDIUM
Assets not at direct risk, but:
- The function of the protocol or its availability could be impacted, OR
- Value could leak with a **hypothetical** attack path (stated assumptions + external requirements required).

### QA — Quality Assurance (Low / Governance / Centralization)
Accumulated in a single QA report per warden. Includes:
- **Low risk**: Assets are not at risk; state handling issues, function incorrect as to spec, comment issues.
- **Governance/Centralization risk**: Issues involving admin privileges.
- **Informational** (DISCOURAGED — do not submit unless highly impactful): code style, clarity, syntax, versioning, off-chain monitoring / events.

**Where assets = funds, NFTs, data, authorization, and any information intended to be private or confidential.**

---

## Severity Caps & Special Rules

### Loss of Fees / Loss of Yield
- **Dust amounts** (rounding errors, marginal variations): QA/Low.
- **Real amounts**: Assessed based on specific conditions and likelihood considerations.
- **Loss of unmatured yield or yield in motion**: Capped at MEDIUM.

### Centralization Risks
- All roles assigned by the system are assumed trustworthy.
- **Reckless admin mistakes are INVALID** — assume calls are previewed before execution.
- **Direct misuse of privileges → QA report** (Low/Governance), NOT Medium/High.
- **Mistakes in code only unblockable through admin mistakes → QA report**.
- **Privilege escalation issues** are judged by **likelihood and impact**.
- Any execution using privileged functions that results in vulnerability **may be classified up to MEDIUM** (never High for admin-gated issues unless escalation is possible by non-admin).

### Unsupported / Non-Standard Tokens & Fee-On-Transfer Tokens
- All non-standard/weird ERC-20 and fee-on-transfer token findings are **OUT OF SCOPE** by default.
- Exceptions: explicitly listed as supported in scope/documentation.
- **USDT is always in scope** despite its non-standard behavior.
- Judges must immediately invalidate findings in this category unless the above exception applies.

### View Functions
- Vulnerabilities in unused view functions are **QA/Low at best**.

### Fault in Out-of-Scope Library vs. Incorrect Implementation
- **Root cause in OOS contract itself → OOS (invalid)**.
- **Root cause is in-scope contract's misuse/incorrect implementation of OOS code → VALID, in-scope**.
- Exceptional scenarios at judge's discretion.

### Conditional on User Mistake
- Findings requiring the user to be careless or enter wrong information are **QA at best, and may be INVALID**.
- Non-privileged users are expected to preview transactions.
- Phishing and improper caution in protocol usage → this rule applies → invalid/QA.

### Speculation on Future Code
- Any issue not exploitable within contest scope = speculating on future code → **INVALID** unless:
  - Root cause is demonstrably in contest scope, AND
  - Warden argues convincingly why a future code change making it manifest is **reasonably likely**.
- If exploitability relies on a 3rd-party integration, likelihood must factor in a **competent, due-diligent integrator**.

### Event-Related Impacts
- Events used for on-chain processes (bridging, inclusion proofs, etc.) → assessed on impacted functionality (may be Med/High).
- EIP non-compliance from events → assessed on actual impact.
- Failure to demonstrate broader impact → **capped at Low**.
- Readability/display/front-end issues from events → **capped at Low**.

### Approve Race Condition
- `approve`/`safeApprove` front-run: **NOT a valid vulnerability**.
- `approve`/`safeApprove` are NOT deprecated.
- `increaseAllowance`/`decreaseAllowance` ARE deprecated but using them is NOT a finding.

### Protocol Does Not Support CryptoPunks
- **Informational (refactoring) → wardens are DISCOURAGED from submitting**.
- Cannot be argued as a vulnerability.

---

## Validity Criteria

Judges assess each submission as `valid`, `invalid`, or `out of scope`.

Validity is evaluated using:
1. **Burden of proof**: Submission must demonstrate the vulnerability concretely.
2. **Good citizenship**: Submission must add genuine value; not disrespectful of sponsor/judge time.
3. **Scope**: Must be in-scope code/issue unless warden makes compelling argument to bring it in.

### Findings from Prior Audit Reports
- Known issues in `README` are generally **out of scope** / invalid.
- Exception: If finding was confirmed but **not mitigated** before the C4 audit → may be valid.
- Exception: If submission demonstrates a **substantively distinct or higher-severity attack path** → may be valid at judge's discretion.

---

## Quality Assessment

Judges assess quality as `sufficient`, `insufficient`, or `low quality/spam`.

**Insufficient quality** (ineligible for awards, penalizes signal score) if:
- Incorrect finding.
- Low/incomplete effort.
- Clearly overinflated severity.
- PoC does not pass the burden of proof test.
- Direct copies of other reports in the same audit.

**Sufficient quality bar**: Roughly at the level of a draft finding in a professional auditor's report — technical substance is the primary criterion; writing quality matters only where it interferes with comprehension.

**QA Report Grades** (for Low/Governance reports):
- **Grade A**: High quality report.
- **Grade B**: Satisfactory report.
- **Grade C**: Unsatisfactory report.
- Only top 3 QA reports receive awards.
- Judges may downgrade QA reports that overstate severity (submitting low/info as med/high).

---

## Duplicate Submissions

Findings are duplicates if they share the **same root cause**:
- If fixing the root cause (in a reasonable manner) would cause the finding to no longer be exploitable → duplicates.
- When similar exploits show different impacts → highest/most irreversible impact is used for scoring.

### Full Credit Requirements
- Identification AND demonstration of the **root cause**.
- Identification AND demonstration of the **maximum achievable impact**.

**Satisfactory demonstration** = either:
1. Step-by-step explanation (root cause → impact) with code snippets or coded PoC, OR
2. At judge's discretion, a high-standard issue may be accepted with less detail.

**Partial credit / downgrade triggers**:
- Lack of root cause identification.
- Lack of maximal impact analysis.
- Poor writing/presentation quality.
- Lack or incorrectness of remediation steps.

---

## Severity Decision Framework

```
1. Is the issue in scope?
   → No → INVALID / OOS
   → Yes → continue

2. Does the root cause exist in in-scope code?
   → OOS library root cause → OOS (invalid)
   → In-scope misuse of OOS library → VALID

3. Does exploitation require admin error / user mistake?
   → Admin error (reckless, previewed) → QA / INVALID
   → User mistake (wrong input) → QA at best / INVALID
   → Privilege escalation (non-admin can trigger) → use Impact × Likelihood

4. Is exploitation speculative / future code only?
   → Yes (no root cause in current scope) → INVALID
   → Root cause in scope, future trigger reasonably likely → Judge's discretion (max MEDIUM typically)

5. Assess Impact:
   → Assets stolen/lost/compromised directly → HIGH candidate
   → Protocol function / availability impacted, or hypothetical path with external conditions → MEDIUM candidate
   → No asset risk; spec-level / state / comment issues → QA/Low

6. Apply Severity Caps:
   → Dust / rounding losses → QA/Low
   → Unmatured yield loss → cap at MEDIUM
   → Admin-only exploitable → cap at MEDIUM (or QA)
   → Non-standard ERC20 (not in scope) → INVALID
   → View-only function → QA/Low
   → Events (no broader impact) → cap at Low
   → Approve race condition → INVALID
   → Conditional on user mistake → QA / INVALID

7. Assign Severity:
   HIGH / MEDIUM / QA(Low/Gov) / INVALID
```

---

## Key Principles

- **Protocol documentation > code** as source of truth for intended behavior.
- Wardens are providing a consultative service; submissions must add value.
- Judges' decisions are final after PJQA period closes.
- The bar for validity evolves with the overall quality of submissions in a contest.

---

## Judge Independence & Anti-Pressure Rules

### Warden Pressure Must Not Inflate Severity

- **Judges determine validity and severity** — sponsor input is considered, but the judge has final authority.
- A warden arguing forcefully for a higher severity during PJQA is **not a technical argument**. Hold the verdict unless new technical evidence is presented.
- **Severity inflation = insufficient quality**: submissions with clearly overinflated severity are ineligible for awards. Do not reward inflation by accepting it.
- It is within the judge's discretion to **invalidate all of a warden's findings** in a contest for repeated low-quality or bad-faith submissions.
- **PJQA is limited in scope**: its purpose is to identify overlooked duplicates and ensure consistent rule application — not to allow wardens to negotiate higher severity. Contacting judges directly outside PJQA is not permitted.
- Judge decisions are **final** once the PJQA window closes.

### Mandatory Severity Escalation (Never Under-Judge)

- If the attack path directly compromises assets without hand-wavy hypotheticals, the severity **must** be HIGH — do not soften to avoid controversy.
- Always assess the **maximum achievable impact** of the root cause. When duplicates demonstrate different impacts, the highest and most irreversible impact governs severity for the entire duplicate group.
- If initial severity was too low and new _technical_ evidence (not warden pressure) shows higher maximum impact, **upgrade** the severity.
- A finding being disputed or generating many PJQA comments does not reduce its severity. Severity is a purely technical determination.

### Raising the Bar Over Time

- C4 criteria explicitly states that judges raising the quality bar as the competition matures is **consistent and correct behavior**, not inconsistency.
- The standard evolves based on the aggregate quality of submissions observed — this is appropriate.
- Apply the highest professional standard consistent with what a competent professional auditor's draft report would meet.
