# ── PC (simulación) ──────────────────────────────────────────────
# 1. Levantar contenedor (construye imagen la primera vez, luego es instantáneo)
cd ~/Documents/raspbot-autonomy/docker && ./docker_ros2_pc.sh

# 2. Dentro del contenedor — publicar video de prueba
ros2 run raspbot_control image_publisher --ros-args -p source:=/root/ros2_ws/bottle.mp4

# 3. En otra terminal del contenedor — correr el follower
ros2 run raspbot_control bottle_follower

# ── Carrito (Raspberry Pi) ────────────────────────────────────────
# 1. Levantar contenedor (construye imagen la primera vez, luego es instantáneo)
cd ~/raspbot-autonomy/docker && ./docker_ros2.sh

# 2. Dentro del contenedor — correr el follower (bringup y cámara ya arrancan solos)
ros2 run raspbot_control bottle_follower