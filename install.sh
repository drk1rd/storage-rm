#!/usr/bin/env bash
# Installs storage-rm into /usr/local/bin (or ~/.local/bin if that isn't writable).
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)/storage-rm"
dest="${PREFIX:-/usr/local}/bin"

if ! mkdir -p "$dest" 2>/dev/null || [[ ! -w $dest ]]; then
  dest="$HOME/.local/bin"
  mkdir -p "$dest"
fi

install -m 755 "$src" "$dest/storage-rm"
echo "Installed storage-rm to $dest/storage-rm"

case ":$PATH:" in
  *":$dest:"*) ;;
  *) echo "Note: $dest isn't on your PATH — add it to ~/.zshrc: export PATH=\"$dest:\$PATH\"" ;;
esac
