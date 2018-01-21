

#!/bin/bash

which ag >/dev/null 2>&1
if [ "$?" -ne "0" ]; then
    echo 'ag (the silver searcher) not found'
    exit 1
fi

echo 'Searching for potentially unused templates.'
echo 'This will take a long time. Why not get some cookies in the meantime?'
echo
find fossir/legacy/webinterface/tpls/ -maxdepth 1 -name '*.tpl' -exec sh -c 'TPL=$(basename {} .tpl); ag -c --nofilename --silent --ignore fossir/translations/ --ignore ext_modules/ $TPL > /dev/null || echo "UNUSED: $TPL"' \;
