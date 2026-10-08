# AI service (AWS)

The NetPulse model runs in the **NetPulse AI service** on Amazon Web Services (region *Asia Pacific – Mumbai*, `ap-south-1`). The desktop app, the CLI and the service all talk to it over HTTPS.

```
NetPulse on your computer
   │  POST /v1/predict  (HTTPS, Authorization: Bearer <your access key>)
   ▼
API Gateway (HTTPS) ─► Lambda function (model server) ─► verified model bundle (model v2)
                         │                                 (checksums + schema checked before use)
                         └─ access keys stored only as SHA-256 hashes
```

## What the service does
- **Checks the request** against the frozen feature schema 1.0.0: exactly 62 features, valid ranges, the same rules the training data passed.
- **Runs the model** in production (v2, XGBoost) with its own evaluated decision policy, so the service makes the same decisions that were tested.
- **Answers** with, for each flow:
    - a label
    - a confidence
    - per-class probabilities
    - a risk level

  plus a batch risk score.
- **Never invents an answer.** If no verified model is loaded, it returns `503 model_unavailable`, and NetPulse shows *"AI service unavailable"*.

## The public API
The client only needs one stable endpoint. New models can be deployed behind it without updating the app.

| Endpoint | Auth | Purpose |
|---|---|---|
| `POST /v1/predict` | access key | Verdicts for 1–1,000 flows |
| `GET /v1/model` | access key | Active model: name, version, classes, schema, quality-gate result |
| `GET /v1/health` | none | Is a verified model loaded? (`200` ok, `503` degraded) |

Service address: `https://r223uzh3ad.execute-api.ap-south-1.amazonaws.com`

```json title="Request (shortened)"
{ "schema_version": "1.0.0", "agent_id": "my-laptop",
  "flows": [ { "flow_ref": "f5667355ba3494-37710",
               "features": { "Dst Port": 8080, "Protocol": 6, "Flow Duration": 1500.0, "...": 0 } } ] }
```

```json title="Response (shortened)"
{ "model_version": "2", "schema_version": "1.0.0",
  "predictions": [ { "flow_ref": "f5667355ba3494-37710", "label": "Bot", "confidence": 0.99,
                     "probabilities": { "Benign": 0.01, "Bot": 0.99, "...": 0.0 }, "risk": "critical" } ],
  "risk_score": 99, "severity": "critical", "timestamp": "2026-10-08T13:20:30+00:00" }
```

Errors share one shape, `{"error": "<code>", "detail": …, "request_id": "…"}`:

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_request`, `invalid_features`, `feature_contract_violation` | The request does not match the schema |
| 401 | `unauthorized` | Missing or wrong access key |
| 409 | `unsupported_schema_version` | Client and service use different feature schemas |
| 413 | `too_many_flows`, `request_too_large` | Batch over 1,000 flows or 4 MB |
| 429 | `rate_limited` | Too many requests for this key |
| 503 | `model_unavailable`, `inference_timeout` | No verified model, or inference too slow |

## Risk levels
Risk is a documented rule, not a second model:
- **Per-flow risk** = impact weight of the family × confidence.
- **Levels:** `low` < 0.2 ≤ `medium` < 0.5 ≤ `high` < 0.8 ≤ `critical`.
- **Batch `risk_score`** = 100 × the highest flow risk in the batch.

NetPulse on your computer then aggregates over the last 5 minutes.

## The model

| | Model v2 (in production) |
|---|---|
| Algorithm | XGBoost (gradient-boosted trees) |
| Training data | CSE-CIC-IDS2018, 7 families |
| Macro-F1 (held-out test split) | 0.867 |
| Bot recall | 0.997 |
| False alarms on benign traffic | 0.44 % |
| Report-only families | WebAttack, Infiltration (too few or too ambiguous samples to gate on) |

The previous model (v1) is kept as a fallback. A model is promoted only after it passes the quality gate, and the test split is evaluated once per model.

## How NetPulse protects you from bad answers
The client accepts a verdict only if the answer:
- uses the same feature schema
- names a model version
- has **exactly one prediction per flow sent, in the same order, for the same flow reference**
- contains only possible values (confidence and probabilities between 0 and 1, a known risk level, risk score ≤ 100)

Anything else, whether truncated, reordered or tampered with, is treated like no answer. The flows stay queued and **no verdict is stored**. The connection itself is HTTPS, so answers cannot be changed in transit without breaking TLS.

## Access keys
- Access is **invite-only**: each person (or computer) gets a personal key, `np_…`.
- The service stores only a **SHA-256 hash** of each key and compares it in constant time. Without any configured keys it refuses everything (fail-closed).
- Keys are never part of the installer and never written into `netpulse.toml`. A key can be revoked on its own without affecting anyone else.

## Availability and cost
The service is serverless. It scales to zero when idle, and a cold start takes a few seconds; NetPulse retries and queues meanwhile. While the service is unreachable, NetPulse keeps up to 50,000 flows and checks them when it is back.
