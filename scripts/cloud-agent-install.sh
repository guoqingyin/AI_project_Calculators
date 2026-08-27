#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for AI_project_Calculators.
set -euo pipefail

VENV="${AI_CALC_VENV:-/home/ubuntu/ai-calc-venv}"

# OpenCV / MediaPipe runtime libs (no-op when already present)
if command -v sudo >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    libegl1 libgl1 libglib2.0-0t64 libgomp1 libxcb-xinerama0 >/dev/null
fi

# Use system Python so --user install is not blocked by an active venv on PATH
/usr/bin/python3 -m pip install --user -q virtualenv
export PATH="${HOME}/.local/bin:${PATH}"

if [[ ! -x "${VENV}/bin/python" ]]; then
  "${HOME}/.local/bin/virtualenv" "${VENV}"
fi

# Prefer wrapper scripts over symlinks so pyvenv.cfg resolution works
mkdir -p "${HOME}/.local/bin"
for cmd in python python3 pip pip3; do
  cat > "${HOME}/.local/bin/${cmd}" <<EOF
#!/usr/bin/env bash
exec "${VENV}/bin/${cmd}" "\$@"
EOF
  chmod +x "${HOME}/.local/bin/${cmd}"
done

"${VENV}/bin/pip" install -U pip
# Core app + training extras. Install d2l without deps (its pins fight modern Python).
"${VENV}/bin/pip" install \
  numpy pandas opencv-python cvzone scikit-learn matplotlib seaborn mediapipe requests jupyter
"${VENV}/bin/pip" install torch torchvision --index-url https://download.pytorch.org/whl/cpu
"${VENV}/bin/pip" install d2l --no-deps

"${VENV}/bin/python" - <<'PY'
import cv2, cvzone, numpy, pandas, sklearn, torch, mediapipe
from cvzone.HandTrackingModule import HandDetector
from d2l import torch as d2l  # noqa: F401
print("install-ok", torch.__version__, cv2.__version__)
PY
