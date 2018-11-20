<?php

	if(!isset($_REQUEST['path']) || !($path = trim($_REQUEST['path']))) {
        exit (json_encode(array('status'=>0, 'msg' => "path not found")));
    }
    exec("/usr/bin/python3 /usr/www/scrapy/py/card.py", $output, $status);
    var_dump($path);
    var_dump($output);
    var_dump($status)