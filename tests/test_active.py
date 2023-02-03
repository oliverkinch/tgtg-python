from urllib.parse import urljoin

import pytest
import responses

from tgtg import ACTIVE_ORDER_ENDPOINT, BASE_URL, INACTIVE_ORDER_ENDPOINT, TgtgClient
from tgtg.exceptions import TgtgAPIError

from .constants import tgtg_client_fake_tokens


def test_get_active_success(refresh_tokens_response):
    responses.add(
        responses.POST,
        urljoin(BASE_URL, ACTIVE_ORDER_ENDPOINT),
        json={"orders": []},
        status=200,
        headers={"set-cookie": "session_id=12345; a=b; c=d"},
    )
    client = TgtgClient(**tgtg_client_fake_tokens)
    assert client.get_active()["orders"] == []
    assert (
        len(
            [
                call
                for call in responses.calls
                if ACTIVE_ORDER_ENDPOINT in call.request.url
            ]
        )
        == 1
    )


def test_get_active_fail(refresh_tokens_response):
    responses.add(
        responses.POST, urljoin(BASE_URL, ACTIVE_ORDER_ENDPOINT), json={}, status=400
    )
    client = TgtgClient(**tgtg_client_fake_tokens)
    with pytest.raises(TgtgAPIError):
        client.get_active()


def test_get_inactive_success(refresh_tokens_response):
    responses.add(
        responses.POST,
        urljoin(BASE_URL, INACTIVE_ORDER_ENDPOINT),
        json={"orders": []},
        status=200,
    )
    client = TgtgClient(**tgtg_client_fake_tokens)
    assert client.get_inactive()["orders"] == []
    assert (
        len(
            [
                call
                for call in responses.calls
                if INACTIVE_ORDER_ENDPOINT in call.request.url
            ]
        )
        == 1
    )


def test_get_inactive_fail(refresh_tokens_response):
    responses.add(
        responses.POST, urljoin(BASE_URL, INACTIVE_ORDER_ENDPOINT), json={}, status=400
    )
    client = TgtgClient(**tgtg_client_fake_tokens)
    with pytest.raises(TgtgAPIError):
        client.get_inactive()
