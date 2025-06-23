import argparse
from ui.cli import run_cli
from ui.guiFrame import run_gui

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["cli", "gui"], default="cli")
    args = parser.parse_args()

    if args.mode == "cli":
        run_cli()
    elif args.mode == "gui":
        run_gui()