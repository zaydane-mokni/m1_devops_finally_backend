# coding: utf-8

from flask import url_for
from conduit.exceptions import USER_NOT_FOUND


def _register_user(testapp, name, **kwargs):
    return testapp.post_json(url_for('user.register_user'), {
          "user": {
              "email": 'foo' + name + '@bar.com',
              "username": name + 'foobar',
              "password": 'myprecious'
          }}, **kwargs)


class TestProfile:

    def test_get_profile_not_loggedin(self, testapp):
        _register_user(testapp, 'not_loggedin')
        resp = testapp.get(url_for('profiles.get_profile', username='not_loggedinfoobar'))
        assert resp.json['profile']['email'] == 'foonot_loggedin@bar.com'
        assert not resp.json['profile']['following']

    def test_get_profile_not_existing(self, testapp):
        resp = testapp.get(url_for('profiles.get_profile', username='unknownfoobar'), expect_errors=True)
        assert resp.status_int == 404
        assert resp.json == USER_NOT_FOUND['message']

    def test_follow_user(self, testapp, user):
        user = user.get()
        resp = _register_user(testapp, 'folow_user')
        token = str(resp.json['user']['token'])
        resp = testapp.post(url_for('profiles.follow_user', username=user.username), headers={
            'Authorization': 'Token {}'.format(token)
        })
        assert resp.json['profile']['following']

    def test_unfollow_user(self, testapp, user):
        user = user.get()
        resp = _register_user(testapp, 'unfolow')
        token = str(resp.json['user']['token'])
        resp = testapp.delete(url_for('profiles.unfollow_user', username=user.username), headers={
            'Authorization': 'Token {}'.format(token)
        })
        assert not resp.json['profile']['following']
