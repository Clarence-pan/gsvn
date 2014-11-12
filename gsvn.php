#! /usr/bin/env php
<?php

require(dirname(__FILE__) . DIRECTORY_SEPARATOR . 'run.php');
require(dirname(__FILE__).DIRECTORY_SEPARATOR."console.php");
define('NEW_LINE', "\n");
array_shift($argv);

$alias = array(
    'help' => array('', '-?', '/?', '-h', '/h', '--help', 'help'),
    'qcommit' => array("qc", 'qco'),
    'commit' => array('c', 'co')
);

$cmd = strtolower(array_shift($argv));
$cmd = get_full_command($cmd, $argv);
return run_command($cmd, $argv);

/**
 * `gsvn` is designed to make svn works with git!
 * Hope it works!
 */
class GSvn {
    public function __construct(){
        $this->_storeFile = str_replace('/', DIRECTORY_SEPARATOR, $this->_storeFile);
    }
    /**
     * help to use gsvn
     * @format help [<cmd>]
     * @param $cmd [optional] - the command which is to help about
     */
    public function help($cmd = null) {
        $class = new ReflectionClass($this);
        $methods = $class->getMethods(ReflectionMethod::IS_PUBLIC);

        if (!$cmd) {
            echo 'About gsvn:' . NEW_LINE;
            echo "  gsvn\t- a tool to make svn works with git!" . NEW_LINE;
            echo NEW_LINE;
            echo 'Commands:' . NEW_LINE;
            foreach ($methods as $m) {
                if (preg_match('/^_/', $m->getName())){
                    continue;
                }
                $doc = new DocComment($m->getDocComment());
                echo "  " . $m->getName() . "\t- " . $doc->title . " " . NEW_LINE;
            }
            echo NEW_LINE;
            $classDoc = new DocComment($class->getDocComment());
            echo $classDoc->title . NEW_LINE;
            echo $classDoc->body . NEW_LINE;
        } else {
            $cmd = get_full_command($cmd, array());
            foreach ($methods as $m) {
                if ($m->getName() == $cmd) {
                    $method = $m;
                    break;
                }
            }
            if (!$method) {
                echo "Error: $cmd not found!" . NEW_LINE;
                die;
            }

            $doc = new DocComment($method->getDocComment());
            echo '#gsvn ' . $method->getName() . "\t- " . $doc->title . " " . NEW_LINE;
            echo NEW_LINE;
            if ($doc->formats){
                echo ' Usage: ' . NEW_LINE;
                foreach ($doc->formats as $fmt) {
                    echo '  ' . $fmt['format'] . NEW_LINE;
                    if ($fmt['title']):
                        echo '     ' . $fmt['title'] . NEW_LINE;
                    endif;
                    if ($fmt['body']):
                        echo '        ' . $fmt['body'] . NEW_LINE;
                    endif;
                }
                echo NEW_LINE;
            }
            if ($doc->params){
                echo ' Parameters: ' . NEW_LINE;
                foreach ($doc->params as $param) {
                    echo '  ' . $param['name'] . "\t" . $param['title'];
                    echo '    ' . $param['body'];
                }
                echo NEW_LINE;
            }
            if ($doc->body){
                echo $doc->body . NEW_LINE;
            }
        }
    }

    /**
     * init a repo
     * @format init <url> [path]
     * @param $url - the url of the repo
     * @param $path - the path to checkout
     */
    public function init($url, $path) {
        if ($path){
            go("svn checkout $url $path");
        }else{
            go("svn checkout $url .");
        }
        go("git init $path");
        file_put_contents(($path ? $path : '.').DIRECTORY_SEPARATOR.'.gitignore', implode(NEW_LINE, array('.svn/', '.bak', '~')));
        go("git add .", $path);
        $r = go("svn info");
        $revision = $this->findFirstMatch('/Revision:\s(\d+)/', $r->output);
        run("git commit -m\"initialized from svn(r$revision)\"", $path);
        run("git checkout -b work", $path);
        go("git tag COMMITED-WORK");
        run("git checkout -b debug", $path);
        go("git tag COMMITED-DEBUG");
    }

    /**
     * stash current working
     * @param $msg -- message for stash
     */
    public function stash($msg=''){
//        go("git add .");
//        go("git commit -m\"STASH: $msg\"");
        if ($this->isGitDirty()){
            run('git stash');
        }
    }

    private function isGitDirty(){
        $r = run("git status");
        if (!$r->success){
            return false;
        }
        if (strstr($r->output[1], 'nothing to commit')){
            return false;
        }
        return true;
    }

    private function getGitCurrentBranch(){
        $r = run("git status");
        if (!$r->success){
            return false;
        }
        preg_match('/On branch (\w+)/', $r->output[0], $matches);
        return $matches[1];
    }

