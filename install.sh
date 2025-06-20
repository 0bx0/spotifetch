#!/bin/bash

APP_NAME="spotifetch"
INSTALL_DIR="$HOME/.spotifetch"
SCRIPT_NAME="spotifetch.py"
LAUNCHER="$HOME/.local/bin/$APP_NAME"
REQ_FILE="$(dirname "$0")/req.txt"
echo "-> Installing dependencies"
pip3 install --user --upgrade pip
pip3 install --user -r "$REQ_FILE"
echo "-> Copying script to $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_NAME" "$INSTALL_DIR/$SCRIPT_NAME"
echo "-> Creating launcher at $LAUNCHER"
mkdir -p "$HOME/.local/bin"
cat > "$LAUNCHER" <<EOF
#!/bin/bash
python3 "$INSTALL_DIR/$SCRIPT_NAME" "\$@"
EOF

chmod +x "$LAUNCHER"
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi
source ~/.bashrc
echo "👉 Type: spotifetch --help"