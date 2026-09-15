---
# Core Classification
protocol: Securitize Dstoken Rebasing
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64389
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
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
finders_count: 3
finders:
  - Stalin
  - Dacian
  - Jorge
---

## Vulnerability Title

Token value locks done as part of issuance restrict subsequently transferred unlocked tokens after negative rebasing

### Overview


The bug report explains that when a token is issued, there are two types of locks that can be put in place: share value based lock and token value based lock. However, there is a problem when negative rebasing occurs and an investor transfers unlocked tokens to another investor. The token value lock from the original issuance restricts the transfer of the unlocked tokens. A proof of concept is provided to show this problem and a recommended solution is to convert the lock system to store all lock amounts in shares rather than tokens. The issue has been acknowledged and can be managed through operational procedures.

### Original Finding Content

**Description:** When a token issuance occurs, as part of that token issuance two types of locks can be enacted:
* share value based lock via:
```solidity
TokenIssuer::issueTokens
-- DSToken::issueTokensWithMultipleLocks
---- TokenLibrary::issueTokensCustom
------ ComplianceService::validateIssuance
-------- ComplianceServiceRegulated::recordIssuance -> createIssuanceInformation
```
* token value based lock via:
```solidity
TokenIssuer::issueTokens
-- DSToken::issueTokensWithMultipleLocks
---- TokenLibrary::issueTokensCustom
------ InvestorLockManager::addManualLockRecord -> createLock -> createLockForInvestor
```

**Impact:** In a scenario where:
* Investor1 has a token issuance for 1000 tokens with both shared-base and token-value based locks for that issuance
* Negative rebasing occurs
* Investor2 transfers 1000 unlocked tokens to Investor1

The token value lock from Investor1's original token issuance will restrict the transfer of the unlocked tokens which Investor2 subsequently transferred to Investor1.

**Proof of Concept:** Add PoC to `test/token-issuer.test.ts`:
```typescript
  it('Token value locks done as part of issuance restrict subsequently transferred tokens after negative rebasing', async function() {
    const [ owner, investor1, investor2 ] = await hre.ethers.getSigners();
    const { dsToken, tokenIssuer, lockManager, rebasingProvider, registryService } = await loadFixture(deployDSTokenRegulated);

    // Register investors
    await registryService.registerInvestor('INVESTOR1', '');
    await registryService.setCountry('INVESTOR1', 'US');
    await registryService.addWallet(investor1.address, 'INVESTOR1');

    await registryService.registerInvestor('INVESTOR2', '');
    await registryService.setCountry('INVESTOR2', 'US');
    await registryService.addWallet(investor2.address, 'INVESTOR2');

    const currentTime = await time.latest();
    const lockRelease = currentTime + 100000;

    // Issue 1000 tokens to Investor1 with 1000 manually locked
    await tokenIssuer.issueTokens(
      'INVESTOR1',
      investor1.address,
      [ 1000, 1 ],
      '',
      [ 1000 ], // Lock ALL tokens
      [ lockRelease ],
      'INVESTOR1',
      'US',
      [0, 0, 0],
      [0, 0, 0]
    );

    // Issue 2000 tokens to Investor2 (no locks)
    await tokenIssuer.issueTokens(
      'INVESTOR2',
      investor2.address,
      [ 2000, 1 ],
      '',
      [],
      [],
      'INVESTOR2',
      'US',
      [0, 0, 0],
      [0, 0, 0]
    );

    // Verify initial state
    expect(await dsToken.balanceOf(investor1.address)).to.equal(1000);
    expect(await lockManager.getTransferableTokens(investor1.address, currentTime)).to.equal(0);

    // Get current multiplier and halve it
    const currentMultiplier = await rebasingProvider.multiplier();
    const halfMultiplier = currentMultiplier / BigInt(2);
    await rebasingProvider.setMultiplier(halfMultiplier);

    // After rebasing, Investor1 has 500 tokens but 1000 still locked
    expect(await dsToken.balanceOf(investor1.address)).to.equal(500);
    const transferableAfterRebasing = await lockManager.getTransferableTokens(investor1.address, currentTime);
    expect(transferableAfterRebasing).to.equal(0); // Over-locked

    // Investor2 transfers 1000 tokens to Investor1
    await dsToken.connect(investor2).transfer(investor1.address, 1000);

    // Final state
    const finalBalance = await dsToken.balanceOf(investor1.address);
    const finalTransferable = await lockManager.getTransferableTokens(investor1.address, currentTime);

    expect(finalBalance).to.equal(1500); // 500 from rebasing + 1000 transfer

    // Investor1 has 500 tokens from their own issuance and 1000 tokens
    // they received as a transfer with no associated lock
    // But the token value lock placed as part of their original issuance
    // affects subsequent transfers which had no locks attached
    //
    // Unlocked tokens received via transfer from Investor2 are partially
    // locked by Investor1's token-value based lock from Investor1's original
    // token issuance
    expect(finalTransferable).to.equal(500);
  });
```

**Recommended Mitigation:** Convert the lock system in `InvestorLockManager` and `LockManager` to store all lock amounts in shares rather than tokens. Alternatively the issue can simply be acknowledged to accept the current behavior.

**Securitize:** Acknowledged; locks are always accounted for in tokens, and yes, for a negative rebasing scenario that could happen. But could also be managed by operational procedures.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Dstoken Rebasing |
| Report Date | N/A |
| Finders | Stalin, Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

