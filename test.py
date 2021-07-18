import argparse
import plistlib
import os
import tempfile
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "maap"))

from maap.misc.app_utils import container_for_app, run_process
from maap.misc.plist import parse_resilient
from maap.extern.tools import tool_named
from maap.bundle.bundle import Bundle

def compile_sb_profile(profile: str) -> bytes:
    compile_sb = tool_named("compile_sb")
    exit_code, result = compile_sb("/dev/stdin", "/dev/stdout", input=profile)
    if exit_code != 0:
        return

    return result

def write_sb_profile(metadata_path: str, profile: bytes):
    """
    Writes (modified) sandbox profile to supplied container
    """
    data = parse_resilient(metadata_path)
    data['SandboxProfileData'] = profile
    with open(metadata_path, "wb") as outfile:
        plistlib.dump(data, outfile)

def run_with_minimized_profile(path_to_app: str, path_to_compiled_profile: str, timeout: int):
    bundle = Bundle.make(path_to_app)
    APP_CONTAINER = container_for_app(bundle)
    APP_METADATA_FILE = os.path.join(APP_CONTAINER, "Container.plist")
    container_metadata = ''
    with open(APP_METADATA_FILE, "rb") as infile:
        container_metadata = infile.read()

    compiled_profile = None
    with open(path_to_compiled_profile, "rb") as infile:
        compiled_profile = infile.read()

    write_sb_profile(APP_METADATA_FILE, compiled_profile)


    with tempfile.TemporaryDirectory() as tempdirname:
        INFO_STDOUT = os.path.join(tempdirname, "stdout")
        INFO_STDERR = os.path.join(tempdirname, "stderr")

        with open(INFO_STDOUT, "w") as stdout_f, open(INFO_STDERR, "w") as stderr_f:
            run_process(bundle.executable_path(), timeout, stdout_f, stderr_f)


    # Restore original container metadata.
    with open(APP_METADATA_FILE, "wb") as outfile:
        outfile.write(container_metadata)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect sandbox coverage information for an application')
    parser.add_argument('--app', required=True,
                        help='Path to the app for which to compute sandbox coverage data.')
    parser.add_argument('--timeout', required=False, default=None, type=int,
                        help='Number of seconds to wait before killing the program. Leave unspecified to not kill the program at all.')
    parser.add_argument('--m', required=True, help='Path to the minimized sandbox profile')
    args = parser.parse_args()

    run_with_minimized_profile(args.app, args.m, args.timeout)
