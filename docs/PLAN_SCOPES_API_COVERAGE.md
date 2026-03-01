# Plan: Complete Databricks Secret Scopes API Coverage

## Goal

Implement and verify full support for all Workspace Secret Scopes endpoints from Databricks API docs, with no omissions.

Reference:
- Databricks Workspace API Scopes: https://docs.databricks.com/api/workspace/api/scopes
- Secret API index: https://docs.databricks.com/api/workspace/secrets/listscopes

## Scope Coverage Matrix (Must Be Complete)

### Secret Scope Endpoints

- [ ] Create scope (`/api/2.0/secrets/scopes/create`)
- [ ] Delete scope (`/api/2.0/secrets/scopes/delete`)
- [ ] List scopes (`/api/2.0/secrets/scopes/list`)

### Secret Endpoints

- [ ] Put secret (`/api/2.0/secrets/put`)
- [ ] Delete secret (`/api/2.0/secrets/delete`)
- [ ] List secrets (`/api/2.0/secrets/list`)
- [ ] Get secret (`/api/2.0/secrets/get`)*

### ACL Endpoints

- [ ] Put ACL (`/api/2.0/secrets/acls/put`)
- [ ] Delete ACL (`/api/2.0/secrets/acls/delete`)
- [ ] List ACLs (`/api/2.0/secrets/acls/list`)
- [ ] Get ACL (`/api/2.0/secrets/acls/get`)

*If Databricks behavior differs by cloud/workspace policy, document exact behavior and keep wrapper semantics aligned.

## Delivery Phases

### Phase 1 - API Wrapper Completion

1. Add missing workspace client methods for all uncovered scope/secret/acl endpoints.
2. Add consistent input validation (scope, key, principal, permission level, etc.).
3. Ensure endpoint catalog/constants include every route.

### Phase 2 - Test Completion

1. Add unit tests for every new wrapper:
   - request path
   - HTTP method
   - payload/params shape
   - validation failures
2. Add negative coverage for empty/malformed identifiers.
3. Add compatibility assertions through `rehla_dbx_tools` namespace.

### Phase 3 - Docs + Examples

1. Update `README.md` and `docs/USAGE.md` with complete scopes examples.
2. Add one practical AWS Databricks example per endpoint family:
   - scope lifecycle
   - secret lifecycle
   - ACL lifecycle
3. Include required permissions and expected response patterns.

### Phase 4 - Non-Destructive Validation

1. Validate read-only list/get operations against live workspace:
   - list scopes
   - list secrets
   - list/get ACL
2. Keep destructive operations opt-in and explicitly documented when run.

## Exit Criteria

- [ ] 100% endpoint coverage from Databricks Secret API index
- [ ] All tests passing
- [ ] Docs updated with examples for each endpoint family
- [ ] Live non-destructive validation evidence recorded in cycle log
- [ ] Release published with changelog entry referencing complete scope coverage
