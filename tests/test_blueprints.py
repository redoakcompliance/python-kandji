def test_list_blueprints(client):
    res = client.list_blueprints(limit=2)
    assert type(res['results']) == list
    assert res != {'response': {'status': 400}}


def test_list_blueprints_not_found(client):
    res = client.list_blueprints(id="97e4e175-1631-43f6-a02b-33fd1c748ab8")
    assert res == {'count': 0, 'next': None, 'previous': None, 'results': []}


def test_get_blueprint(client, blueprint_id):
    res = client.get_blueprint(id=blueprint_id)
    assert res.get('id')
    assert res != {'response': {'status': 404}}


def test_get_blueprint_not_found(client):
    res = client.get_blueprint(id="97e4e175-1631-43f6-a02b-33fd1c748ab8")
    assert res == {'response': {'status': 404}}


def test_get_blueprint_templates(client):
    res = client.get_blueprint_templates()
    assert type(res['results']) == list
    assert res != {'response': {'status': 404}}
