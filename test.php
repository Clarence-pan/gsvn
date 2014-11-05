#! /usr/bin/env php
<?php
/**
 * Created by PhpStorm.
 * User: clarence
 * Date: 14-11-5
 * Time: 下午11:02
 */

require(dirname(__FILE__).'/run.php');


$r = run('git status');
//var_dump($r);

run("svn status");

var_dump($GLOBALS);