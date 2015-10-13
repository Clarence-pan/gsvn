使用场景
========

1. 初始化项目
-------------

```
gsvn init <svn-repository-url> [work-directory]
```

2. 更新项目
-----------

```
gsvn update [work-directory]
```

注意：如果SVN更新的时候有冲突，则将弹出TSVN的解决冲突对话框，解决冲突后继续；但是若git merge的时候有冲突，请自行使用`gsvn resolve`进行解决冲突，因为已经到最后一步了。


3. 提交修改(到SVN)
-----------

```
gsvn commit <message>
```
此命令将`svn`分支的修改提交到SVN版本库上。
注意：如果有未加入版本控制的文件或者冲突的问题，则会弹出SVN的修改对话框，解决冲突后再继续。

4. 快速提交
-----------
```
gsvn qcommit <message>
```
同时提交git和SVN。

5. 标记本地debug代码
--------------------

```
gsvn make-debug
```
将会把当前SVN的修改标记为debug代码，这些代码将不会被提交到SVN上。


注意事项
--------------------

如果出现git和svn的换行不一致的情况，请执行`git config core.autocrlf false`，防止git在提交代码的时候自动转换换行符。
