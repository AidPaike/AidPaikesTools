# 综合comfuzz以及五个对比工具

## CodeAlchemist

此工具在comfuzz容器中  

[testcases](CodeAlchemist_Tools/testcase)：CodeAlchemist生成的测试用例，用作测试

## deepsmith

[correct.py](deepsmith_TOOLS/correct.py)：deepsmith的正确率统计

[creatCombineCovageRate.py](comfuzzCompareTools/deepsmith_TOOLS/creatCombineCovageRate.py)：deepsmith的覆盖率统计

## DIE

[rmrepeat.py](DIE_TOOLS/DIE_target/rmrepeat.py)：通过md5加密算法进行去重，因为有可能文件夹名称是不同的，但是内容是相同的。

[get_testcase_2_change](DIE_TOOLS/DIE_watch_tmp/get_testcase_2_changed.py)：通过watch_dog进行监控两个cpu的生成，下面16是监控所有的cpu生成结果。

## Fuzzilli

[correct.py](fuzzilli_Tools/correct.py)：测试fuzzilli工具生成的testcase的语法正确率。   

要求：先启动Fuzzilli的docker容器，并且将testcases放入`/root/fuzzilli/interesting/`路径下

[creatCombineCovageRate.py](fuzzilli_Tools/creatCombineCovageRate.py)：测试montage工具的引擎覆盖率，由于覆盖率文件大小原因，分批进行生成和合并覆盖率，最终覆盖率文件是不会备份，但是测试用例都将存在，为了解决中途异常退出等问题，每个testcase在生成并合并覆盖率后都将重命名后加`.changed` 同时代码中也提供了整体还原，速度很快，影响可以忽略不计。

[test.js](fuzzilli_Tools/test.js)：fuzzilli生成的其中一个测试用例

[watch_dog.py](fuzzilli_Tools/watch_dog.py)：监控montage的中间文件，中途的测试用例进行保存。

## Montage
[correct.py](Montage_Tools/correct.py)：测试montage工具生成的testcase的语法正确率。   

要求：先启动Montage的docker容器，并且将testcases放入`/root/Montage/testcase/`路径下

[creatCombineCovageRate.py](Montage_Tools/creatCombineCovageRate.py)：测试montage工具的引擎覆盖率，由于覆盖率文件大小原因，分批进行生成和合并覆盖率，最终覆盖率文件是不会备份，但是测试用例都将存在，为了解决中途异常退出等问题，每个testcase在生成并合并覆盖率后都将重命名后加`.changed` 同时代码中也提供了整体还原，速度很快，影响可以忽略不计。

[readDBdemo.py](Montage_Tools/readDBdemo.py)：为读取数据库的测试用例做准备，就是将个范围的数据分割成多个范围的区间，为了多线程读取数据库使用。

[watch_dog.py](Montage_Tools/watch_dog.py)：监控montage的中间文件，中途的测试用例进行保存。

## nanotools

[howmanyfilesUderDir.py](nanotools/howmanyfilesUderDir.py)：主要是提供了列出文件夹内有多少文件。  shell的`ls -lh|wc -l `

有异曲同工之妙！

[limitCPU.py](nanotools/limitCPU.py)：控制你的程序限制到某个/几个 CPU上，这样不会影响其他人用服务器。

[readTxt.py](nanotools/readTxt.py)：读取txt的testcase文件，并且将testacase的内容存成列表形式返回。

