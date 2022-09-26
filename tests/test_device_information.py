def test_list_devices(client):
    res = client.list_devices(limit=2)
    assert type(res) == list


def test_list_devices_not_found(client):
    res = client.list_devices(asset_tag="notag")
    assert res == []


def test_get_device(client, device_id):
    res = client.get_device(id=device_id)
    assert type(res) == dict
    assert res.get('device_id')


def test_get_device_not_found(client):
    res = client.get_device(id="noid")
    assert res == {'response': {'status': 404}}


def test_get_device_details(client, device_id):
    res = client.get_device_details(id=device_id)
    assert type(res) == dict
    assert res.get('general')


def test_get_device_activity(client, device_id):
    res = client.get_device_activity(id=device_id)
    assert type(res) == dict
    assert res.get('device_id')


def test_get_device_note(client, device_id, note_id):
    res = client.get_device_note(device_id=device_id, note_id=note_id)
    assert type(res) == dict
    assert res.get('note_id')


def test_get_device_note_not_found(client, device_id):
    res = client.get_device_note(device_id=device_id, note_id="noid")
    assert res == {'response': {'status': 500}}
