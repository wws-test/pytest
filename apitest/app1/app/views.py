# coding:utf-8

from flask import render_template, request, jsonify, redirect, url_for, flash


import glob
import os
from datetime import datetime as dt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml

from apitest.app1.app import app
from common.ApiData import testinfo
from config.conf import YAML_PATH
from forms import configForm
from tools.logger import log

CONFIG_FILE = 'config.yaml'

config = testinfo.load(YAML_PATH)
taffy_dir = 'D:\\pytst\\apitest'
reportDir = 'D:\\pytst\\allure-report'


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/report", methods=["GET", "POST"])
def report():
    return render_template("report.html")


@app.route("/case", methods=["GET", "POST"])
def case():
    if request.method == "GET":
        return render_template("case.html")


@app.route("/yaml", methods=["GET", "POST"])
def yaml():
    if request.method == "GET":
        return render_template("yaml.html")


@app.route("/config", methods=["GET", "POST"])
def config():
    form = configForm()
    config = testinfo.load(YAML_PATH)
    if form.validate_on_submit():
        del form.data['csrf_token']
        config = form.data
        yaml.dump(form.data, open(CONFIG_FILE, 'w'))
        flash(u'配置保存成功！', 'success')
        return redirect(url_for('config'))

    for c in config:
        getattr(form, c).data = config[c]
    return render_template("config.html", form=form)


@app.route("/getCase", methods=["GET", "POST"])
def getCase():
    if request.method == "GET":
        # 读取配置
        result = {}
        result["case_paths"] = glob.glob(taffy_dir + '/**/test_*.py')
        return jsonify(result)


@app.route("/getYaml", methods=["GET", "POST"])
def getYaml():
    if request.method == "GET":
        # 读取配置
        result = {}
        result["yaml_paths"] = glob.glob(taffy_dir + '/**/basics_*.yaml')
        return jsonify(result)


@app.route("/saveCase", methods=["GET", "POST"])
def saveCase():
    if request.method == "POST":
        caseName = request.form.get("caseName")
        caseScript = request.form.get("caseScript").encode('utf-8')
        mode = request.form.get("mode")
        result = {}

        # 判断文件是否含有路径
        if '/' in caseName:
            caseFile = caseName
            caseName = caseName.split('/')[-1]
        elif '\\' in caseName:
            caseFile = caseName
            caseName = caseName.split('\\')[-1]
        else:
            # 先判断文件夹是否存在，不存在则新建
            caseDir = os.path.join(taffy_dir, 'tests')
            if not os.path.exists(caseDir):
                os.makedirs(caseDir)
            caseFile = os.path.join(caseDir, caseName)

        if caseName.startswith('test_') and caseName.endswith('.py'):
            # 新建文件不可重复
            if u'新建' in mode:
                if os.path.exists(caseFile):
                    result['desc'] = u'文件已存在：{0}'.format(caseFile)
                else:
                    try:
                        with open(caseFile, 'wb') as f:
                            f.write(caseScript)
                        result['desc'] = 'pass'
                    except Exception as e:
                        result['desc'] = u'文件保存失败：{0}'.format(e)
            elif u'编辑' in mode:
                try:
                    with open(caseFile, 'w') as f:
                        f.write(caseScript)
                    result['desc'] = 'pass'
                except Exception as e:
                    result['desc'] = u'文件保存失败：{0}'.format(e)
        else:
            result['desc'] = u'文件格式错误：非test_xxx.py格式'
        return jsonify(result)


@app.route("/saveYaml", methods=["GET", "POST"])
def saveYaml():
    if request.method == "POST":
        caseName = request.form.get("yamlName")
        caseScript = request.form.get("YamlScript").encode('utf-8')
        mode = request.form.get("mode")
        result = {}

        # 判断文件是否含有路径
        if '/' in caseName:
            caseFile = caseName
            caseName = caseName.split('/')[-1]
        elif '\\' in caseName:
            caseFile = caseName
            caseName = caseName.split('\\')[-1]
        else:
            # 先判断文件夹是否存在，不存在则新建
            caseDir = os.path.join(taffy_dir, 'apiData')
            if not os.path.exists(caseDir):
                os.makedirs(caseDir)
            caseFile = os.path.join(caseDir, caseName)
        # 现在只控制bascis格式 这边以后要控制出更多权限
        if caseName.startswith('basics_') and caseName.endswith('.yaml'):
            # 新建文件不可重复
            if u'新建' in mode:
                if os.path.exists(caseFile):
                    result['desc'] = u'文件已存在：{0}'.format(caseFile)
                else:
                    try:
                        with open(caseFile, 'wb') as f:
                            f.write(caseScript)
                        result['desc'] = 'pass'
                    except Exception as e:
                        result['desc'] = u'文件保存失败：{0}'.format(e)
            elif u'编辑' in mode:
                try:
                    with open(caseFile, 'w') as f:
                        f.write(caseScript)
                    result['desc'] = 'pass'
                except Exception as e:
                    result['desc'] = u'文件保存失败：{0}'.format(e)
        else:
            result['desc'] = u'文件格式错误：非basics_xxx.yaml格式'
        return jsonify(result)


