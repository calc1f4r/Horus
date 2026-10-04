---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49431
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#1-broken-authorization
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Broken authorization

### Overview


The bug report highlights issues with certain functions in a protocol that do not have proper checks in place for important actions. This could potentially allow unauthorized users to transfer funds, manipulate prices, and make changes that could negatively impact all users. The report recommends implementing strict access controls and ownership checks for these functions, as well as restricting external calls and adding access controls for certain functions. These measures would help prevent unauthorized actions and ensure the security of the protocol.

### Original Finding Content

##### Description
Some functions lack authorization checks for critical actions.

**LendingPool Functions:**
* `supplyFor()`: Anyone can call this function with arbitrary arguments for `depositor` and `receiver`, enabling the transfer of approved limits from any user to any other user.
* `repayFor()`: Anyone can call this function with arbitrary `borrower` and `repayer` arguments, allowing the transfer of approved limits from any user to any other user.
* `reBalance()`: Anyone can call this function with an arbitrary `_depositor`, potentially allowing funds to be taken from any user and swapped for a different asset, which could incur slippage and value loss.
* `withdrawFor()`: Through settlement hooks, a solver can call this function with arbitrary `depositor` arguments, enabling the transfer of any user's supply to any other user.
* `borrowFor()` (both overloaded versions): Through settlement hooks, a solver can call this function with arbitrary `borrower` and `receiver` (or `borrower` and `recipient`) arguments, allowing funds to be borrowed from any user for the benefit of any other user.

**Additional Functions:**
* `PriceProvider.setFallbackProvider()`: Any user can call this function to set a fallback price provider, potentially enabling malicious actions and price data manipulation.
* Any user can submit arbitrary IRM parameters via `Configurator.propose()` and execute them with `Configurator.execute()`. Since only the proposer can cancel the proposal, a malicious user only needs to wait for the `delay + period` time to execute it. Modifying IRM settings is a critical action that could negatively impact all protocol users.

##### Recommendation

We recommend adding strict access controls and checks for critical functions, particularly to prevent unauthorized actions:

1. **Implement Role-Based Access Control (RBAC) for Critical Functions:**
   * Assign specific roles to users who are permitted to execute sensitive functions.
   * Require functions such as `supplyFor()`, `repayFor()`, `reBalance()`, `withdrawFor()`, `borrowFor()`, `setFallbackProvider()`, and `Configurator`-related functions to verify the caller’s role before proceeding.

2. **Require Ownership or Delegation Checks:**
   * **For `supplyFor()`, `repayFor()`, `withdrawFor()`, and `borrowFor()`**: Ensure the caller is either the owner of the funds or has explicit delegation to act on behalf of the user specified in the arguments (e.g., `depositor`, `borrower`, `receiver`).
   * This can prevent unauthorized third parties from calling these functions and accessing or manipulating funds without the owner’s permission.

3. **Restrict External Calls via Settlement Hooks:**
   * Apply checks and validation to settlement hooks to prevent Solver-role from exploiting functions like `withdrawFor()` and `borrowFor()` with arbitrary arguments.
   * Consider whitelisting approved entities or functions that can interact with these hooks.

4. **Add Access Control to `setFallbackProvider()` and `Configurator` Functions:**
   * Limit access to `PriceProvider.setFallbackProvider()` to trusted users or a multisig account. This will prevent unauthorized users from setting or manipulating fallback providers and price data.
   * Similarly, restrict `Configurator.propose()` and `Configurator.execute()` to only authorized users or roles that have been vetted for security. Additionally, a review and approval mechanism for IRM parameter changes must be enforced, ensuring they are properly vetted before execution.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#1-broken-authorization
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

