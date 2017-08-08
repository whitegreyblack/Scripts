#!/usr/bin/env bash

function verse() {
  # save the current directory
  curr=$PWD
  [[ ! -d ~/Pictures/Verses ]] && mkdir ~/Pictures/Verses
  cd ~/Pictures/Verses
  curl --silent https://www.bible.com/verse-of-the-day |\
    grep "votd-image" |\
    grep -oh "/.*jpg" |\
    awk '{print "https:"$1 }' |\
    wget -i- > /dev/null 2>&1
  cd "$curr"
}
verse
