import unittest
import shutil
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from click.testing import CliRunner
from command_groups import login
from tbs_client.models.jwt import JWT
from command_groups.tests import generate_random_string

from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner


class TestLogin(unittest.TestCase):
    def setUp(self):
        timestamp = str(datetime.now().timestamp()).replace(".", "")
        self.home_dir = Path(f"/tmp/{timestamp}")
        self.home_dir.mkdir(parents=True)

    def tearDown(self):
        if self.home_dir.exists():
            shutil.rmtree(str(self.home_dir))

    @patch("tbs_client.AuthApi.auth_jwt_token_auth")
    @patch("builtins.open")
    @patch("json.dumps")
    def test_first_login_attempt_successful(self, mock_json_dumps, mock_open, mock_token_auth):
        token = generate_random_string(length=50)
        mock_token_auth.return_value = JWT(token=token)
        runner = CliRunner(env={'HOME': str(self.home_dir)})
        # with runner.isolated_filesystem():
        username = generate_random_string(length=15)
        password = generate_random_string(length=25)
        result = runner.invoke(login, input=f"{username}\n{password}")
        # Note: It's important (I think) that this dict matches the ordering of the dict
        # That json.dumps is actually called with. This is guaranteed to be true in python 3.6
        mock_json_dumps.assert_called_with({'token': token, 'namespace': username})
        mock_open.assert_called_with(Path(self.home_dir, ".threeblades.config"), "w")
        expected_output = f"Username: {username}\nPassword: \nUser '{username}' successfully logged in.\n"
        self.assertEqual(result.output, expected_output)

if __name__ == '__main__':
    if is_running_under_teamcity():
        print("We are running under teamcity. Using teamcity test runner..")
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
