#coding: utf-8
from flask import Module, url_for, g, session, current_app, request, redirect
from flask import render_template
from libs import phpserialize
from web.helpers import auth, getSeedFieldsBySid, checkboxVal
from web.models import Seed, Field, Seed_fields

seed = Module(__name__)

@seed.route("/add/", methods=("GET", "POST"))
@auth
def add():
    field = Field(current_app)
    if request.method == "POST":
        list1 = {
            "urlformat": request.form.get("urlformat"),
            "urltype": request.form.get("urltype"),
            "startpage": request.form.get("startpage"),
            "maxpage": request.form.get("maxpage"),
            "step": request.form.get("step"),
            "listparent": request.form.get("listparent"),
            "entryparent": request.form.get("entryparent"),
            "pageparent": request.form.get("pageparent"),
            "filters": request.form.get("filters")
        }
        save = {
            "type": request.form.get("type"),
            "seed_name": request.form.get("seed_name"),
            "charset": request.form.get("charset"),
            "frequency": request.form.get("frequency"),
            "timeout": request.form.get("timeout"),
            "tries": request.form.get("tries"),
            "enabled": request.form.get("enabled") is 1 and 1 or 0,
            "listtype": request.form.get("listtype"),
            "lang": request.form.get("lang"),
            "rule": phpserialize.dumps(list1)
        }
        seed = Seed(current_app)
        sid = seed.add(**save)
        if sid:
            seed_field = Seed_fields(current_app)
            fields = field.list(save["type"])
            for field in fields:
                seed_value = {}
                seed_value["seed_id"] = sid
                seed_value["field_id"] = field.id
                seed_value["value"] = request.form.get(field.name)
                seed_field.add(**seed_value)
        return redirect(url_for("seeds.index"));
    fields = field.getSeedType()
    if request.method == "GET" and request.args.get("type"):
        seed_data = {}
        seed_data["rule"] = {}
        seed_type = request.args.get("type");
        fields = field.list(seed_type)
        return render_template("seed/add.html", seed_type=seed_type, fields=fields, seed_data=seed_data)
    return render_template("seed/select_type.html", fields=fields)
    
@seed.route("/view/<int:seed_id>/")
@auth
def view(seed_id):
    return seed_id

@seed.route("/addlink/")
@auth
def add_link():
    return render_template("seed/add_link.html")

@seed.route("/edit/<int:seed_id>/", methods=("GET", "POST"))
@auth
def edit(seed_id):
    if request.method == "POST" and request.form.get("sid"):
        sid = request.form.get("sid")
        enabled = checkboxVal(request.form.get("enabled"))
        list1 = {
            "urlformat": request.form.get("urlformat"),
            "urltype": request.form.get("urltype"),
            "startpage": request.form.get("startpage"),
            "maxpage": request.form.get("maxpage"),
            "step": request.form.get("step"),
            "listparent": request.form.get("listparent"),
            "entryparent": request.form.get("entryparent"),
            "pageparent": request.form.get("pageparent"),
            "filters": request.form.get("filters")
        }
        save = {
            "type": request.form.get("type"),
            "seed_name": request.form.get("seed_name"),
            "charset": request.form.get("charset"),
            "frequency": request.form.get("frequency"),
            "timeout": request.form.get("timeout"),
            "tries": request.form.get("tries"),
            "enabled": enabled,
            "listtype": request.form.get("listtype"),
            "lang": request.form.get("lang"),
            "rule": phpserialize.dumps(list1)
        }
        seed = Seed(current_app)
        msg = seed.edit(sid, **save)
        field = Field(current_app)
        fields = field.list(save["type"])
        seed_field = Seed_fields(current_app)
        for field in fields:
            seed_field.edit(sid, field.id, request.form.get(field.name))
        return redirect(url_for("seeds.index"))
    if request.method == "GET" and seed_id > 0:
        seed = Seed(current_app)
        seed_data = seed.view(seed_id)[0]
        seed_field = getSeedFieldsBySid(seed_id)
        seed_type = seed_data["type"]
        if seed_data["rule"]:
            seed_data["rule"] = phpserialize.loads(seed_data["rule"])
    return render_template("seed/add.html", seed_type=seed_type, fields=seed_field, seed_data=seed_data, sid=seed_id)

@seed.route("/delete/<int:seed_id>")
@auth
def delete(seed_id):
    return seed_id
