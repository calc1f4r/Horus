# Treehouse Finance

## Smart Contract

## Security Assessment

```
VERSION 1.
```
AUDIT DATES:

AUDITED BY:

```
March 24th to April 2nd, 2025
IllIllI
Mario Poneder
```

- Contents 1 Introduction
      - 1.1 About Zenith
      - 1.2 Disclaimer
      - 1.3 Risk Classification
   - 2 Executive Summary
      - 2.1 About Treehouse Finance
      - 2.2 Scope
      - 2.3 Audit Timeline
      - 2.4 Issues Found
   - 3 Findings Summary
   - 4 Findings
      - 4.1 Medium Risk
      - 4.2 Low Risk
      - 4.3 Informational


### 1

Introduction

#### 1.1 About Zenith

```
Zenith is an offering by Code4rena that provides consultative audits from the very best
security researchers in the space. We focus on crafting a tailored security team specifically
for the needs of your codebase.
```
```
Learn more about us athttps://code4rena.com/zenith.
```
#### 1.2 Disclaimer

```
This report reflects an analysis conducted within a defined scope and time frame, based on
provided materials and documentation. It does not encompass all possible vulnerabilities
and should not be considered exhaustive.
```
```
The review and accompanying report are presented on an "as-is" and "as-available" basis,
without any express or implied warranties.
```
```
Furthermore, this report neither endorses any specific project or team nor assures the
complete security of the project.
```
#### 1.3 Risk Classification

```
SEVERITY LEVEL IMPACT: HIGH IMPACT: MEDIUM IMPACT: LOW
```
```
Likelihood: High Critical High Medium
```
```
Likelihood: Medium High Medium Low
```
```
Likelihood: Low Medium Low Low
```

### 2 Executive Summary

#### 2.1 About Treehouse Finance

```
Treehouse is a decentralized application that introduces Treehouse Assets (tAssets) and
Decentralized Offered Rates (DOR), new primitives that enable fixed income products in
digital assets.
```
```
Users who deposit ETH or liquid staking tokens (LST) into the protocol receive tETH and
contribute to the convergence of fragmented on-chain ETH rates.
```
```
tETH also enhances the cryptoeconomic security of DOR, a consensus mechanism for
benchmark rate setting.
```
#### 2.2 Scope

```
The engagement involved a review of the following targets:
```
```
Target boring-vault-svm
```
```
Repository https://github.com/Veda-Labs/boring-vault-svm
```
```
Commit Hash ea1e9036856accfaaf2767835230547fb59530a
```
```
Files boring-onchain-queue/*
boring-vault-svm/*
```

#### 2.3 Audit Timeline

```
March 24, 2025 Audit start
```
```
April 2, 2025 Audit end
```
```
April 9, 2025 Draft Report published
```
#### 2.4 Issues Found

```
SEVERITY COUNT
```
```
Critical Risk 0
```
```
High Risk 0
```
```
Medium Risk 1
```
```
Low Risk 10
```
```
Informational 10
```
```
Total Issues 21
```

### 3 Findings Summary

```
ID Description Status
```
```
M-1 CPI digest restrictions can be circumvented using up-
gradeable programs
```
```
Resolved
```
```
L-1 Division before multiplication precision loss Resolved
```
```
L-2 Users cannot withdraw assets from vault if with-
draw_authority is not a queue
```
```
Acknowledged
```
```
L-3 First one to invoke permissionless initialization can set au-
thorities
```
```
Resolved
```
```
L-4 Share token mint not explicitly created using Token-2022 Resolved
```
```
L-5 Vault wind-downs may cause fees to become stuck if mul-
tiple sub-accounts are used
```
```
Acknowledged
```
```
L-6 Fee updates apply retroactively Acknowledged
```
```
L-7 Exchange rate volatility may affect fee compounding fre-
quency
```
```
Acknowledged
```
```
L-8 Unnecessary pause check when updating CPI digest ac-
counts
```
```
Resolved
```
```
L-9 update_cpi_digest() does not validate expected_size Resolved
```
```
L-10 validate_associated_token_accounts() should use Invali-
dAssociatedTokenAccount as the error code
```
```
Resolved
```
```
I-1 Limited usability of view_cpi_digest instruction Resolved
```
```
I-2 Use of outdated switchboard-on-demand library Resolved
```
```
I-3 Exchange rate does not reflect owed fees Acknowledged
```
```
I-4 Performance fees incentivize delayed exchange rate up-
dates
```
```
Acknowledged
```
```
I-5 Asset account not checked in update_asset_data instruc-
tion
```
```
Resolved
```

