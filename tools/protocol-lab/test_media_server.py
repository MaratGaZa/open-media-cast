"""HTTP response contract for the E00.6 reference server, not the Rust product."""
import http.client
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.parse import urlsplit


class MediaServerContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="omc-http-test-")
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        # HTTP bytes only: deliberately not a playable movie or codec fixture.
        self.data = bytes(range(256)) * 16
        media = root / "synthetic.mp4"
        media.write_bytes(self.data)
        url_file = root / "url"
        self.log = (root / "server.log").open("w+")
        self.addCleanup(self.log.close)
        self.server = subprocess.Popen(
            [sys.executable, "-u", str(Path(__file__).with_name("media_server.py")),
             "--file", str(media), "--receiver", "127.0.0.1",
             "--url-file", str(url_file), "--seconds", "30"],
            stdout=self.log, stderr=self.log,
        )
        self.addCleanup(self.stop_server)
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if self.server.poll() is not None:
                self.log.seek(0)
                raise AssertionError("Server exited before readiness: " + self.log.read())
            if url_file.exists():
                url = url_file.read_text().strip()
                if url.endswith(".mp4"):
                    self.url = urlsplit(url)
                    return
            time.sleep(0.02)
        raise AssertionError("Server readiness timeout")

    def stop_server(self):
        if self.server.poll() is None:
            self.server.send_signal(signal.SIGINT)
            try:
                self.server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server.kill()
                self.server.wait(timeout=5)

    def request(self, method="GET", path=None, headers=None):
        conn = http.client.HTTPConnection(self.url.hostname, self.url.port, timeout=3)
        try:
            conn.request(method, path if path is not None else self.url.path,
                         headers=headers or {})
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def test_get_exact_selected_bytes(self):
        status, headers, body = self.request()
        self.assertEqual(status, 200)
        self.assertEqual(body, self.data)
        self.assertEqual(int(headers["Content-Length"]), len(self.data))
        self.assertEqual(headers["Content-Type"], "video/mp4")

    def test_head_has_length_and_no_body(self):
        status, headers, body = self.request("HEAD")
        self.assertEqual(status, 200)
        self.assertEqual(int(headers["Content-Length"]), len(self.data))
        self.assertEqual(body, b"")

    def test_range_status_headers_and_bytes(self):
        size = len(self.data)
        for header, start, end in [("bytes=19-118", 19, 118),
                                   ("bytes=4000-", 4000, size - 1),
                                   ("bytes=-73", size - 73, size - 1),
                                   ("bytes=4000-9999", 4000, size - 1)]:
            with self.subTest(range=header):
                status, headers, body = self.request(headers={"Range": header})
                self.assertEqual(status, 206)
                self.assertEqual(headers["Content-Range"], f"bytes {start}-{end}/{size}")
                self.assertEqual(int(headers["Content-Length"]), end - start + 1)
                self.assertEqual(body, self.data[start:end + 1])

    def test_unsatisfiable_range(self):
        status, headers, body = self.request(headers={"Range": f"bytes={len(self.data)}-"})
        self.assertEqual(status, 416)
        self.assertEqual(headers["Content-Range"], f"bytes */{len(self.data)}")
        self.assertNotEqual(body, self.data)

    def test_wrong_token_and_directory_do_not_expose_file(self):
        for path in ["/wrong-token.mp4", "/", "/synthetic.mp4", "/../synthetic.mp4"]:
            with self.subTest(path=path):
                status, _, body = self.request(path=path)
                self.assertEqual(status, 404)
                self.assertNotIn(self.data, body)

    def test_post_is_rejected(self):
        status, _, body = self.request("POST")
        self.assertEqual(status, 405)
        self.assertNotIn(self.data, body)

    def test_shutdown_closes_listener(self):
        self.stop_server()
        self.assertEqual(self.server.returncode, 0)
        self.log.seek(0)
        self.assertIn('"event":"server_closed"', self.log.read())
        with self.assertRaises((ConnectionRefusedError, ConnectionResetError)):
            self.request()


if __name__ == "__main__":
    unittest.main()
