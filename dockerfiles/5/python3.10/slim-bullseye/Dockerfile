#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "python generate.py dockerfiles"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

# pre-build wheels for installation in slim image
FROM python:3.10-bullseye as wheelhouse

RUN mkdir /wheels \
    && pip install -U pip setuptools wheel \
    && pip wheel -w /wheels dwave-ocean-sdk

FROM python:3.10-slim-bullseye

COPY --from=wheelhouse /wheels /tmp/wheels

RUN pip install --no-cache-dir --no-index -f /tmp/wheels/ \
        dwave-ocean-sdk==5.3.0 \
    && rm -rf /tmp/*

CMD ["python"]
