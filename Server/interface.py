# -*- coding: utf-8 -*-
import os
import time
import requests
from flask import Flask, request, session, url_for, render_template, send_from_directory, redirect, Response, jsonify, \
    safe_join, current_app, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from sqlalchemy import text
import json
import urllib
from werkzeug.utils import secure_filename
from config.setting import ALLOWED_EXTENSIONS


# app初始化，从配置setting.py中加载
class Application(Flask):
    def __init__(self, import_name, template_folder=None):
        super(Application, self).__init__(import_name, template_folder=template_folder)

        # load config
        self.config.from_pyfile('config/setting.py')

        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__, template_folder=os.getcwd() + '/web/')
manager = Manager(app)


class WeChatApi:
    def __init__(self):
        self.corpid = 'wx9dc3a069c71ba1af'
        self.corpsecret = '46c445a802736b5a068f29bc787d5160'

    def _get_access_token(self):
        result = requests.get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.corpid,
                "secret": self.corpsecret,
            }
        ).json()

        if result.get("access_token"):
            access_token = result.get('access_token')
        else:
            access_token = None
        return access_token

    def get_access_token(self):
        curr_time = time.time()
        try:
            with open('./tmp/access_token.conf', 'r') as f:
                t, acctoken = f.read().split()
            if 0 < curr_time - float(t) < 7260:
                return acctoken
            else:
                with open('./tmp/access_token.conf', 'w') as f:
                    acctoken = self._get_access_token()
                    f.write('\t'.join([str(curr_time), acctoken]))
                    return acctoken
        except:
            with open('./tmp/access_token.conf', 'w') as f:
                acctoken = self._get_access_token()
                curr_time = time.time()
                f.write('\t'.join([str(curr_time), acctoken]))
                return acctoken

    def get_openid(self, user_id):
        result = requests.get(
            url="https://api.weixin.qq.com/sns/jscode2session?appid=" + self.corpid + "&secret=" + self.corpsecret + "&js_code=" + user_id + "&grant_type=authorization_code",
            params={
                "js_code": user_id,
                "appid": self.corpid,
                "secret": self.corpsecret,
            }
        ).json()
        if result.get("openid"):
            openid = result.get('openid')
        else:
            openid = None
        return openid

    def sendmsg(self, openid, msg):
        access_token = self._get_access_token()

        body = {
            "touser": openid,
            "msgtype": "text",
            "text": {
                "content": msg
            }
        }
        response = requests.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            params={
                'access_token': access_token
            },
            data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
        )
        # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
        result = response.json()
        return result


wechat = WeChatApi()


class MerchantData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(100), unique=False, nullable=False)
    merchant_queue = db.Column(db.Boolean, unique=False, nullable=False)
    merchant_enable = db.Column(db.Boolean, unique=False, nullable=False)
    small_total = db.Column(db.Integer, unique=False, nullable=False)
    middle_total = db.Column(db.Integer, unique=False, nullable=False)
    big_total = db.Column(db.Integer, unique=False, nullable=False)
    small_index = db.Column(db.Integer, unique=False, nullable=False)
    middle_index = db.Column(db.Integer, unique=False, nullable=False)
    big_index = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, merchant_name, merchant_queue, merchant_enable, small_total, middle_total, big_total, small_index, middle_index, big_index):
        self.merchant_name = merchant_name
        self.merchant_queue = merchant_queue
        self.merchant_enable = merchant_enable
        self.small_total = small_total
        self.middle_total = middle_total
        self.big_total = big_total
        self.small_index = small_index
        self.middle_index = middle_index
        self.big_index = big_index

    def __repr__(self):
        return '<MerchantName %r>' % self.merchantname


class MerchantQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(100), unique=False, nullable=False)
    table_type = db.Column(db.String(100), unique=False, nullable=False)
    table_index = db.Column(db.Integer, unique=False, nullable=False)
    user_name = db.Column(db.String(100), unique=False, nullable=False)
    user_id = db.Column(db.String(100), unique=False, nullable=False)
    user_phone = db.Column(db.String(100), unique=False, nullable=False)
    eat_number = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, merchant_name, table_type, table_index, user_name, user_id, user_phone, eat_number):
        self.merchant_name = merchant_name
        self.table_type = table_type
        self.table_index = table_index
        self.user_name = user_name
        self.user_id = user_id
        self.user_phone = user_phone
        self.eat_number = eat_number

    def __repr__(self):
        return '<MerchantName %r>' % self.merchantname


class MerchantConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(100), unique=False, nullable=False)
    merchant_position = db.Column(db.String(100), unique=False, nullable=False)
    merchant_phone = db.Column(db.String(100), unique=False, nullable=False)
    user = db.Column(db.String(100), unique=False, nullable=False)
    pwd = db.Column(db.String(100), unique=False, nullable=False)
    small_count = db.Column(db.Integer, unique=False, nullable=False)
    middle_count = db.Column(db.Integer, unique=False, nullable=False)
    big_count = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, merchant_name, merchant_position, merchant_phone, user, pwd, small_count, middle_count, big_count):
        self.merchant_name = merchant_name
        self.merchant_position = merchant_position
        self.merchant_phone = merchant_phone
        self.user = user
        self.pwd = pwd
        self.small_count = small_count
        self.middle_count = middle_count
        self.big_count = big_count

    def __repr__(self):
        return '<MerchantName %r>' % self.merchantname

# Key value map
class MerchantMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=False, nullable=False)
    value = db.Column(db.String(1000), unique=False, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<value %r>' % self.value


# 测试接口
@app.route('/', methods=['GET', 'POST'])
def test():
    ret = {'version': 'v1.4.1'}
    ret['merchant_name'] = request.values.get('merchant_name')
    ret['user_name'] = request.values.get('user_name')
    ret['table_type'] = request.values.get('table_type')
    if str(request.method) == 'POST':
        ret['method'] = 'POST'
    elif str(request.method) == 'GET':
        ret['method'] = 'GET'
    return json.dumps(ret)


@app.errorhandler(404)
def page_not_found(i):
    return 'page not found'


@app.route('/user/<username>')
def profile(username):
    with app.test_request_context():
        print(url_for('index'))
        print(url_for('profile', username='hc.z'))
    return username


# 测试接口
@app.route('/testToken', methods=['GET', 'POST'])
def testToken():
    return wechat._get_access_token()

# 测试接口
@app.route('/testsendmsg', methods=['GET', 'POST'])
def testsendmsg():
    openid = request.values.get('openid')
    msg = request.values.get('msg')
    return wechat.sendmsg(openid, msg)

# 排队
@app.route("/line_up", methods=['GET', 'POST'])
def line_up():
    ret = {}
    merchant_name = request.values.get('merchant_name')
    user_name = request.values.get('user_name') if request.values.get('user_name') is not None else ""
    table_type = request.values.get('table_type')
    user_id = request.values.get('user_id') if request.values.get('user_id') is not None else ""
    user_phone = request.values.get('user_phone') if request.values.get('user_phone') is not None else ""
    eat_number = request.values.get('eat_number') if request.values.get('eat_number') is not None else ""
    if request.method == 'POST':    # 进行排队
        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            bcreat = False
            exists2 = False
            openid = ""
            if user_name is None or user_name == "":
                bcreat = True
            else:
                exists2 = db.session.query(db.exists().where(MerchantQueue.user_name == user_name)).scalar()
                if not exists2:
                    bcreat = True
                    if user_id == "":
                        openid = wechat.get_openid(user_id)

            if bcreat:      # 需要创建新排队
                result2 = MerchantData.query.filter_by(merchant_name=merchant_name).first()
                front = 1
                index = 1
                if table_type == 'small':
                    index = int(result2.small_total) + 1
                    result2.small_total = index
                    front = index - int(result2.small_index)
                elif table_type == 'middle':
                    index = int(result2.middle_total) + 1
                    result2.middle_total = index
                    front = index - int(result2.middle_index)
                elif table_type == 'big':
                    index = int(result2.big_total) + 1
                    result2.big_total = index
                    front = index - int(result2.big_index)

                temp = MerchantQueue(merchant_name=merchant_name,
                                    table_type=table_type,
                                    table_index=index,
                                    user_name=user_name,
                                    user_id=openid,
                                    user_phone=user_phone,
                                    eat_number=eat_number)


                # 通过会话将对象添加到数据库中 (session是与数据库的链接会话)
                db.session.add(temp)
                # 提交任务到数据库中
                db.session.commit()

                ret = {'code': 0, 'message': 'update success', 'index': index, 'front': front}
            else:
                ret = {'code': -1, 'message': 'user repeat'}
        else:
            ret = {'code': -2, 'message': 'merchant not exist'}
        return json.dumps(ret)
    return json.dumps({'code': -101, 'message': 'please use POST', 'method': request.method})
    # elif request.method == 'GET':   # 查询排队状态
    #     exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
    #     if exists1:
    #         result = MerchantData.query.filter_by(merchant_name=merchant_name).first()
    #         if (table_type == 'small' and result.small_tatol == result.small_index) or (table_type == 'middle' and result.middle_total == result.middle_index) or (table_type == 'big' and result.big_total == result.big_index) :
    #             ret = {'code': 1, 'message': 'No need to line up'}
    #         else:
    #             ret = {'code': -1, 'message': 'Please line up', 'data':[
    #                 {'type': 'small', 'total': result.small_total, 'index': result.small_index},
    #                 {'type': 'middle', 'total': result.middle_total, 'index': result.middle_index},
    #                 {'type': 'big', 'total': result.big_total, 'index': result.big_index}]}
    #     else:
    #         ret = {'code': -2, 'message': 'Merchant not exist'}
    #     return ret


#api9 数据刷新
@app.route("/refresh", methods=['GET'])
def refresh():
    if request.method == 'GET':
        # if not merchant_name in g_merchant_table:
        #     return 'not find %r' % merchant_name     # 无商户
        # for data in g_merchant_table[merchant_name]:
        #     if data[username] == username:
        #         index = data['index']
        #         tabletype = data['tabletype']
        #         queuelen = g_merchant_table[merchant_name][tabletype + 'total'] - index
        #         return 'There are %r tables in front of you. The waiting time is about %s minutes' % (
        #         queuelen, queuelen * 10 if queuelen > 3 else 30)
        ret = {}
        merchant_name = request.values.get('merchant_name')
        user_name = request.values.get('user_name')
        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            exists2 = db.session.query(db.exists().where(MerchantQueue.user_name == user_name)).scalar()
            if exists2:
                result1 = MerchantQueue.query.filter_by(merchant_name=merchant_name, user_name=user_name).first()
                index = result1.table_index
                result2 = MerchantData.query.filter_by(merchant_name=merchant_name).first()
                s = result2.small_total
                m = result2.middle_total
                b = result2.big_total
                if result1.table_type == 'small':
                    ret = {'code': 0, 'front': int(s) - int(index), 'index': int(index)}
                elif result1.table_type == 'middle':
                    ret = {'code': 0, 'front': int(m) - int(index), 'index': int(index)}
                elif result1.table_type == 'big':
                    ret = {'code': 0, 'front': int(b) - int(index), 'index': int(index)}
            else:
                ret = {'code': -1, 'message': 'user not exist'}
        else:
            ret = {'code': -2, 'message': 'merchant not exist'}
        return json.dumps(ret)


# api1, 商户更新自身数据
@app.route("/sendStatus", methods=['POST'])
def sendStatus():
    ret = {}
    if request.method == 'POST':
        merchant_name = request.values.get('merchant_name')
        merchant_queue = True if (request.values.get('merchant_queue') == None) else bool(request.values.get('merchant_queue'))
        merchant_enable = True if (request.values.get('merchant_enable') == None) else bool(request.values.get('merchant_enable'))

        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            data = MerchantData.query.filter_by(merchant_name=merchant_name).first()
            data.merchant_queue = merchant_queue
            data.merchant_enable = merchant_enable
            if (request.values.get('small_total') != None):
                data.small_total = int(request.values.get('small_total'))
            if (request.values.get('middle_total') != None):
                data.middle_total = int(request.values.get('middle_total'))
            if (request.values.get('big_total') != None):
                data.big_total = int(request.values.get('big_total'))
            if (request.values.get('small_index') != None):
                data.small_index = int(request.values.get('small_index'))
            if (request.values.get('middle_index') != None):
                data.middle_index = int(request.values.get('middle_index'))
            if (request.values.get('big_index') != None):
                data.big_index = int(request.values.get('big_index'))
            db.session.commit()
            ret = {'code': 0, 'message': 'update success'}
        else:
            ret = {'code': -2, 'message': 'Merchant not exist'}
        return json.dumps(ret)
    return json.dumps({'code': -101, 'message': 'please use POST', 'method': request.method})

# api2,开始营业
@app.route("/startQueue", methods=['POST'])
def startQueue():
    if request.method == 'POST':
        merchant_name = request.values.get('merchant_name')
        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            data = MerchantData.query.filter_by(merchant_name=merchant_name).first()
            data.merchant_queue = True
            data.merchant_enable = True
            db.session.commit()
            return json.dumps({'code': 0, 'message': 'update success'})
        else:
            return json.dumps({'code': -2, 'message': 'Merchant not exist'})
    return json.dumps({'code': -101, 'message': 'please use POST', 'method': request.method})

# api3,停止
@app.route("/stopQueue", methods=['POST'])
def stopQueue():
    if request.method == 'POST':
        merchant_name = request.values.get('merchant_name')
        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            data = MerchantData.query.filter_by(merchant_name=merchant_name).first()
            data.merchant_queue = False
            data.merchant_enable = False
            data.small_total = 0
            data.middle_total = 0
            data.big_total = 0
            data.small_index = 0
            data.middle_index = 0
            data.big_index = 0
            db.session.commit()
            return json.dumps({'code': 0, 'message': 'update success'})
        else:
            return json.dumps({'code': -2, 'message': 'Merchant not exist'})
    return json.dumps({'code': -101, 'message': 'please use POST', 'method': request.method})


# api4, 提交餐厅数据
@app.route("/commitConfig", methods=['GET', 'POST'])
def commitConfig():
    root_pwd = request.values.get('root_pwd')
    user = request.values.get('user')
    pwd = request.values.get('pwd')
    merchant_name = request.values.get('merchant_name')
    small_count = request.values.get('small_count')
    middle_count = request.values.get('middle_count')
    big_count = request.values.get('big_count')
    exists1 = db.session.query(db.exists().where(MerchantConfig.merchant_name == merchant_name)).scalar()
    if request.method == 'POST':
        if root_pwd == '123!@#qwe':
            if exists1:     # Update config
                data = MerchantConfig.query.filter_by(merchant_name=merchant_name).first()
                if (small_count != None):
                    data.small_count = int(small_count)
                if (middle_count != None):
                    data.middle_count = int(middle_count)
                if (big_count != None):
                    data.big_count = int(big_count)
                exists2 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
                if not exists2:
                    temp1 = MerchantData(merchant_name=merchant_name,
                                         merchant_queue=False,
                                         merchant_enable=False,
                                         small_total=0,
                                         middle_total=0,
                                         big_total=0,
                                         small_index=0,
                                         middle_index=0,
                                         big_index=0)
                    db.session.add(temp1)
                # 提交任务到数据库中
                db.session.commit()
                return {'code': 0, 'message': 'update success with root', 'merchant_name':merchant_name , 'small_count':data.small_count , 'middle_count':data.middle_count , 'big_count':data.big_count}
            else:          # add new merchant
                temp = MerchantConfig(merchant_name=merchant_name,
                                     user=user,
                                     pwd=pwd,
                                     merchant_position = str(request.values.get('merchant_position')),
                                     merchant_phone = str(request.values.get('merchant_phone')),
                                     small_count=int(small_count),
                                     middle_count=int(middle_count),
                                     big_count=int(big_count))

                # 通过会话将对象添加到数据库中 (session是与数据库的链接会话)
                db.session.add(temp)
                # 提交任务到数据库中
                db.session.commit()

                exists2 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
                if not exists2:
                    temp1 = MerchantData(merchant_name=merchant_name,
                                        merchant_queue = False,
                                        merchant_enable = False,
                                        small_total = 0,
                                        middle_total = 0,
                                        big_total = 0,
                                        small_index = 0,
                                        middle_index = 0,
                                        big_index = 0)
                    db.session.add(temp1)
                    # 提交任务到数据库中
                    db.session.commit()

                return {'code': 0, 'message': 'add success', 'merchant_name': merchant_name,
                        'small_count': small_count, 'middle_count': middle_count, 'big_count': big_count}
        else:
            if exists1:  # Update config
                data = MerchantConfig.query.filter_by(merchant_name=merchant_name).first()
                exists2 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
                if not exists2:
                    temp1 = MerchantData(merchant_name=merchant_name,
                                         merchant_queue=False,
                                         merchant_enable=False,
                                         small_total=0,
                                         middle_total=0,
                                         big_total=0,
                                         small_index=0,
                                         middle_index=0,
                                         big_index=0)
                    db.session.add(temp1)
                    # 提交任务到数据库中
                    db.session.commit()

                if user == data.user and pwd == data.pwd :
                    if (small_count != None):
                        data.small_count = int(small_count)
                    if (middle_count != None):
                        data.middle_count = int(middle_count)
                    if (big_count != None):
                        data.big_count = int(big_count)
                    db.session.commit()
                    return {'code': 0, 'message': 'update success,root error', 'merchant_name': merchant_name, 'merchant_position': data.merchant_position, 'merchant_phone': data.merchant_phone,
                            'small_count': data.small_count, 'middle_count': data.middle_count, 'big_count': data.big_count}
                else:
                    return {'code': -3, 'message': 'pwd error'}
            else:
                return {'code': -2, 'message': 'Merchant not exist'}
    elif request.method == 'GET':
        if exists1:  # Update config
            data = MerchantConfig.query.filter_by(merchant_name=merchant_name).first()
            # if user == data.user and pwd == data.pwd:
            if (small_count != None):
                data.small_count = int(small_count)
            if (middle_count != None):
                data.middle_count = int(middle_count)
            if (big_count != None):
                data.big_count = int(big_count)
            db.session.commit()
            return {'code': 0, 'message': 'update success,root error', 'merchant_name': merchant_name, 'merchant_position': data.merchant_position, 'merchant_phone': data.merchant_phone,
                        'small_count': data.small_count, 'middle_count': data.middle_count, 'big_count': data.big_count}
        else:
            return {'code': -2, 'message': 'Merchant not exist'}
    return json.dumps({'code': -101, 'message': 'please use POST', 'method': request.method})


# api10 ,添加key、value数据
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    key = str(request.values.get('key'))
    value = str(request.values.get('value'))
    exists1 = db.session.query(db.exists().where(MerchantMap.key == key)).scalar()
    if request.method == 'POST':
        if exists1:
            data = MerchantMap.query.filter_by(key=key).first()
            data.value = value
            db.session.commit()
            return {'code': 0,  'message': 'update success', 'value': data.value}
        else:
            temp = MerchantMap(key=key, value=value)
            db.session.add(temp)
            db.session.commit()
            return {'code': 0, 'message': 'upload success', 'key': key, 'value': value}
    elif request.method == 'GET':
        if exists1:
            data = MerchantMap.query.filter_by(key=key).first()
            return {'code': 0,  'message': 'get success', 'value': data.value}
        else:
            return {'code': -3, 'message': 'key not exist'}
    return json.dumps({'code': -101, 'message': 'please use POST', 'method': request.method})


# api5 商户获取队列信息
@app.route("/getQueue/", methods=['GET'])
def getQueue():
    if request.method == 'GET':
        merchant_name = request.values.get('merchant_name')
        result = MerchantData.query.filter_by(merchant_name=merchant_name).first()
        content = {'code': 0, 'message': 'ok', 'data': [
            {'type': 'small', 'total': result.small_total, 'index': result.small_index},
            {'type': 'middle', 'total': result.middle_total, 'index': result.middle_index},
            {'type': 'big', 'total': result.big_total, 'index': result.big_index}]}

        # sql = text("INSERT INTO Ranks VALUES ('merchant name', 'username', 'userphone', 'tabletype', 'eatnumber')")
        # result = db.engine.execute(sql)
        return json.dumps(content)
    return json.dumps({'code': -101, 'message': 'please use GET', 'method': request.method})

# api6, 商户pass过号
@app.route("/passNum/", methods=['GET'])
def passNum():
    if request.method == 'GET':
        ret = {}
        merchant_name = request.values.get('merchant_name')
        table_index = request.values.get('table_index')
        table_type = request.values.get('table_type')

        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            exists2 = db.session.query(db.exists().where(MerchantQueue.table_index == table_index)).scalar()
            if exists2:
                result = MerchantQueue.query.filter_by(merchant_name=merchant_name, table_index=table_index).first()
                result2 = MerchantData.query.filter_by(merchant_name=merchant_name).first()
                if table_type == 'small':
                    result2.small_index = result2.small_index + 1
                elif table_type == 'middle':
                    result2.middle_index = result2.middle_index + 1
                elif table_type == 'big':
                    result2.big_index = result2.big_index + 1
                db.session.commit()

                # 通知小程序
                weret = wechat.sendmsg(result.user_name, 'your number has passed')

                # delete
                db.session.delete(result)
                ret = {'code': 0, 'message': 'ok', 'wechat': weret}

            else:
                ret = {'code': -1, 'message': 'user not exist'}
        else:
            ret = {'code': -2, 'message': 'merchant not exist'}
        return json.dumps(ret)
    return json.dumps({'code': -101, 'message': 'please use GET', 'method': request.method})

# api7, 商户通知就餐
@app.route("/dining/", methods=['GET'])
def dining():
    if request.method == 'GET':
        ret = {}
        merchant_name = request.values.get('merchant_name')
        table_index = request.values.get('table_index')
        table_type = request.values.get('table_type')

        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            exists2 = db.session.query(db.exists().where(MerchantQueue.table_index == table_index)).scalar()
            if exists2:
                result = MerchantQueue.query.filter_by(merchant_name=merchant_name, table_index=table_index).first()
                result2 = MerchantData.query.filter_by(merchant_name=merchant_name).first()
                if table_type == 'small':
                    result2.small_index = result2.small_index + 1
                elif table_type == 'middle':
                    result2.middle_index = result2.middle_index + 1
                elif table_type == 'big':
                    result2.big_index = result2.big_index + 1
                db.session.commit()

                # 通知小程序
                weret = wechat.sendmsg(result.user_name, 'please ready to have dinner')
                db.session.delete(result)
                ret = {'code': 0, 'message': 'ok', 'wechat': weret}
            else:
                ret = {'code': -1, 'message': 'user not exist'}
        else:
            ret = {'code': -2, 'message': 'merchant not exist'}
        return json.dumps(ret)
    return json.dumps({'code': -101, 'message': 'please use GET', 'method': request.method})

# api12, 取消排队
@app.route("/cancel/", methods=['GET'])
def cancel():
    if request.method == 'GET':
        ret = {}
        merchant_name = request.values.get('merchant_name')
        user_name = request.values.get('user_name')

        exists2 = db.session.query(db.exists().where(MerchantQueue.user_name == user_name, MerchantQueue.merchant_name == merchant_name)).scalar()
        if exists2:
            result = MerchantQueue.query.filter_by(merchant_name=merchant_name, user_name=user_name).first()

            # delete
            db.session.delete(result)
            db.session.commit()
            ret = {'code': 0, 'message': 'ok'}
        else:
            ret = {'code': -2, 'message': 'merchant or user_name not exist'}
        return json.dumps(ret)
    return json.dumps({'code': -101, 'message': 'please use GET', 'method': request.method})

# api11
@app.route("/searchMerchant/", methods=['GET'])
def searchMerchant():
    if request.method == 'GET':
        result = MerchantData.query.all()
        data = []
        for d in result:
            data.append({'name': d.merchant_name,
                         'enable': d.merchant_enable,
                         'small_total': d.small_total,
                         'middle_total': d.middle_total,
                         'big_total': d.big_total})

        # content = {'code': 0, 'message': 'ok', 'data': data}
        # [
        #     {'type': 'small', 'total': result.small_total, 'index': result.small_index},
        #     {'type': 'middle', 'total': result.middle_total, 'index': result.middle_index},
        #     {'type': 'big', 'total': result.big_total, 'index': result.big_index}]
        # sql = text("INSERT INTO Ranks VALUES ('merchant name', 'username', 'userphone', 'tabletype', 'eatnumber')")
        # result = db.engine.execute(sql)
        return json.dumps({'code': 0, 'message': 'ok', 'data': data})
    return json.dumps({'code': -101, 'message': 'please use GET', 'method': request.method})


# 判断上传的文件是否是允许的后缀
def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 图片展示
@app.route('/show/<filename>')
def show(filename):
    # send_from_directory可以从目录加载文件
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 获取资源文件名
@app.route('/getResource')
def getResource():
    filetype = request.values.get('filetype')
    data = []
    for root, dirs, files in os.walk(os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])):
        for file in files:
            if os.path.splitext(file)[1] == filetype:
                data.append(file)
    return json.dumps({'code': 0, 'message': 'ok', 'data': data})

