#!/bin/bash
# Copy AI script to /usr/local/bin
echo "Copying ai_assistant.py"
cp ../hooks/chroot_local-packages/99-ai-start.sh /usr/local/bin/ai_assistant.py
chmod +x /usr/local/bin/ai_assistant.py
