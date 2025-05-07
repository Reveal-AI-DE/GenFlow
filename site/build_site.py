# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import git

def generate_site(repo: git.Repo, output_dir: os.PathLike):
    repo_root = Path(repo.working_tree_dir)

    with tempfile.TemporaryDirectory() as temp_dir:
        content_loc = Path(temp_dir, "site")
        shutil.copytree(repo_root / "site", content_loc, symlinks=True)

        def run_hugo(
            destination_dir: os.PathLike,
            *,
            extra_env_vars: dict[str, str] = None,
            executable: Optional[str] = "hugo",
        ):
            extra_kwargs = {}

            if extra_env_vars:
                extra_kwargs["env"] = os.environ.copy()
                extra_kwargs["env"].update(extra_env_vars)

            subprocess.run(  # nosec
                [
                    executable,
                    "--destination",
                    str(destination_dir),
                    "--config",
                    "hugo.toml",
                ],
                cwd=content_loc,
                check=True,
                **extra_kwargs,
            )

        # Process the develop version
        run_hugo(output_dir, executable="hugo")

        # Create a temp repo for checkouts
        temp_repo_path = Path(temp_dir) / "tmp_repo"
        shutil.copytree(repo_root, temp_repo_path, symlinks=True)
        temp_repo = git.Repo(temp_repo_path)
        temp_repo.git.reset(hard=True, recurse_submodules=True)

def validate_env():
    try:
        subprocess.run(["hugo", "version"], capture_output=True)  # nosec
    except (subprocess.CalledProcessError, FileNotFoundError) as ex:
        raise Exception(f"Failed to run 'hugo', please make sure it exists.") from ex


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = repo_root / "public"

    validate_env()

    with git.Repo(repo_root) as repo:
        generate_site(repo, output_dir)