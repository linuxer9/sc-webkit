#!/usr/bin/python
# -*- coding: UTF-8 -*-
# this program is simplified and Webkit based Software center allows you to install, remove
# and search programs.. with a nice GUI based on design off debi control center.
# the goal of this program is to provide an environment allows user to control packages easily.
  


import gtk,pygtk,commands,gettext
import webkit
import apt
from locale import getdefaultlocale



pygtk.require("2.0")

cache = apt.Cache()
def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

# i18n
gettext.install("sc", "/usr/share/locale")
program = _("software center")
version = '0.1'
categories = ["featured","internet","multimedia","graphics","office","games",
"islamic","tools","education","development"]
class sc:
	def __init__(self):
		self.frontend()
	def frontend(self):
		self.window = gtk.Window()
		self.window.connect('destroy', gtk.main_quit)
		self.window.set_title(program)
		#self.window.set_icon("software-center")
		self.window.set_size_request(800, 620)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.browser = webkit.WebView()
		swindow = gtk.ScrolledWindow()
		self.window.add(swindow)
		swindow.add(self.browser)
		self.window.show_all()
		self.browser.connect("navigation-requested", self.functions)
		self.browser.connect("load-finished", self._on_load_finished)
		filee=open('/usr/lib/sc/frontend/default.html', 'r')
		html=filee.read()
		
		html = self.i18n(html)
		self.browser.load_html_string(html, 'file:///usr/lib/sc/frontend/')
		#no right click menu
		settings = self.browser.get_settings()
		settings.set_property('enable-default-context-menu', False)
		self.browser.set_settings(settings)
		self.icons = gtk.IconTheme()
		self.icons.prepend_search_path("/usr/share/app-install/icons")
		
		
	def _on_load_finished(self,view, frame):
		self.show_category(1)
		print "loaded category 1"
	def i18n(self,html):
		# A اللغة
		lang=getdefaultlocale()[0].split('_')[0]

		if lang=="ar":
			html=html.replace("{DIR_dir}", "rtl")
		else:
			html=html.replace("{DIR_dir}", "ltr")
		#Aتحديد اللغة في الملف  
		html=html.replace("{LANG_lang}", lang)
		translation = [ ["{string_1}",_("Featured")],
							 ["{string_2}",_("Internet")],
							 ["{string_3}",_("Multimedia")],
							 ["{string_4}",_("Graphics")],
							 ["{string_5}",_("Office")],
							 ["{string_6}",_("Games")],
							 ["{string_7}",_("Islamic")],
							 ["{string_8}",_("System")],
							 ["{string_9}",_("Education")],
							 ["{string_10}",_("Development")],
							 ["{remove_str}",_("remove")],
							 ["{install_str}",_("install")],
							 ["{details_str}",_("details")]

		]
		for i in translation:
			html=html.replace(i[0], i[1])
		return html
		
	def functions(self,view, frame, req, data=None):
		'''This function is to receive functions from webkit
		functions() لاستقبال الأوامر والدوال من المتصفح'''
		uri = req.get_uri()
		ida, path=uri.split('://', 1)
		path = path.replace("%20"," ")
		print ida
		print uri
		
		if ida == "file":
			
			return False
		if ida=="about":
			'''launch About dialog
			ida==about فتح صندوق حوار عن البرنامج'''
			
			text = _('this program is simplified and Webkit based Software center allows you to install, remove and search programs.. with a nice GUI based on design off debi control center.This program licensed under the terms of GPL 2 or newer version.')
			self.browser.execute_script("show_about('%s','%s','%s')" %(program, version, text))

	        	
	        	return True
		if ida=="cat":

			self.browser.execute_script("cats_empty()")
			return self.show_category(int(path))
		if ida == "pro":

			self.browser.execute_script("show_package('%s')"%(path))
			return True
		if ida == 'packclick':
			desc = cache[path].candidate.summary
			installed = str(cache[path].is_installed).lower()
			self.browser.execute_script("focus_change()")
			self.browser.execute_script("show_desc('%s','%s','%s')"%(path,desc,installed))
			return True
			
			

				
			
		
	def show_category(self, category_num):
		self.browser.execute_script("clear_category(%s)" %(str(category_num)))

		category = str(category_num)+"-" + categories[category_num-1] + ".list"
		
		category = open("/usr/lib/sc/categories/" + category).read().split()
		
		category = [ i for i in category if i in cache ]
		category.sort()
		for i in category :
			# function add_package(Name, desc, icon, category) { }
			self.browser.execute_script("add_package('%s','%s', %i)" %(i, self.get_icon(i), category_num))
			#print "add_package('%s','%s', '%s', %i)" %(i, i, i, category_num)
		return True
	def get_icon(self, package):
		#icon = xdg.IconTheme.getIconPath(package, 48, "debi-icon-theme")

		icon = self.icons.lookup_icon(package,48,0)
		if icon is not None and ".xpm" not in icon.get_filename()  :
			return "file://" + icon.get_filename() 
		else:
			return "file:///usr/lib/sc/frontend/icons/default.png"
	#def get_summary(self, package):
	#	return apt.Cache()[package].summary
	#def get_pack_info(self, pack):
		
		#return [screen_shot, description, status, size, depends]
a = sc()
gtk.main()