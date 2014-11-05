#! /usr/bin/env php
<?php

require(dirname(__FILE__).'/run.php');

array_shift($argv);

foreach ($argv as &$arg){
    if (strstr($arg, ' ')){
        $arg = "\"$arg\"";
    }
}

$cmd = array_shift($argv);

$cmdMap = array(
    'a' => 'add',
    's' => 'status',
    'c' => 'commit',
);

if (isset($cmdMap[$cmd])){
    $cmd = $cmdMap[$cmd];
}

$forceColorCommands = array('diff');
if (in_array($cmd, $forceColorCommands)){
    array_push($argv, '--color=always');
}


run('git '.$cmd.' '.implode(' ', $argv));

