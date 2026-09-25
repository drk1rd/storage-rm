# storage-rm

Find and clear the stuff that quietly eats a Mac developer's disk: Docker build cache, Xcode DerivedData, Gradle/npm/pnpm/brew caches, app caches, old emulators and stale `node_modules`.

Everything it removes by default gets rebuilt automatically when it's needed again. It's a single bash script that works with the stock macOS bash 3.2 and has no dependencies.

```text
$ storage-rm
==> Scanning (nothing is deleted)…

  CATEGORY          SIZE  WHAT
  docker           40.1G  Docker build cache + dangling images (containers and volumes kept)
  xcode            12.3G  Xcode DerivedData, older iOS DeviceSupport, simulator caches, unavailable simulators
  gradle            6.8G  Gradle caches, daemon logs, old wrapper distributions
  app-caches        8.9G  App caches: Spotify, browsers, Electron, Playwright, Steam, Epic, …
  ...
  clean would free about 77.4G
```

## Install

```bash
git clone https://github.com/drk1rd/storage-rm.git && cd storage-rm && ./install.sh
```

This installs to `/usr/local/bin`, or to `~/.local/bin` if `/usr/local/bin` isn't writable. You can also just run `./storage-rm` from the repo.

## Usage

```bash
storage-rm                          # scan: show what each category would free (deletes nothing)
storage-rm clean                    # clear the default categories, asks first
storage-rm clean -y                 # same, no prompt (for cron/launchd)
storage-rm clean -n                 # dry run: list every path it would remove
storage-rm clean -o docker,xcode    # only some categories
storage-rm clean -s app-caches      # everything except some
storage-rm clean -o node-modules --days 60   # stale node_modules (opt-in)
storage-rm big 30                   # 30 largest folders in your home
storage-rm list                     # describe all categories
```

## Categories

| Category | What goes | Default |
|---|---|---|
| `docker` | `docker builder prune -af` + dangling images. Containers and volumes are never touched. | yes |
| `xcode` | DerivedData, simulator caches, older iOS DeviceSupport (keeps the newest per device model), unavailable simulators | yes |
| `gradle` | `~/.gradle/caches`, daemon logs, wrapper distributions except the newest 2 (`--keep-gradle N`) | yes |
| `npm` / `pnpm` / `yarn` / `pip` / `cocoapods` | package manager caches | yes |
| `brew` | `brew cleanup -s --prune=all` | yes |
| `app-caches` | Spotify, Firefox, Chrome, Brave, Edge, Playwright browsers, Electron, Steam, Epic, … Skips apps that are running unless `--force`. | yes |
| `claude` | Claude desktop app simulator builds | yes |
| `android-avd` | Android emulators and SDK system images | opt-in |
| `node-modules` | `node_modules` in projects with no file changed in `--days` (default 30), searched under `~/Documents ~/Developer ~/code ~/Projects ~/dev ~/src` or `--roots a:b` | opt-in |
| `trash` | empties `~/.Trash` | opt-in |

Opt-in categories only run when you name them with `-o` or pass `--all`.

## Safety

- `scan` and `clean -n` never delete anything.
- `clean` shows the plan with sizes and asks before deleting, unless you pass `-y`.
- It refuses to delete anything outside your home folder.
- Read-only cached files are unlocked before removal. Anything macOS still protects is reported rather than forced.
- Some folders (such as `~/.Trash`, or caches holding `.app` bundles) need Full Disk Access or App Management for your terminal in System Settings → Privacy & Security.

## Run it automatically

Weekly via cron (Sunday 10:00):

```bash
(crontab -l 2>/dev/null; echo "0 10 * * 0 /usr/local/bin/storage-rm clean -y >> ~/Library/Logs/storage-rm.log 2>&1") | crontab -
```

## License

MIT