ID Description Status

I-6 Theupdate_cpi_digestinstructiondoesnotallowtoupdate
the CPI digest’s properties

```
Resolved
```
I-7 Base asset mint not checked in deploy instruction Resolved

I-8 Project relies on vulnerable crate dependencies Acknowledged

I-9 get_rate_in_quote() will not work with SOL as the quote as-
set

```
Resolved
```
I-10 Share token mint could benefit from associated metadata Resolved


### 4 Findings

#### 4.1 Medium Risk

```
A total of 1 medium risk findings were identified.
```
```
[M-1] CPI digest restrictions can be circumvented using
upgradeable programs
```
```
SEVERITY:Medium IMPACT:Low
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L289-L
- programs/boring-vault-svm/src/lib.rs#L845-L

Description:

```
The CPI digest verification mechanism is intended to whitelist specific operations on a
vault, e.g. transferring assets from the deposit sub-account to the withdrawal sub-account
in the simplest case.
```
```
This mechanism is based on the assumption that a whitelisted instruction's underlying
program is immutable. However, neither the vault'smanageinstruction nor its
update_cpi_digestinstruction verifies the program's immutability. Consequently, any CPI
digest restrictions could be bypassed by upgrading an initially genuine underlying program
after whitelisting, allowing potentially malicious operations on a vault.
```
Recommendations:

```
It is recommended to verify within theupdate_cpi_digestinstruction that the instruction's
program is owned by the non-upgradeable version of theBPFLoader, or has its upgrade
authority set toNone, or is any of Solana's built-in programs.
```
```
Treehouse: Resolved with@b0e92dbef81...by adding theIngestInstructionDataSize
operator.
```
```
Zenith:Verified
```

#### 4.2 Low Risk

A total of 10 low risk findings were identified.

[L-1] Division before multiplication precision loss

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L715-L
- programs/boring-vault-svm/src/utils/teller.rs#L310-L
- programs/boring-vault-svm/src/utils/teller.rs#L443-L

Description:

In the above instances, division before multiplication or unnecessary division by the inverse
is performed, leading to a potential precision loss.

Recommendations:

It is recommended to restructure the above instances such that multiplications are
performed before divisions and divisions by the inverse are replaced by straightforward
multiplications.

Treehouse: Resolved with@06db56c4705...

Zenith:Verified


[L-2] Users cannot withdraw assets from vault if
withdraw_authorityis not a queue

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Acknowledged LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L
- programs/boring-vault-svm/src/lib.rs#L1532-L

Description:

In the vault'swithdrawinstruction, thewithdraw_authority(if set) cannot withdraw assets
on behalf of a user, but has to own the shares itself, i.e. has to be the authority of the
user_sharestoken account.

This is designed to be used with theboring_onchain_queueprogram, where users transfer
their shares to thequeueon a withdrawal request. Thisqueueis configured as the
withdraw_authorityto facilitate the withdrawal.

However, thedeployas well as theset_withdraw_authorityinstructions impose no
restrictions on thewithdraw_authoritywhich leaves users unable to withdraw in case the
withdraw_authoritywas set to any authority different from the respectivequeueaccount of
theboring_onchain_queueprogram.

Please note that this issue does not persist in case of permissionless withdrawals where the
_withdraw_authority_ is set to the zero account.

Recommendations:

It is recommended to validate the givenwithdraw_authorityin thedeployand
set_withdraw_authorityinstructions to ensure that only the respectivequeueaccount of
theboring_onchain_queueprogram can be set as thewithdraw_authority.

Treehouse: Acknowledged. This is a possible configuration mistake an admin could make
when setting up a vault, but if they do make this mistake the correction is fairly easy, they
just need to change the withdraw authority.

Zenith:Acknowledged as a remediable configuration mistake.


[L-3] First one to invoke permissionless initialization can set

authorities

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-onchain-queue/src/lib.rs#L475-L
- programs/boring-vault-svm/src/lib.rs#L1172-L

Description:

The permissionless nature (nosignerrestriction) of theinitializeinstructions and their
respectiveInitializeaccount contexts allows the first caller after deployment to set the
authorityin the program configs.

Recommendations:

It is recommended to require co-signing of theinitializeinstructions using the programs'
keypairs, which should only be known to the deployer. This can be achieved by modifying
theInitializeaccount contexts as follows:

```
pubstructInitialize<'info> {
#[account(mut)]
pub signer: Signer<'info>,
```
```
#[account(address = crate/:ID)]
pub program: Signer<'info>
```
```
#[account(
init,
payer=signer,
space= 8 +std/:mem/:size_of/:<ProgramConfig>(),
seeds=[BASE_SEED_CONFIG],
bump,
)]
pub config: Account<'info, ProgramConfig>,
```

```
pub system_program: Program<'info, System>,
}
```
Treehouse: Resolved with@5680c49bb4...

Zenith:Verified.


[L-4] Share token mint not explicitly created using Token-

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L1210-L

Description:

The mint of the vault's share token (share_mint) is not explicitly created with the
Token-2022 program although the relateduser_sharesandqueue_sharesATAs are
explicitly handled using the Token-2022 program in all instances.

Recommendations:

It is recommended to adapt theshare_mintinitialization as follows:

```
/// The mint of the share token.
#[account(
init,
payer=signer,
mint/:token_program = token_program_2022,
mint/:decimals=base_asset.decimals,
mint/:authority=boring_vault_state.key(),
seeds=[BASE_SEED_SHARE_TOKEN, boring_vault_state.key().as_ref()],
bump,
)]
pub share_mint: InterfaceAccount<'info, Mint>,
```
```
pub token_program_2022: Program<'info, Token2022>,
```
Treehouse: Resolved with@01dd9c33dcb...

Zenith:Verified


[L-5] Vault wind-downs may cause fees to become stuck if

multiple sub-accounts are used

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Acknowledged LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L580-L

Description:

Fees are collected in _each_ sub-account PDA of each vault, but during calls to
claim_fees_in_base(), only one of the vault's sub-accounts can be specified as the source
ATA of the fees. If multiple sub-accounts have been used, it is likely that the fees will
likewise be distributed over multiple sub-accounts. When it comes time to claim the fees,
there may not be enough of the base asset present in a _single_ sub-account if the vault
has been wound down, and all users have redeemed their shares.

Recommendations:

Modifyclaim_fees_in_base()to take in an amount to claim, rather than requiring the
claiming of all fees.

Treehouse: Acknowleded.

Users are only benefitted from this, and really it comes down to mis-management on the
strategists part. Fees will be regularly collected so even if a vault is wound down and this
does happen, the loss to the strategist will be minimal compared to the fees they collected
overtime. With this in mind it is best to keep the code simpler, and the function signature
simpler so it is easier for strategists to collect fees.


[L-6] Fee updates apply retroactively

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Acknowledged LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L494-L

Description:

When an admin callsset_fees()the new fee rates are set immediately, without
checkpointing the fee compounding for the prior period. The next time the
exchange_rate_providercallsupdate_exchange_rate(), the new fee will apply to the
period of time since the last call toupdate_exchange_rate(), which may be a long time ago

Recommendations:

Modifyset_fees()to compound the fees at the current rate (as ifupdate_exchange_rate()
had been called with its previous value) prior to updating the fees. This may affect the
compounding rate, however.

Treehouse: Acknowledged.


[L-7] Exchange rate volatility may affect fee compounding

frequency

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Acknowledged LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L673-L

Description:

As a safety mechanism, if theexchange_rate_provider's update in too soon, or if the
change as compared to the prior value is too large or too small, the protocol is
automatically paused for manual inspection. When it is later unpaused, there is no code
that performs the protocol fee compounding that would have occurred had the protocol
not been paused. This means that if there are multiple such events in a row, the protocol
fee compounding will not match the predicted rate. Rather than using continuous
compounding, the protocol uses discrete compounding, so any changes in the frequency
of non-pausing calls toupdate_exchange_rate(), will cause the stated interest rate not to
match the publicly stated one.

Recommendations:

Document the expected compounding behavior during pauses and how this affects the
interest rate, along with the period minimums and high water mark

Treehouse: Acknowledged.


[L-8] Unnecessary pause check when updating CPI digest
accounts

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L

Description:

One of the constraints in theUpdateCpiDigestaccount struct causes requests made while
the vault is paused. If there is a market event that causes the exchange rate to change such
that the vault becomes paused, it may be advantageous to be able to create or disable CPI
digests while the market is still paused, to ensure that there is no automation that was
forgotten to be disabled, that may perform out-dated operations.

Recommendations:

Remove the constraint requiring that the vault is unpaused

Treehouse: Resolved with@d8fb374aaef...

Zenith:Verified.


[L-9]update_cpi_digest()does not validateexpected_size

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L283-L

Description:

The function documentation forupdate_cpi_digest()states that it does not validate that
the inputOperators hash to the right ID, presumably to save CUs. It does not comment on
whetherexpected_sizeis validated. Theapply_operators()function itself does acheck
against the maximum length, and it is a waste of transaction fees and CU for the check not
to be done inupdate_cpi_digest()instead

Recommendations:

Move the maximumexpected_sizevalidation fromapply_operators()to
update_cpi_digest(), or update the comment to reflect that it is not checked in
update_cpi_digest()

Treehouse: Resolved with@b0e92dbef81...

Zenith:Verified.


[L-10]validate_associated_token_accounts()should use

InvalidAssociatedTokenAccountas the error code

```
SEVERITY:Low IMPACT:Low
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-onchain-queue/src/utils/utils.rs#L74-L
- programs/boring-onchain-queue/src/utils/validate.rs#L15-L
- programs/boring-vault-svm/src/utils/teller.rs#L91-L

