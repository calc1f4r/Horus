---
# Core Classification
protocol: Debt DAO
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6236
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-debt-dao-contest
source_link: https://code4rena.com/reports/2022-11-debtdao
github_link: https://github.com/code-423n4/2022-11-debtdao-findings/issues/119

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - business_logic

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - payments
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - adriro
  - berndartmueller
  - Lambda
  - aphak5010
---

## Vulnerability Title

[H-02] Non-existing revenue contract can be passed to claimRevenue to send all tokens to treasury

### Overview


This bug report is about a vulnerability in the SpigotLib smart contract. The vulnerability is that neither `SpigotLib.claimRevenue` nor `SpigotLib._claimRevenue` checks that the provided `revenueContract` was registered before. As a result, all of the tokens are sent to the treasury and none are sent to the escrow, which is problematic for revenue tokens that use push payments. This can be exploited by a malicious actor to ensure that no revenue is available for the lender. 

The recommended mitigation step is to check that a revenue contract was registered before, and revert if it does not. This would prevent the malicious actor from exploiting the vulnerability and ensure that the revenue is sent to the appropriate party.

### Original Finding Content


Neither `SpigotLib.claimRevenue` nor `SpigotLib._claimRevenue` check that the provided `revenueContract` was registered before. If this is not the case, `SpigotLib._claimRevenue` assumes that this is a revenue contract with push payments (because `self.settings[revenueContract].claimFunction` is 0) and just returns the difference since the last call to `claimRevenue`:

```solidity
       if(self.settings[revenueContract].claimFunction == bytes4(0)) {
            // push payments

            // claimed = total balance - already accounted for balance
            claimed = existingBalance - self.escrowed[token]; //@audit Rebasing tokens
            // underflow revert ensures we have more tokens than we started with and actually claimed revenue
        }
```

`SpigotLib.claimRevenue` will then read `self.settings[revenueContract].ownerSplit`, which is 0 for non-registered revenue contracts:

```solidity
uint256 escrowedAmount = claimed * self.settings[revenueContract].ownerSplit / 100;
```

Therefore, the whole `claimed` amount is sent to the treasury.

This becomes very problematic for revenue tokens that use push payments. An attacker (in practice the borrower) can just regularly call `claimRevenue` with this token and a non-existing revenue contract. All of the tokens that were sent to the spigot since the last call will be sent to the treasury and none to the escrow, i.e. a borrower can ensure that no revenue will be available for the lender, no matter what the configured split is.

### Proof Of Concept

As mentioned above, the attack pattern works for arbitrary tokens where one (or more) revenue contracts use push payments, i.e. where the balance of the Spigot increases from time to time. Then, the attacker just calls `claimRevenue` with a non-existing address. This is illustrated in the following diff:

```diff
--- a/contracts/tests/Spigot.t.sol
+++ b/contracts/tests/Spigot.t.sol
@@ -174,7 +174,7 @@ contract SpigotTest is Test {
         assertEq(token.balanceOf(address(spigot)), totalRevenue);
         
         bytes memory claimData;
-        spigot.claimRevenue(revenueContract, address(token), claimData);
+        spigot.claimRevenue(address(0), address(token), claimData);
```

Thanks to this small modification, all of the tokens are sent to the treasury and none are sent to the escrow.

### Recommended Mitigation Steps

Check that a revenue contract was registered before, revert if it does not.

**[kibagateaux (Debt DAO) confirmed](https://github.com/code-423n4/2022-11-debtdao-findings/issues/119)** 


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Debt DAO |
| Report Date | N/A |
| Finders | adriro, berndartmueller, Lambda, aphak5010 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-debtdao
- **GitHub**: https://github.com/code-423n4/2022-11-debtdao-findings/issues/119
- **Contest**: https://code4rena.com/contests/2022-11-debt-dao-contest

### Keywords for Search

`Validation, Business Logic`

