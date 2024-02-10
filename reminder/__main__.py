import argparse
import os

import uvicorn


def extract_args() -> dict:
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "-e",
        "--env",
        type=str,
        help='Server environment. Either "local", "dev", or "prod".',
        choices=["dev", "local", "prod"],
        default="dev",
    )
    argParser.add_argument("--host", type=str, help="Host for the server to run on", default="127.0.0.1")
    argParser.add_argument("--port", type=int, help="Port for the server to run on", default=8888)
    args = argParser.parse_args()
    return {"env": args.env, "host": args.host, "port": args.port}


def main(env: str, host: str, port: int) -> None:
    os.environ["ENV"] = env
    print(f"- Running server in {env} environment...")
    uvicorn.run(
        app="reminder.server:app",
        host=host,
        port=port,
        log_level="info",
        reload=True if env == "dev" else False,
    )


# Run `python -m peerloop` to start the server
if __name__ == "__main__":
    args = extract_args()
    main(env=args["env"], host=args["host"], port=args["port"])
