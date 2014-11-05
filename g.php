#! /usr/bin/env php
<?php

require(dirname(__FILE__).'/run.php');

array_shift($argv);

foreach ($argv as &$arg){
    if (strstr($arg, ' ')){
        $arg = "\"$arg\"";
    }
}
$cmdMap = array(
    'a' => 'add',
    's' => 'status',
    'c' => 'commit',
);
if (isset($cmdMap[$argv[0]])){
    $argv[0] = $cmdMap[$argv[0]];
}

run('git '.implode(' ', $argv));

