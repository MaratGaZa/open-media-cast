"""E00.6: aiohttp single-file server; no DLNA headers or custom Range code."""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket

from aiohttp import web


async def main(args):
    path = Path(args.file).resolve(strict=True)
    if not path.is_file():
        raise ValueError("Expected a regular file")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect((args.receiver, 9))  # Route lookup; sends no UDP payload.
        bind = sock.getsockname()[0]
    route = "/" + secrets.token_urlsafe(24) + ".mp4"

    async def serve(request):
        # FileResponse implements HEAD/Range; no directory route is registered.
        print(json.dumps({"method": request.method,
                          "range": request.headers.get("Range")}), flush=True)
        return web.FileResponse(path, headers={"Content-Type": "video/mp4"})

    app = web.Application()
    app.router.add_get(route, serve)
    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    site = web.TCPSite(runner, bind, 0)
    await site.start()
    port = runner.addresses[0][1]
    url_file = Path(args.url_file)
    try:
        # Exclusive private file; do not overwrite another run's URL.
        fd = os.open(url_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(f"http://{bind}:{port}{route}\n")
        with path.open("rb") as source:
            checksum = hashlib.file_digest(source, "sha256").hexdigest()
        print(json.dumps({"event": "server_ready", "lifetime_s": args.seconds,
                          "size": path.stat().st_size,
                          "sha256": checksum,
                          "dlna_headers": False}), flush=True)
        await asyncio.sleep(args.seconds)
    finally:
        await runner.cleanup()
        print('{"event":"server_closed"}', flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--file", required=True)
    p.add_argument("--receiver", required=True, help="Explicit authorized LAN receiver")
    p.add_argument("--url-file", required=True, help="New private file outside Git")
    p.add_argument("--seconds", type=int, choices=range(30, 1801), default=600)
    try:
        asyncio.run(main(p.parse_args()))
    except KeyboardInterrupt:
        pass