    /**
     * commit to svn
     * note: commit which begins with 'debug' will NOT be commited!
     * @param $msg -- message for commit
     * @param $continue -- continue cherry-pick and commit
     */
    public function commit($msg='', $continue=false){
        try {
            if (!$msg){
                echo "Error: please specify the message of commit.".NEW_LINE;
                return 1;
            }
            if (!$continue) {
                $this->debug();
                //$this->stash("before commit $msg");
                if ($this->isGitDirty()){
                    echo "Error: dirty working directory! Please stash or commit local changes to git.";
                    die;
                }

                $logs = $this->getGitLog(' COMMITED-DEBUG..HEAD --no-merges');
                $logs = array_reverse($logs);
                array_shift($logs); // 最初一个是已经提交过的
                $logs = array_filter($logs, function ($log) {
                    $comment = strtolower($log['comment']);
                    return !preg_match('/^debug/', $comment)
                        and !preg_match('/^updated to svn/', $comment);
                });
                $shas = array_map(function ($log) {
                        return $log['sha'];
                    }, $logs);
                echo NEW_LINE;
                echo " Need pickup " . implode(' ', $shas) . NEW_LINE;

                $this->saveState(array(
                    'state' => 'commit',
                    'data' => $shas
                ));
                go("git checkout work");
            } else {
                $data = $this->loadState();
                if (!$data or $data['state'] != 'commit') {
                    echo "Error: invalid state!" . NEW_LINE;
                    die;
                }
                $shas = $data['data'];
                $sha = $data['process'];
                while ($sha != array_shift($shas)) ;
            }
            if ($continue != 'tag') {
                foreach ($shas as $sha) {
                    $this->saveState(array(
                        'state' => 'commit',
                        'data' => $shas,
                        'process' => $sha
                    ));
                    go("git cherry-pick $sha");
                }
                go("svn commit --message \"$msg\"");
            }else{
                run("git checkout work");
            }
            run("git tag -d COMMITED-WORK");
            go("git tag COMMITED-WORK HEAD");
            $r = go("svn status");
            if (trim(implode("", $r->output)) != ""){
				echo "Error: svn and work do NOT match! Please update work.".NEW_LINE;
				return 1;
            }
            go("git checkout debug");
            go("git merge debug");
            run("git tag -d COMMITED-DEBUG");
            go("git tag COMMITED-DEBUG HEAD");
            $this->update();
        }catch(Exception $e){
            echo "Error: commit failed! Please solve the conflicts and use 'gsvn commit --continue' to go on.";
            echo NEW_LINE;
            throw $e;
        }
    }

    /**
     * 提交到git，并提交svn
     * @param $msg 提交的消息
     * @param $continue 是否继续
     * @alias qc
     */
    public function qcommit($msg, $continue=false){
        go("git status");
        go("git add .");
        $this->tryCommitGit($msg);
        $this->commit($msg, $continue);
    }

    private $_storeFile = './.git/.gsvn-store';
    private function saveState($data){
        file_put_contents($this->_storeFile, var_export($data, true));
    }
    private function loadState(){
        $code = file_get_contents($this->_storeFile);
        if (!$code){
            return false;
        }
        return eval('return '.$code.';');
    }

    /**
     * update the working directory
     * @param $nostash - don't stash, just update it!
     */
    public function update($nostash){
        if (!$nostash){
            $this->stash('before update');
        }
        go("git checkout work");
        go("svn update");
        go("git add .");
        $r = go("svn info");
        $revision = $this->findFirstMatch('/Revision:\s(\d+)/', $r->output);
        //go("git commit -m\"updated to svn(r$revision)\"");
        $this->tryCommitGit("updated to svn(r$revision)");
        run("git tag -d UPDATE-TO-r$revision");
        go("git tag UPDATE-TO-r$revision HEAD");
		$r = go("svn status");
		if (trim(implode("", $r->output)) != ""){
			echo "Error: svn and work do NOT match! Please update work.".NEW_LINE;
			return 1;
		}
        go("git checkout debug");
        go("git merge work");
    }

    /**
     * see the status of git and svn
     */
    public function status(){
        go("svn status");
        go("git status");
    }

    /**
     * validate it
     * @param $nostash - don't stash, just update it!
     */
    public function validate($nostash){
        if (!$nostash){
            $this->stash('before update');
        }
        go("git checkout work");
        $r = go("svn status");
        if (trim(implode("", $r->output)) != ""){
            echo "Error: svn and work do NOT match! Please update work.".NEW_LINE;
            return 1;
        }else{
            echo "It's OK.".NEW_LINE;
            go("git checkout debug");
            return 0;
        }
    }
    /*
     * use tools to resolve conflicts
     */
    public function resolvetool(){
        run('tortoisegitproc /command:resolve');
    }
    private function tryCommitGit($msg){
        try{
            $r = go("git commit --message \"$msg\"");
        }catch(CmdFailException $e){
            if (strstr(implode(' ', $e->getResult()->output), 'nothing to commit')){
                return $e->getResult();
            }
            throw $e;
        }
    }
    /**
     * @param $reg
     * @param $lines
     * @return mixed
     */
    private function findFirstMatch($reg, $lines){
        $matches = $this->findFirstMatches($reg, $lines);
        return $matches[1];
    }

