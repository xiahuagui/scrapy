<?php

	if(!isset($_REQUEST['path']) || !($path = trim($_REQUEST['path']))) {
        exit (json_encode(array('status'=>0, 'msg' => "path not found")));
    }
    exec('/usr/bin/python3 /usr/www/scrapy/py/card.py', $rs, $status);
    #$rs = shell_exec("/usr/bin/python3 /usr/www/scrapy/py/card.py");
    var_dump($path);
    var_dump($rs);
    #var_dump($status);
