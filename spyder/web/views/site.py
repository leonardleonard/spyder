#coding: utf-8
from flask import Module, url_for, g, session, current_app, request, redirect
from flask import render_template

from libs import phpserialize
from web.helpers import auth
from web.models import Site, Field

import MySQLdb

site = Module(__name__)

@site.route("/add/", methods=("GET", "POST"))
@auth
def add():
    error = None
    site = {}
    site["sync_profile"] = {}
    if request.method == "POST":
        name = request.form.get("name")
        url = request.form.get("url")
        descript = request.form.get("descript")
        sync_type = request.form.get("sync_type")
        if not name:
            error = "请输入站点名称"
        elif not url:
            error = "请输入站点链接"
        elif not sync_type:
            error = "请选择入库方式"
        else:
            site = Site(current_app)
            sync_profile = {
                "staticUrl": request.form.get("staticUrl"),
                "mysql_server": request.form.get("mysql_server"),
                "mysql_dbname": request.form.get("mysql_dbname"),
                "mysql_prefix": request.form.get("mysql_prefix"),
                "mysql_username": request.form.get("mysql_username"),
                "mysql_password": request.form.get("mysql_password"),
                "api_url": request.form.get("api_url")
            }
            sync_profile = phpserialize.dumps(sync_profile)
            id = site.add(name=name, url=url, descript=descript, sync_type=sync_type, sync_profile=sync_profile)
            if id > 0:
                return redirect(url_for('sites.index'))
            else:
                error = "error"
    return render_template("site/add.html", error=error, site=site)
    
@site.route("/view/<int:site_id>/")
@auth
def view(site_id):
    return site_id
    
@site.route("/test_mysql/", methods=("GET", "POST"))
@auth
def test_mysql():
    if request.method == "POST":
        mysql_server = request.form.get("mysql_server")
        mysql_dbname = request.form.get("mysql_dbname")
        mysql_username = request.form.get("mysql_username")
        mysql_password = request.form.get("mysql_password")
        try:
            MySQL = MySQLdb.connect(host=mysql_server, user=mysql_username, passwd=mysql_password, db=mysql_dbname, connect_timeout=10)
            return "1"
        except:
            return "0"
    return "0"

@site.route("/edit/<int:site_id>/", methods=("GET", "POST"))
@auth
def edit(site_id):
    site = Site(current_app)
    if request.method == "POST":
        name = request.form.get("name")
        url = request.form.get("url")
        descript = request.form.get("descript")
        sync_type = request.form.get("sync_type")
        if not name:
            error = "请输入站点名称"
        elif not url:
            error = "请输入站点链接"
        elif not sync_type:
            error = "请选择入库方式"
        else:
            site = Site(current_app)
            sync_profile = {
                "staticUrl": request.form.get("staticUrl"),
                "mysql_server": request.form.get("mysql_server"),
                "mysql_dbname": request.form.get("mysql_dbname"),
                "mysql_prefix": request.form.get("mysql_prefix"),
                "mysql_username": request.form.get("mysql_username"),
                "mysql_password": request.form.get("mysql_password"),
                "api_url": request.form.get("api_url")
            }
            sync_profile = phpserialize.dumps(sync_profile)
            site.edit(id=site_id, name=name, url=url, descript=descript, sync_type=sync_type, sync_profile=sync_profile)
            return redirect(url_for('sites.index'))
    per = site.view(site_id)[0]
    if per["sync_profile"]:
        per["sync_profile"] = phpserialize.loads(per["sync_profile"])
    field = Field(current_app)
    types = field.getSeedType()
    return render_template("site/add.html", site=per, types=types)

@site.route("/delete/<int:site_id>")
@auth
def delete(site_id):
    return site_id