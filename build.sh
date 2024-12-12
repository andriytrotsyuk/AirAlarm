set -e  # exit immediately if any command within the script returns a non-zero exit status
pyinstaller --add-data="src/_internal:." --add-data "linux/megaphone.svg:." src/airalarm.py
cp linux/root/* dist
cp LICENSE dist
name=airalarm_linux_v$1
mv dist "$name"
tar -zcvf "$name.tar.gz" "$name"
rm -r build
rm airalarm.spec
