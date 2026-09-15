---
# Core Classification
protocol: Popcorn
chain: everychain
category: uncategorized
vulnerability_type: weird_erc20

# Attack Vector Details
attack_type: weird_erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22011
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/503

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
  - weird_erc20
  - fee_on_transfer

protocol_categories:
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 19
finders:
  - koxuan
  - 0xSmartContract
  - KIntern\_NA
  - 0xNazgul
  - rbserver
---

## Vulnerability Title

[M-14] Fee on transfer token not supported

### Overview


A bug was discovered in the Lock fund for escrow using a fee on transfer token. When a user makes a Lock fund, the contract receives less amount (X-fees) than the full amount (X) due to fees, but the escrow object is created for the full amount (X). When the escrow duration is over and a claim is made using the claimRewards function, the claimable amount is the full amount (X), but this fails on transfer to the account since the contract has only the amount minus the fees (X-fees). 

To mitigate this issue, it is recommended to compute the balance before and after transfer and subtract them to get the real amount. Additionally, using nonReentrant while using this can prevent reentrancy in ERC777 tokens. This bug was confirmed by RedVeil (Popcorn).

### Original Finding Content


If you are making a Lock fund for escrow using a fee on transfer token then contract will receive less amount (X-fees) but will record full amount (X). This becomes a problem as when claim is made then call will fail due to lack of funds. Worse, one user will unknowingly take the missing fees part from another user deposited escrow fund.

### Proof of Concept

1.  User locks token X as escrow which takes fee on transfer
2.  For same, he uses `lock` function which transfers funds from user to contract

<!---->

     function lock(
        IERC20 token,
        address account,
        uint256 amount,
        uint32 duration,
        uint32 offset
      ) external {
    ...
     token.safeTransferFrom(msg.sender, address(this), amount);
    ...
    escrows[id] = Escrow({
          token: token,
          start: start,
          end: start + duration,
          lastUpdateTime: start,
          initialBalance: amount,
          balance: amount,
          account: account
        });
    ...
    }

3.  Since token has fee on transfer, the contract receives only `amount-fees` but the escrow object is created for full `amount`

4.  Lets say escrow duration is over and claim is made using `claimRewards` function

<!---->

    function claimRewards(bytes32[] memory escrowIds) external {
    ...
     uint256 claimable = _getClaimableAmount(escrow);
    ...    
     escrow.token.safeTransfer(escrow.account, claimable);
    ...
    }

5.  Since full duration is over, the claimable amount is `amount`. But this fails on transfer to account since contract has only `amount-fees`

### Recommended Mitigation Steps

Compute the balance before and after transfer and subtract them to get the real amount. Also use nonReentrant while using this to prevent from reentrancy in ERC777 tokens.

**[RedVeil (Popcorn) confirmed](https://github.com/code-423n4/2023-01-popcorn-findings/issues/503)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | koxuan, 0xSmartContract, KIntern\_NA, 0xNazgul, rbserver, joestakey, btk, Josiah, csanuragjain, Bauer, Deivitto, Viktor\_Cortess, RaymondFam, UdarTeam, rvi0x, 0xdeadbeef0x, pavankv, 0xNineDec, Rolezn |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/503
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`Weird ERC20, Fee On Transfer`

