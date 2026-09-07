# TDD in Python (pytest + FastAPI)

Local addendum — the disciplines in [SKILL.md](SKILL.md), [tests.md](tests.md), and
[mocking.md](mocking.md) are language-neutral; the examples there are TypeScript. This
file restates them in the idiom of a `uv` / pytest / FastAPI project so the patterns
map without translation. When the two disagree on *syntax*, follow this file; the
*discipline* is identical.

## Running the loop

- Run tests with `uv run pytest` (never bare `pytest`/`python -m` — this project is
  `uv`-managed). Prefer the project's own entrypoint when one exists (`make ci`,
  `make test`) so you run tests the way CI does — hermetic, clean-env, not sourcing
  `.env`.
- Tighten the loop the same way: `-x` (stop on first failure), `-k <expr>` to narrow
  to one seam, `--lf` (last-failed) while iterating. A 2-second targeted run beats a
  full suite on every red→green cycle.

## What a good test is — pytest form

Test observable behavior through the public interface, not internals. `expect().toBe()`
becomes a plain `assert`.

```python
# GOOD — tests observable behavior through the public surface
def test_user_can_checkout_with_valid_cart():
    cart = create_cart()
    cart.add(product)
    result = checkout(cart, payment_method)
    assert result.status == "confirmed"
```

Tautological test (the anti-pattern from tests.md), Python form — the expected value is
recomputed the way the code computes it, so it can never disagree:

```python
# BAD — expected value restates the implementation
def test_calculate_total():
    items = [{"price": 10}, {"price": 5}]
    expected = sum(i["price"] for i in items)
    assert calculate_total(items) == expected

# GOOD — expected value is an independent, known literal
def test_calculate_total():
    assert calculate_total([{"price": 10}, {"price": 5}]) == 15
```

Verify through the interface, not a side channel — don't reach into Postgres to check a
write; retrieve through the same public API:

```python
# BAD — bypasses the interface to verify via the DB
def test_create_user_saves_to_db(db):
    create_user(name="Alice")
    row = db.execute(text("SELECT * FROM users WHERE name = :n"), {"n": "Alice"}).first()
    assert row is not None

# GOOD — verifies through the interface
def test_create_user_makes_user_retrievable():
    user = create_user(name="Alice")
    assert get_user(user.id).name == "Alice"
```

## Seams in a FastAPI service

The public boundaries you test at, cheapest to most integrated:

- **A pure function / service method** — call it directly with plain inputs.
- **A route via `TestClient`/`httpx.AsyncClient`** — `client.post("/api/v1/assessment", json=...)`
  then assert on status + body. This is the seam that matches how the app is actually
  used, and it survives internal refactors. Prefer it for behavior that spans request →
  scoring → response.
- **The DB layer** — use a real test database or a transaction rolled back per test
  (fixture), not a mock of the session. Matches the "prefer a test DB over mocking the
  database" rule in mocking.md.

As in SKILL.md: **agree the seams up front**. Route-level + a few pure-function tests on
the scoring logic usually covers the critical paths; don't unit-test every helper.

## Mocking — Python form

Same rule: mock only at **system boundaries** (external APIs, time, randomness),
never your own collaborators.

- **Dependency injection** is even cleaner in FastAPI — use `app.dependency_overrides`
  to swap a boundary dependency in tests instead of patching globals. For plain
  functions, pass the client in as a parameter (exactly the DI example in mocking.md).
- **Patching a boundary** when DI isn't wired: `monkeypatch.setattr(...)` or
  `unittest.mock.patch` at the boundary — e.g. the Resend email client or an outbound
  `httpx` call — not at an internal function.
- **Time / randomness**: `freezegun` or inject a clock; seed with a fixed value. Same
  intent as the TS "mock time/randomness".
- The TS "SDK-style interface over a generic fetcher" advice maps to: give each external
  operation its own typed function (Pydantic models for the shapes) rather than one
  generic `request()` — each is independently patchable and its response shape is
  explicit.

## Idiom cheat-sheet

| tests.md / mocking.md (TS) | Python equivalent |
|---|---|
| `test("...", () => {})` | `def test_...():` |
| `expect(x).toBe(y)` | `assert x == y` |
| `expect(x).toEqual(y)` | `assert x == y` (or `== ` on the model/dict) |
| `jest.mock(mod)` / `jest.fn()` | `monkeypatch.setattr` / `unittest.mock.patch` / `MagicMock` |
| dependency injection via arg | function param **or** FastAPI `dependency_overrides` |
| test DB over mocking the DB | transaction-rollback fixture or a disposable test DB |
| "type safety per endpoint" | Pydantic request/response models per route |
| `pnpm run test` | `uv run pytest` (or `make ci`) |
