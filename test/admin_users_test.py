"""
Module for testing the Terraform Cloud API Endpoint: Admin Users.
"""

from .base import TestTFCBaseTestCase


class TestTFCAdminUsers(TestTFCBaseTestCase):
    """
    Class for testing the Terraform Cloud API Endpoint: Admin Users.
    """

    _unittest_name = "users"

    def test_admin_users(self):
        """
        Test the Admin Users API endpoints: ``grant_admin``, ``list``,
        ``revoke_admin``, ``suspend``, ``unsuspend``.

        Not tested, as they can't be reverted via the API: ``destroy``, ``disable_two_factor``.

        Not tested, as it's not super valuable via the API: ``impersonate``, ``unimpersonate``.
        """
        # List all the users through the admin users API, but query for our test
        # user
        listed_users = self._api.admin_users.list(query=self._test_username, page=0, page_size=50)["data"]
        self.assertEqual(len(listed_users), 1)

        # Extract the test users's ID
        test_user_id = listed_users[0]["id"]

        # Suspend the user, confirm they are suspended
        suspended_user = self._api.admin_users.suspend(test_user_id)["data"]
        self.assertTrue(suspended_user["attributes"]["is-suspended"])

        # Unsuspend the user, confirm they are no longer suspended
        unsuspended_user = self._api.admin_users.unsuspend(test_user_id)["data"]
        self.assertFalse(unsuspended_user["attributes"]["is-suspended"])

        # Grant the user admin rights, confirm they are now admins
        admin_user = self._api.admin_users.grant_admin(test_user_id)["data"]
        self.assertTrue(admin_user["attributes"]["is-admin"])

        # Revoke the user's admin rights, confirm they are no longer admins
        nonadmin_user = self._api.admin_users.revoke_admin(test_user_id)["data"]
        self.assertFalse(nonadmin_user["attributes"]["is-admin"])