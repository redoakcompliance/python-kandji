def test_get_device_bypasscode(client, device_id):
    res = client.get_device_bypasscode(id=device_id)
    assert type(res) == dict
    assert 'device_based_albc' in res
    assert 'device_based_albc' in res


def test_get_device_filevaultkey(client, device_id):
    res = client.get_device_filevaultkey(id=device_id)
    assert type(res) == dict
    assert 'key' in res


def test_get_device_unlockpin(client, device_id):
    res = client.get_device_unlockpin(id=device_id)
    assert type(res) == dict
    assert 'pin' in res


def test_get_device_unlockpin_not_found(client):
    res = client.get_device_unlockpin(id="noid")
    assert res == {'response': {'status': 404}}