@app.route("/readCase", methods=["GET", "POST"])
def readCase():
    if request.method == "GET":
        caseName = request.args.get("caseName")
        result = {}
        try:
            with open(caseName, 'rb') as f:
                result['content'] = f.read()
        except Exception as e:
            result['exception'] = u'文件读取失败：{0}'.format(e)
        return jsonify(result)


@app.route("/readYaml", methods=["GET", "POST"])
def readYaml():
    if request.method == "GET":
        caseName = request.args.get("YamlName")
        result = {}
        try:
            with open(caseName, 'rb') as f:
                result['content'] = f.read()
        except Exception as e:
            result['exception'] = u'文件读取失败：{0}'.format(e)
        return jsonify(result)


@app.route("/delCase", methods=["GET", "POST"])
def delCase():
    if request.method == "POST":
        # 获取数组参数
        caseFiles = request.form.getlist("caseFiles[]")
        result = {}
        try:
            for f in caseFiles:
                os.remove(f)
            result['desc'] = 'pass'
        except Exception as e:
            result['desc'] = u'文件删除失败：{0}'.format(e)
        return jsonify(result)


@app.route("/delYaml", methods=["GET", "POST"])
def delYaml():
    if request.method == "POST":
        # 获取数组参数
        caseFiles = request.form.getlist("YamlFiles[]")
        result = {}
        try:
            for f in caseFiles:
                os.remove(f)
            result['desc'] = 'pass'
        except Exception as e:
            result['desc'] = u'文件删除失败：{0}'.format(e)
        return jsonify(result)


@app.route("/runCase", methods=["GET", "POST"])
def runCase():
    if request.method == "POST":
        # 获取数组参数
        caseFiles = request.form.getlist("caseFiles[]")
        result = {}
        try:
            case = ' '.join(caseFiles)

            command = 'pytest -v {}   --alluredir=./result  '.format(
                case)
            cd=os.system('cd D:\pytst\\apitest\\tests')
            log.info('cd到目标目录%s'%cd)
            result['desc'] = os.system(command)
            log.info('cmd运行结果%s'%result['desc'])
            allure=os.system('allure generate ./result -o ./report --clean')
            log.info('生产报告%s'%allure)


            # 判断是否自动发送结果邮件
            # if True:
            #     result = sendReportMail(report_file)
        except Exception as e:
            result['exception'] = u'用例运行失败：{0}'.format(e)
        return jsonify(result)


@app.route("/getReport", methods=["GET", "POST"])
def getReport():
    if request.method == "GET":
        result = {}
        # 测试报告名称
        result['report_paths'] = glob.glob(
          'D:\pytst\\report\\index.html')
        # 测试报告按时间排序
        return jsonify(result)


@app.route("/sendMail", methods=["GET", "POST"])
def sendMail():
    if request.method == "GET":
        report_file = request.args.get("reportName")
        return jsonify(sendReportMail(report_file))


def sendReportMail(report_file):
    report_name = report_file.split('\\')[-1]
    result = {}
    # 邮件服务器
    mail_host = config['mail_host']
    # 邮件服务器端口
    mail_port = config['mail_port']
    # 发件人地址
    mail_user = config['mail_user']
    # 发件人密码
    mail_pwd = config['mail_pwd']
    # 邮件标题
    mail_subject = config['mail_subject'] + \
        '_{0}'.format('_'.join(report_name.strip('.html').split('_')[-2:]))
    # 收件人地址list
    mail_to = config['mail_to']

    # 判断报告文件是否存在
    if not os.path.exists(report_file):
        return jsonify(
            dict(
                desc=u'测试报告文件不存在：{0}，<strong>先运行一次测试吧！</strong>'.format(report_file)))
    try:
        # 读取测试报告内容
        with open(report_file, 'r') as f:
            content = f.read().encode('utf-8')

        msg = MIMEMultipart('mixed')
        # 添加邮件内容
        msg_html = MIMEText(content, 'html', 'utf-8')
        msg.attach(msg_html)

        # 添加附件
        msg_attachment = MIMEText(content, 'html', 'utf-8')
        msg_attachment["Content-Disposition"] = 'attachment; filename="{0}"'.format(
            report_name)
        msg.attach(msg_attachment)

        msg['Subject'] = mail_subject
        msg['From'] = mail_user
        msg['To'] = mail_to

        # 连接邮件服务器
        s = smtplib.SMTP(mail_host, mail_port)
        # 登陆
        s.login(mail_user, mail_pwd)
        # 发送邮件
        s.sendmail(mail_user, mail_to, msg.as_string())
        # 退出
        s.quit()
        result['desc'] = u'测试报告发送成功'

    except Exception as e:
        result['desc'] = u'测试报告发送失败：{0}'.format(e)

    return result
