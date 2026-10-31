import os
import tempfile
import unittest
from app import create_app


class CampusCareTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = os.path.join(self.temp_dir.name, "test.db")
        self.app = create_app({
            "TESTING": True,
            "DATABASE": db_path,
            "SECRET_KEY": "test-secret",
            "ADMIN_PASSWORD": "test-admin-password",
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_ticket(self):
        return self.client.post("/submit", data={
            "student_name": "Test Student",
            "email": "student@example.edu",
            "category": "Wi-Fi Problem",
            "description": "Wi-Fi is not connecting in Lab 2.",
        }, follow_redirects=True)

    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CampusCare", response.data)

    def test_ticket_can_be_submitted(self):
        response = self.create_ticket()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Your ticket is in the system.", response.data)
        self.assertIn(b"#1", response.data)

    def test_ticket_can_be_tracked_by_id_and_email(self):
        self.create_ticket()
        response = self.client.post("/track", data={
            "ticket_id": "1",
            "email": "student@example.edu",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wi-Fi Problem", response.data)

    def test_wrong_email_cannot_view_ticket(self):
        self.create_ticket()
        response = self.client.post("/track", data={
            "ticket_id": "1",
            "email": "wrong@example.edu",
        })
        self.assertNotIn(b"Wi-Fi is not connecting", response.data)

    def test_admin_requires_login(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login", response.location)

    def test_admin_can_update_ticket(self):
        self.create_ticket()
        self.client.post("/admin/login", data={
            "password": "test-admin-password",
        })
        response = self.client.post("/admin", data={
            "ticket_id": "1",
            "status": "Resolved",
            "priority": "High",
        })
        self.assertEqual(response.status_code, 200)
        tracked = self.client.post("/track", data={
            "ticket_id": "1",
            "email": "student@example.edu",
        })
        self.assertIn(b"Resolved", tracked.data)
        self.assertIn(b"High", tracked.data)


if __name__ == "__main__":
    unittest.main()
