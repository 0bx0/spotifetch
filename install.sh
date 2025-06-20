#!/bin/bash

set -e

APP_NAME="spotifetch"
INSTALL_DIR="$HOME/.spotifetch"
VENV_DIR="$INSTALL_DIR/venv"
SCRIPT_NAME="spotifetch.py"
LAUNCHER="$HOME/.local/bin/$APP_NAME"

echo "-> Creating virtual environment at $VENV_DIR"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "-> Installing dependencies"
pip install --upgrade pip
pip install -r req.txt

echo "-> Copying script to $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_NAME" "$INSTALL_DIR/$SCRIPT_NAME"

echo "-> Creating launcher at $LAUNCHER"
mkdir -p "$HOME/.local/bin"

cat > "$LAUNCHER" <<EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"
python "$INSTALL_DIR/$SCRIPT_NAME" "\$@"
EOF

chmod +x "$LAUNCHER"

echo "Spotifetch has been installed successfully!"
echo "Type Spotifetch --help for help"
