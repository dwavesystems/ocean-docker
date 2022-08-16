# Ocean Docker Images

[Ocean](https://docs.ocean.dwavesys.com/en/stable) is
[D-Wave's](<https://www.dwavesys.com>) suite of tools for solving hard problems
with quantum computers.

## Build Matrix

- Ocean: [`latest`](https://github.com/dwavesystems/dwave-ocean-sdk/releases)
- Python: `3.8` (except on Windows), `3.9`, `3.10`
- Platform: [`bullseye`](https://wiki.debian.org/DebianBullseye), `slim` (minimal bullseye), `windowsservercore`

## Architectures

All Linux images are built for `amd64` and `arm64` architectures, and are available
as multi-arch docker images.

Windows images are build for `amd64` only.

## Canonical Tags (Single-platform) with Aliases

```
5.3.0-python3.8-bullseye:
  5-python3.8-bullseye, 5.3-python3.8-bullseye, python3.8-bullseye

5.3.0-python3.8-slim-bullseye:
  5-python3.8-slim, 5-python3.8-slim-bullseye, 5.3-python3.8-slim, 5.3-python3.8-slim-bullseye, 5.3.0-python3.8-slim, python3.8-slim, python3.8-slim-bullseye

5.3.0-python3.9-bullseye:
  5-bullseye, 5-python3.9-bullseye, 5.3-bullseye, 5.3-python3.9-bullseye, 5.3.0-bullseye, bullseye, python3.9-bullseye

5.3.0-python3.9-slim-bullseye:
  5-python3.9-slim, 5-python3.9-slim-bullseye, 5-slim, 5-slim-bullseye, 5.3-python3.9-slim, 5.3-python3.9-slim-bullseye, 5.3-slim, 5.3-slim-bullseye, 5.3.0-python3.9-slim, 5.3.0-slim, 5.3.0-slim-bullseye, python3.9-slim, python3.9-slim-bullseye, slim, slim-bullseye

5.3.0-python3.9-windowsservercore:
  5-python3.9-windowsservercore, 5-windowsservercore, 5.3-python3.9-windowsservercore, 5.3-windowsservercore, 5.3.0-windowsservercore, python3.9-windowsservercore, windowsservercore

5.3.0-python3.10-bullseye:
  5-python3.10-bullseye, 5.3-python3.10-bullseye, python3.10-bullseye

5.3.0-python3.10-slim-bullseye:
  5-python3.10-slim, 5-python3.10-slim-bullseye, 5.3-python3.10-slim, 5.3-python3.10-slim-bullseye, 5.3.0-python3.10-slim, python3.10-slim, python3.10-slim-bullseye

5.3.0-python3.10-windowsservercore:
  5-python3.10-windowsservercore, 5.3-python3.10-windowsservercore, python3.10-windowsservercore
```

## Shared Tags (Multi-platform)

```
latest, 5, 5.3, 5.3.0, python3.9, 5-python3.9, 5.3-python3.9, 5.3.0-python3.9:
  5.3.0-python3.9-bullseye
  5.3.0-python3.9-windowsservercore

python3.10, 5-python3.10, 5.3-python3.10, 5.3.0-python3.10:
  5.3.0-python3.10-bullseye
  5.3.0-python3.10-windowsservercore
```

## License

Ocean is released under the Apache License 2.0.

Ocean dockerfiles (in this repo) are released under the Apache License 2.0 as well.
See [LICENSE](./LICENSE) file.

However, bear in mind that docker images in general contain other software which
may be under other licenses. It is the image user's responsibility to ensure
that any use of this image complies with any relevant licenses for all software
contained within.
