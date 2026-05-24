# PSR Article Mapping

> A working mapping of the Payment Services Regulation obligations to product capabilities, owning teams, and the specific decisions a risk engine must make under each.

---

## Reading this document

This mapping is intended as a **product working artefact**, not a legal interpretation. For each obligation, it captures:

- **The regulatory obligation** — what PSR requires.
- **The product capability required** — what has to exist in the platform.
- **The owning team (typical org)** — where the work usually lives today.
- **The decision the engine has to make** — what the runtime system must evaluate.
- **The liability if missed** — the cost of getting this wrong under PSR.

Article numbering refers to the Council of the EU final compromise texts published 23 April 2026 (ST-8221-2026-INIT for PSR, ST-8222-2026-INIT for PSD3). Final numbering may shift upon Official Journal publication.

---

## Core obligations mapping

### Verification of Payee (PSR Art. 50, 57)

| Dimension | Detail |
|---|---|
| **Obligation** | PSPs must verify that the payee's name matches the unique identifier (e.g. IBAN) before executing a credit transfer, and notify the payer of any mismatch. |
| **Product capability** | Real-time name/IBAN matching service, mismatch notification flow, payer override capture, decision logging. |
| **Owning team** | Acquiring + Risk |
| **Engine decision** | Given a VoP result (`match` / `close_match` / `mismatch`), select between `approve`, `vop_warn`, `step_up`, or `block`. |
| **Liability if missed** | If the PSP did not apply VoP correctly and fraud follows, the PSP absorbs the loss. Article 57 grants a longer implementation window (27 months for some rails) but the liability is unavoidable. |

### Real-time transaction monitoring

| Dimension | Detail |
|---|---|
| **Obligation** | PSPs must monitor transactions in real time, applying appropriate fraud prevention mechanisms. Failure to do so is directly linked to refund outcomes. |
| **Product capability** | Multi-signal risk scoring service operating in the authorisation latency budget; behavioural, payee, and contextual features. |
| **Owning team** | Risk + Fraud |
| **Engine decision** | Compute `P(fraud)` per transaction and feed it into the action selection. |
| **Liability if missed** | Failure to monitor → refund obligation when fraud occurs. The PSP cannot argue lack of capability as a defence. |

### Environmental and device intelligence

| Dimension | Detail |
|---|---|
| **Obligation** | Monitoring must include information about the environmental and behavioural characteristics of the payer — notably presence of malware, remote-access tools (AnyDesk, TeamViewer, etc.), and ongoing phone calls during a payment session. |
| **Product capability** | Device intelligence SDK or partnership; signal ingestion into the risk scorer. |
| **Owning team** | Fraud + Mobile/Web Engineering |
| **Engine decision** | Adjust `P(fraud)` based on environmental signals. A transaction during an active TeamViewer session combined with new payee is a strong block candidate. |
| **Liability if missed** | A reimbursement claim where environmental signals would have surfaced the fraud, but were not captured, is unlikely to be defensible. |

### Right and obligation to block suspicious transactions

| Dimension | Detail |
|---|---|
| **Obligation** | PSPs have the right and the obligation to block or delay a transaction where their systems detect strong evidence of fraud in progress. |
| **Product capability** | Decision engine with `block` as a first-class action, supported by a customer-facing communication flow and an audit log. |
| **Owning team** | Risk + Customer Operations |
| **Engine decision** | Select `block` over `approve` or `step_up` when expected liability cost favours it. |
| **Liability if missed** | The PSP that approved a transaction it should have blocked absorbs the loss. Conversely, blocking legitimate transactions excessively drives conversion and merchant churn — the engine must optimise across both. |

### Refund obligations linked to monitoring failure (PSR refund framework)

| Dimension | Detail |
|---|---|
| **Obligation** | Refund obligations for unauthorised transactions are tightened, with stricter deadlines (end of next business day for the unrestricted refund) and broader scope. Failure to demonstrate appropriate monitoring weakens the PSP's defence. |
| **Product capability** | Decision logging that captures the full feature vector, model version, rule weights, alternative actions, and chosen action for every transaction — retrievable months later. |
| **Owning team** | Risk + Legal + Data Platform |
| **Engine decision** | For every action, write a reconstructable audit record. |
| **Liability if missed** | Inability to demonstrate a reasoned decision in dispute = loss of dispute. |

### APP fraud reimbursement framework

| Dimension | Detail |
|---|---|
| **Obligation** | Where a payer was misled by a fraudster into authorising a payment (Authorised Push Payment fraud), the PSP can be held liable for reimbursement if it failed to meet expected detection standards. Modelled on the UK Contingent Reimbursement Model. |
| **Product capability** | Impersonation pattern detection, payee reputation signals, behavioural anomaly detection on authorised transactions. |
| **Owning team** | Fraud + Customer Operations |
| **Engine decision** | Identify high-APP-risk patterns even on payer-authorised transactions; trigger friction or block accordingly. |
| **Liability if missed** | Direct reimbursement to the victim, with the PSP unable to argue the transaction was "authorised" as a defence. |

### PSP impersonation fraud

| Dimension | Detail |
|---|---|
| **Obligation** | If a fraudster impersonates the PSP (e.g. spoofed bank caller ID, fake bank SMS) and the customer reports the fraud promptly, the PSP must reimburse — even though the payment was technically authorised. |
| **Product capability** | Detection of session anomalies that correlate with impersonation patterns; out-of-band confirmation flows; cross-channel signal correlation. |
| **Owning team** | Fraud + Customer Communications |
| **Engine decision** | Elevate `P(fraud)` on transactions correlated with known impersonation patterns (recent inbound call, recent SMS-driven session, unusual payee). |
| **Liability if missed** | Direct reimbursement. This is the obligation most likely to drive significant unexpected losses in the first 12 months of application. |

### Cross-ecosystem liability (telecoms, platforms)

| Dimension | Detail |
|---|---|
| **Obligation** | Payment firms reimbursing fraud victims may pursue platforms (telecoms, social media) where the fraud was enabled — for example via number spoofing or fraudulent advertising. |
| **Product capability** | Evidence chain capture: which channel introduced the fraud, what content was involved, when the platform was notified. |
| **Owning team** | Legal + Risk + Data Platform |
| **Engine decision** | Tag transactions with the inferred fraud channel where possible, to support downstream recovery claims. |
| **Liability if missed** | Lost recovery — the PSP absorbs costs that could have been recovered from the ecosystem actor that enabled the fraud. |

---

## Cross-cutting implications

Three patterns emerge from the article-by-article mapping:

**1. Most obligations have a runtime decision component.** PSR is not satisfied by policy documents and quarterly reviews. The engine must make defensible, logged decisions in milliseconds.

**2. Most obligations cross domain boundaries.** VoP straddles Acquiring and Risk. APP fraud straddles Fraud and Customer Operations. Decision logging straddles Risk, Legal, and Data Platform. Domain-siloed roadmaps will produce gaps.

**3. The decision log is the single most reused capability.** Almost every obligation requires the ability to reconstruct why an action was taken. Building this once, well, is leverage. Building it per-domain produces both duplication and gaps.

A Group PM owning the PSD3/PSR product response should expect to spend significant political capital on cross-domain coordination — and significant engineering investment on a unified decision logging substrate.

---

## Status and revision

This mapping reflects the Council of the EU final compromise texts of 23 April 2026. It will be revised as:

- The Official Journal publishes the consolidated texts (expected Q2 2026, possibly Q3).
- The European Banking Authority issues Level 2 and Level 3 technical standards.
- National competent authorities publish implementation guidance.

*Karim Ouriachi — last revised May 2026.*