Description:

Thevalidate_associated_token_accounts()functions currently return an
InvalidTokenAccounterror code if the associated token account that the user provides
does not match the one expected, given the intended owner. If a user provides an ATA
owned by the right owner, but with the wrong token program, they'll get an
InvalidTokenAccounteven though they provided the correct token account.

Recommendations:

UseInvalidAssociatedTokenAccountfor the flagged cases instead, since the validation is
of the ATAs, not of the owners themselves, which are validated elsewhere.

Treehouse: Resolved with@9477732b718...

Zenith:Verified.


#### 4.3 Informational

A total of 10 informational findings were identified.

[I-1] Limited usability ofview_cpi_digestinstruction

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L1091-L

Description:

Theview_cpi_digestinstruction is intended to compute and return the expected digest for
a given instruction with the specified operators applied. However, in order to return the
desired CPI digest, the instruction already expects the correct hash data size to be passed.
This might become a usability limitation since theexpected_sizeis most likely still unknown
at this point.

Recommendations:

It is recommended to alter theview_cpi_digestinstruction such that it returns the CPI
digest as well as the hash data size.

Treehouse: Resolved with@b0e92dbef8...by removing the expected_size check.

Zenith:Verified.


[I-2] Use of outdatedswitchboard-on-demandlibrary

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/Cargo.toml#L25l