# 下载文件
@app.route('/downloadFile')
def downloadFile():
    def send_file(filename):
        # store_path = app.config['UPLOAD_FOLDER']+filename
        with open(filename, 'rb') as targetfile:
            while 1:
                data = targetfile.read(20 * 1024 * 1024)  # 每次读取20M
                if not data:
                    break
                yield data

    filename = request.values.get('filename')
    fullname = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isabs(fullname):
        fullname = os.path.join(current_app.root_path, fullname)
    try:
        if not os.path.isfile(fullname):
            return json.dumps({'code': -1, 'message': 'not file', 'file': fullname})
    except (TypeError, ValueError):
        return json.dumps({'code': -2, 'message': 'exception'})

    response = Response(send_file(fullname), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % filename
    return response


@app.route("/commitUrl", methods=['GET', 'POST'])
def commitUrl():
    if request.method == 'GET':  # 请求方式是get
        return render_template('upload.html')  # 返回模板,需要本地存在upload.html
    else:
        # if "file" not in request.files:
        #     return redirect(request.url)
        try:
            file = request.files.get('file')  # 获取文件

            if file.filename == '':
                return redirect(request.url)
            for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
                for f in files:
                    if file.filename == f:
                        return json.dumps({'code': -1, 'message': 'file exist'})
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)  # 用这个函数确定文件名称是否是安全 （注意：中文不能识别）
                file.save(os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename))  # 保存文件
                return json.dumps({'code': 0, 'message': 'ok'})     # redirect(url_for('show', filename=filename))
        except KeyError:
            return json.dumps({'code': -1, 'message': KeyError})

