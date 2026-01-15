---
# Core Classification
protocol: NFT protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50405
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/woonkly/nft-protocol-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/woonkly/nft-protocol-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

OWNER IN ERC721DEFAULTAPPROVALMINIMAL.ISAPPROVEDOROWNER IS NOT CORRECTLY VERIFIED

### Overview


This bug report is about a function called `isApprovedOrOwner()` in a contract called `ERC721DefaultApprovalMinimal`. This function is used to check if an address is approved or the owner for certain transactions. However, the logic used in this function is incorrect, which means that it can sometimes give a wrong result. This bug can be reproduced by using a specific address that is not actually approved or the owner, but still getting a true result. The report includes a code example that shows how this bug can be reproduced. The impact and likelihood of this bug are both rated as 3 out of 5. The recommendation is to modify the condition parameters in the code to correctly check for `ownerOf(tokenId)` instead of `msg.sender()` and `spender`. This issue has been solved by the Woonkly team.

### Original Finding Content

##### Description

The contract `ERC721DefaultApprovalMinimal` contains the function `isApprovedOrOwner()`:

#### ERC721WoonklyNFTRevealWave.sol

```
function _isApprovedOrOwner(address spender, uint256 tokenId) internal virtual override view returns (bool) {
        return !rejectedDefaultApprovals[_msgSender()][spender] && (spender==transferProxy || spender==extraOperator || super._isApprovedOrOwner(spender, tokenId));
    }

```

This function returns if an address is approved or the owner for transactions but the logic followed to determine if he is approved or is the owner is not correct. It is possible to get a true result using an address that is not actually approved nor owner.

#### test.js

```
    //minting 5 tokens to owner
    await token.mint(5, 0, [], { from: owner });

    let res = await token.isApprovedOrOwner(owner, 1, { from: owner });
    console.log("1 - owner approved owner, it should be true. The result is " + res);

    res = await token.isApprovedOrOwner(owner, 1, { from: accounts[5] });
    console.log("2 - random addr approved owner, it should be false. The result is " + res);

```

When the above tests are executed, the following result is obtained.

```
1 - owner approved owner, it should be true. The result is true
2 - random addr approved owner, it should be false. The result is true

```

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED**: The `Woonkly team` modified the condition parameters to correctly check for `ownerOf(tokenId)` instead of `msg.sender()` and `spender`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | NFT protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/woonkly/nft-protocol-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/woonkly/nft-protocol-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

