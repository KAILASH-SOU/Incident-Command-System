# Post Mortem: DB Lock during Migration

## Issue
On 2023-11-12, a database migration caused table locks on `users`, leading to an auth-service outage.

## Root Cause
The migration script executed an `ALTER TABLE` which locked the table for 15 minutes.
