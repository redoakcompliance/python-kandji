def test_list_ade_integrations(client):
    res = client.list_ade_integrations()
    assert type(res['results']) == list
    assert res != {'response': {'status': 400}}


def test_list_ade_devices(client, ade_token_id):
    res = client.list_ade_devices(ade_token_id)
    assert type(res['results']) == list
    assert res != {'response': {'status': 404}}


def test_get_ade_integration(client, ade_token_id):
    res = client.get_ade_integration(ade_token_id)
    assert res.get('id')
    assert res != {'response': {'status': 404}}


def test_get_ade_public_key(client):
    res = client.get_ade_public_key()
    assert type(res) == str
