#!/bin/bash
# Install Windows XP Luna theme for XFCE
theme_dir=/usr/share/themes/LunaXPTP
icons_dir=/usr/share/icons/LunaIcons
mkdir -p "$theme_dir" "$icons_dir"
# Assume files are in project-xp-ai/theme/ (to be added)
cp -r ../theme/* "$theme_dir/"
cp -r ../icons/* "$icons_dir/"
# Set XFCE settings
xfconf-query --channel xfwm4 --property /general/theme --set "LunaXPTP"
xfconf-query --channel xsettings --property /Net/IconThemeName --set "LunaIcons"
