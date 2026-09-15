---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27612
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - asimaranov
  - Citris
---

## Vulnerability Title

re-entrency possible on processWithdraw since external call is made before burning user's shares in Vault

### Overview


This bug report is about re-entrency vulnerability on processWithdraw since an external call is made before burning user's shares in Vault. This vulnerability can result in the drain of user funds, which is a medium risk. The relevant GitHub link is https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWithdraw.sol#L182-L197. The recommended solution is to burn user's share first, before executing the external call at the end.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWithdraw.sol#L182-L197">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWithdraw.sol#L182-L197</a>


## Summary
re-entrency possible on processWithdraw since external call is made before burning user's shares in Vault

```solidity
      if (self.withdrawCache.withdrawParams.token == address(self.WNT)) {
        self.WNT.withdraw(self.withdrawCache.tokensToUser);
@>audit transfer ETH and call        (bool success, ) = self.withdrawCache.user.call{value: address(this).balance}("");
        require(success, "Transfer failed.");
      } else {
        // Transfer requested withdraw asset to user
        IERC20(self.withdrawCache.withdrawParams.token).safeTransfer(
          self.withdrawCache.user,
          self.withdrawCache.tokensToUser
        );
      }

      // Transfer any remaining tokenA/B that was unused (due to slippage) to user as well
      self.tokenA.safeTransfer(self.withdrawCache.user, self.tokenA.balanceOf(address(this)));
      self.tokenB.safeTransfer(self.withdrawCache.user, self.tokenB.balanceOf(address(this)));

      // Burn user shares
@> burn is after      self.vault.burn(self.withdrawCache.user, self.withdrawCache.withdrawParams.shareAmt);
```

https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWithdraw.sol#L182-L197

Since the function is only accessible by keeper (likely a router), which from the example of the mockRouter, would bundle the withdraw and "afterWithdrawalExecution" together. However since the router is out-of-scope, and there is still a possible chance that the user can make use of the router to re-enter into the function (without re-entrency lock), and be able to drain more fund that he actually deserves. This is submitted as a medium risk.

## Vulnerability Details

## Impact
drain of user funds.

## Tools Used

## Recommendations
burn user's share first, before executing external call at the end.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | asimaranov, Citris |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

