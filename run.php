<?php

/**
 * @param string $cmd  命令
 * @param bool $echo 是否回显内容
 * @return array output: 命令执行的输出结果，也是数组，分行
 *               return: 命令执行退出的返回值
 */
function run($cmd, $cwd=null, $env=array()){
    global $echo;
    global $defaultEnv;
    $output = null;
    if ($echo){
        echo "> $cmd \n";
    }
    $env = array_merge($_SERVER, $defaultEnv, $env);
    $pipes = array();
    $stdout = fopen("php://stdout", 'a');
    unset($env['argv']);
    unset($env['argc']);
//    var_dump($cmd ." 2>&1 ", array(1 => array('pipe', 'w')), $pipes, $cwd, $env);
    $p = proc_open($cmd ." 2>&1 ", array(1 => array('pipe', 'w')), $pipes, $cwd, $env);
    if ($p) {
        do{
            $block = fread($pipes[1], 1024 * 4);
            fwrite($stdout, $block);
            fflush($stdout);
            $output .= $block;
            break;
        }while(!feof($pipes[1]));

        fclose($stdout);
        foreach ($pipes as $pipe){
            fclose($pipe);
        }
        $returnVar = proc_close($p);
    }

    $output = explode("\n", $output);

    return (object)array('output' => $output, 'return' => $returnVar );
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