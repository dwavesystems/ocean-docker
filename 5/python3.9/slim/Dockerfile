ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim-bullseye

## skip in slim
# RUN apt-get update \
#     && apt-get install -yq --no-install-recommends \
#         build-essential \
#         man-db \
#         htop \
#         less \
#         vim \
#         curl \
#         git \
#     && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

ARG OCEAN_VERSION

RUN pip install --no-cache-dir \
        dwave-ocean-sdk==${OCEAN_VERSION} \
    && rm -rf /tmp/*

## skip in slim
# RUN pip install --no-cache-dir \
#         ipython \
#     && rm -rf /tmp/*

CMD ["python"]
