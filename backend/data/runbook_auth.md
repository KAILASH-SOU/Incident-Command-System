# Auth Service Outage Runbook

## Overview
If the auth-service experiences high latency or 5xx errors, it might be due to a Redis cache failure or DB connection exhaustion.

## Mitigation Steps
1. Check Redis cluster health.
2. Verify connection pooling limits on the user-db.
3. Restart auth-service pods.
