#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "python generate.py dockerfiles"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM python:3.12-windowsservercore

# Install Microsoft Visual C++ Build Tools (required for source install of some ocean packages)
RUN Invoke-WebRequest -Uri https://aka.ms/vs/17/release/vs_BuildTools.exe -OutFile vs_BuildTools.exe; \
    \
    Start-Process vs_BuildTools.exe -Wait -NoNewWindow -PassThru \
        # arguments: https://learn.microsoft.com/en-us/visualstudio/install/use-command-line-parameters-to-install-visual-studio
        # (note the importance of --quiet, --wait and --norestart in automated non-gui flows!)
        -ArgumentList @( \
            '--quiet', '--wait', '--norestart', '--nocache', \
            # components: https://learn.microsoft.com/en-us/visualstudio/install/workload-component-id-vs-build-tools
            '--add', 'Microsoft.VisualStudio.Workload.VCTools;includeRecommended' \
        ); \
    \
    Remove-Item vs_BuildTools.exe -Force

RUN pip install --no-cache-dir \
        dwave-ocean-sdk==9.1.0

CMD ["python"]
