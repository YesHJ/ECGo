# -*- coding: utf-8 -*-
import os
from flask import Flask, request, session, url_for, render_template, send_from_directory, redirect
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

# 商户排队临时表
g_merchant_queue = {
'canting1': [{'username': 'lisi', 'userphone': '213433', 'index': 1, 'tabletype': 'small', 'eatnumber': 2},
            {'username': 'zhangsan', 'userphone': '34235', 'index': 1, 'tabletype': 'small', 'eatnumber': 2}, ],
'canting2': [{'username': 'wqeq1', 'userphone': '324', 'index': 1, 'tabletype': 'small', 'eatnumber': 2},
            {'username': 'wqeq2', 'userphone': '324', 'index': 2, 'tabletype': 'small', 'eatnumber': 2},
            {'username': 'wqeq3', 'userphone': '324', 'index': 3, 'tabletype': 'small', 'eatnumber': 2},
            {'username': 'wqeq4', 'userphone': '324', 'index': 4, 'tabletype': 'small', 'eatnumber': 2},
            {'username': 'wqeq5', 'userphone': '324', 'index': 5, 'tabletype': 'small', 'eatnumber': 2},
            {'username': 'rwrew', 'userphone': '453', 'index': 1, 'tabletype': 'small', 'eatnumber': 2}, ],
'canting3': [{'username': 'dffdgs', 'userphone': '34', 'index': 1, 'tabletype': 'small', 'eatnumber': 2},
            {'username': 'dsf', 'userphone': '45343', 'index': 1, 'tabletype': 'small', 'eatnumber': 2}, ],
                    }
# 商户排队计数表
g_merchant_table = {'canting1': {'smalltotal': 1, 'middletotal': 1, 'bigtotal': 0, 'smallindex': 1, 'middleindex': 1, 'bigindex': 0},
                    'canting2': {'smalltotal': 5, 'middletotal': 3, 'bigtotal': 2, 'smallindex': 3, 'middleindex': 3, 'bigindex': 1},
                    'canting3': {'smalltotal': 9, 'middletotal': 9, 'bigtotal': 5, 'smallindex': 2, 'middleindex': 2, 'bigindex': 2}
                    }


class MerchantData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(80), unique=False, nullable=False)
    merchant_enable = db.Column(db.String(10), unique=False, nullable=False)
    small_total = db.Column(db.String(10), unique=False, nullable=False)
    middle_total = db.Column(db.String(10), unique=False, nullable=False)
    big_total = db.Column(db.String(10), unique=False, nullable=False)
    small_index = db.Column(db.String(10), unique=False, nullable=False)
    middle_index = db.Column(db.String(10), unique=False, nullable=False)
    big_index = db.Column(db.String(10), unique=False, nullable=False)

    def __init__(self, merchant_name, merchant_enable, small_total, middle_total, big_total, small_index, middle_index, big_index):
        self.merchant_name = merchant_name
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
    merchant_name = db.Column(db.String(80), unique=False, nullable=False)
    table_type = db.Column(db.String(10), unique=False, nullable=False)
    table_index = db.Column(db.String(10), unique=False, nullable=False)
    user_name = db.Column(db.String(10), unique=False, nullable=False)
    user_phone = db.Column(db.String(10), unique=False, nullable=False)
    eat_number = db.Column(db.String(10), unique=False, nullable=False)

    def __init__(self, merchant_name, table_type, table_index, user_name, user_phone, eat_number):
        self.merchant_name = merchant_name
        self.table_type = table_type
        self.table_index = table_index
        self.user_name = user_name
        self.user_phone = user_phone
        self.eat_number = eat_number

    def __repr__(self):
        return '<MerchantName %r>' % self.merchantname

@app.route('/')
def index():
    # user = User.query.first()
    # movies = Movie.query.all()
    return 'index'#render_template('index.html', user=user, movies=movies)


@app.errorhandler(404)
def page_not_found(i):
    return 'page not found'


@app.route('/user/<username>')
def profile(username):
    with app.test_request_context():
        print(url_for('index'))
        print(url_for('profile', username='hc.z'))
    return username

