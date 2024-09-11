#!/bin/bash

declare -A param
while IFS='=' read -r -d '&' key value && [[ -n "$key" ]]; do
    param["$key"]=$value
done <<< "$(cat /dev/stdin)&"

alias urldecode=''

url=$(echo "${param[url]}" | sed "s@+@ @g;s@%@\\\\x@g" | xargs -0 printf "%b")
title=$(echo "${param[title]}" | sed "s@+@ @g;s@%@\\\\x@g" | xargs -0 printf "%b")

/usr/alifeee/thermalprinter/env/bin/python /usr/alifeee/thermalprinter/qr.py -t "${title}" -url "${url}"

echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<h1>Printed!</h1>
<p>Title: <b>'"${title}"'</b></p>
<p>URL: <a href="'"${url}"'">'"${url}"'</a></p>
<p><a href="javascript:history.back()">Back</a></p>
</body>
</html>
'
