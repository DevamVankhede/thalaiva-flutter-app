#!/usr/bin/env python3
"""
Thalaivaa Agent Sandbox Runner
Enables autonomous agents to execute test cases, security audits, and code execution
inside an isolated Docker Desktop container sandbox without host system risk.
"""

import sys
import subprocess
import shutil

def is_docker_available():
    return shutil.which("docker") is not None

def run_in_sandbox(command: str):
    if not is_docker_available():
        print("[WARNING] Docker CLI not found on host. Executing in local virtual environment...")
        return subprocess.run(command, shell=True).returncode

    print(f"[SANDBOX] Launching isolated Docker container for: {command}")
    docker_cmd = [
        "docker", "compose", "run", "--rm",
        "--profile", "testing",
        "sandbox",
        "sh", "-c", command
    ]
    return subprocess.run(docker_cmd).returncode

if __name__ == "__main__":
    cmd = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "php artisan test"
    exit_code = run_in_sandbox(cmd)
    sys.exit(exit_code)
