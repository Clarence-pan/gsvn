<?php
/**
 * console application basic operations
 */
class Console {

}

/**
 * document of comment
 */
class DocComment {
    public $title = '';
    public $formats = array(); // array of { format: 'xx', title: 'xxx', body: 'xx' }
    public $body = '';
    public $params = array(); // array of { name: 'xxx', title: 'xxx', body: 'xxx' }
    public function  __construct($comment) {
        $lines = explode("\n", $comment);
        // 忽略第一个行和最后一行
        array_shift($lines);
        array_pop($lines);
        // 去除行首和尾部的*以及空格
        foreach ($lines as &$line) {
            $line = trim($line, ' *');
        }

        $this->title = array_shift($lines);
        $this->body = $this->readBody($lines);
        if (count($lines)) {
            while ($this->readCommand($lines)) ;
        }
    }

    private function readBody(&$lines) {
        $body = '';
        // 取出body, body是指到下一个@命令之前的内容
        while ($line = array_shift($lines)) {
            if ('@' == $line[0]) {
                array_unshift($lines, $line);
                break;
            }
            $body .= $line;
        }

        return $body;
    }

    private function readCommand(&$lines) {
        $cmdline = array_shift($lines);
        $i = strpos($cmdline, ' ');
        if ($i <= 0) {
            echo "Error: invalid document! " . NEW_LINE;
            echo implode(NEW_LINE, $lines);
            die;
        }
        $cmd = substr($cmdline, 0, $i);
        $cmd = strtolower($cmd);
        if ($cmd[0] != '@') {
            echo "Error: invalid command! " . NEW_LINE;
            echo implode(NEW_LINE, $lines);
            die;
        }
        $otherPart = substr($cmdline, $i + 1);
        $otherPart = trim($otherPart);
        switch ($cmd) {
            case '@param':
                $i = strpos($otherPart, ' ');
                if ($i <= 0) {
                    echo "Error: invalid param $cmd ! " . NEW_LINE;
                    echo implode(NEW_LINE, $lines);
                    die;
                }
                $param = substr($otherPart, 0, $i);
                $param = str_replace('$', '', $param);
                $title = substr($otherPart, $i + 1);
                $optional = !!strstr($title, '[optional]') || !!strstr($title, '[opt]');
                $title = str_replace('[optional]', '', $title);
                $title = str_replace('[opt]', '', $title);
                $body = $this->readBody($lines);
                $this->params[] = array(
                    'name' => $param,
                    'optional' => $optional,
                    'title' => $title,
                    'body' => $body
                );
                break;

            case '@format':
                $title = array_shift($lines);
                $body = $this->readBody($lines);
                $this->formats[] = array(
                    'format' => $otherPart,
                    'title' => $title,
                    'body' => $body
                );
                break;
        }

        return count($lines);
    }
}