Description:

The protocol depends onv0.2.2of theswitchboard-on-demandlibrary although there
already is the substantially newerv0.3.5available.

Recommendations:

It is recommended to upgrade to a newer version of theswitchboard-on-demandlibrary, if
possible concerning compatibility.

Treehouse: Resolved with@15c9aa6c09...

Zenith:Verified.


[I-3] Exchange rate does not reflect owed fees

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Acknowledged LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L631-L786

Description:

The exchange rate effectively establishes a relation between a vault's shares and its
contained/withdrawable assets. On each exchange rate update, the owed fees (platform
and performance fees) are computed and can be claimed from a vault. This reduces the
amount of a vault's base assets, effectively reducing the exchange rate.

Recommendations:

It is recommended to ensure that a vault's owed fees are reflected in its current exchange
rate, or update the documentation accordingly in case they already are.

Treehouse: Acknowledged. If fees are being collected regularly, then the pending fees
should have a negligible impact on share price, but if for some reason fees are piling up
and the admin is not collecting it is expected the strategist will adjust the exchange rate
they provide to account for this. Acommenthas been added to call this out.


[I-4] Performance fees incentivize delayed exchange rate

updates

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Acknowledged LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L725-L750

Description:

A vault's performance fees are proportional to(new_exchange_rate - high_water_mark) *
share_supply, whereby thehigh_water_markis set tonew_exchange_rateevery time the
performance fees are calculated on invocation ofupdate_exchange_rate.

Assuming a growing share supply and an exchange rate provider who directly or indirectly
profits from the performance fees, they are incentivized to delay exchange rate updates to
apply(new_exchange_rate - high_water_mark)at the greatest possibleshare_supply.

Recommendations:

It is recommended to utilize the average share supply since the last performance
computation on exchange rate update for a fairer performance fee computation, i.e.
(curr_share_supply + prev_share_supply) / 2.

