import yaml, requests
from flask import Flask

app = Flask(__name__)
@app.route('/')
def get_config():
    with open('/usr/clashx_remote_conf/Hypex.yaml','r') as yf:
        doc = yaml.load(yf, Loader=yaml.FullLoader)
    yaml_res = requests.get('http://www.diguass.cc/modules/servers/V2raySocks/clashsub.php?sid=15651&token=12345425', verify=False)
    digua_conf = yaml.load(yaml_res.text, Loader=yaml.FullLoader)
    doc['proxies'].extend(digua_conf['Proxy'])    # 将digua_conf的代理服务器添加到doc的proxies列表
    for pg in digua_conf['Proxy Group']:
        if pg['name']=='auto':              # 寻找digua_conf中名为auto的代理分组
            #pg['interval'] = 120            # 服务器测速间隔设为120秒
            #doc['proxy-groups'].append(pg)   # 将auto组加到doc的proxy-groups数组中
            #doc['proxy-groups'][0]['proxies'].insert(0,'auto')       # 在doc文件的Auto组中加入auto组作为一个选项
            doc['proxy-groups'][0]['proxies'].extend(pg['proxies'])  # 在doc文件的Proxy组中加入auto组中的代理服务器列表
            doc['proxy-groups'][1]['proxies'].extend(pg['proxies'])	# 在doc文件的Auto组中加入auto组中的代理服务器列表
    data = str(yaml.dump(doc, allow_unicode=True, sort_keys=False, indent=2))
    return data
