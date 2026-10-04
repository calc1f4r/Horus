---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25214
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/89

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-03]  `AccountantDelegate`: `sweepInterest` function will destroy the cnote in the contract.

### Overview


This bug report details an issue with the AccountantDelegate contract in the Plex Lending Market. When the user borrows note tokens, the AccountantDelegate contract provides note tokens and gets cnote tokens in return. However, when the user repays the note tokens, the cnote tokens are destroyed and the note tokens are transferred to the AccountantDelegate contract.

The issue is that in the sweepInterest function of the AccountantDelegate contract, all cnote tokens in the contract are transferred to address 0. This will prevent the user from repaying the note tokens, and the sweepInterest function will not calculate the interest correctly later. The bug was found by both cccz and WatchPug and can be seen in the provided Proof of Concept.

The recommended mitigation steps are to add a require statement to the sweepInterest function to ensure that the cNoteConverted is greater than or equal to the noteDifferential. This will prevent the cnote tokens from being transferred to address 0, thus allowing the user to repay the note tokens and the sweepInterest function to calculate the interest correctly.

The bug was confirmed by tkkwon1998 (Canto) and Alex the Entreprenerd (judge) commented that the sponsor should look into redeeming the cNote over destroying it. Alex also agreed with High Severity for the bug.

### Original Finding Content

_Submitted by cccz, also found by WatchPug_

When the user borrows note tokens, the AccountantDelegate contract provides note tokens and gets cnote tokens. Later, when the user repays the note tokens, the cnote tokens are destroyed and the note tokens are transferred to the AccountantDelegate contract.
However, in the sweepInterest function of the AccountantDelegate contract, all cnote tokens in the contract will be transferred to address 0. This will prevent the user from repaying the note tokens, and the sweepInterest function will not calculate the interest correctly later.

### Proof of Concept

<https://github.com/Plex-Engineer/lending-market/blob/ab31a612be354e252d72faead63d86b844172761/contracts/Accountant/AccountantDelegate.sol#L74-L92><br>
<https://github.com/Plex-Engineer/lending-market/blob/ab31a612be354e252d72faead63d86b844172761/contracts/CToken.sol#L533>

### Recommended Mitigation Steps

        function sweepInterest() external override returns(uint) {
    		
    		uint noteBalance = note.balanceOf(address(this));
    		uint CNoteBalance = cnote.balanceOf(address(this));

    		Exp memory expRate = Exp({mantissa: cnote.exchangeRateStored()}); // obtain exchange Rate from cNote Lending Market as a mantissa (scaled by 1e18)
    		uint cNoteConverted = mul_ScalarTruncate(expRate, CNoteBalance); //calculate truncate(cNoteBalance* mantissa{expRate})
    		uint noteDifferential = sub_(note.totalSupply(), noteBalance); //cannot underflow, subtraction first to prevent against overflow, subtraction as integers

    		require(cNoteConverted >= noteDifferential, "Note Loaned to LendingMarket must increase in value");
    		
    		uint amtToSweep = sub_(cNoteConverted, noteDifferential);

    		note.transfer(treasury, amtToSweep);

    -		cnote.transfer(address(0), CNoteBalance);

    		return 0;
        }

**[tkkwon1998 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-findings/issues/89)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/89#issuecomment-1205796186):**
 > The warden has shown how, due to a programmer mistake, interest bearing Note will be burned.
> 
> It is unclear why this decision was made, and I believe the sponsor should look into `redeem`ing the `cNote` over destroying it.
> 
> The sponsor confirmed, and because this finding shows unconditional loss of assets, I agree with High Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/89
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

