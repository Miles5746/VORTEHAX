import re
import subprocess


def get_vortex_network_info():
    try:
        # Run `lsof -i -n -P` directly using subprocess
        result = subprocess.run(
            ["lsof", "-i", "-n", "-P"],
            capture_output=True,
            text=True,
            check=True,
        )

        for line in result.stdout.splitlines():
            # Only target Vortex lines and ignore standard HTTP/HTTPS ports (443/80)
            if "Vortex" in line and ":443" not in line and ":80" not in line:
                match = re.search(
                    r"(\d+\.\d+\.\d+\.\d+):\[?(\d+)[^->]*\]?->\[?(\d+\.\d+\.\d+\.\d+:\d+)",
                    line,
                )

                if match:
                    local_port = match.group(2)
                    server = match.group(3)

                    print(f"'Local Port: {local_port}'")
                    print(f"'Server: {server}'")
                    break  # Stop after processing the main connection

    except subprocess.CalledProcessError as e:
        print(f"Error running lsof: {e}")
    except FileNotFoundError:
        print("Error: 'lsof' command not found.")


if __name__ == "__main__":
    get_vortex_network_info()