# Production verification
- Live: https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/
- Verified deployment `15dbfbb3-e383-4634-bb78-a14212797772`, R2 Worker version `028d3ad6-6f07-4345-96ac-cd354905fca5` at 100% traffic.
- Signed-out/cache-busted public root and four companion files matched the approved release byte-for-byte. The public [deployment fingerprint](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/deployment.json) has bundle SHA256 `32402e26323e67e2c1d3a696a6567275e49de5da4fde99a57fb79d444fd5ce89`.
- R2 desktop browser interaction checks include marker and tab selection, metric changes, and chart selection retaining keyboard focus. Mobile viewport was not independently tested. External GitHub Workers Builds checks remain separate; the worker was deployed using its existing confirmed version flow.
- No account, permission, credential, production binding, or Mac worktree edits. Previous known production version was `d357866c-f76c-431b-9e68-26ac6d2a3d87`; no rollback performed.
- Live website is not an official NASA submission receipt and is separate from the short Demo media requirement.
