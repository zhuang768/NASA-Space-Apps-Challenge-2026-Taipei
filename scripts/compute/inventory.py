"""Read-only runtime/data inventory; no scientific calculation or training."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def command(args, cwd=None):
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=10)
        return {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()[:500]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"error": str(e)}


def inventory(root: Path, include_files=True):
    root = root.resolve()
    packages = {}
    for name in ["numpy", "xarray", "netCDF4", "rasterio", "matplotlib", "scipy", "pytest", "pypdf", "pypdfium2", "torch", "cupy"]:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    files = []
    for base in (["data", "outputs", "scripts/compute"] if include_files else []):
        directory = root / base
        if not directory.exists():
            continue
        for p in sorted(directory.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts:
                continue
            with p.open("rb") as stream:
                sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
            files.append({"path": str(p.relative_to(root)), "bytes": p.stat().st_size, "sha256": sha256})
    cgroups = {}
    for name in ["memory.max", "memory.current", "cpu.max", "cpuset.cpus.effective"]:
        p = Path("/sys/fs/cgroup") / name
        if p.is_file():
            cgroups[name] = p.read_text().strip()
    gpu = {"device_paths": [str(p) for pattern in ["/dev/kfd", "/dev/dri/render*"] for p in Path("/").glob(pattern.lstrip("/"))],
           "rocm_smi": shutil.which("rocm-smi"), "amd_smi": shutil.which("amd-smi"),
           "computation_backend_used": "CPU", "gpu_computation_performed": False}
    if packages.get("torch"):
        gpu["torch_probe"] = command([sys.executable, "-c", "import torch,json; print(json.dumps({'hip':torch.version.hip,'cuda_available':torch.cuda.is_available(),'device_count':torch.cuda.device_count()}))"])
    return {"project_root": str(root), "cwd": os.getcwd(), "python_executable": sys.executable,
            "python": sys.version, "platform": platform.platform(), "machine": platform.machine(),
            "logical_cpu_count_host": os.cpu_count(), "cgroup_limits": cgroups,
            "packages": packages, "gpu": gpu,
            "git_branch": command(["git", "branch", "--show-current"], root),
            "git_commit": command(["git", "rev-parse", "HEAD"], root),
            "git_status": command(["git", "status", "--short"], root), "files": files,
            "note": "Host CPU/memory figures are not an allocation guarantee; cgroup values govern when present."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = inventory(args.root)
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
