#!/bin/bash
# Register AI assistant in autostart
mkdir -p /etc/xdg/autostart
cat > /etc/xdg/autostart/ai-assistant.desktop <<'EOF'
[Desktop Entry]
Name=AI Assistant
Exec=/usr/local/bin/ai_assistant.py
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
EOF
