#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "python generate.py dockerfiles"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM python:3.8-bullseye

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        build-essential \
        man-db \
        curl \
        htop \
        less \
        git \
        vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

RUN pip install --no-cache-dir \
        dwave-ocean-sdk==7.1.0 \
    && rm -rf /tmp/*

RUN pip install --no-cache-dir \
        ipython \
    && rm -rf /tmp/*

CMD ["python"]
