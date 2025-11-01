set -e  # exit immediately if any command within the script returns a non-zero exit status
pyinstaller \
  --add-data="src/_internal:." \
  --add-data "linux/AirAlarmIcon.svg:." \
  --hidden-import "PIL._tkinter_finder" \
  src/airalarm.py
name=AirAlarm-$1
cp LICENSE dist/airalarm
mkdir -p "$name/opt"
mv dist/airalarm "$name/opt/AirAlarm"
mkdir -p "$name/DEBIAN"
cp linux/control "$name/DEBIAN"
cp linux/preinst "$name/DEBIAN"
chmod 0755 "$name/DEBIAN/preinst"
cp linux/postrm "$name/DEBIAN"
chmod 0755 "$name/DEBIAN/postrm"
mkdir -p "$name/usr/share/applications"
cp linux/airalarm.desktop "$name/usr/share/applications"
mkdir -p "$name/usr/share/icons/hicolor/scalable/apps"
cp linux/AirAlarmIcon.svg "$name/usr/share/icons/hicolor/scalable/apps"
dpkg-deb --build "$name"
rm -r dist
rm -r build
rm airalarm.spec
rm -r "$name"
