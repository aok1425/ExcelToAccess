# sets up the folders and such to make it like the video!

mv ./dist/tkinter_gui.exe "./dist/Validation Check.exe"
cp e2Boston_RsrPlus-empty.mdb ./dist/e2Boston_RsrPlus-empty.mdb
mv ./dist "./Validation Check program"
rm -rf ./build

# make all files in program folder hidden except for EXE
# make zip file out of folder