    private function findFirstMatches($reg, $lines){
        foreach ($lines as $line) {
            if (preg_match($reg, $line, $matches)){
                return $matches;
            }
        }
        return null;
    }

    /**
     * see the info of current path
     */
    public function info(){
        try{
            go("svn info");
        }catch(Exception $e){
            echo $e->getMessage().NEW_LINE;
        }
    }

    /**
     * there are many aliases, this command show the aliases
     */
    public function alias(){
        global $alias;
        echo ' Command    Aliases '.NEW_LINE;
        foreach ($alias as $full => $a) {
            echo ' '.$full."\t   ".implode(' ', $a);
        }
    }

    /**
     * switch to work branch
     */
    public function work(){
        if ($this->getCurrentBranch() != 'work'){
            go("git checkout work");
        }
    }

    /**
     * switch to debug branch
     */
    public function debug(){
        if ($this->getCurrentBranch() != 'debug'){
            go("git checkout debug");
        }
        go("git merge work");
    }

    private function getCurrentBranch(){
        $r = go("git status");
        $m = $this->findFirstMatch('/On branch (\w+)/', $r->output);
        return $m;
    }

    private function getGitLog($options){
        $r = go("git log --format=\"format:%h %s\" $options");
        $ret = array();
        foreach ($r->output as $line) {
            $line = trim($line);
            list($sha, $comment) = $this->splitFirst($line);
            $ret[$sha] = array('sha' => $sha, 'comment' => $comment);
        }
        return $ret;
    }

    // split the $line into 2 parts, by $spliter
    private function splitFirst($line, $spliter = ' '){
        $pos = strpos($line, $spliter);
        return array(substr($line, 0, $pos),
                     substr($line, $pos + 1));
    }
}

class Setted
{
    public function __toString(){
        return '';
    }
}

function get_full_command($cmd, $argv) {
    global $alias;

    foreach ($alias as $fullCommand => $aliaArr) {
        if (in_array($cmd, $aliaArr) or $fullCommand == $cmd) {
            $cmd = $fullCommand;
            break;
        }
    }

    return $cmd;
}

function run_command($cmd, $argv) {
    $gsvn = new GSvn();
    $class = get_class($gsvn);

    $method = null;
    try {
        $method = new ReflectionMethod($class, $cmd);
    } catch (Exception $e) {}

    if (!$method or !$method->isPublic()) {
        echo "Error: command '$cmd' does NOT exist!\n";
        $cmd = 'help';
        $method = new ReflectionMethod($class, $cmd);
        $paramValues = array();
    }  else {
        $paramValues = get_param_values($argv, $method);
    }
    try {
        return call_user_func_array(array($gsvn, $cmd), $paramValues);
    }catch(Exception $e) {
        echo $e->getMessage() . NEW_LINE;
        return $e->getCode();
    }
}

/**
 * @param $argv
 * @param $method
 * @return array
 */
function get_param_values($argv, $method)
{
    $parameters = $method->getParameters();
    $paramInfo = array();
    $paramValues = array();
    $paramIndex = 0;
    foreach ($parameters as $parameter) {
        $paramInfo[$parameter->getName()] = array(
            'name' => $parameter->getName(),
            'allowNull' => $parameter->allowsNull(),
            'defaultValue' => $parameter->isOptional() ? $parameter->getDefaultValue() : null,
            'index' => $paramIndex
        );
        @$paramValues[$paramIndex] = $paramInfo['defaultValue'];
        $paramIndex++;
    }

    while (count($argv)) {
        $arg = array_shift($argv);
        if (strpos($arg, '--') === 0) {
            $argName = substr($arg, 2);
            $param = $paramInfo[$argName];
            unset($paramInfo[$argName]);
            if (count($argv) > 0) {
                $argValue = array_shift($argv);
                if (strpos($argValue, '--') === 0) {
                    array_unshift($argv, $argValue);
                    $argValue = new Setted(); // 可以用isset来判断此开关
                }
            } else {
                $argValue = new Setted();
            }
        } else {
            $param = array_shift($paramInfo);
            $argValue = $arg;
        }

        if (!$param) {
            echo "Error: unknown parameter: $arg" . NEW_LINE;
            die;
        }

        $paramValues[$param['index']] = $argValue;
    }
    return $paramValues;
}
class CmdFailException extends Exception{
    private $cmd;
    private $result;
    public function __construct($cmd, $result, $msg=null){
        if (!$msg){
            $msg = "run \"$cmd\" failed, last error is ".$result->lastError;
        }
        $this->cmd = $cmd;
        $this->result = $result;
        parent::__construct($msg, $errorCode);
    }
    public function getCmd(){
        return $this->cmd;
    }
    public function getResult(){
        return $this->result;
    }
}
/*
 * run $cmd
 * if failed, throw exception.
 */
function go($cmd, $cwd=null, $env=array()){
    $r = run($cmd, $cwd, $env);
    if (!$r->success){
        throw new CmdFailException($cmd, $r);
    }
    return $r;
}