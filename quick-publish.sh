#!/bin/bash
# Quick publish helpers for common content types

case "$1" in
  tweet)
    python publish.py "$2" "$3" --platform "Twitter/X" --type "tweet" --tags "cardiology"
    ;;
  thread)
    python publish.py "$2" "$3" --platform "Twitter/X" --type "thread" --tags "cardiology"
    ;;
  youtube)
    python publish.py "$2" "$3" --platform "YouTube" --type "script" --tags "cardiology,hinglish"
    ;;
  newsletter)
    python publish.py "$2" "$3" --platform "Newsletter" --type "newsletter" --tags "cardiology"
    ;;
  *)
    echo "Usage: ./quick-publish.sh [type] [title] [content]"
    echo ""
    echo "Types:"
    echo "  tweet       - Single tweet"
    echo "  thread      - Twitter thread"
    echo "  youtube     - YouTube script"
    echo "  newsletter  - Email newsletter"
    echo ""
    echo "Example:"
    echo "  ./quick-publish.sh tweet \"Statins 101\" \"Content here...\""
    ;;
esac
