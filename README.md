# Ocean Docker Images

[Ocean](https://docs.ocean.dwavesys.com/en/stable) is
[D-Wave's](<https://www.dwavesys.com>) suite of tools for solving hard problems
with quantum computers.


## Build Matrix

- Ocean: [`6.9.0`](https://github.com/dwavesystems/dwave-ocean-sdk/releases/6.9.0)
- Python: `3.8` (except on `windowsservercore`), `3.9`, `3.10`, `3.11` (default), `3.12`
- Platform: [`bullseye`](https://wiki.debian.org/DebianBullseye), `slim` (minimal bullseye), `windowsservercore`


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

- [Ocean: `6.9.0`, Python: `3.8`, Platform: `bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.8/bullseye/Dockerfile)
  - `6-python3.8-bullseye`
  - `6.9-python3.8-bullseye`
  - `6.9.0-python3.8-bullseye`
  - `python3.8-bullseye`

- [Ocean: `6.9.0`, Python: `3.8`, Platform: `slim-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.8/slim-bullseye/Dockerfile)
  - `6-python3.8-slim`
  - `6-python3.8-slim-bullseye`
  - `6.9-python3.8-slim`
  - `6.9-python3.8-slim-bullseye`
  - `6.9.0-python3.8-slim`
  - `6.9.0-python3.8-slim-bullseye`
  - `python3.8-slim`
  - `python3.8-slim-bullseye`

- [Ocean: `6.9.0`, Python: `3.9`, Platform: `bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.9/bullseye/Dockerfile)
  - `6-python3.9-bullseye`
  - `6.9-python3.9-bullseye`
  - `6.9.0-python3.9-bullseye`
  - `python3.9-bullseye`

- [Ocean: `6.9.0`, Python: `3.9`, Platform: `slim-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.9/slim-bullseye/Dockerfile)
  - `6-python3.9-slim`
  - `6-python3.9-slim-bullseye`
  - `6.9-python3.9-slim`
  - `6.9-python3.9-slim-bullseye`
  - `6.9.0-python3.9-slim`
  - `6.9.0-python3.9-slim-bullseye`
  - `python3.9-slim`
  - `python3.9-slim-bullseye`

- [Ocean: `6.9.0`, Python: `3.9`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.9/windowsservercore/Dockerfile)
  - `6-python3.9-windowsservercore`
  - `6.9-python3.9-windowsservercore`
  - `6.9.0-python3.9-windowsservercore`
  - `python3.9-windowsservercore`

- [Ocean: `6.9.0`, Python: `3.10`, Platform: `bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.10/bullseye/Dockerfile)
  - `6-python3.10-bullseye`
  - `6.9-python3.10-bullseye`
  - `6.9.0-python3.10-bullseye`
  - `python3.10-bullseye`

- [Ocean: `6.9.0`, Python: `3.10`, Platform: `slim-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.10/slim-bullseye/Dockerfile)
  - `6-python3.10-slim`
  - `6-python3.10-slim-bullseye`
  - `6.9-python3.10-slim`
  - `6.9-python3.10-slim-bullseye`
  - `6.9.0-python3.10-slim`
  - `6.9.0-python3.10-slim-bullseye`
  - `python3.10-slim`
  - `python3.10-slim-bullseye`

- [Ocean: `6.9.0`, Python: `3.10`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.10/windowsservercore/Dockerfile)
  - `6-python3.10-windowsservercore`
  - `6.9-python3.10-windowsservercore`
  - `6.9.0-python3.10-windowsservercore`
  - `python3.10-windowsservercore`

- [Ocean: `6.9.0`, Python: `3.11`, Platform: `bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.11/bullseye/Dockerfile)
  - `6-bullseye`
  - `6-python3.11-bullseye`
  - `6.9-bullseye`
  - `6.9-python3.11-bullseye`
  - `6.9.0-bullseye`
  - `6.9.0-python3.11-bullseye`
  - `bullseye`
  - `python3.11-bullseye`

- [Ocean: `6.9.0`, Python: `3.11`, Platform: `slim-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.11/slim-bullseye/Dockerfile)
  - `6-python3.11-slim`
  - `6-python3.11-slim-bullseye`
  - `6-slim`
  - `6-slim-bullseye`
  - `6.9-python3.11-slim`
  - `6.9-python3.11-slim-bullseye`
  - `6.9-slim`
  - `6.9-slim-bullseye`
  - `6.9.0-python3.11-slim`
  - `6.9.0-python3.11-slim-bullseye`
  - `6.9.0-slim`
  - `6.9.0-slim-bullseye`
  - `python3.11-slim`
  - `python3.11-slim-bullseye`
  - `slim`
  - `slim-bullseye`

- [Ocean: `6.9.0`, Python: `3.11`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.11/windowsservercore/Dockerfile)
  - `6-python3.11-windowsservercore`
  - `6-windowsservercore`
  - `6.9-python3.11-windowsservercore`
  - `6.9-windowsservercore`
  - `6.9.0-python3.11-windowsservercore`
  - `6.9.0-windowsservercore`
  - `python3.11-windowsservercore`
  - `windowsservercore`

- [Ocean: `6.9.0`, Python: `3.12`, Platform: `bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.12/bullseye/Dockerfile)
  - `6-python3.12-bullseye`
  - `6.9-python3.12-bullseye`
  - `6.9.0-python3.12-bullseye`
  - `python3.12-bullseye`

- [Ocean: `6.9.0`, Python: `3.12`, Platform: `slim-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.12/slim-bullseye/Dockerfile)
  - `6-python3.12-slim`
  - `6-python3.12-slim-bullseye`
  - `6.9-python3.12-slim`
  - `6.9-python3.12-slim-bullseye`
  - `6.9.0-python3.12-slim`
  - `6.9.0-python3.12-slim-bullseye`
  - `python3.12-slim`
  - `python3.12-slim-bullseye`

- [Ocean: `6.9.0`, Python: `3.12`, Platform: `windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.12/windowsservercore/Dockerfile)
  - `6-python3.12-windowsservercore`
  - `6.9-python3.12-windowsservercore`
  - `6.9.0-python3.12-windowsservercore`
  - `python3.12-windowsservercore`


### Shared Tags

- `6-python3.9`, `6.9-python3.9`, `6.9.0-python3.9`, `python3.9`
  - [`6.9.0-python3.9-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.9/bullseye/Dockerfile)
  - [`6.9.0-python3.9-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.9/windowsservercore/Dockerfile)

- `6-python3.10`, `6.9-python3.10`, `6.9.0-python3.10`, `python3.10`
  - [`6.9.0-python3.10-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.10/bullseye/Dockerfile)
  - [`6.9.0-python3.10-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.10/windowsservercore/Dockerfile)

- `6`, `6-python3.11`, `6.9`, `6.9-python3.11`, `6.9.0`, `6.9.0-python3.11`, `latest`, `python3.11`
  - [`6.9.0-python3.11-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.11/bullseye/Dockerfile)
  - [`6.9.0-python3.11-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.11/windowsservercore/Dockerfile)

- `6-python3.12`, `6.9-python3.12`, `6.9.0-python3.12`, `python3.12`
  - [`6.9.0-python3.12-bullseye`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.12/bullseye/Dockerfile)
  - [`6.9.0-python3.12-windowsservercore`](https://github.com/dwavesystems/ocean-docker/blob/master/dockerfiles/6/python3.12/windowsservercore/Dockerfile)



## License

Ocean is released under the Apache License 2.0.

Ocean dockerfiles (in this repo) are released under the Apache License 2.0 as well.
See [LICENSE](./LICENSE) file.

However, bear in mind that docker images in general contain other software which
may be under other licenses. It is the image user's responsibility to ensure
that any use of this image complies with any relevant licenses for all software
contained within.
