#!/bin/bash
set -e

APP_NAME="spotifetch"
INSTALL_DIR="$HOME/.spotifetch"
SCRIPT_NAME="spotifetch.py"
VENV_DIR="$INSTALL_DIR/venv"
LAUNCHER="$HOME/.local/bin/$APP_NAME"

echo "-> Creating app directory at $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

echo "-> Creating virtual environment at $VENV_DIR"
python3 -m venv "$VENV_DIR/venv"

echo "-> Activating venv and installing dependencies"
source "$VENV_DIR/venv/bin/activate"

pip install --upgrade pip
pip install spotipy flask pkce requests
deactivate

echo "-> Copying your script to $INSTALL_DIR"
cp "$SCRIPT_NAME" "$INSTALL_DIR/$SCRIPT_NAME"
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

echo "-> Creating launcher at $LAUNCHER"
mkdir -p "$(dirname "$LAUNCHER")"

cat > "$LAUNCHER" <<EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"
python "$INSTALL_DIR/$SCRIPT_NAME" "\$@"
deactivate
EOF

chmod +x "$LAUNCHER"

# Add ~/.local/bin to PATH if missing
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
  echo "-> Added ~/.local/bin to PATH. Run: source ~/.bashrc"
fi

alias spotifetch='source ~/.spotifetch/venv/bin/activate && ~/.local/bin/spotifetch'
echo "-> Crated 'spotifetch' alias"
echo "✅ Spotifetch installed! Run spotifetch --help for a list of commands"