# 排队
@app.route("/line_up/", methods=['GET', 'POST'])
def line_up():
    ret = {}
    merchant_name = request.values.get('merchant_name')
    user_name = request.values.get('user_name')
    table_type = request.values.get('table_type')
    if request.method == 'POST':    # 进行排队
        '''
        merchant_name = request.values.get('merchant_name')
        table_type = request.values.get('table_type')
        eat_number = request.values.get('eat_number')
        user_name = request.values.get('user_name')
        user_phone = request.values.get('user_phone')
        # g_merchant_table[merchant_name][table_type + 'total'] = g_merchant_table[merchant_name][table_type] + 1       # 队列+1
        # index = g_merchant_table[merchant_name][table_type + 'total']
        # print('Table Type = %s; Number of diners = %s' % (table_type, eat_number))
        # data = {'user_name': user_name, 'user_phone': user_phone, 'index': index, 'table_type': table_type, 'eat_number': eat_number}
        # g_merchant_queue[merchant_name].append(data)
        # queuelen = g_merchant_table[merchant_name][table_type + 'total'] - g_merchant_table[merchant_name][table_type + 'index']
    
        sql = text("SELECT * FROM `Merchant`")
        result = db.engine.execute(sql)
        for row in result:
            app.logger.info(row)
        return 'There are %r tables in front of you. The waiting time is about %s minutes' % (queuelen,  queuelen*10 if queuelen > 3 else 30)
        '''
        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            exists2 = db.session.query(db.exists().where(MerchantQueue.user_name == user_name)).scalar()
            if exists2:
                result2 = db.MerchantData.query.filter_by(merchant_name=merchant_name).first()
                s = result2.small_total
                m = result2.middle_total
                b = result2.big_total
                index = 1
                if table_type == 'small':
                    index = int(s) + 1
                    result2.small_total = index
                elif table_type == 'middle':
                    index = int(m) + 1
                    result2.middle_total = index
                elif table_type == 'big':
                    index = int(b) + 1
                    result2.big_total = index
                temp = MerchantQueue(merchant_name=merchant_name,
                                    table_type=table_type,
                                    table_index=index,
                                    user_name=user_name,
                                    user_phone=str(request.values.get('user_phone')),
                                    eat_number=str(request.values.get('eat_number')))

                # 通过会话将对象添加到数据库中 (session是与数据库的链接会话)
                db.session.add(temp)
                # 提交任务到数据库中
                db.session.commit()

                ret = {'Error': 0, 'Msg': 'update success'}
            else:
                ret = {'Error': -1, 'Msg': 'user not exist'}
        else:
            ret = {'Error': -2, 'Msg': 'merchant not exist'}
        return json.dumps(ret)
    elif request.method == 'GET':   # 查询排队状态
        # merchantname = username#request.values.get('merchantname')
        # tabletype = 'small'#request.values.get('tabletype')
        # 数据库查询
        # if merchantname in g_merchant_table:
        #     if g_merchant_table[merchantname][tabletype + 'total'] - g_merchant_table[merchantname][tabletype + 'index'] == 0:
        #         return 'No need to line up'
        #     else:
        #         return '''
        #         <form action="" method="post">
        #             <p>Table Type<input type=text name=tabletype>
        #             <p>Number of diners<input type=text name=eatnumber>
                #     <p><input type=submit value=Line Up>
                # </form>
                # '''
        # else:
        #     return 'No merchant name %r' % merchantname
        exists1 = db.session.query(db.exists().where(MerchantData.merchant_name == merchant_name)).scalar()
        if exists1:
            mer = db.MerchantData.query.filter_by(merchant_name=merchant_name).first()
            if (table_type == 'small' and mer.small_tatol == mer.small_index) or (table_type == 'middle' and mer.middle_total == mer.middle_index) or (table_type == 'big' and mer.big_total == mer.big_index) :
                ret = {'Error': 1, 'Msg': 'No need to line up'}
            else:
                ret = {'Error': -1, 'Msg': 'Please line up'}
        return ret


