#!/usr/bin/env bash
# naive rss/xml parser

__parsetag()
{
  local IFS='>'
  read -d '<' TAG VAL
}
__cdata_clean()
{
  echo
}
curl --silent $1 | while __parsetag ; do
  case $TAG in
    'item')
      name=''
      link=''
      desc=''
      date=''
      tag=''
      ;;
    'title')
      tag="name"
      ;;
    'link')
      tag="link"
      ;;
    'description')
      tag="desc"
      ;;
    'pubDate')
      tag="date"
      echo "$TAG: $VAL"
      ;;
    ![\[A-TA[Step]]
      case $tag in
        'name')
          echo "$TAG: $val"
          echo "title:{$val}"
      esac
      ;;
    '/item')
      echo "item: /item"
      ;;
  esac
done
