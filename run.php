<?php

function dump(){
    return;
    return call_user_func_array('var_dump', func_get_args());
}

/**
 * @param string $cmd  命令
 * @param bool $echo 是否回显内容
 * @return array output: 命令执行的输出结果，也是数组，分行
 *               return: 命令执行退出的返回值
 */
function run($cmd, $cwd=null, $env=array()){
    global $echo;
    global $pwd;
    global $defaultEnv;
    if ($cwd == null){
        $cwd = $pwd;
    }
    $output = null;
    if ($echo){
        echo "> $cmd \n";
    }
    $env = array_merge($_SERVER, $defaultEnv, $env);
    $pipes = array();
    $stdout = fopen("php://stdout", 'a');
    unset($env['argv']);
    unset($env['argc']);
    dump($cmd ." 2>&1 ", array(1 => array('pipe', 'w')), $pipes, $cwd, $env);
    $p = proc_open($cmd ." 2>&1 ", array(1 => array('pipe', 'w')), $pipes, $cwd, $env);
    dump($p, $pipes);
    dump($GLOBALS);
    if ($p) {
        do{
            $block = fread($pipes[1], 1024 * 4);
            fwrite($stdout, $block);
            fflush($stdout);
            $output .= $block;
        }while(!feof($pipes[1]));

        fclose($stdout);
        foreach ($pipes as $pipe){
            fclose($pipe);
        }
        $returnVar = proc_close($p);
    }

    $output = explode("\n", $output);

    return (object)array('output' => $output, 'lastError' => $returnVar , 'success' => (0 == $returnVar));
}
//
//$output = run("svn log ../gsvn-repo");
//
//echo implode("\n", $output);
//$echo = false;
//run('sh source ~/locale-us');
$echo = true;
$defaultEnv = array(
    'LANG' => 'en_US.utf8',
    'LANGUAGE' => 'en_US.utf8',
    'LC_ALL' => 'en_US.utf8'
);

// windows:
$pwd = trim(`cd`, " \t\n\r");
if (!$pwd){
    // linux: get current working directory path
    $pwd = trim(`pwd`, " \t\n\r");
}

