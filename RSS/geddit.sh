# Geddit - xml parser for reddit rss feeds
# author: Sam Whang | WGB

regex='(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'

function usage()
{
    echo "Beautify: an xml parser and printer written in bash"
    echo "usage: beatify [OPTIONS] [XML PATH]"
    echo
    echo "Options:"
    echo "      [-h] HELP"
    echo "      [-u] UPDATE"
    echo "      [-a] ADD"
}


if [[ $# -lt 1 ]]; then
    usage    
fi

while [[ $# -gt 1 ]]; do
    key=$1

    case $key in
        -p|--parse)
        echo "parse -- push mode -- line by line reading -- slow"
        shift
        ;;
        -d|--debug)
        echo "debug"
        shift
        ;;
        -f|--full)
        echo "parse"
        shift
        ;;
        -u|--update)
        echo "update"
        shift
        ;;
        -h|--help)
        echo "help"
        shift
        ;;
        -t|--time)
        echo "time"
        shift
        ;;
        *)
        ;;
    esac
    shift
done

if [[ $# -lt 1 ]]; then
  echo "no url to parse"
  exit
fi

echo "curling in $1"
if [[ $1 =~ $regex ]]; then
  echo " valid string"
  python -c "import xml.etree.ElementTree as tree; \
t=tree.parse('$1').getroot(); \
for post in t.findall('entry'): print(post.get('name'))"
fi
