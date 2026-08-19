# v1.1 baseline vs assurance candidate — external fixture A/B

This experiment moves beyond self-hosted tasks in the Over the Luna repository. GitHub Actions generated two small standalone Python projects at runtime, then ran the same task against fixed baseline and assurance-candidate plugin revisions.

Hidden tests did not exist until after Copilot completed, so neither Main nor Reviewer could inspect them. All hidden assertions corresponded to acceptance criteria explicitly stated in the user prompt; they were not secret requirements designed to make review win.

Fixed plugin revisions:

- baseline: `de1f63057c57e06764a359ebfe148a3e031dcf19`
- assurance candidate: `173590bc0645188d35a19b2945a247c5721f5902`

Both used GPT-5.6 Luna only and zero premium requests.

## Fixture A — HTTP Retry-After

Task: preserve non-negative delta-seconds behavior and add HTTP-date support, timezone validation, ceiling-rounded future delay, past-date clamping, invalid handling, and focused tests.

Hidden checks:

- fractional remaining time rounds up;
- past HTTP date returns zero;
- timezone-less parsed date is rejected.

### Baseline

- `Mode: SIMPLE — direct Luna`
- Reviewer: **0**
- model calls: 5
- tool calls: 7
- OTel input/output: 69,845 / 1,347
- session nanoAIU: 648,624,000
- observed event span: about 20.8 s
- hidden tests: **3/3 pass**.

### Assurance candidate

- `Mode: SIMPLE — direct Luna`
- `Assurance: REVIEW — Luna Reviewer`
- actual Reviewer: **1**
- model calls: 9
- tool calls: 13
- OTel input/output: 121,606 / 2,609
- Main input/output: 117,494 / 1,539
- Reviewer input/output: 4,112 / 1,070
- session nanoAIU: 980,699,000
- observed event span: about 39.2 s
- hidden tests: **3/3 pass**.

Reviewer found one concrete test-coverage gap: the implementation correctly handled the explicitly required `None` input, but the visible tests did not assert it. Main accepted the finding, added the assertion, and reran focused tests.

Outcome:

- hidden behavioral correctness: tie;
- visible regression coverage: candidate stronger;
- nanoAIU: candidate about **51% higher**;
- observed event-span latency: candidate about **89% higher**.

## Fixture B — TTL cache update/eviction

Task: fix `TTLCache.set` so updates refresh value/expiry/MRU without evicting another live key, expired entries are purged before capacity eviction, and any remaining eviction chooses exactly the live LRU entry.

Hidden checks:

- update at capacity does not evict another live key;
- expired entries are removed before a live LRU is evicted.

### Baseline

- `Mode: SIMPLE — direct Luna`
- Reviewer: **0**
- model calls: 7
- tool calls: 9
- OTel input/output: 101,701 / 1,518
- session nanoAIU: 752,077,000
- observed event span: about 19.8 s
- hidden tests: **2/2 pass**.

### Assurance candidate

- `Mode: SIMPLE — direct Luna`
- `Assurance: REVIEW — Luna Reviewer`
- actual Reviewer: **1**
- model calls: 9
- tool calls: 13
- OTel input/output: 126,841 / 2,881
- Main input/output: 122,217 / 2,016
- Reviewer input/output: 4,624 / 865
- session nanoAIU: 1,062,541,000
- observed event span: about 35.2 s
- hidden tests: **2/2 pass**.

Reviewer found one concrete coverage gap: the visible update regression proved value/MRU behavior but did not advance the clock to prove expiry refresh. Main accepted the finding and strengthened the test without changing the implementation.

Outcome:

- hidden behavioral correctness: tie;
- visible regression coverage: candidate stronger;
- nanoAIU: candidate about **41% higher**;
- observed event-span latency: candidate about **78% higher**.

## Cross-fixture interpretation

The external fixtures reinforce two conclusions at once.

### 1. The two-axis contract has strong runtime adherence

Both tasks remained SIMPLE. The candidate nevertheless invoked exactly one fresh Reviewer after mutation/validation, while baseline invoked none. This matches the intended separation of implementation routing from post-change assurance.

### 2. `REVIEW for every non-trivial mutation` is not yet economically justified

Baseline achieved 5/5 hidden behavioral assertions across the two fixtures without review. Candidate also achieved 5/5, while improving visible test coverage for two explicitly stated requirements.

The review was therefore not useless: it strengthened regression evidence. But in this small sample it did **not** convert a failing hidden behavior into a passing one, while total trajectory AIU and latency rose materially.

The cost increase is not primarily the raw Reviewer token count. The expensive unit is the entire follow-up trajectory:

> Reviewer call -> Main adjudication -> accepted test/repair -> revalidation

This suggests the next optimization target should be **review trajectory efficiency/precision**, not a rollback to a single routing axis and not a blind lowering of SIMPLE.

## Updated hypothesis

Keep the explicit Assurance decision because it solved the observed adherence problem and remains independently measurable.

Do not yet lock the policy to `all non-trivial mutations => REVIEW`.

The next candidate should test whether the same independent assurance value can be bought more cheaply, for example by making review **artifact-first and bounded**: give a fresh Reviewer the exact completed patch + acceptance criteria + validation evidence first, and use repository reads only when a concrete finding depends on unchanged context.

Compare that compact-review trajectory against the current integrated Reviewer on the same fixtures. Success means retaining useful verified findings while materially reducing added Main turns, Reviewer browsing, wall time, and AIU.
