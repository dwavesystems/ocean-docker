# Ocean Docker Images

[Ocean](https://docs.dwavequantum.com/en/latest/ocean/) is
[D-Wave's](<https://www.dwavesys.com>) suite of tools for solving hard problems
with quantum computers.


## Build Matrix

- Ocean: [`9.1.0`](https://github.com/dwavesystems/dwave-ocean-sdk/releases/9.1.0)
- Python: `3.10`, `3.11`, `3.12`, `3.13` (default), `3.14`
- Platform:
    [`trixie`](https://wiki.debian.org/DebianTrixie) (default),
    `slim-trixie` (minimal trixie),
    `windowsservercore`


## Architectures

All Linux images are built for `amd64` and `arm64` architectures, and are available
as multi-arch docker images.

Windows images are build for `amd64` only.


## Supported tags, with `Dockerfile` links

Simple tags represent "canonical images" and their aliases. Each simple tag maps
to an image with specific ocean version, python version, and platform.
Architecture can be shared, though; Linux simple tags point to multi-arch images.

Shared tags map to multi-platform/multi-architecture images.

### Simple Tags

- [Ocean: `9.1.0`, Python: `3.10`, Platform: `slim-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.10/slim-trixie/Dockerfile)
  - `9-python3.10-slim`
  - `9-python3.10-slim-trixie`
  - `9.1-python3.10-slim`
  - `9.1-python3.10-slim-trixie`
  - `9.1.0-python3.10-slim`
  - `9.1.0-python3.10-slim-trixie`
  - `python3.10-slim`
  - `python3.10-slim-trixie`

- [Ocean: `9.1.0`, Python: `3.10`, Platform: `trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.10/trixie/Dockerfile)
  - `9-python3.10-trixie`
  - `9.1-python3.10-trixie`
  - `9.1.0-python3.10-trixie`
  - `python3.10-trixie`

- [Ocean: `9.1.0`, Python: `3.10`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.10/windowsservercore/Dockerfile)
  - `9-python3.10-windowsservercore`
  - `9.1-python3.10-windowsservercore`
  - `9.1.0-python3.10-windowsservercore`
  - `python3.10-windowsservercore`

- [Ocean: `9.1.0`, Python: `3.11`, Platform: `slim-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.11/slim-trixie/Dockerfile)
  - `9-python3.11-slim`
  - `9-python3.11-slim-trixie`
  - `9.1-python3.11-slim`
  - `9.1-python3.11-slim-trixie`
  - `9.1.0-python3.11-slim`
  - `9.1.0-python3.11-slim-trixie`
  - `python3.11-slim`
  - `python3.11-slim-trixie`

- [Ocean: `9.1.0`, Python: `3.11`, Platform: `trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.11/trixie/Dockerfile)
  - `9-python3.11-trixie`
  - `9.1-python3.11-trixie`
  - `9.1.0-python3.11-trixie`
  - `python3.11-trixie`

- [Ocean: `9.1.0`, Python: `3.11`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.11/windowsservercore/Dockerfile)
  - `9-python3.11-windowsservercore`
  - `9.1-python3.11-windowsservercore`
  - `9.1.0-python3.11-windowsservercore`
  - `python3.11-windowsservercore`

- [Ocean: `9.1.0`, Python: `3.12`, Platform: `slim-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.12/slim-trixie/Dockerfile)
  - `9-python3.12-slim`
  - `9-python3.12-slim-trixie`
  - `9.1-python3.12-slim`
  - `9.1-python3.12-slim-trixie`
  - `9.1.0-python3.12-slim`
  - `9.1.0-python3.12-slim-trixie`
  - `python3.12-slim`
  - `python3.12-slim-trixie`

- [Ocean: `9.1.0`, Python: `3.12`, Platform: `trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.12/trixie/Dockerfile)
  - `9-python3.12-trixie`
  - `9.1-python3.12-trixie`
  - `9.1.0-python3.12-trixie`
  - `python3.12-trixie`

- [Ocean: `9.1.0`, Python: `3.12`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.12/windowsservercore/Dockerfile)
  - `9-python3.12-windowsservercore`
  - `9.1-python3.12-windowsservercore`
  - `9.1.0-python3.12-windowsservercore`
  - `python3.12-windowsservercore`

- [Ocean: `9.1.0`, Python: `3.13`, Platform: `slim-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.13/slim-trixie/Dockerfile)
  - `9-python3.13-slim`
  - `9-python3.13-slim-trixie`
  - `9-slim`
  - `9-slim-trixie`
  - `9.1-python3.13-slim`
  - `9.1-python3.13-slim-trixie`
  - `9.1-slim`
  - `9.1-slim-trixie`
  - `9.1.0-python3.13-slim`
  - `9.1.0-python3.13-slim-trixie`
  - `9.1.0-slim`
  - `9.1.0-slim-trixie`
  - `python3.13-slim`
  - `python3.13-slim-trixie`
  - `slim`
  - `slim-trixie`

- [Ocean: `9.1.0`, Python: `3.13`, Platform: `trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.13/trixie/Dockerfile)
  - `9-python3.13-trixie`
  - `9-trixie`
  - `9.1-python3.13-trixie`
  - `9.1-trixie`
  - `9.1.0-python3.13-trixie`
  - `9.1.0-trixie`
  - `python3.13-trixie`
  - `trixie`

- [Ocean: `9.1.0`, Python: `3.13`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.13/windowsservercore/Dockerfile)
  - `9-python3.13-windowsservercore`
  - `9-windowsservercore`
  - `9.1-python3.13-windowsservercore`
  - `9.1-windowsservercore`
  - `9.1.0-python3.13-windowsservercore`
  - `9.1.0-windowsservercore`
  - `python3.13-windowsservercore`
  - `windowsservercore`

- [Ocean: `9.1.0`, Python: `3.14`, Platform: `slim-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.14/slim-trixie/Dockerfile)
  - `9-python3.14-slim`
  - `9-python3.14-slim-trixie`
  - `9.1-python3.14-slim`
  - `9.1-python3.14-slim-trixie`
  - `9.1.0-python3.14-slim`
  - `9.1.0-python3.14-slim-trixie`
  - `python3.14-slim`
  - `python3.14-slim-trixie`

- [Ocean: `9.1.0`, Python: `3.14`, Platform: `trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.14/trixie/Dockerfile)
  - `9-python3.14-trixie`
  - `9.1-python3.14-trixie`
  - `9.1.0-python3.14-trixie`
  - `python3.14-trixie`

- [Ocean: `9.1.0`, Python: `3.14`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.14/windowsservercore/Dockerfile)
  - `9-python3.14-windowsservercore`
  - `9.1-python3.14-windowsservercore`
  - `9.1.0-python3.14-windowsservercore`
  - `python3.14-windowsservercore`


### Shared Tags

- `9-python3.10`, `9.1-python3.10`, `9.1.0-python3.10`, `python3.10`
  - [`9.1.0-python3.10-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.10/trixie/Dockerfile)
  - [`9.1.0-python3.10-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.10/windowsservercore/Dockerfile)

- `9-python3.11`, `9.1-python3.11`, `9.1.0-python3.11`, `python3.11`
  - [`9.1.0-python3.11-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.11/trixie/Dockerfile)
  - [`9.1.0-python3.11-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.11/windowsservercore/Dockerfile)

- `9-python3.12`, `9.1-python3.12`, `9.1.0-python3.12`, `python3.12`
  - [`9.1.0-python3.12-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.12/trixie/Dockerfile)
  - [`9.1.0-python3.12-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.12/windowsservercore/Dockerfile)

- `9`, `9-python3.13`, `9.1`, `9.1-python3.13`, `9.1.0`, `9.1.0-python3.13`, `latest`, `python3.13`
  - [`9.1.0-python3.13-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.13/trixie/Dockerfile)
  - [`9.1.0-python3.13-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.13/windowsservercore/Dockerfile)

- `9-python3.14`, `9.1-python3.14`, `9.1.0-python3.14`, `python3.14`
  - [`9.1.0-python3.14-trixie`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.14/trixie/Dockerfile)
  - [`9.1.0-python3.14-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/9/python3.14/windowsservercore/Dockerfile)



## License

Ocean is released under the Apache License 2.0.

Ocean dockerfiles (in this repo) are released under the Apache License 2.0 as well.
See [LICENSE](./LICENSE) file.

However, bear in mind that docker images in general contain other software which
may be under other licenses. It is the image user's responsibility to ensure
that any use of this image complies with any relevant licenses for all software
contained within.
