if [[ $1 == "" ]]
then
  python -m unittest subunit.SubUnittest
else
  python -m unittest subunit.SubUnittest.$1
fi