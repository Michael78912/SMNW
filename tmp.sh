git clone https://github.com/michael78912/smnw-archives
cd smnw-archives
git init
echo copying archives...
cp ../Archives/* .
git add *
git commit -m "updated archives"
git push origin master
cd ..
rm smnw-archives/*
rm -r smnw-archives
