#!/usr/bin/env python3

import logging
import json
import pathlib

try:
    import tomlkit
    from aiohttp import web
except ImportError as e:
    import sys

    message = """Could not import required packages.
Please ensure you've installed all necessary packages first!

On Debian-based distributions, you should be able to install them via:

\tapt update
\tapt install python3-aiohttp python3-tomlkit"""

    print(message, file=sys.stderr)

    raise e

DEFAULT_ANSWER_FILE_PATH = pathlib.Path("./config/default.toml")
ANSWER_FILE_DIR = pathlib.Path("./config/answers/")

routes = web.RouteTableDef()


@routes.post("/answer")
async def answer(request: web.Request):
    try:
        request_data = json.loads(await request.text())
    except json.JSONDecodeError as e:
        return web.Response(
            status=500,
            text=f"Internal Server Error: failed to parse request contents: {e}",
        )

    logging.info(
        f"Request data for peer '{request.remote}':\n"
        f"{json.dumps(request_data, indent=1)}"
    )

    try:
        answer = create_answer(request_data)

        logging.info(f"Answer file for peer '{request.remote}':\n{answer}")

        return web.Response(text=answer)
    except Exception as e:
        logging.exception(f"failed to create answer: {e}")
        return web.Response(status=500, text=f"Internal Server Error: {e}")


def create_answer(request_data: dict) -> str:
    with open(DEFAULT_ANSWER_FILE_PATH) as file:
        answer = tomlkit.parse(file.read())

    for nic in request_data.get("network_interfaces", []):
        if "mac" not in nic:
            continue

        answer_mac = lookup_answer_for_mac(nic["mac"])
        if answer_mac is not None:
            answer = answer_mac

    return tomlkit.dumps(answer)


def lookup_answer_for_mac(mac: str) -> tomlkit.TOMLDocument | None:
    mac = mac.lower()

    for filename in ANSWER_FILE_DIR.glob("*.toml"):
        if filename.name.lower().startswith(mac):
            with open(filename) as mac_file:
                return tomlkit.parse(mac_file.read())


def assert_default_answer_file_exists():
    if not DEFAULT_ANSWER_FILE_PATH.exists():
        raise RuntimeError(
            f"Default answer file '{DEFAULT_ANSWER_FILE_PATH}' does not exist"
        )


def assert_default_answer_file_parseable():
    with open(DEFAULT_ANSWER_FILE_PATH) as file:
        try:
            tomlkit.parse(file.read())
        except Exception as e:
            raise RuntimeError(
                "Could not parse default answer file "
                f"'{DEFAULT_ANSWER_FILE_PATH}':\n{e}"
            )


def assert_answer_dir_exists():
    if not ANSWER_FILE_DIR.exists():
        raise RuntimeError(f"Answer file directory '{ANSWER_FILE_DIR}' does not exist")


if __name__ == "__main__":
    assert_default_answer_file_exists()
    assert_answer_dir_exists()
    assert_default_answer_file_parseable()

    app = web.Application()

    logging.basicConfig(level=logging.INFO)

    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=8000)
