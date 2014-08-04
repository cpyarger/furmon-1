#!/bin/bash
# pflint
# transfer furmon monitor to docbox...
cat out.html |sed 's|url=http://10.0.1.45/furmon/out.html|http://docbox.flint.com/~flint/furmon/furmon.html|g' > furmon.html
# scp furmon.html flint@docbox.flint.com:./public_html/furmon/furmon.html


