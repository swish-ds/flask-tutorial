from flaskr import create_app

# If config is not passed, there should be some default configuration, otherwise the configuration should be overridden.
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

# Pytest uses fixtures by matching their function names with the names of arguments in the test functions.
# test_hello takes a client argument. Pytest matches that with the client fixture function, calls it,
# and passes the returned value (app.test_client()) to the test function.
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'