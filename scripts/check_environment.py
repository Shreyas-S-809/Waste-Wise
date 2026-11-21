#!/usr/bin/env python3
"""
WasteWise — Environment Check Script
Verifies Python version, required packages, GPU availability, and system info.
"""

import sys
import platform
import os


def check_python_version():
    """Check that Python version is >= 3.8."""
    ver = sys.version_info
    ok = ver >= (3, 8)
    print(f"  Python version : {sys.version} {'[OK]' if ok else '[WARN: 3.8+ recommended]'}")
    return ok


def check_package(name, import_name=None):
    """Try to import a package and report success/failure."""
    import_name = import_name or name
    try:
        mod = __import__(import_name)
        version = getattr(mod, "__version__", "unknown")
        print(f"  {name:20s} : {version} [OK]")
        return True
    except ImportError:
        print(f"  {name:20s} : NOT INSTALLED [MISSING]")
        return False


def check_gpu():
    """Check TensorFlow GPU availability."""
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices("GPU")
        if gpus:
            for gpu in gpus:
                print(f"  GPU detected: {gpu.name}")
            print(f"  Total GPUs: {len(gpus)} [OK]")
            return True
        else:
            print("  No GPU detected — training will use CPU [WARN]")
            return False
    except ImportError:
        print("  TensorFlow not installed — cannot check GPU [SKIP]")
        return False
    except Exception as e:
        print(f"  GPU check error: {e} [ERROR]")
        return False


def report_system_info():
    """Print system information."""
    print(f"  OS            : {platform.system()} {platform.release()}")
    print(f"  Architecture  : {platform.machine()}")
    print(f"  Processor     : {platform.processor()}")
    print(f"  Python path   : {sys.executable}")
    print(f"  Working dir   : {os.getcwd()}")


def main():
    print("=" * 60)
    print("  WasteWise — Environment Check")
    print("=" * 60)

    print("\n[System Information]")
    report_system_info()

    print("\n[Python Version]")
    check_python_version()

    print("\n[Required Packages]")
    packages = [
        ("TensorFlow", "tensorflow"),
        ("Keras", "keras"),
        ("Pillow (PIL)", "PIL"),
        ("NumPy", "numpy"),
        ("Pandas", "pandas"),
        ("scikit-learn", "sklearn"),
        ("Matplotlib", "matplotlib"),
        ("Seaborn", "seaborn"),
    ]
    results = {}
    for display_name, import_name in packages:
        results[display_name] = check_package(display_name, import_name)

    print("\n[GPU Availability]")
    gpu_ok = check_gpu()

    # Summary
    missing = [name for name, ok in results.items() if not ok]
    print("\n" + "=" * 60)
    if missing:
        print(f"  MISSING PACKAGES ({len(missing)}): {', '.join(missing)}")
        print("  Install with: pip install -r requirements.txt")
    else:
        print("  All required packages are installed!")
    if not gpu_ok:
        print("  Note: GPU not available. Training will be slower on CPU.")
    print("=" * 60)


if __name__ == "__main__":
    main()
