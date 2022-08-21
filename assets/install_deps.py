from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError

class Dependencies:
    """
    Nukebot's Dependencies class, full of code ensuring dependencies are all installed.
    The idea is give 0 errors: Nukebot MUST run properly.
    """
    deps = ["disnake", "colorama"]

    def install():
        """Installs every non-standard lib dependency Nukebot needs."""
        print(f"Installing/updating {len(Dependencies.deps)} packages")
        def pkgs():
            current_pkg = 1
            failed_pkgs = 0
            successful  = 0
            for dep in Dependencies.deps:
                print(f"Installing {dep} {current_pkg}/{len(Dependencies.deps)}")
                try:
                    out = check_output(["python", "-m", "pip", "install", dep, "--upgrade", "--no-warn-conflicts", "--no-warn-script-location"])
                    if "PermissionError: [Errno 13]" in out.decode():
                        print(f"Failed installation of {dep}\nError: PermissionError: [Errno 13]...\nSkipping!")
                        failed_pkgs += 1
                    elif f"Successfully installed {dep}" in out.decode():
                        print(f"Successfully installed {dep}")
                        current_pkg += 1
                        successful += 1
                    elif f"Requirement already satisfied: {dep}" in out.decode():
                        print(f"Was already installed {dep}")
                        current_pkg += 1
                        successful += 1
                    else:
                        print(f"""Something went wrong whilst installing "{dep}"\nI suggest you try to install it manually: "pip3 install {dep}" """)
                        failed_pkgs += 1
                except CalledProcessError as e:
                    e.returncode
            return {
                "success":successful, "failed":failed_pkgs, "total":len(Dependencies.deps)}
        results = pkgs()
        print(f"""{results["success"]} dependencies were successfully installed!""")
        print(f"""{results["failed"]} dependencies failed to be installed""")
        input("Press enter / enter something")
        if results["failed"] > 0:
            print(f"Some package failed to install. As a result, Nukebot is lacking required dependencies.")
            print(f"You should try to install the following dependencies by yourself:\n--> colorama\n--> disnake\nQUITTING!")
            quit(1)