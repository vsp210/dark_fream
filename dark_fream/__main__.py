import sys
from .app import run_server, create_app

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m dark_fream.app runserver or python -m dark_fream.app createapp <app_name>")
        sys.exit(1)
    if sys.argv[1] == "runserver":
        run_server()
    elif sys.argv[1] == "createapp":
        if len(sys.argv) != 3:
            print("Usage: python -m dark_fream.app createapp <app_name>")
            sys.exit(1)
        create_app(sys.argv[2])
    else:
        print("Unknown command")
        sys.exit(1)
