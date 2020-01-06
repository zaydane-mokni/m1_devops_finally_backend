# coding: utf-8

from flask import url_for
from conduit.exceptions import USER_ALREADY_REGISTERED


def _register_user(testapp, name, **kwargs):
    return testapp.post_json(url_for("user.register_user"), {
        "user": {
            "username": "mo" + name,
            "email": "mo" + name + "@mo.mo",
            "password": "momo"
        }
    }, **kwargs)


class TestAuthenticate:

    def test_register_user(self, testapp):
        resp = _register_user(testapp, 'register_user')
        assert resp.json['user']['email'] == 'moregister_user@mo.mo'
        assert resp.json['user']['token'] != 'None'
        assert resp.json['user']['token'] != ''

    def test_user_login(self, testapp):
        _register_user(testapp, 'login')

        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': 'mologin@mo.mo',
            'password': 'momo'
        }})

        assert resp.json['user']['email'] == 'mologin@mo.mo'
        assert resp.json['user']['token'] != 'None'
        assert resp.json['user']['token'] != ''

    def test_get_user(self, testapp):
        resp = _register_user(testapp, 'getUser')
        token = str(resp.json['user']['token'])
        resp = testapp.get(url_for('user.get_user'), headers={
            'Authorization': 'Token {}'.format(token)
        })
        assert resp.json['user']['email'] == 'mogetUser@mo.mo'
        assert resp.json['user']['token'] == token

    def test_register_already_registered_user(self, testapp):
        _register_user(testapp, 'already_register')
        resp = _register_user(testapp, 'already_register', expect_errors=True)
        assert resp.status_int == 422
        assert resp.json == USER_ALREADY_REGISTERED['message']

    def test_update_user(self, testapp):
        resp = _register_user(testapp, 'update')
        token = str(resp.json['user']['token'])
        resp = testapp.put_json(url_for('user.update_user'), {
            'user': {
                'email': 'meh@mo.mo',
                'bio': 'I\'m a simple man',
                'password': 'hmm'
            }
        }, headers={
            'Authorization': 'Token {}'.format(token)
        })
        assert resp.json['user']['bio'] == 'I\'m a simple man'
        assert resp.json['user']['email'] == 'meh@mo.mo'
