cp -r airalarm ~/.local/opt/
mkdir -p ~/.local/share/applications/
cp airalarm.desktop ~/.local/share/applications/
sed -i "2iIcon=$HOME/.local/opt/airalarm/megaphone.svg\nExec=$HOME/.local/opt/airalarm/airalarm" ~/.local/share/applications/airalarm.desktop
