from databricks_api.response import normalize_json, to_pandas_df


def test_normalize_json_handles_nested_list_payload():
    payload = {"items": [{"id": 1, "meta": {"name": "a"}}, {"id": 2, "meta": {"name": "b"}}]}
    rows = normalize_json(payload)
    assert len(rows) == 2
    assert rows[0]["meta.name"] == "a"


def test_to_pandas_df_scalar():
    df = to_pandas_df(42)
    assert list(df.columns) == ["value"]
    assert df.iloc[0]["value"] == 42


def test_normalize_json_handles_runs_payload_key():
    payload = {"runs": [{"run_id": 1001}, {"run_id": 1002}], "has_more": False}
    rows = normalize_json(payload)
    assert len(rows) == 2
    assert rows[1]["run_id"] == 1002


def test_normalize_json_handles_nested_result_items_payload():
    payload = {"result": {"items": [{"id": "a-1"}, {"id": "a-2"}]}, "request_id": "req-1"}
    rows = normalize_json(payload)
    assert len(rows) == 2
    assert rows[0]["id"] == "a-1"
