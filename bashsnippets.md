# Bash Scripts

#### Read file and skip empty lines and comments
```sh
while read -r line; do
  # skip empty lines
  [[ -n "${line// /}" ]] || continue
  # skip comments
  [[ "${line// /}" == '#'* ]] || continue
done < file.txt
```
or
```sh
while read -r line || [[ -n "$line" ]] || [[ "${line// /}" == "#"* ]]; do
  # read stuff
done < file.txt
```

#### Get and download a picture verse
```sh
[[ -d ~/Pictures/Verses ]] && cd ~/Pictures/Verses || return
curl --silent https://www.bible.com/verse-of-the-day |\
  grep "votd-image" |\
  grep -oh "/.*jpg" |\
  awk '{print "https:"$1 }' |\
  wget -i- > /dev/null 2>&1
```

#### Create a Github allowable repo for python (untested)
```sh
while IFS='==' read -a line || [[ -n "$line" ]]; do
  echo "${line[0]}"
  while IFS=':' read -a package || [[ -n "$package" ]]; do
    old=""
    new=""
    if [[ "${package[0]}" == "  INSTALLED" ]]; then
      old="${package[2]}"
    elif [[ "${package[0]}" == "  LATEST" ]]; then
      new="${package[2]}"
    fi
    if [[ ! "$old" == "" && ! "$new" == "" && "$new" != "$old" ]]; then
      echo "installing ${package[0]} $old $new"
      pip install "${package[0]}"
    fi
  done <<< "$(pip search ${line[0]})"
done <<< "$(pip freeze)"
```

#### Print Github branch name only
```sh
if [[ -d "$PWD"/.git ]]; then
  alias twig='git symbolic-ref --short -q HEAD'
fi
```

#### Refresh bashrc or bash_aliases in shell
```sh
. ~/.bashrc
. ~/.bash_aliases
```

#### Get local movie listings
```sh
echo " --- Valley City Listings --- " && \
curl --silent http://bison6cinema.com/valley-city/ |\
  grep -o '<h4 class=\"heading14\">.*</h4>' |\
  sed 's/\(<h4 class=\"heading14\">\|<\/h4>\)//g' && \
echo && \
echo " ---  Jamestown Listings  --- " && \
curl --silent http://bison6cinema.com |\
  grep -o '<h4 class=\"heading18\">.*</h4>' |\
  sed 's/\(<h4 class=\"heading18\">\|<\/h4>\)//g'
```
updated:
```sh
echo " --- Valley City Listings --- "
curl --silent http://bison6cinema.com/valley-city/ |\
  grep -o '<h4 class=\"heading14\">.*</h4>' |\
  sed 's/\(<[^\>]*>\|<\/[^\>]*>\)//g'

echo
echo " ---  Jamestown Listings  --- "
jt=$(curl --silent http://bison6cinema.com)
grep -o '18\">.*</' <<< "$jt" | sed 's/\<[^\>]*>\|<\///g'

echo
echo " ---    Upcoming Movie    --- "
grep -o '<span>.*</span>' <<< "$jt" | sed 's/\(<[^\>]*>\|<br.*>\)//g' 
```
