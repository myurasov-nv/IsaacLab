# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Command-line entrypoint for the isaaclab package."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys


def main(argv: list[str] | None = None) -> int:
    """Command-line entrypoint for the isaaclab package."""

    parser = argparse.ArgumentParser(
        description="Isaac Lab command-line utilities."
    )

    parser.add_argument(
        "--generate-vscode-settings",
        action="store_true",
        help=(
            "Generate .vscode/settings.json and launch.json files."
        ),
    )

    args = parser.parse_args(argv)

    if args.generate_vscode_settings:

        # find the isaaclab installation root
        current = Path(__file__).resolve()
        isaaclab_install_path = None

        # look up until we find the .vscode folder (top-level folder)
        for parent in (current, *current.parents):
            candidate = parent / ".vscode" / "tools" / "setup_vscode.py"
            if candidate.exists():
                isaaclab_install_path = parent
                print(
                    "Found Isaac Lab installation at:" +
                    f" {isaaclab_install_path}"
                )
                break

        if isaaclab_install_path is None:
            raise FileNotFoundError(
                "Could not locate isaaclab installation path."
            )

        # execute the VSCode settings generation script
        script_path = (
            isaaclab_install_path / ".vscode" / "tools" / "setup_vscode.py"
        )

        spec = importlib.util.spec_from_file_location(
            "isaaclab_setup_vscode", script_path
        )
        if spec is None or spec.loader is None:
            raise ImportError(
                f"Could not load VSCode setup script: {script_path}"
            )

        module = importlib.util.module_from_spec(spec)
        sys.modules["isaaclab_setup_vscode"] = module
        spec.loader.exec_module(module)

        if not hasattr(module, "main"):
            raise AttributeError(f"Expected main() in {script_path}")

        module.main()
        print(
            "Successfully generated VSCode settings and launch configs at "
                f"{isaaclab_install_path / '.vscode'}")
        return 0

    # parse arguments with help to show usage
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
