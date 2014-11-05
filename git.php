<?PHP
require(dirname(__FILE__).'/run.php');


class git
{
    public static function stash($action=null, $params=null){
        $output = run("git stash $action $params");
        if (strstr($output[0], 'No local changes to save')){
            return null;
        } else {
            return 'need-pop';
        }
    }

    public static function stash_pop($name){
        if ($name){
            return self::stash('pop');
        }
    }

    public static function status(){
        $output = run("git status");
        if (strstr($output[0], 'On branch')){
            $branch = trim( str_replace("On branch", "", $output[0]));
        }
        $allOutput = implode("\n", $output);
        if (strstr($allOutput, 'nothing to commit, working directory clean')
            or strstr($allOutput, 'nothing added to commit but untracked files present ')){
            $clean = true;
        }
        return array(
            'branch' => $branch,
            'clean' => $clean,
        );
    }

    public static function run($cmd=null, $param=null){
        return run("git $cmd $param");
    }

    public static function svn_dcommit(){
        self::run("difftool git-svn work");
        if (!self::get_confirm("Are you sure to commit to SVN? [y/n]")){
            return false;
        }
        return self::run("svn dcommit");
    }

    public static function svn_update(){
        if ($output = self::run("svn fetch")){
            $output = self::run('svn merge git-svn');
        }
        return $output;
    }

    public static function checkout($branch){
        return self::run("checkout $branch");
    }

    public static function get_confirm($msg=null){
        echo $msg;
        $output = run("get-confirm.bat", $ret, false);
        if (strstr($output[1], 'You have confirmed!')){
            return true;
        }
    }
}


