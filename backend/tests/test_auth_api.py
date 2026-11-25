import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.app.main import app


class TestAuthAndSiteLockApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self._tmp_dir = tempfile.TemporaryDirectory()
        self.profile_path = Path(self._tmp_dir.name) / 'personal_profile.json'
        self.profile_path.write_text(
            json.dumps({'ui': {'screeningBadgeTitle': 'TEST_BADGE'}}, ensure_ascii=False),
            encoding='utf-8',
        )

    def tearDown(self) -> None:
        self._tmp_dir.cleanup()

    def test_site_lock_blocks_root_and_api_and_sets_crawler_headers(self) -> None:
        with (
            patch.object(settings, 'SITE_LOCK_ENABLED', True),
            patch.object(settings, 'ADMIN_USERNAME', 'admin'),
            patch.object(settings, 'ADMIN_PASSWORD', 'secret-pass-123'),
        ):
            root_res = self.client.get('/', follow_redirects=False)
            self.assertEqual(root_res.status_code, 302)
            self.assertEqual(root_res.headers.get('location'), '/login')
            self.assertIn('no-store', root_res.headers.get('cache-control', ''))
            self.assertEqual(root_res.headers.get('x-robots-tag'), 'noindex, nofollow, noarchive')

            api_res = self.client.get('/api/v1/content/summary')
            self.assertEqual(api_res.status_code, 401)
            self.assertIn('no-store', api_res.headers.get('cache-control', ''))
            self.assertEqual(api_res.headers.get('x-robots-tag'), 'noindex, nofollow, noarchive')

            robots_res = self.client.get('/robots.txt')
            self.assertEqual(robots_res.status_code, 200)
            self.assertEqual(robots_res.text, 'User-agent: *\nDisallow: /\n')
            self.assertEqual(robots_res.headers.get('x-robots-tag'), 'noindex, nofollow, noarchive')

            login_page = self.client.get('/login')
            self.assertEqual(login_page.status_code, 200)
            self.assertIn('autocomplete="username"', login_page.text)
            self.assertIn('autocomplete="current-password"', login_page.text)
            self.assertIn('no-store', login_page.headers.get('cache-control', ''))

    def test_login_invalid_and_valid_credentials_sets_httponly_cookie(self) -> None:
        with (
            patch.object(settings, 'SITE_LOCK_ENABLED', True),
            patch.object(settings, 'ADMIN_USERNAME', 'admin'),
            patch.object(settings, 'ADMIN_PASSWORD', 'secret-pass-123'),
            patch.object(settings, 'SESSION_TTL_DAYS', 30),
        ):
            bad_res = self.client.post(
                '/api/v1/auth/login',
                json={'username': 'admin', 'password': 'wrong-password'},
            )
            self.assertEqual(bad_res.status_code, 401)
            self.assertIn('no-store', bad_res.headers.get('cache-control', ''))

            ok_res = self.client.post(
                '/api/v1/auth/login',
                json={'username': 'admin', 'password': 'secret-pass-123'},
            )
            self.assertEqual(ok_res.status_code, 200)
            self.assertEqual(ok_res.json(), {'authenticated': True, 'username': 'admin'})
            self.assertIn('no-store', ok_res.headers.get('cache-control', ''))

            set_cookie = ok_res.headers.get('set-cookie', '')
            self.assertIn('pba_session=', set_cookie)
            self.assertIn('HttpOnly', set_cookie)
            self.assertIn('Max-Age=2592000', set_cookie)

            me_res = self.client.get('/api/v1/auth/me')
            self.assertEqual(me_res.status_code, 200)
            self.assertTrue(me_res.json()['authenticated'])
            self.assertTrue(me_res.json()['site_lock_enabled'])

            root_after = self.client.get('/')
            self.assertEqual(root_after.status_code, 200)

    def test_private_profile_requires_auth_and_returns_temp_json(self) -> None:
        with (
            patch.object(settings, 'SITE_LOCK_ENABLED', False),
            patch.object(settings, 'ADMIN_USERNAME', 'admin'),
            patch.object(settings, 'ADMIN_PASSWORD', 'secret-pass-123'),
            patch.object(settings, 'PRIVATE_PROFILE_PATH', str(self.profile_path)),
        ):
            unauth_res = self.client.get('/api/v1/private/profile')
            self.assertEqual(unauth_res.status_code, 401)
            self.assertIn('no-store', unauth_res.headers.get('cache-control', ''))

            login_res = self.client.post(
                '/api/v1/auth/login',
                json={'username': 'admin', 'password': 'secret-pass-123'},
            )
            self.assertEqual(login_res.status_code, 200)

            prof_res = self.client.get('/api/v1/private/profile')
            self.assertEqual(prof_res.status_code, 200)
            self.assertIn('no-store', prof_res.headers.get('cache-control', ''))
            self.assertEqual(prof_res.json(), {'ui': {'screeningBadgeTitle': 'TEST_BADGE'}})

    def test_private_profile_static_path_always_returns_404(self) -> None:
        with (
            patch.object(settings, 'SITE_LOCK_ENABLED', False),
            patch.object(settings, 'ADMIN_USERNAME', 'admin'),
            patch.object(settings, 'ADMIN_PASSWORD', 'secret-pass-123'),
        ):
            res_unauth = self.client.get('/data/private/personal_profile.json')
            self.assertEqual(res_unauth.status_code, 404)

            self.client.post(
                '/api/v1/auth/login',
                json={'username': 'admin', 'password': 'secret-pass-123'},
            )
            res_auth = self.client.get('/data/private/personal_profile.json')
            self.assertEqual(res_auth.status_code, 404)
