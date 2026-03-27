FROM yahboomtechnology/ros-humble:0.1.0

# Install system deps
RUN apt-get update -qq && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install heavy Python deps once (ARM-compatible wheels from PyPI)
RUN python3 -m pip install --no-cache-dir \
      torch torchvision && \
    python3 -m pip install --no-cache-dir \
      ultralytics opencv-python-headless

ENTRYPOINT ["/root/entrypoint.sh"]
