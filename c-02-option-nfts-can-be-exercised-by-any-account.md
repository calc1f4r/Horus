---
# Core Classification
protocol: Sharwafinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36473
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[C-02] Option NFTs can be exercised by any account

### Overview


The severity and impact of this bug are high, and the likelihood of it occurring is also high. The `exercise` function in the code does not check if the margin account owns the token that is being exercised. This means that any account can exercise the options of another account and receive its profit. A proof of concept code is provided to demonstrate how this bug can be exploited. To fix this issue, a requirement should be added to check if the margin account has ownership of the token before it can be exercised.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** High

**Description**

The `exercise` function flow does not check if the margin account owns the token to be exercised. This allows any account to exercise the options of another account and get its profit.

**Proof of concept**

```solidity
function test_exerciseByNotOwner() public {
    uint256 aliceAccountValue = marginTrading.calculateMarginAccountValue(marginAccountID[alice]);
    uint256 bobAccountValue = marginTrading.calculateMarginAccountValue(marginAccountID[bob]);
    uint256 aliceOptionID = optionID[alice];

    vm.prank(alice);
    marginTrading.provideERC721(marginAccountID[alice], address(hegicPositionsManager), aliceOptionID);

    vm.prank(bob);
    marginTrading.exercise(marginAccountID[bob], address(hegicPositionsManager), aliceOptionID);

    uint256 aliceAccountIncrease = marginTrading.calculateMarginAccountValue(marginAccountID[alice]) - aliceAccountValue;
    uint256 bobAccountIncrease = marginTrading.calculateMarginAccountValue(marginAccountID[bob]) - bobAccountValue;
    assert(aliceAccountIncrease == 0);
    assert(bobAccountIncrease == 1_000e6);
}
```

**Recommendations**

```diff
    function exercise(uint marginAccountID, address token, uint collateralTokenID) external nonReentrant onlyApprovedOrOwner(marginAccountID)  {
+       require(marginAccount.checkERC721Value(marginAccountID, token, value), "You are not allowed to execute this ERC721 token");
        marginAccount.exercise(marginAccountID, token, BASE_TOKEN, collateralTokenID, msg.sender);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sharwafinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

