#!/usr/local/bin/python

import requests
import argparse
import logging
import json
import sys
import os

log = logging.getLogger(name="lifx-buildlight")


def json_argument(value):
    try:
        return json.loads(value)
    except (ValueError, TypeError) as error:
        raise argparse.ArgumentTypeError(
            f"Failed to interpret option as json from {value}: {error}"
        )


def action_type(value):
    if value == "state":
        return ("put", "/v1/lights/{selector}/state")
    elif value == "states":
        return ("put", "/v1/lights/states")
    elif value == "toggle":
        return ("post", "/v1/lights/{selector}/toggle")
    elif value == "effect":
        return ("post", "/v1/lights/{selector}/effects/{effect}")
    elif value == "cycle":
        return ("post", "/v1/lights/{selector}/cycle")
    elif value == "scene":
        return ("put", "/v1/scenes/{selector}/activate")


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selector", default=os.environ.get("SELECTOR", "all"))
    parser.add_argument("--uri", default=os.environ.get("URI", "https://api.lifx.co"))
    parser.add_argument("--body", type=json_argument, default=os.environ.get("BODY", "{}"))
    parser.add_argument(
        "--action-type",
        choices=["state", "states", "toggle", "effect", "cycle", "scene"],
        default=os.environ.get("ACTION_TYPE", "state"),
    )
    return parser


def main(lifx_token, argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)

    headers = {"Authorization": f"Bearer {lifx_token}"}

    method, path_template = action_type(args.action_type)
    format_args = {"selector": args.selector}
    if args.action_type == "effect":
        if "effect" not in args.body:
            sys.exit("You must specify an effect in --body when the action type is effect")
        else:
            format_args["effect"] = args.body.pop("effect")
    path = path_template.format(**format_args)

    res = getattr(requests, method)(f"{args.uri}{path}", headers=headers, json=args.body)
    content = json.loads(res.content.decode())
    content_str = json.dumps(content)

    if res.status_code != requests.status_codes.codes.MULTI_STATUS:
        sys.exit(f"Failed to change lights: {res.status_code}: {content_str}")

    def find_failed(results):
        return any(s["status"] != "ok" for s in results)

    if action_type == "states":
        any_failed = any(find_failed(s["results"]) for s in content["results"])
    else:
        any_failed = find_failed(content["results"])

    if any_failed:
        sys.exit(f"Failed to change lights: {res.status_code}: {content_str}")
    else:
        print(content)


if __name__ == "__main__":
    if not os.environ.get("LIFX_TOKEN"):
        sys.exit("Missing LIFX_TOKEN. Add it as a secret to your repo")

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    main(os.environ["LIFX_TOKEN"])
