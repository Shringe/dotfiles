source $HOME/.profile
if status is-interactive
    # Commands to run in interactive sessions can go here
    # alias ls='colorls'

    # eza package must be installed
    alias ls="eza --icons --group-directories-first"
end
