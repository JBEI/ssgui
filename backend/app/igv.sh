#!/bin/bash
#set -euo pipefail
set -x

echo 'igv.sh process launched with PID: ' $$

# Note, cannot use xvfb-run --auto-servernum because
# xvfb-run does not exit nicely and hard to find PID
# https://unix.stackexchange.com/a/311599
find_free_servernum() {
    i=10
    while [ -f /tmp/.X$i-lock ]; do
        i=$(($i + 1))
    done
    echo $i
}
DISPLAY_ID=$(find_free_servernum)
Xvfb :$DISPLAY_ID &
X_PID=$!
echo 'Xvfb process launched with PID: ' $X_PID

echo 'Batch file contents: ' "${1}"
cat "${1}"

prefix=`dirname $(readlink $0 || echo $0)`
DISPLAY=:$DISPLAY_ID java -showversion --module-path="${prefix}/lib" -Xmx3g \
    @"${prefix}/igv.args" \
    -Dapple.laf.useScreenMenuBar=true \
    -Djava.net.preferIPv4Stack=true \
    --module=org.igv/org.broad.igv.ui.Main -b "${1}" &
JAVA_PID=$!

echo 'igv java process launched with PID: ' $JAVA_PID
wait $JAVA_PID
echo 'igv java process finished with PID: ' $JAVA_PID

kill -9 $X_PID
kill -9 $JAVA_PID
rm "/tmp/.X${DISPLAY_ID}-lock"
echo 'Xvfb process finished with PID: ' $X_PID
