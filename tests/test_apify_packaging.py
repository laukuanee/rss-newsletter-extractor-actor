import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("actor_main", ROOT / "main.py")
actor_main = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["actor_main"] = actor_main
SPEC.loader.exec_module(actor_main)


class ApifyPackagingTests(unittest.TestCase):
    def test_input_schema_defines_pages_array(self):
        schema = json.loads((ROOT / "INPUT_SCHEMA.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["title"], "RSS and Newsletter Page Extractor")
        self.assertEqual(schema["type"], "object")
        self.assertIn("pages", schema["properties"])
        self.assertEqual(schema["properties"]["pages"]["type"], "array")

    def test_actor_manifest_defines_store_metadata_and_dataset_view(self):
        manifest = json.loads((ROOT / ".actor" / "actor.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["name"], "rss-newsletter-extractor-actor")
        self.assertEqual(manifest["dockerfile"], "../Dockerfile")
        self.assertEqual(manifest["input"]["properties"]["pages"]["type"], "array")
        fields = manifest["storages"]["dataset"]["fields"]["properties"]
        self.assertIn("record_type", fields)
        self.assertIn("source_url", fields)
        self.assertIn("url", fields)

    def test_local_actor_entrypoint_writes_feed_and_item_records(self):
        payload = {
            "pages": [
                {
                    "url": "https://example.com/blog",
                    "html": (
                        "<html><head><link rel=\"alternate\" type=\"application/rss+xml\" "
                        "title=\"RSS\" href=\"/feed.xml\"></head><body>"
                        "<a href=\"/newsletter/june\">June newsletter</a></body></html>"
                    ),
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = pathlib.Path(temp_dir) / "input.json"
            records_path = pathlib.Path(temp_dir) / "records.jsonl"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

            exit_code = actor_main.run_local(input_path, records_path)

            records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(exit_code, 0)
            self.assertEqual([record["record_type"] for record in records], ["feed", "item"])
            self.assertEqual(records[0]["url"], "https://example.com/feed.xml")
            self.assertEqual(records[1]["url"], "https://example.com/newsletter/june")


if __name__ == "__main__":
    unittest.main()
