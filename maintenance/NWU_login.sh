# linux登陆校园网NWUNET的脚本
# cxk  fzy(练习时常两年半)
# 2021.4.14
# 2023.4.3
# shellcheck disable=SC2028



function login_campus_network() {
    read -p "请输入学号：" name
    if [ -z $name ]; then
        echo "输入不能为空"
    elif [ $name == exit -o $name == quit -o $name == q ]; then
        exit 1;
    else
        read -p "请输入密码：" password
        NET_INFO=$(curl  'http://10.0.1.165/a70.htm' \
            -H 'Content-Type: application/x-www-form-urlencoded' \
            --data-raw "DDDDD=$name&upass=$password&0MKKey=123456"\
            -s \
            | iconv -f gb2312 -t utf-8)

        success_info="认证成功页"

        if [[ $NET_INFO =~ $success_info ]]; then
            echo "》》》》》》》》登录成功！《《《《《《《《"
            return 0
        else
            echo "》》》》》》》》登录失败，用户名或密码错误或无可用流量《《《《《《《《"
            return 1
        fi
    fi
    return
}

function find_user_network(){
  NET_INFO=$(curl  'http://10.0.1.165/')
#  if [[ $NET_INFO =~ uid=\'([0-9]+)*\' ]]; then
#    uid=${BASH_REMATCH[1]}
#    echo "目前登录的用户为：$uid"
#  else
#    echo "目前没有用户正在登录~."
#  fi
  # 提取time
  time=$(echo "$NET_INFO" | grep -oP "(?<=time=')[^']+(?=')" )

  # 提取flow
  flow=$(echo "$NET_INFO" | grep -oP "(?<=flow=')[^']+(?=')" )
#  flow_gb=$(echo "$flow / 1024 / 1024 / 1024" | bc)
  # shellcheck disable=SC2004
  flow=$(($flow / 1024 / 1024))
  # 提取uid
  uid=$(echo "$NET_INFO" | grep -oP "(?<=uid=')[^']+(?=')" )

  # 输出结果
  echo "》》》》》》》》已使用时间：$time Min《《《《《《《《"
  echo "》》》》》》》》当前使用流量/总流量：$flow GB/150GB《《《《《《《《"
  echo "》》》》》》》》目前登录的用户为：$uid , 感谢无私奉献的人！《《《《《《《《"
}

function logout_user_network(){
  NET_INFO=$(curl 'http://10.0.1.165/F.htm')
  if echo "$NET_INFO" | grep -q "Logout Error(-1)"; then
      echo "》》》》》》》》Logout Error(-1)  大概意思就是目前没有账号正在登录，需要登陆一个新账号《《《《《《《《"
  else
      echo "》》》》》》》》注销成功《《《《《《《《"
  fi
  return
}

while true
do
echo "请选择一个选项(注意大写哦~)："
echo " A:查询当前登录账户"
echo " B:登录账户"
echo " C:退出账户"
echo " D:退出该程序脚本"
echo -n "您的选择是： "
read option
case $option in
  [A])
    echo "》》》》》》》》您选择了选项 A.《《《《《《《《"
    find_user_network
    continue
  ;;
  [B])
    echo "》》》》》》》》您选择了选项 B.《《《《《《《《"
    login_campus_network
    continue
  ;;
  [C])
    echo "》》》》》》》》您选择了选项 C.《《《《《《《《"
    logout_user_network
    continue
  ;;
  [D])
    echo "》》》》》》》》祝你天天开心^_^《《《《《《《《"
    exit
  ;;
  *)
    echo "》》》》》》》》无效的选项，请重新选择.《《《《《《《《"
    continue
  ;;
esac

done

#
#
#time='1999      ';flow='1932408   ';fsele=1;fee='0         ';xsele=0;xip='000.000.000.000.';
#
#flow0=flow%1024;flow1=flow-flow0;flow0=flow0*1000;flow0=flow0-flow0%1024;fee1=fee-fee%100;
#
#flow3='.';
#
#cvid=0,pvid=0;
#
#pwm=1;v6af=0;v6df=0;uid='202233397';pwd='';v46m=0;v4ip='10.15.22.88';v6ip='::';// 7890123456';v46m=001;v4ip='192.168.100.100';v6ip='0000:0000:0000:0000:0000:0000:0000:0000';////
#
#olmac='04d4c41f555a';////
#
#
#
#/** 哆点参数 start */
#
#//1.基本参数
#
#portalid='SX0301121_000';//门户ID
#portalname='西北大学';//门户名称
#
#//2.可选参数
#
#portalver='';//门户版本
#
#serialno='';//序列号
#
#logourl='';//门户logo
#
#bannerurl='';//横幅广告
#
#welcome='';//欢迎词
#
#businessurl='';//业务接口
#
#//3.旁路参数
#
#authexenable='0';//是否启用旁路扩展模式
#
#authtype=1;//登录协议
#
#authloginIP='';//登录IP
#
#authloginport=801;//登录端口
#
#authloginpath='/eportal/?c=ACSetting&a=Login';//登录路径
#
#authloginparam=''; //登录参数
#
#authuserfield='DDDDD';//账号节点
#
#authpassfield='upass';//密码节点
#
#terminalidentity=1;//终端识别标识 先配置成填写
#
#authlogouttype=1;//注销协议
#
#authlogoutIP='';//注销IP
#
#authlogoutport=80;//注销端口
#
#authlogoutpath='';//注销路径
#
#authlogoutparam='';//注销参数
#
#authlogoutpost='';//注销post参数
#
#querydelay=0;//登录后延时查询网络状态
#
#querytype=1;//状态查询协议
#
#queryIP='';//状态查询IP
#
#queryport=80;//状态查询端口
#
#querypost='';//状态查询post参数
#
#querypath='/eportal/?c=ACSetting&a=Query';//状态查询路径
#
#queryparam='';//状态查询参数
#
#authsuccess='Dr.COMWebLoginID_3.htm';//登录成功标志
#
#authfail='Dr.COMWebLoginID_2.htm';//登录失败标志
#
#isquery=0;
#
#authhost='';
#
#authoffpost='';
#
#charset='gb2312';//页面编码
#
#exparam=0;//扩展标志位
#
#//4.运营商选择
#
#carrier='{"yys":{"title":"服务类型","mode":"radiobutton","data":[{"id":"1","name":"校园用户","suffix":"@xyw"},{"id":"2","name":"校园电信","suffix":"@dx"},{"id":"3","name":"校园联通","suffix":"@lt"},{"id":"4","name":"校园其他","suffix":""}],"defaultID":"1"}}';//运营商选择
#
#//5.限制非哆点客户端登陆
#
#//把原先Dr.COMWebLoginID_ 改成: Dr.COM1.0WebLoginID_
#
#/** 哆点参数 end */
#
#
#
#var programUrl = window.location.protocol + "//" + window.location.hostname + ":801/eportal/extern/xibei/";
#
#newComm.setArgsCookies(programUrl,null,v4ip);
#
#
#
#//判断pc/手机
#
#if(normalFun.getTermType() == 2){
#
#	newComm.setNessArg('mobile_31');
#
#}else{
#
#	newComm.setNessArg('pc_1');
#
#}
#
#
#
#newComm.setNessJs();
#
#
#
#//广告统计设置
#
#hnaSetAdCount('1001', '000000000000', uid, v4ip, olmac);
#
#
