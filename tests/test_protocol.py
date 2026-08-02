import http.server
import os
import socket
import sys
import tempfile
import threading
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "lib"))

import announce
import base64e
import discover
import fetch
import index
import loot


class IPv4UDPServer(discover.UDPServer):
    address_family = socket.AF_INET

    def useIPv6(self):
        return False


class ProtocolTests(unittest.TestCase):
    def test_announcement_is_discovered_over_udp(self):
        with tempfile.TemporaryDirectory() as root:
            dynamic = os.path.join(root, "var")
            discover.forbanpath = root
            server = IPv4UDPServer(("127.0.0.1", 0), discover.MyUDPHandler)
            thread = threading.Thread(target=server.handle_request)
            thread.start()

            message = announce.message(
                name="python-3-peer",
                port=server.server_address[1],
                destination=["127.0.0.1"],
                dynpath=dynamic,
            )
            message.gen()
            message.auth("test-hmac")
            peer_id = message.get().split(";uuid;")[1].split(";", 1)[0]
            message.send()

            thread.join(timeout=2)
            server.server_close()
            self.assertFalse(thread.is_alive())
            discovered = loot.loot(dynamic)
            self.assertEqual(discovered.getname(peer_id), "python-3-peer")
            self.assertEqual(discovered.getipv4(peer_id), "127.0.0.1")
            self.assertEqual(discovered.gethmac(peer_id), "test-hmac")

    def test_index_hmac_matches_protocol_payload(self):
        with tempfile.TemporaryDirectory() as root:
            share = os.path.join(root, "share")
            os.makedirs(os.path.join(share, "docs"))
            with open(os.path.join(share, "docs", "hello.txt"), "wb") as output:
                output.write(b"hello from Python 3\n")
            manager = index.manage(sharedir=share, forbanglobal=root)
            os.makedirs(os.path.dirname(manager.location))
            manager.build()
            self.assertEqual(manager.gethmac(), manager.calchmac(manager.location))
            self.assertIn("/docs/hello.txt,20\n", manager.search("hello"))

    def test_http_file_transfer_preserves_binary_data(self):
        payload = bytes(range(256))

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Disposition", "attachment; filename=data.bin")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, format, *args):
                pass

        with tempfile.TemporaryDirectory() as root:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            thread = threading.Thread(target=server.serve_forever)
            thread.start()
            destination = os.path.join(root, "download.bin")
            try:
                url = "http://127.0.0.1:%d/file" % server.server_address[1]
                self.assertTrue(fetch.urlget(url, destination))
            finally:
                server.shutdown()
                thread.join(timeout=2)
                server.server_close()
            with open(destination, "rb") as downloaded:
                self.assertEqual(downloaded.read(), payload)

    def test_base64_filename_encoding_is_text_and_round_trips(self):
        filename = "/données/été.txt"
        encoded = base64e.encode(filename)
        self.assertIsInstance(encoded, str)
        self.assertEqual(base64e.decode(encoded), filename)


if __name__ == "__main__":
    unittest.main()