# 数据刷新
@app.route("/refresh/", methods=['GET'])
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
                result1 = db.MerchantQueue.query.filter_by(merchant_name=merchant_name, user_name=user_name).first()
                index = result1.table_index
                result2 = db.MerchantData.query.filter_by(merchant_name=merchant_name).first()
                s = result2.small_total
                m = result2.middle_total
                b = result2.big_total
                if result1.table_type == 'small':
                    ret = {'Front': int(s) - int(index), 'Index': int(index)}
                elif result1.table_type == 'middle':
                    ret = {'Front': int(m) - int(index), 'Index': int(index)}
                elif result1.table_type == 'big':
                    ret = {'Front': int(b) - int(index), 'Index': int(index)}
            else:
                ret = {'Error': -1, 'Msg': 'user not exist'}
        else:
            ret = {'Error': -2, 'Msg': 'merchant not exist'}
        return json.dumps(ret)


# 商户获取队列信息
@app.route("/getMerchantQueue/", methods=['GET'])
def getMerchantQueue():
    if request.method == 'GET':
        merchant_name = request.values.get('merchant_name')
        # 数据库查询
        # if merchant_name in g_merchant_table:
        #     return g_merchant_table[merchant_name]
        # else:
        #     return 'No merchant name %r' % merchant_name
        # db.execute('''SELECT * FROM MerchantData WHERE merchant_name=%r''' % merchant_name)
        # rv = db.fetchall()
        # content = {}
        # for result in rv:
        #     content = {'merchant_name': result[0]
        #         , 'merchant_enable': result[1]
        #         , 'small_total': result[2]
        #         , 'middle_total': result[3]
        #         , 'big_total': result[4]
        #         , 'small_index': result[5]
        #         , 'middle_index': result[6]
        #         , 'big_index': result[7]}
        result = db.MerchantData.query.filter_by(merchant_name=merchant_name).first()
        content = {'merchant_name': result.merchant_name
                , 'merchant_enable': result.merchant_enable
                , 'small_total': result.small_total
                , 'middle_total': result.middle_total
                , 'big_total': result.big_total
                , 'small_index': result.small_index
                , 'middle_index': result.middle_index
                , 'big_index': result.big_index}

        # sql = text("INSERT INTO Ranks VALUES ('merchant name', 'username', 'userphone', 'tabletype', 'eatnumber')")
        # result = db.engine.execute(sql)
        return json.dumps(content)


# 商户更新自身数据
@app.route("/updateMerchantInfo", methods=['POST'])
def updateMerchantInfo(name):
    if request.method == 'POST':
        temp = MerchantData(merchant_name=str(request.values.get('merchant_name')),
                             merchant_enable=str(request.values.get('merchant_enable')),
                             small_total=str(request.values.get('small_total')),
                             middle_total=str(request.values.get('middle_total')),
                             big_total=str(request.values.get('big_total')),
                             small_index=str(request.values.get('small_index')),
                             middle_index=str(request.values.get('middle_index')),
                             big_index=str(request.values.get('big_index')))

        # 通过会话将对象添加到数据库中 (session是与数据库的链接会话)
        db.session.add(temp)
        # 提交任务到数据库中
        db.session.commit()

        ret = {'Error': 0, 'Msg': 'update success'}
        return json.dumps(ret)

    # sql = text("INSERT INTO Ranks VALUES ('merchant name', 'username', 'userphone', 'tabletype', 'eatnumber')")
    # result = db.engine.execute(sql)
    return "current index"




# 判断上传的文件是否是允许的后缀
def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':  # 请求方式是get
        return render_template('upload.html')  # 返回模板,需要本地存在upload.html
    else:
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files.get('file')  # 获取文件

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # 用这个函数确定文件名称是否是安全 （注意：中文不能识别）
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # 保存文件
            return redirect(url_for('show', filename=filename))


# 图片展示
@app.route('/show/<filename>')
def show(filename):
    # send_from_directory可以从目录加载文件
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




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



class WeChat(object):
    __token_id = ''

    # init attribute
    def __init__(self, url):
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

