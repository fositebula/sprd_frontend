for f in `find . -name __pycache__`
do
rm $f -d
done
