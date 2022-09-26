def test_get_device_commands(client, device_id):
    res = client.get_device_commands(id=device_id)
    assert type(res['commands']) == dict
    assert res != {'response': {'status': 404}}


def test_get_device_commands_not_found(client):
    res = client.get_device_commands(id="noid")
    assert res == {'response': {'status': 404}}
