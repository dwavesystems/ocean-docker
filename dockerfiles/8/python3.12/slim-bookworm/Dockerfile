#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "python generate.py dockerfiles"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        build-essential git \
    && pip install --no-cache-dir \
        dwave-ocean-sdk==8.3.0 \
    && apt-get remove -yq build-essential git \
    && apt-get autoremove -yq \
    && apt-get clean \
    && pip cache purge \
    && rm -rf /var/lib/apt/lists/* /tmp/*

CMD ["python"]