@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    try:
        file = request.files.get('file')  # 获取文件

        if file.filename == '':
            return redirect(request.url)
        for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
            for f in files:
                if file.filename == f:
                    return json.dumps({'code': -1, 'message': 'file exist'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # 用这个函数确定文件名称是否是安全 （注意：中文不能识别）
            file.save(os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename))  # 保存文件
            return json.dumps({'code': 0, 'message': 'ok'})  # redirect(url_for('show', filename=filename))
    except KeyError:
        return json.dumps({'code': -1, 'message': KeyError})
    # file = request.files['file']
    #
    # save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    # current_chunk = int(request.form['dzchunkindex'])
    #
    # # If the file already exists it's ok if we are appending to it,
    # # but not if it's new file that would overwrite the existing one
    # if os.path.exists(save_path) and current_chunk == 0:
    #     return make_response(('File already exists', 400))
    #
    # try:
    #     with open(save_path, 'ab') as f:
    #         f.seek(int(request.form['dzchunkbyteoffset']))
    #         f.write(file.stream.read())
    # except OSError:
    #     return make_response(("Not sure why,"
    #                           " but we couldn't write the file to disk", 500))
    #
    # total_chunks = int(request.form['dztotalchunkcount'])
    #
    # if current_chunk + 1 == total_chunks:
    #     # This was the last chunk, the file should be complete and the size we expect
    #     if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
    #         return make_response(('Size mismatch', 500))
    #
    # return make_response(("Chunk upload successful", 200))


# # 通知用户
@app.route("/send_notice")
def send_notice():
    # 服务端接口token
    serverToken = '33_0YjkW9kCMa-0N10emqbOcEzI4G9VCWT_r9E8cU0JfKdtu8EpgAnyGe62DQix7CKvHLtyzBY3eUV1ZSMj2RyzvaPIDuckkozn_MHLahXW11pl3PvVdxxdbVgWY4If78UjYeEOUr0ZW49gUsI3RSGhAAAUVJ'
    # 要请求的微信API
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={serverToken}'.format(serverToken=serverToken)

    data = '{\'msg\':\'Please arrive at the restaurant as soon as possible\'}'

    # 数据格式化(从这里开始对上面的data进行格式化,转成符合post的json参数形式)
    data = json.dumps(data)
    # 数据格式化
    data = bytes(data, 'utf8')
    # 数据格式化
    req = urllib.request.Request(url)
    # post服务器请求
    result = urllib.request.urlopen(req, data).read()
    # 打印结果
    print(result)
    return result


# request.args
# 这个是用来获取具体内容的，使用字典方式获取。
# 例如前端给input标签设置了一个id值，就可以使用这个方法直接获取到id的内容。
#
# request.form

# 这个是用来专门获取表单数据的。
# 例如前端的表单里填了用户名和密码，就可以使用这个方法获取内容。
#
# request.method
# 这个是用来专门获取用户端的请求方法的，默认是GET请求。
# 例如前端设置了post请求方法和get请求方法，并且有表单需要提交，就得用这个方法来获取用户的请求方法是什么，然后再根据请求方法处理
#
# request.referrer
# 这个是用来获取用户在请求之前所在的url。
# 例如用户在网站的一个页面中跳到了另一个页面，可能会需要知道他第一个页面的地址，或者是从别的网站跳转过来的，我们可能也想知道他是从哪个网站过来的。
#
#
# request.user_agent
# 这个是用来获取用户是使用什么东西来请求的。
# 例如用户使用windos笔记本，谷歌浏览器来请求的，就可以用这个方法去获取。
#
# request.files
# 这个是用来获取用户上传的文件的方法。



class WeChat1(object):
    __token_id = ''

    # init attribute
    def __init__(self, url='https://qyapi.weixin.qq.com/cgi-bin'):
        self.__url = url.rstrip('/')
        self.__corpid = '[企业号的标识]'
        self.__secret = '[管理组凭证密钥]'

    # Get TokenID
    def auth_id(self):
        params = {'corpid': self.__corpid, 'corpsecret': self.__secret}
        data = urllib.parse.urlencode(params)

        content = self.getToken(data)

        try:
            self.__token_id = content['access_token']
            # print content['access_token']
        except KeyError:
            raise KeyError

    # Establish a connection
    def get_token(self, data, url_prefix='/'):
        url = self.__url + url_prefix + 'gettoken?'
        try:
            response = urllib.request.Request(url + data)
        except KeyError:
            raise KeyError
        result = urllib.request.urlopen(response)
        content = json.loads(result.read())
        return content

    # Get sendmessage url
    def post_data(self, data, url_prefix='/'):
        url = self.__url + url_prefix + 'message/send?access_token=%s' % self.__token_id
        request = urllib.request.Request(url, data.encode())
        print(url)
        print(data)
        try:
            result = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            if hasattr(e, 'reason'):
                print('reason', e.reason)
            elif hasattr(e, 'code'):
                print('code', e.code)
            return 0
        else:
            content = json.loads(result.read())
            result.close()
        return content

    # send message
    def send_message(self, touser, message):

        self.authID()

        data = json.dumps({
            'touser': "[企业号中的用户帐号]",
            'toparty': "[企业号中的部门id]",
            'msgtype': "[消息类型]",
            'agentid': "[企业号中的应用id]",
            'text': {
                'content': message
            },
            'safe': "0"
        }, ensure_ascii=False)

        response = self.postData(data)
        print(response)


# def get_access_token():
#     """
#     获取微信全局接口的凭证(默认有效期俩个小时)
#     如果不每天请求次数过多, 通过设置缓存即可
#     """
#     result = requests.get(
#         url="https://api.weixin.qq.com/cgi-bin/token",
#         params={
#             "grant_type": "client_credential",
#             "appid": "wx9dc3a069c71ba1af",
#             "secret": "46c445a802736b5a068f29bc787d5160",
#         }
#     ).json()
#
#     if result.get("access_token"):
#         access_token = result.get('access_token')
#     else:
#         access_token = None
#     return access_token
#
# def sendmsg(openid,msg):
#
#     access_token = get_access_token()
#
#     body = {
#         "touser": openid,
#         "msgtype": "text",
#         "text": {
#             "content": msg
#         }
#     }
#     response = requests.post(
#         url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
#         params={
#             'access_token': access_token
#         },
#         data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
#     )
#     # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
#     result = response.json()
#     print(result)

