import sys
import os
import json
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# test connection to the DB
DB_AVAILABLE   = False
TABLE_HAS_DATA = False

try:
    import psycopg2
    from config import DB_CONFIG, PROCESSED_TABLE
    _conn = psycopg2.connect(**DB_CONFIG)
    _cur  = _conn.cursor()
    _cur.execute(f"SELECT COUNT(*) FROM {PROCESSED_TABLE}")
    _count = _cur.fetchone()[0]
    _conn.close()
    DB_AVAILABLE   = True
    TABLE_HAS_DATA = _count > 0
except Exception as _e:
    print(f"[integration] DB not available: {_e} — tests will be skipped.")

# Import the Flask app 
try:
    from app import app as flask_app
    flask_app.config["TESTING"] = True
    FLASK_AVAILABLE = True
except Exception as _fe:
    print(f"[integration] Flask app import failed: {_fe}")
    FLASK_AVAILABLE = False

@unittest.skipUnless(DB_AVAILABLE and FLASK_AVAILABLE,
                     "DB or Flask app not available")

class TestFlaskAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = flask_app.test_client()

    # test /api/stats 
    def test_stats_returns_200(self):
        resp = self.client.get("/api/stats")
        self.assertEqual(resp.status_code, 200,
                         msg=f"Expected 200, got {resp.status_code}")

    def test_stats_content_type_is_json(self):
        resp = self.client.get("/api/stats")
        self.assertIn("application/json", resp.content_type)

    def test_stats_has_required_keys(self):
        resp = self.client.get("/api/stats")
        data = json.loads(resp.data)
        required_keys = [
            "total_processed", "avg_magnitude", "max_magnitude",
            "min_magnitude",   "avg_depth_km",  "outlier_count",
            "raw_count",
        ]
        for key in required_keys:
            self.assertIn(key, data, msg=f"Missing key in /api/stats: '{key}'")

    @unittest.skipUnless(TABLE_HAS_DATA, "Table is empty")
    def test_stats_processed_count_positive(self):
        resp = self.client.get("/api/stats")
        data = json.loads(resp.data)
        self.assertGreater(int(data["total_processed"]), 0)

    @unittest.skipUnless(TABLE_HAS_DATA, "Table is empty")
    def test_stats_avg_magnitude_in_valid_range(self):
        resp = self.client.get("/api/stats")
        data = json.loads(resp.data)
        avg = float(data["avg_magnitude"])
        self.assertGreaterEqual(avg, -2.0)
        self.assertLessEqual(avg,   10.0)

    @unittest.skipUnless(TABLE_HAS_DATA, "Table is empty")
    def test_stats_max_gte_min_magnitude(self):
        resp = self.client.get("/api/stats")
        data = json.loads(resp.data)
        self.assertGreaterEqual(
            float(data["max_magnitude"]),
            float(data["min_magnitude"])
        )

    def test_index_returns_200(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_index_content_type_is_html(self):
        resp = self.client.get("/")
        self.assertIn("text/html", resp.content_type)

if __name__ == "__main__":
    unittest.main(verbosity=2)