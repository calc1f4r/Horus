---
# Core Classification
protocol: Cooler
chain: everychain
category: uncategorized
vulnerability_type: transferfrom_vs_safetransferfrom

# Attack Vector Details
attack_type: transferfrom_vs_safetransferfrom
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6278
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/36
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/335

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
  - transferfrom_vs_safetransferfrom
  - safetransfer

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 58
finders:
  - HollaDieWaldfee
  - 0x52
  - psy4n0n
  - Metadev
  - yixxas
---

## Vulnerability Title

H-1: Use safeTransfer/safeTransferFrom consistently instead of transfer/transferFrom

### Overview


This bug report was found by tsvetanovv, 0x52, polthedev, wagmi, enckrish, ak1, IllIllI, yongkiws, ctrlc03, zaskoh, Trumpero, TrungOre, Breeje, imare, jonatascm, cccz, Metadev, Nyx, neumo, Atarpara, serial-coder, yixxas, Tricko, 8olidity, Qeew, ahmedovv, libratus, usmannk, MohanVarma, psy4n0n, 0x4non, kiki\_dev, peanuts, 0xhacksmithh, eyexploit, 0xSmartContract, supernova, Zarf, thekmj, ltyu, ck, sach1r0, hansfriese, John, HollaDieWaldfee, HonorLt, rvierdiiev, zaevlad, 0xAgro, Avci, gjaldon, Madalad, ch0bu, bin2chen, Bahurum, seyni, 0xadrii, and Deivitto.

The issue is that transfer/transferFrom is being used instead of safeTransfer/safeTransferFrom in the Cooler contract. This could lead to serious problems because some tokens do not revert on failure, but instead return false. For example, if the debt token is ZRX, the lender can clear the request without providing any debt token. The impact of this is that the lender could exploit this vulnerability and clear the request without providing any debt token.

The recommendation is to use safeTransfer/safeTransferFrom consistently instead of transfer/transferFrom. The tool used to find this bug was manual review. The sponsor commented that it was a good spot and a niche case.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/335 

## Found by 
tsvetanovv, 0x52, polthedev, wagmi, enckrish, ak1, IllIllI, yongkiws, ctrlc03, zaskoh, Trumpero, TrungOre, Breeje, imare, jonatascm, cccz, Metadev, Nyx, neumo, Atarpara, serial-coder, yixxas, Tricko, 8olidity, Qeew, ahmedovv, libratus, usmannk, MohanVarma, psy4n0n, 0x4non, kiki\_dev, peanuts, 0xhacksmithh, eyexploit, 0xSmartContract, supernova, Zarf, thekmj, ltyu, ck, sach1r0, hansfriese, John, HollaDieWaldfee, HonorLt, rvierdiiev, zaevlad, 0xAgro, Avci, gjaldon, Madalad, ch0bu, bin2chen, Bahurum, seyni, 0xadrii, Deivitto

## Summary
Use safeTransfer/safeTransferFrom consistently instead of transfer/transferFrom
## Vulnerability Detail
Some tokens do not revert on failure, but instead return false (e.g. [ZRX](https://etherscan.io/address/0xe41d2489571d322189246dafa5ebde1f4699f498#code)).
https://github.com/d-xo/weird-erc20/#no-revert-on-failure
tranfser/transferfrom is directly used to send tokens in many places in the contract and the return value is not checked.
If the token send fails, it will cause a lot of serious problems.
For example, in the clear function, if debt token is ZRX, the lender can clear request without providing any debt token.
```solidity
    function clear (uint256 reqID) external returns (uint256 loanID) {
        Request storage req = requests[reqID];

        factory.newEvent(reqID, CoolerFactory.Events.Clear);

        if (!req.active) 
            revert Deactivated();
        else req.active = false;

        uint256 interest = interestFor(req.amount, req.interest, req.duration);
        uint256 collat = collateralFor(req.amount, req.loanToCollateral);
        uint256 expiration = block.timestamp + req.duration;

        loanID = loans.length;
        loans.push(
            Loan(req, req.amount + interest, collat, expiration, true, msg.sender)
        );
        debt.transferFrom(msg.sender, owner, req.amount);
    }
```
## Impact
If the token send fails, it will cause a lot of serious problems.
For example, in the clear function, if debt token is ZRX, the lender can clear request without providing any debt token.
## Code Snippet
https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L85-L86
https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L122-L123
https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L146-L147
https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L179-L180
https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L205-L206
https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L102-L103
## Tool used

Manual Review

## Recommendation
Consider using safeTransfer/safeTransferFrom consistently.

## Discussion

**hrishibhat**

Sponsor comment:
> Good spot. Niche case.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cooler |
| Report Date | N/A |
| Finders | HollaDieWaldfee, 0x52, psy4n0n, Metadev, yixxas, gjaldon, polthedev, ctrlc03, Nyx, ch0bu, yongkiws, 0xSmartContract, MohanVarma, tsvetanovv, ltyu, Trumpero, Qeew, usmannk, peanuts, kiki\_dev, ahmedovv, Breeje, zaevlad, Zarf, Avci, supernova, eyexploit, 0xadrii, 0xAgro, 0x4non, IllIllI, Deivitto, Bahurum, 0xhacksmithh, cccz, Tricko, Atarpara, Madalad, hansfriese, ak1, imare, serial-coder, zaskoh, TrungOre, 8olidity, rvierdiiev, enckrish, bin2chen, sach1r0, John, HonorLt, thekmj, wagmi, neumo, libratus, seyni, jonatascm, ck |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/335
- **Contest**: https://app.sherlock.xyz/audits/contests/36

### Keywords for Search

`transferFrom vs safeTransferFrom, SafeTransfer`

