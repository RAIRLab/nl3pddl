
if [ "$#" -eq 2  ]; then
    ./submodules/VAL/build/bin/Validate -v ./data/domains/$1 ./data/domains/$2
fi

if [ "$#" -eq 3  ]; then
    ./submodules/VAL/build/bin/Validate -v ./data/domains/$1 ./data/domains/$2 ./data/domains/$3
fi

