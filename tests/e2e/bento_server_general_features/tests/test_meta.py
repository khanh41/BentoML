# pylint: disable=redefined-outer-name
# type: ignore[no-untyped-def]

import pytest

from bentoml.testing.utils import async_request


@pytest.mark.asyncio
async def test_api_server_meta(host: str) -> None:
    status, _, _ = await async_request("GET", f"http://{host}/")
    assert status == 200
    status, _, _ = await async_request("GET", f"http://{host}/healthz")
    assert status == 200
    status, _, _ = await async_request("GET", f"http://{host}/livez")
    assert status == 200
    status, _, _ = await async_request("GET", f"http://{host}/docs.json")
    assert status == 200
    status, _, _ = await async_request("GET", f"http://{host}/readyz")
    assert status == 200
    status, _, body = await async_request("GET", f"http://{host}/metrics")
    assert status == 200
    assert body


@pytest.mark.asyncio
async def test_cors(host: str, server_config_file: str) -> None:
    ORIGIN = "http://bentoml.ai"

    status, headers, body = await async_request(
        "OPTIONS",
        f"http://{host}/echo_json",
        headers={
            "Content-Type": "application/json",
            "Origin": ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    if server_config_file == "server_config_cors_enabled.yml":
        assert status == 200
    else:
        assert status == 405

    status, headers, body = await async_request(
        "POST",
        f"http://{host}/echo_json",
        headers={"Content-Type": "application/json", "Origin": ORIGIN},
        data='"hi"',
    )
    if server_config_file == "server_config_cors_enabled.yml":
        assert status == 200
        assert body == b'"hi"'
        assert headers["Access-Control-Allow-Origin"] in ("*", ORIGIN)
        assert "Content-Length" in headers.get("Access-Control-Expose-Headers", [])
        assert "Server" not in headers.get("Access-Control-Expect-Headers", [])
    else:
        assert status == 200
        assert headers.get("Access-Control-Allow-Origin") not in ("*", ORIGIN)
        assert "Content-Length" not in headers.get("Access-Control-Expose-Headers", [])


"""
@pytest.since_bentoml_version("0.11.0+0")
@pytest.mark.asyncio
async def test_customized_route(host):
    CUSTOM_ROUTE = "$~!@%^&*()_-+=[]\\|;:,./predict"

    def path_in_docs(response_body):
        d = json.loads(response_body.decode())
        return f"/{CUSTOM_ROUTE}" in d['paths']

    await async_request(
        "GET",
        f"http://{host}/docs.json",
        headers=(("Content-Type", "application/json"),),
        assert_data=path_in_docs,
    )

    await async_request(
        "POST",
        f"http://{host}/{CUSTOM_ROUTE}",
        headers=(("Content-Type", "application/json"),),
        data=json.dumps("hello"),
        assert_data=bytes('"hello"', 'ascii'),
    )


@pytest.mark.asyncio
async def test_customized_request_schema(host):
    def has_customized_schema(doc_bytes):
        json_str = doc_bytes.decode()
        return "field1" in json_str

    await async_request(
        "GET",
        f"http://{host}/docs.json",
        headers=(("Content-Type", "application/json"),),
        assert_data=has_customized_schema,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "metrics",
    [
        pytest.param(
            '_mb_request_duration_seconds_count',
            marks=pytest.mark.skipif(
                psutil.MACOS, reason="microbatch metrics is not shown in MacOS tests"
            ),
        ),
        pytest.param(
            '_mb_request_total',
            marks=pytest.mark.skipif(
                psutil.MACOS, reason="microbatch metrics is not shown in MacOS tests"
            ),
        ),
        '_request_duration_seconds_bucket',
    ],
)
async def test_api_server_metrics(host, metrics):
    await async_request(
        "POST", f"http://{host}/echo_json", data='"hi"',
    )

    await async_request(
        "GET",
        f"http://{host}/metrics",
        assert_status=200,
        assert_data=lambda d: metrics in d.decode(),
    )
"""