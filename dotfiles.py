import os, sys
import subprocess

# specify dotfiles here, more info with:
# python3 dotfiles.py --help
dotfiles: list = [
    "~/.config/fish",
    "~/.config/polybar",
    "~/.config/i3",
    "~/.config/MangoHud",
    "~/.config/alacritty",
    "~/.config/picom.conf",
    "~/.config/Kvantum",
    "~/.config/qt5ct",
    "~/.config/qt6ct",
    "~/.config/dotfiles",
    "~/.config/frogminer",
    "~/.config/dunst",
    "~/.profile",
    "~/.bashrc",
    "~/.config/wallpapers",
    "~/.local/bin",
    "~/.config/betterlockscreen"
]


# optional dependency presets for auto installation of
# dependencies for certain configs
dependencyInstallCommand: list = ["yay", "-S", "--needed"]
dependencyGroups: dict = {
    "i3wm":     ["i3", "picom", "polybar", "dunst", "greenclip", "feh", "xidlehook"],
    "qtTheme":  ["kvantum"],
    "fish":     ["fish", "fisher", "eza", "bat"],
    "fonts":    ["ttf-meslo-nerd-font-powerlevel10k", "ttf-dejavu"]
}


def linkDotfiles(dotfiles: list) -> None:
    for file in dotfiles:
        # infering location of dotfiles in current repo, and getting fullpath of locatoin to symlink
        repositoryLocation: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.basename(file))
        systemLocation: str = os.path.expanduser(file)

        try:
            os.symlink(repositoryLocation, systemLocation)
            print(f"✔️ > Symlinked {repositoryLocation} to {systemLocation}")
        except FileExistsError:
            print(f"❌> Symlinked {repositoryLocation} to {systemLocation}")


def installGroups(installCommand: str, groupsToInstall: list):
    # removing nested lists
    packages: list = sum(groupsToInstall, [])

    # installing group
    print(subprocess.run(installCommand + packages, shell=False))


def handleCLI(parameters: list) -> None:
    helpMessage = """Simple dotfile manager script:
  restore               links filepaths specified in 'dotfiles' list. '❌' means path already exists, '✔️ ' means symlink was succesfull
  ig | install-group    installs groups of dependencies specified under 'dependencyGroups', command to install specified under 'dependencyInstallCommand'

To add dotfiles:
  'mv' them to the repository location, and then list them under 'dotfiles' list.
       do NOT nest or change their names, this script looks in its own directory
       for the file/directory names of the paths in 'dotfiles' list
"""
    # printing help message and returning if parameters are empty
    if not parameters:
        print(helpMessage)
        return

    # handling CLI, stripping all '-' from beginning
    match parameters[0].lstrip('-'):
        case "restore":
            linkDotfiles(dotfiles)
        case "ig" | "install-group":
            installCommand: list = dependencyInstallCommand
            # installing all groups listed after install-group
            try:
                groupsToInstall: list = [dependencyGroups[g] for g in parameters[1:]]
                if not groupsToInstall:
                    print("No groups specified, exiting.")
                    sys.exit(1)

                installGroups(installCommand, groupsToInstall)
            except KeyError:
                print("Invalid group name.")
                sys.exit(1)
        case _:
            print(helpMessage)



if __name__ == "__main__":
    handleCLI(sys.argv[1:])
