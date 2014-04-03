#!/usr/bin/env python
#coding: utf-8

import os, sys
from flask import Flask, g

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parentdir not in sys.path:
    sys.path.insert(0,parentdir) 

from web import views
from web.config import DefaultConfig
from web import model
from web import helpers
from libs.daemon import Daemon
from datetime import datetime

app_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ['spyder_web']

class spyder_web:
    DEFAULT_APP_NAME = "spyder_web"
    MODULES = (
	(views.home, ""),
	(views.settings, "/settings"),
	(views.site_map, "/site_map"),
	(views.seed, "/seed"),
	(views.seeds, "/seeds"),
	(views.article, "/article"),
	(views.site, "/site"),
	(views.sites, "/sites"),
	(views.user, "/user"),
	(views.users, "/users"),
	(views.status, "/status"),
	(views.test_seed, "/test_seed")
    );

    def __init__(self):
	# Register an application in Flask
	# @param appName
	# @param static_path
	# @param static_url_path
	# @param static_folder (default: static)
	# @param template_folder (default: templates)
	# @param instance_path
	# @param instance_relative_config 
	self.app = Flask(self.DEFAULT_APP_NAME, static_folder=os.path.join(app_dir, "static"),template_folder=os.path.join(app_dir, "templates"))
	#load config
	self.app.config.from_object(DefaultConfig());
	self.configure_modules()
	self.app.secret_key = self.app.config.get("SECRET_KEY", "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT")

	@self.app.template_filter()
	def timesince(value):
	    return helpers.timesince(value)

	@self.app.template_filter()
	def getSiteStatus(value):
	    return helpers.getSiteStatus(value)

	@self.app.template_filter()
	def getPageTypeText(value):
	    return helpers.getPageTypeText(value)

	@self.app.template_filter()
	def getSeedTypeText(value):
	    return helpers.getSeedTypeText(value)

	@self.app.template_filter()
	def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
		return datetime.fromtimestamp(value).strftime(format)

	@self.app.context_processor
	def utility_processor():
	    def somefunc(name):
		return helpers.somefunc(name)
	    return dict(somefunc=somefunc)

    def configure_modules(self):
	"""
	Mapping the module url rules
	"""
	for module, url_prefix in self.MODULES:
	    self.app.register_module(module, url_prefix=url_prefix)


    def run(self, host=None, port=None, **options):
	"""
	Runs the application on a local development server.
	@param host  the hostname to listen on. Set this to `0.0.0.0` to have the server
	    available externally as well. Defaults to `127.0.0.1`
	@param port  the port of the webserver. Defaults 5000
	@param debug if given, enable or disable debug mode
	@param options: see `werkzeug.serving.run_simple` for more infomation
	"""
	debug = self.app.config.get("DEBUG", False);
	self.app.run(host, port, debug, **options);

if __name__ == "__main__":
    app = spyder_web();
    app = app.run(host="0.0.0.0", port=8080);