Treehouse: Acknowledged. It's more likely that the share supply decreases over time
leading to the opposite incentive.


[I-5] Asset account not checked inupdate_asset_data

instruction

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L1303-L1304

Description:

Theassetaccount of theupdate_asset_datainstruction is expected to be checked within
the instruction according to the comment in theUpdateAssetDatacontext. However, the
current implementation neglects to validate whether theassetis a zero account (native
SOL) or a SPL-Token / Token-2022 mint.

Recommendations:

It is recommended to implement the intended checks of theassetaccount.

Treehouse: Resolved with@2e92f1c4c0...

Zenith:Verified.


[I-6] Theupdate_cpi_digestinstruction does not allow to

update the CPI digest's properties

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L1564-L1574

Description:

Thecpi_digestaccount of theupdate_cpi_digestinstruction is created with Anchor's
initconstraint. Therefore, the CPI digest's properties such asoperatorsand
expected_sizecannot be updated.

Recommendations:

Typically, a change of theoperatorsandexpected_sizeleads to a change of the
cpi_digestitself, eliminating the need to update its properties. Therefore, it is
recommended to rename the instruction fromupdate_cpi_digestto
initialize_cpi_digest.

Treehouse: Resolved with@0761b9e205...

Zenith:Verified.


[I-7] Base asset mint not checked indeployinstruction

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L1221-L1222

Description:

Thebase_assetmint account of thedeployinstruction is expected to be checked within
the instruction according to the comment in theDeploycontext. However, the current
implementation neglects to perform further custom validation of thebase_assetmint, e.g.
potential whitelist checks.

Recommendations:

It is recommended to implement the intended check of thebase_assetmint or remove the
comment.

Treehouse: Resolved with@47c701a18b...

Zenith:Verified.


[I-8] Project relies on vulnerable crate dependencies

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Acknowledged LIKELIHOOD:Low
```
Target

- Cargo.lock

Description:

The following vulnerable create dependencies were identified throughcargo audit:

```
Crate: curve25519-dalek
Version: 3.2.1
Title: Timing variability in `curve25519-dalek`'s
`Scalar29/:sub`/`Scalar52/:sub`
Date: 2024-06-18
ID: RUSTSEC-2024-0344
URL: https://rustsec.org/advisories/RUSTSEC-2024-0344
Solution: Upgrade to /=4.1.3
```
```
Crate: ed25519-dalek
Version: 1.0.1
Title: Double Public Key Signing Function Oracle Attack on
`ed25519-dalek`
Date: 2022-06-11
ID: RUSTSEC-2022-0093
URL: https://rustsec.org/advisories/RUSTSEC-2022-0093
Solution: Upgrade to /=2
```
```
Crate: ring
Version: 0.17.8
Title: Some AES functions may panic when overflow checking is enabled.
Date: 2025-03-06
ID: RUSTSEC-2025-0009
URL: https://rustsec.org/advisories/RUSTSEC-2025-0009
Solution: Upgrade to /=0.17.12
```

Recommendations:

It is recommended to upgrade the affected dependencies if applicable and viable
concerning compatibility.

Treehouse: Acknowledged.


[I-9]get_rate_in_quote()will not work with SOL as the quote
asset

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L1847-L1848

Description:

Thedeposit_sol()instruction allows one to deposit native SOL to the vault, but there is no
way to check the exchange rate because theget_rate_in_quote()instruction requires a
Mintaccount, whereas the protocol uses the blank address (whose account is not owned
by either token program) as the SOL address. Since the protocol does not support
withdrawing SOL, the missing functionality inget_rate_in_quote()has no impact on the
protocol itself, but adding it may help others to integrate and simplify their calculations.

Recommendations:

Consider modifying the function to support the blank address

Treehouse: Documented the behaviour with thiscommit

Zenith:Verified.


[I-10] Share token mint could benefit from associated metadata

```
SEVERITY:Informational IMPACT:Informational
```
```
STATUS:Resolved LIKELIHOOD:Low
```
Target

- programs/boring-vault-svm/src/lib.rs#L1211-L1219

Description:

Although the mint of the vault's share token (share_mint) is intended to be created with the
Token-2022 program which supports extensions, no extensions are utilized.

Recommendations:

It is recommended to utilize themetadata_pointerextension to attachTokenMetadata
(name, symbol, URI, etc.) to the vault's share mint.

Treehouse: Resolved with@93a0b481112...and@83ecdb1ab57...

Zenith:Verified


