import telegram, json, logging,os
from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
import time;
import yaml
import requests

file_path = "/etc/prometheus.yml"
#file_path = "/opt/dev_prometheus/server/prometheus.yml"

app = Flask(__name__)
app.secret_key = 'lAlAlA123'
basic_auth = BasicAuth(app)

tag = os.getenv("TAG")
chatID = int(os.getenv("CHATID"))
token = os.getenv("TOKEN")



app.config['BASIC_AUTH_FORCE'] = False
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '123456'


bot = telegram.Bot(token=token)

@app.route('/', methods = ['GET'])
def index():

    return "success"
    

    
    
@app.route('/add_node', methods = ['GET'])
def add_node():
    try:
        node = request.args.get("node")
        if len(node.split(":")) >=2 :
            node = node.split(":")[0] + ":9100" 
        else:
            node = f"{node}:9100"
        res = do_port(node,"add","node")
        return f"add node {node} success"
    except Exception as e:
        return str(e)
        return "no node arg"
 
    
@app.route('/delete_node', methods = ['GET'])
def delete_node():
    try:
        node = request.args.get("node")
        if len(node.split(":")) >=2 :
            node = node.split(":")[0] + ":9100"
        else:
            node = f"{node}:9100"
        res = do_port(node,"delete","node")
        return f"delete node {node} success"

    except Exception as e:
        return str(e)
        return "no node arg"



@app.route('/add_tcp', methods = ['GET'])
def add_port():
    
    try:
        node = request.args.get("node")
        res = do_port(node,"add","tcp_check")
        return f"add port{node} success"

    except Exception as e:
        print(e);
        return "no node arg"
 
    
@app.route('/delete_tcp', methods = ['GET'])
def delete_port():
    try:
        node = request.args.get("node")
        res = do_port(node,"delete","tcp_check")
        return f"delete port {node} success"

    except:
        return "no node arg"
        
        
@app.route('/add_mysql', methods = ['GET'])
def add_mysql():
    
    try:
        node = request.args.get("node")
        res = do_port(node,"add","mysql")
        return f"add mysql{node} success"

    except Exception as e:
        print(e);
        return "no node arg"
 
    
@app.route('/delete_mysql', methods = ['GET'])
def delete_mysql():
    try:
        node = request.args.get("node")
        res = do_port(node,"delete","mysql")
        return f"delete mysql {node} success"

    except:
        return "no node arg"
   
   
'''
@app.route('/add_redis', methods = ['GET'])
def add_redis():
    
    try:
        node = request.args.get("node")
        res = do_port(node,"add","redis")
        return f"add redis{node} success"

    except Exception as e:
        print(e);
        return "no node arg"
 
    
@app.route('/delete_redis', methods = ['GET'])
def delete_redis():
    try:
        node = request.args.get("node")
        res = do_port(node,"delete","redis")
        return f"delete redis {node} success"

    except:
        return "no node arg"
        

@app.route('/add_mongo', methods = ['GET'])
def add_mongo():
    
    try:
        node = request.args.get("node")
        res = do_port(node,"add","mongo")
        return f"add mongo{node} success"

    except Exception as e:
        print(e);
        return "no node arg"
 
    
@app.route('/delete_mongo', methods = ['GET'])
def delete_mongo():
    try:
        node = request.args.get("node")
        res = do_port(node,"delete","mongo")
        return f"delete mongo {node} success"

    except:
        return "no node arg"     
        


@app.route('/add_kafka', methods = ['GET'])
def add_kafka():
    
    try:
        node = request.args.get("node")
        res = do_port(node,"add","kafka")
        return f"add kafka{node} success"

    except Exception as e:
        print(e);
        return "no node arg"
 
    
@app.route('/delete_kafka', methods = ['GET'])
def delete_kafka():
    try:
        node = request.args.get("node")
        res = do_port(node,"delete","kafka")
        return f"delete kafka {node} success"

    except:
        return "no node arg"
        
'''     


def get_targets2(job_name="node"):
    info = [];
    info_index = None;
    
    try:
        file = open(file_path,"r",encoding="utf-8");
        content = yaml.load(file.read(), Loader=yaml.FullLoader)
        targets = content["scrape_configs"]
        
        for i in targets:
            if i["job_name"] == job_name:
                info= i["static_configs"][0]["targets"]
                info_index = targets.index(i)
                
        file.close();

        return content,info,info_index;
    except Exception as e:
        print(e);
        print("读取文件错误"); 



   
def do_port(node,func,tag):
    node_list = node.split(":");
    if len(node_list)!=2:
        return None;
    try:
        content,targets,info_index = get_targets2(tag);
        if targets!=None and info_index!=None:
            if func == "add":
                if node not in targets:
                    targets.append(node);
                    do_prometheus_yml(content,targets,info_index);
                    
            if func == "delete":
                if node  in targets:
                    del targets[targets.index(node)]
                    do_prometheus_yml(content,targets,info_index); 
        else:
            return None
    
    except Exception as e:
        print(e);
    
        return None;
        
 

def do_prometheus_yml(content,targets,info_index):
    content["scrape_configs"][info_index]["static_configs"][0]["targets"] = targets
    content_yml = yaml.dump(content,sort_keys=False,Dumper=yaml.SafeDumper)
    f = open(file_path,"w",encoding="utf-8");
    f.write(content_yml);
    f.close();
    requests.post("http://172.17.0.1:9090/-/reload",timeout=3)
    
    
@app.route('/alert', methods = ['POST'])
def postAlertmanager():
    content = json.loads(request.get_data())
    message = f"报警标识:{tag}\n"
    try:
        for alert in content['alerts']:
            message += "状态: "+alert['status']+"\n"
            instance = alert['labels']['instance']
            message += "实例: "+ instance + "\n"
            annotations = alert['annotations']
            if 'summary' in alert['annotations']:
                message += "名称: "+alert['annotations']['summary'].replace(f"Instance {instance}",'')+"\n"

            if 'description' in alert['annotations']:
                message += "描述: "+alert['annotations']['description'].replace(f"{instance} of job ",'')+"\n"

            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
                currenTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.mktime(time.strptime(correctDate, "%Y-%m-%d %H:%M:%S"))) + 8*3600 ))
                message += "时间: "+ currenTime

            if alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
                currenTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.mktime(time.strptime(correctDate, "%Y-%m-%d %H:%M:%S"))) + 8*3600 ))
                message += "时间: " + currenTime

        print(message)
        bot.sendMessage(chat_id=chatID, text=message)
        return "Alert OK", 200

    except Exception as error:
        print(str(error));
        return "Alert fail", 200
        
app.run(host='0.0.0.0',port=9119,debug=True)