---
# Core Classification
protocol: Dexe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27308
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
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

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

Distribution proposals simultaneously funded by both ETH and ERC20 tokens results in stuck eth

### Overview


This bug report is about a function in the DeXe-Protocol called `DistributionProposal::execute()` which allows distribution proposals to be funded by both Ethereum (ETH) and ERC20 tokens in the same transaction. The problem is that when this occurs, claiming rewards only releases the ERC20 tokens, leaving the ETH permanently stuck in the `DistributionProposal` contract. This bug is demonstrated in an example of code added to the `test/gov/proposals/DistributionProposal.test.js` file.

The recommended mitigation for this bug is to make `DistributionProposal::execute()` revert if the token is not ETHEREUM_ADDRESS and the message value is greater than zero. This fix should also be applied to other places where the same issue appears, such as `TokenSaleProposalBuy::buy()` and `TokenSaleProposalWhitelist::lockParticipationTokens()`.

The bug has been fixed in two commits, 5710f31 and 64bbcf5. These commits have been verified by Cyfrin.

### Original Finding Content

**Description:** [`DistributionProposal::execute()`](https://github.com/dexe-network/DeXe-Protocol/tree/f2fe12eeac0c4c63ac39670912640dc91d94bda5/contracts/gov/proposals/DistributionProposal.sol#L49-L69) allows distribution proposals to be simultaneously funded by both eth & erc20 tokens in the same transaction.

**Impact:** When this occurs claiming rewards only releases the erc20 tokens - the eth is permanently stuck in the `DistributionProposal` contract.

**Proof of Concept:** Add the PoC to `test/gov/proposals/DistributionProposal.test.js` under the section `describe("claim()", () => {`:
```javascript
      it("audit new distribution proposals funded by both eth & erc20 tokens results in stuck eth", async () => {
        // DistributionProposal eth balance starts at 0
        let balanceBefore = toBN(await web3.eth.getBalance(dp.address));
        assert.equal(balanceBefore, 0);

        // mint reward tokens to sending address
        await token.mint(govPool.address, wei("10"));

        // use GovPool to create a proposal with 10 wei reward
        await govPool.createProposal(
          "example.com",
          [
            [token.address, 0, getBytesApprove(dp.address, wei("10"))],
            [dp.address, 0, getBytesDistributionProposal(1, token.address, wei("10"))],
          ],
          [],
          { from: SECOND }
        );

        // fully fund the proposal using both erc20 token and eth at the same time
        await impersonate(govPool.address);
        await token.approve(dp.address, wei("10"), { from: govPool.address });
        await dp.execute(1, token.address, wei("10"), { value: wei(10), from: govPool.address });

        // only 1 vote so SECOND should get the entire 10 wei reward
        await govPool.vote(1, true, 0, [1], { from: SECOND });

        // claiming the reward releases the erc20 tokens but the eth remains stuck
        await dp.claim(SECOND, [1]);

        // DistributionProposal eth balance at 10 wei, reward eth is stuck
        let balanceAfter = toBN(await web3.eth.getBalance(dp.address));
        assert.equal(balanceAfter, wei("10"));
      });
```
Run with `npx hardhat test --grep "audit new distribution proposals funded by both eth & erc20 tokens results in stuck eth"`

**Recommended Mitigation:** `DistributionProposal::execute()` should revert if `token != ETHEREUM_ADDRESS && msg.value > 0`.

Similar fixes will need to be made in places where the same issue appears:
* `TokenSaleProposalBuy::buy()`
* `TokenSaleProposalWhitelist::lockParticipationTokens()`

**Dexe:**

Fixed in commits [5710f31](https://github.com/dexe-network/DeXe-Protocol/commit/5710f31a515b40fab27d55e55adc3df19efca489#diff-9559fcfcd35b0e7d69c24765fb0d5996a7b0b87781860c7f821867c26109814f) & [64bbcf5](https://github.com/dexe-network/DeXe-Protocol/commit/64bbcf5b1575e88ead4e5fd58d8ee210a815aad6).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Dexe |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

