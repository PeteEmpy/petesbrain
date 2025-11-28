#!/bin/bash
# Syncs all project skills to user-level ~/.claude/skills/
# Run automatically or manually after adding new skills

SOURCE_DIR="/Users/administrator/Documents/PetesBrain/.claude/skills"
TARGET_DIR="$HOME/.claude/skills"

mkdir -p "$TARGET_DIR"

for skill in "$SOURCE_DIR"/*/; do
  skill_name=$(basename "$skill")
  if [ -d "$skill" ] && [ ! -L "$TARGET_DIR/$skill_name" ]; then
    ln -sf "$skill" "$TARGET_DIR/$skill_name"
    echo "Linked: $skill_name"
  fi
done
