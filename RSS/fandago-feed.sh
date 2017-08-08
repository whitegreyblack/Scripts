#!/usr/bin/env bash


function __setup() 
{
  # create cache table in sql
  # if already exists then skips
  # allows for corrupr or missing tables

  sqlite3 test.db "create table if not exists movies (id integer);"
}

function movies()
{
  if [[ "$#" == "0" ]]; then
    echo "yes"
  fi
}

movies "$@"
