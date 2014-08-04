ps aux | grep fm.py |grep sample | tail -1 | tr -s [:space:] | cut -d " " -f 2 |xargs kill -9
