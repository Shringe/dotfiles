import os

# In order to use:
# move dotfiles/folders to this repo, then add the location for them
# in this list
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
    "~/.config/frogminer"
    
]


for file in dotfiles:
    # infering location of dotfiles in current repo, and getting fullpath of locatoin to symlink
    repositoryLocation: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.basename(file))
    systemLocation: str = os.path.expanduser(file)

    try:
        os.symlink(repositoryLocation, systemLocation)
        print(f"✔️ > Symlinked {repositoryLocation} to {systemLocation}")
    except FileExistsError:
        print(f"❌> Symlinked {repositoryLocation} to {systemLocation}")
