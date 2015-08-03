#!/usr/bin/python
import os
#os.system("sudo apt-get install python-wnck") #modifica mia
#os.system("sudo apt-get install python-xlib") #idem
import commands
import pygtk
import sys
import gobject
pygtk.require('2.0')
import base64
import gtk
import subprocess
import random
import xml.dom.minidom
from xml.dom.minidom import Node
import urllib, urllib2
import gtk, wnck, webbrowser
import re, getpass
import httplib
from urllib import FancyURLopener
from random import choice


from Xlib import X, display
# import re

homedir = os.environ['HOME']+"/.ubuntuwintv/"
icodir = "/usr/share/ubuntuwintv/"
versione = "0.7"
player = "vlc"
userlingua = os.environ['LANG']
lingua = userlingua[:2]
verificalingua = userlingua[:2]

vlcdir	= ""
agent	= "Mozilla/5.0 (X11; U; Linux x86_64; it; rv:1.9.1.7) Gecko/20100106 Ubuntu/9.10 (karmic) Firefox/3.5.7"


try:
	os.remove(homedir+'versione.txt')
except:
	pass

class progressbar:

	def updatebar(self,blocks, blocksize, filesize):
		bytes = blocks * blocksize
		if bytes >= filesize: 
			self.window.destroy()
			return
		perc = (100.0 * bytes) / filesize
		while gtk.events_pending():
			gtk.main_iteration(False)
		self.pbar.set_fraction((perc*0.01))
		self.window.show_all()
	
	
		
	def __init__(self,msg):
		self.window = gtk.Window()
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.resize(300,100)
		self.pbar = gtk.ProgressBar()
		self.pbar.set_pulse_step(0.1)
		self.label = gtk.Label(msg)
		self.box = gtk.VBox()
		self.box.add(self.label)
		self.box.add(self.pbar)
		self.window.add(self.box)
		self.window.show_all()


num = 0
button = gtk.Button()
rai = []
schermo = 0
videotop= 0
full = 0
radio = 0
posatt = 0
utente = getpass.getuser()
fileconf = "/home/"+utente+"/.ubuntuwintv/conf.txt"
mmode = 0
mplayer = 0
tgcom = []



def esci():
	sys.exit(0)

def ripeti():
	global posatt, mmode, player
	if (mmode==1):
		window_list = wnck.screen_get_default().get_windows()
		for win in window_list:
			#print win.get_name()
			nome = win.get_application().get_name().upper()
			if ((nome.find(player.upper())!=-1)):
				(x, y, width, height) = win.get_client_window_geometry()		
				d = display.Display().screen().root.query_pointer()._data
				mx = d['root_x']
				my = d['root_y']

				if ((nome.find(player.upper())!=-1) and (mx>x) and (my>y) and (mx<(x+width)) and (my<(y+width))):
					if posatt < 500: 
						posatt = 500
					else: 
						posatt = 0
					win.set_geometry ('WNCK_WINDOW_GRAVITY_CURRENT', 'WNCK_WINDOW_CHANGE_Y', x, posatt, width, height)

						
				elif ((nome.find(player.upper())!=-1) and (my<y) and (mx<x)):
						win.set_geometry ('WNCK_WINDOW_GRAVITY_CURRENT', 'WNCK_WINDOW_CHANGE_Y', x, 0, width, height)

			#print str(mx)
	d = []
	return True
		

def avvia():
		global button, utente, homedir, lingua,verificalingua
		carica
		#win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		#win.set_position(gtk.WIN_POS_MOUSE)
		#win.set_default_size(250,20)
		#win.set_title("UBUNTUWIN TV")
		
		#verifica esistenza lingua
		if os.path.exists("/usr/share/ubuntuwintvlingua_"+lingua+".txt")==False:
			verificalingua = lingua
			lingua = "en" 
		
		staticon = gtk.StatusIcon()
		staticon.set_from_file("/usr/share/icons/ubuntuwintv.png")		
		staticon.connect("activate", showMenu, None)
		staticon.set_visible(True)

		
		#image = gtk.Image()
		#image.set_from_file("/usr/share/icons/ubuntuwintv.png")
		##image.set_size_request(24, 24)
		
		
		#button.set_image(image)
		#button.connect("button_press_event", showMenu)
		##button.set_relief(gtk.RELIEF_NONE)
		#button.show()
		#screen = button.get_screen()
		#colormap = screen.get_rgba_colormap()
		#button.set_colormap(colormap)

		#win.add(button)
		#win.show_all()

		#showMenu()
				
		try:
			os.stat(homedir)
		except:
			os.mkdir(homedir)
		gobject.timeout_add(200,ripeti)
		
		gtk.main()
		return True
		
def loadico(naz):
		global icodir
		image = gtk.Image()
		image.set_from_file(icodir+naz+'.png')
		return image

def on_button_clicked(button, *args):
        global num
        if (num%2==0):
                image = gtk.Image()
                image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-red.png")
                button.set_image(image)
                button.set_label("")
        else:
                image = gtk.Image()
                image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-green.png")
                button.set_image(image)
                button.set_label("")
        num=num+1

def about(*arguments, **keywords):
		d = gtk.AboutDialog()
		d.set_name("Ubuntuwin TV")
		d.set_version("0.7")
		f = open ('/usr/share/common-licenses/GPL-3','r')
		gpl = f.readlines()
		txt = ""
		for lin in gpl:
			txt+=lin
		f.close()
		d.set_license(txt)
		d.set_wrap_license(True)
		d.set_authors(["UBUNTUWIN TV 0.7 @2009 Palumbo Roberto\n - palumborobertomail@gmail.com"])
		d.set_documenters(["Ringrazio il prof. Ing. Antonio Cantaro\n dell'Istituto Majorana di Gela \nper le sue guide sui miei programmi.\n Roberto Palumbo"])
		d.set_website("http://ubuntuwin.altervista.org")
		d.set_copyright("2009 Palumbo Roberto - palumborobertomail@gmail.com")
		d.run()
		d.destroy()

def create_menu(applet):
	propxml="""
			<popup name="button3">
			<menuitem name="bbb" verb="About" label="About"/>
			<menuitem name="bbb" verb="About" label="Aggiornamenti su: ubuntuwin.altervista.org"/>
			</popup>"""
	verbs = [("About", about)]
	applet.setup_menu(propxml, verbs, None)


def encode1(token):
        encoded = ""
        for ch in token:
                encoded += chr(ord(ch)^1)
        print(encoded+";1")
        return encoded+";1"
 
def encode2(token, key="hMrxuE2T8V0WRW0VmHaKMoFwy1XRc+hK7eBX2tTLVTw="):
        i = len(token)-1
        j = 0
        encoded = ""
        while i>=0:
                enc = chr(ord(token[i]) ^ ord(key[j]))
                encoded = enc + encoded
                i = i-1
                j = j+1
        print(encoded)
        return encoded

def encode3(token):
        return base64.encodestring(str.encode(token)).decode()

def tog(widget,data):
	global schermo,full,videotop,mplayer
	if data=='DISPLAY':
		if widget.get_active()==True:
			display=1
		else:
			display=0
	if data=='FULL':
		if widget.get_active()==True:
			full=1
		else:
			full=0
	if data=='VIDEOTOP':
		if widget.get_active()==True:
			videotop=1
		else:
			videotop=0
	if data=='MPLAYER':
		if widget.get_active()==True:
			mplayer=1
		else:
			mplayer=0

def salva(self):
	pass

def carica():
	global schermo,full,videotop,fileconf, radio, player
	if os.path.isfile(fileconf)==True:
		f = open(fileconf,'r')
		rl = f.readlines()
		f.close()
		for lin in rl:
			(n,par) = lin.split("=")
			if (n=="RADIOPLAYER"): 
				radio = par
				print par
			if (n=="DISPLAY"): schermo = int(par)
			if (n=="FULL"): full = int(par)
			if (n=="VIDEOTOP"): videotop = int(par)
			if (n=="PLAYER"): player = par



user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
]

class MyOpener(FancyURLopener, object):
    version = choice(user_agents)

def apricanale(can):
	global homedir
	canale = can
	myopener = MyOpener()
	myopener.addheader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	myopener.addheader("Accept-Language", "it-it,it;q=0.8,en-us;q=0.5,en;q=0.3")
	myopener.addheader("Accept-Encoding", "gzip,deflate")
	myopener.addheader("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
	myopener.addheader("Connection", "keep-alive")
	myopener.addheader("Keep-Alive", "115")
	myopener.addheader("viaurl", "www.rai.tv")
	myopener.addheader("ttAuth", raiauth(can))
	myopener.addheader("Content-Length", "0")
	
	
	myopener.retrieve(can, homedir+'raitv')
	f = open (homedir+"raitv",'r')
	g = f.readlines()
	m = "".join(g);
	#m.split('"');
	trov = m.split('"');
	for lis in trov:
		if (lis.find("mms://")!=-1):
			canale = lis
		if lis.find("http://")!=-1:
			canale = lis;
	return canale

def salva(self,win):
	global schermo,full,videotop, fileconf, player
	f = open(fileconf,'w')
	f.write("RADIOPLAYER=vlc"+"\n")
	f.write("DISPLAY="+str(schermo)+"\n")
	f.write("FULL="+str(full)+"\n")
	f.write("VIDEOTOP="+str(videotop)+"\n")
	f.write("PLAYER="+player)
	f.close()
	win.destroy()

#def visplay(widget,treeview,event,liststore):
	#path = widget.get_path_at_pos(int(event.x), int(event.y))
	#if (path == None):
		#"""If we didn't get apath then we don't want anything
		#to be selected."""
		#selection = widget.get_selection()
		#selection.unselect_all()
	#if (path != None):
		#treeselection = treeview.get_selection()
		#(model,iter) = treeselection.get_selected()
		#scegli(treeview,liststore.get_value(iter,1),liststore.get_value(iter,0),'s')

def selplayer(treeview,liststore):
	global player
	treeselection = treeview.get_selection()
	(model,iter) = treeselection.get_selected()
	if iter!=None:
		player = liststore.get_value(iter, 1)

def visplay(treeview, path, column):
	model = treeview.get_model()
	try:
		iter = model.get_iter(path)
		if model.get_value(iter,1)!=None:
			player = scegli(treeview,model.get_value(iter,2),model.get_value(iter,1),model.get_value(iter,3))
	except ValueError:
		return		

#def visarray(self,parametro,titolo):
	###init config
	#self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	#self.win.set_position(gtk.WIN_POS_MOUSE)
	#self.win.set_default_size(450,350)
	#self.win.set_title(titolo)
	#scroll = gtk.ScrolledWindow()
	#treeview = gtk.TreeView()
	#lista = gtk.TreeStore(str,str) 
	#treeview.set_model(lista)
	#tc = gtk.TreeViewColumn("Seleziona un programma")
	#cr = gtk.CellRendererText()
	#tc.pack_start(cr, True)
	#tc.add_attribute(cr, "text", 0)

	##parametro.sort()
	#headprec = ""
	#for menuItem in parametro:
		#head = menuItem[0]
		#if (head!=headprec):
			#print head
			#it = lista.append(None,[head,None])
		#lista.append(it,[menuItem[1],menuItem[2]])
		#headprec = menuItem[0]
		###if len(menuItem[2])>0:
	#treeview.append_column(tc)
	#treeview.connect('row_activated', visplay)
	#scroll.add(treeview)
	#box = gtk.VBox()
	##editcompl = gtk.EntryCompletion()
	##editcompl.set_model(lista)
	##editcompl.set_text_column(0)
	##edit = gtk.Entry()
	##edit.set_completion(editcompl)
	##box.add(edit)
	##box.add(scroll)
	#self.win.add(scroll)
	#self.win.show_all()


def finestrarimuovicanale(self,parametro,titolo,numfile):
	##init config
	self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.win.set_position(gtk.WIN_POS_MOUSE)
	self.win.set_default_size(450,350)
	self.win.set_title(titolo)
	scroll = gtk.ScrolledWindow()
	treeview = gtk.TreeView()
	lista = gtk.ListStore(str,str, str) 
	treeview.set_model(lista)
	tc = gtk.TreeViewColumn("Tipo")
	cr = gtk.CellRendererText()
	tc.pack_start(cr, True)
	tc.add_attribute(cr, "text", 0)
	tc.set_sort_column_id(0)

	treeview.append_column(tc)
	
	tc = gtk.TreeViewColumn("Canale")
	cr = gtk.CellRendererText()
	tc.pack_start(cr, True)
	tc.add_attribute(cr, "text", 1)
	tc.set_sort_column_id(0)

	treeview.append_column(tc)
	#parametro.sort()
	headprec = ""
	x = 0
	for menuItem in parametro:
		lista.append([x,menuItem[0],menuItem[1]])
		x=x+1
		##if len(menuItem[2])>0:
	treeview.set_rules_hint(True)
	treeview.connect('row_activated', cancellacanale,numfile)

	scroll.add(treeview)
	box = gtk.VBox()
	#editcompl = gtk.EntryCompletion()
	#editcompl.set_model(lista)
	#editcompl.set_text_column(0)
	#edit = gtk.Entry()
	#edit.set_completion(editcompl)
	#box.add(edit)
	#box.add(scroll)
	self.win.add(scroll)
	self.win.show_all()

def visarray(self,parametro,titolo):
	##init config
	self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.win.set_position(gtk.WIN_POS_MOUSE)
	self.win.set_default_size(450,350)
	self.win.set_title(titolo)
	scroll = gtk.ScrolledWindow()
	treeview = gtk.TreeView()
	lista = gtk.ListStore(str, str,str,str) 
	treeview.set_model(lista)
	tc = gtk.TreeViewColumn(trad("id"))
	cr = gtk.CellRendererText()
	tc.pack_start(cr, True)
	tc.add_attribute(cr, "text", 0)
	tc.set_sort_column_id(0)

	treeview.append_column(tc)
	
	tc = gtk.TreeViewColumn(trad("canale"))
	cr = gtk.CellRendererText()
	tc.pack_start(cr, True)
	tc.add_attribute(cr, "text", 1)
	tc.set_sort_column_id(1)

	treeview.append_column(tc)
	#parametro.sort()
	headprec = ""
	for menuItem in parametro:
		lista.append([menuItem[0],menuItem[1],menuItem[2],menuItem[3]])
		##if len(menuItem[2])>0:
	treeview.set_rules_hint(True)
	treeview.connect('row_activated', visplay)

	scroll.add(treeview)
	box = gtk.VBox()
	self.win.add(scroll)
	self.win.show_all()
	

def config(self,parametro):
	#global treeview,liststore
	global schermo,full,videotop,radio, player, verificalingua
	self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.win.set_position(gtk.WIN_POS_MOUSE)
	self.win.set_default_size(250,150)
	self.win.set_title(trad('conftitle'))
	self.title = 'App'
	self.button_r1 = gtk.CheckButton(trad('secondarydisplay'))
	self.button_r2 = gtk.CheckButton(trad('fullscreen'))
	self.button_r3 = gtk.CheckButton(trad('videoontop'))
	
	##init config
	treeview = gtk.TreeView()
	liststore = gtk.ListStore(str,str) 
	treeview.set_model(liststore)
	tc = gtk.TreeViewColumn(trad("defaultplayer"))
	cr = gtk.CellRendererText()
	tc.pack_start(cr, False)
	tc.set_attributes(cr, text = 0)
	liststore.append(["Vlc","vlc"])
	liststore.append(["Mplayer","mplayer"])
	liststore.append(["Kaffeine","kaffeine"])
	liststore.append(["Totem-xine","totem"])
	treeview.append_column(tc)
	if (player=="vlc"): 
		treeview.set_cursor(0)
	elif (player=="mplayer"):
		treeview.set_cursor(1)
	elif (player=="kaffeine"):
		treeview.set_cursor(2)
	elif (player=="totem"):
		treeview.set_cursor(3)
	treeview.connect('cursor-changed', selplayer,liststore)
	##	

	if (display==1):
		self.button_r1.set_active(True)
	if (full==1):
		self.button_r2.set_active(True)
	if (videotop==1):
		self.button_r3.set_active(True)
	
	self.button_r1.connect('toggled',tog,'DISPLAY')
	self.button_r2.connect('toggled',tog,'FULL')
	self.button_r3.connect('toggled',tog,'VIDEOTOP')
		

	avv = gtk.Label(trad("funzionaresolo"))
	avv.show()
	sep = gtk.VSeparator()
	sep.show()
	if os.path.exists("/usr/share/ubuntuwintvlingua_"+verificalingua+".txt")==True:	
		lin = gtk.Label(trad("linguatrovata"))
	else:
		lin = gtk.Label(trad("linguanontrovata")+" -> File not found : /etc/ubuntuwintv_"+verificalingua+".txt")
	lin.show()
	
	self.vbox = gtk.VBox(False,7)
	self.vbox.pack_start(self.button_r1,False,False,0)
	self.vbox.pack_start(self.button_r2,False,False,0)
	self.vbox.pack_start(self.button_r3,False,False,0)
	self.vbox.pack_start(sep,False,False,0)
	
	self.vbox.pack_start(avv,False,False,0)
		
	self.vbox.pack_start(treeview,False,False,0)

	
	self.save = gtk.Button(trad("saveandexit"))
	self.save.connect("clicked",salva,self.win)
	self.vbox.pack_start(self.save,False,False,0)
	self.vbox.pack_start(lin,False,False,0)
	self.win.add(self.vbox)
	self.win.show_all()

def downloadimage(url):
	global barra, homedir
	#progress_bar = ProgressBar(urllib.urlopen(url).info()['content-length'])
	barra = progressbar(trad("completeimage"))
	try:
		urllib.urlretrieve(url, homedir+"ubuntuwintvtemppng.png", barra.updatebar)

	except:
		pass

def download(url,titolo,nomefile):
	global barra, utente, homedir
	#urllib.urlopen(url).info()
	#progress_bar = ProgressBar(urllib.urlopen(url).info()['content-length'])
	barra = progressbar(titolo)
	try:
		urllib.urlretrieve(url, homedir+nomefile, barra.updatebar)

	except:
		print trad("scaricamentononriuscito").homedir+nomefile
		
	  #print "eccezione: n  %s, n  %s, n  %s n  durante lo scaricamento di %s" % (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2], url)
	  # remove potentially only partially downloaded file


#
#	webFile = urllib.urlopen(url)
#	localFile = open("/tmp/canali.xml", 'w')
#	localFile.write(webFile.read())
#	webFile.close()
#	localFile.close()

def procheck(widget,event):
	global mmode
	if event == "MMODE":
		if widget.get_active()==False:
			mmode = 0
		else:
			mmode = 1

def televideo(widget,p):
	webbrowser.open('http://www.televideo.rai.it/televideo/pub/solotesto.jsp?pagina='+p)

def apripalinsesti(widget):
	webbrowser.open('http://ubuntuwin.altervista.org/index.php?id=palinsesti')

def aggiornacanali(segnale):
	global rai, utente, homedir
	### rimuovi i file dei canali cosi' poi costringi il programma a ricaricarli
	#for l in range(1,6):
			#try:
	if ((segnale==0) and (os.path.exists(homedir+"canali.xml")==False)) or ((segnale!=0)):
		os.remove(homedir+"can.xml")
			#except:
				#pass
	if ((segnale==0) and (os.path.exists(homedir+"canali.xml")==False)) or ((segnale!=0)):
		download("http://www.rai.tv/dl/RaiTV/videoWall/PublishingBlock-5566288c-3d21-48dc-b3e2-af7fbe3b2af8.xml","Sto scaricando la lista delle trasmissioni RAI","canali.xml")
	doc = xml.dom.minidom.parse(homedir+"canali.xml")
	nome = ""
	indirizzo =""
	rai = []
	testo = ""
	for nodi in doc.getElementsByTagName("item"):
		nome = nodi.getAttribute("name")
		for imgunit in nodi.getElementsByTagName('imageUnit'):
			for img in imgunit.getElementsByTagName("image"):
				img = img.firstChild.nodeValue
		for txtunit in nodi.getElementsByTagName("textUnit"):
			if txtunit.getAttribute("type")=="Testo breve":
				for txt in txtunit.getElementsByTagName("text"):
					testo=txt.firstChild.nodeValue
		for video in nodi.getElementsByTagName("videoUnit"):
			subnome = video.getAttribute("name")
			for turl in video.getElementsByTagName("url"):
				indirizzo = turl.firstChild.nodeValue
				rai.append(("RAI TV",nome.upper()+" - "+subnome,indirizzo,testo,img))
	return


def creacatalogo (widget):
	global rai,homedir
	htm = open (homedir+'ubuntuwintv.html','w')
	barra = progressbar(trad("creazionecatalogo"))
	x = 1
	tutti = len(rai)
	htm.write('<html><head>'+trad("catalogocanalirai")+'</head><body>')
	htm.write('<p><strong>'+trad("canalivisibilicon")+' <a href="http://ubuntuwin.altervista.org">UBUNTUWIN TV</a>. '+trad("loghirai")+'</strong></p>')
	for menuItem in rai:
			htm.write('<p style="font-weight: bold; font-size: 12px">'+menuItem[1]+'</p>')
			htm.write('<p>'+menuItem[3]+'</p>')
			if menuItem[3].find("http")!=-1:
				htm.write('<p><img src="'+menuItem[3]+'"></p>')
			else:
				htm.write('<p><img height="150px;" border="1" src="http://www.rai.it/'+menuItem[4]+'"></p>')
			while gtk.events_pending():
				gtk.mainiteration(False)
			barra.pbar.set_fraction(float(x)/float(tutti))
			barra.window.show_all()
			x = x + 1
	htm.write('</body></html')
	htm.close()
	barra.window.hide_all()
	webbrowser.open(homedir+'ubuntuwintv.html')

def confermainserimento(widget,finestra,genere,nome,link,repid,tipo):
	global homedir
	nomes = nome.get_text()
	links = link.get_text()
	if (tipo=='rep'):
		repids = repid.get_text()
	
	errore = 0
	
	try:
		repids = str(int(repid.get_text()))
	except:
		errore = 0
			
	if ((tipo=="rep")):
		url = urllib.urlopen("http://ubuntuwin.altervista.org/repository.php?id="+repids).read()
		ar = url.split("#")
		nomes = ar[0]
		links = ar[1]
		if (len(nomes)==0):
			errore = 1
		if errore == 0:
			mostramessaggio (trad("aggiungerecanale")+nomes);
	if errore == 0:
		f = open (homedir+'canali'+str(genere)+'.txt','a')
		f.write (nomes.upper()+'#'+links+'\n')
		f.close()
		aggiornacanali(0)
		finestra.destroy()

def aggiungicanale(widget, genere):
	win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	win.set_position(gtk.WIN_POS_MOUSE)
	win.set_default_size(250,150)
	win.set_title(trad("aggiungicanale"))
	nome = gtk.Entry()
	nome.set_text(trad("nomecanale"))
	link = gtk.Entry()
	link.set_text(trad("linkcanale"))
	but = gtk.Button()
	but.set_label("Conferma")
	but.connect("clicked",confermainserimento,win,genere,nome,link,"","norep")
	orizz = gtk.HBox()
	repid = gtk.Entry()
	repid.set_text("RepID")
	butrep = gtk.Button()
	butrep.set_label(trad("aggiungidalrepository"))
	butrep.connect("clicked",confermainserimento,win,genere,repid,link,repid,"rep")
	linkrep = gtk.LinkButton("http://ubuntuwin.altervista.org/index.php?id=80",trad("Web Repository"))
	linkrep.show()
	orizz.add(repid)
	orizz.add(butrep)
	orizz.add(linkrep)
	h = gtk.VBox(4)
	h.add(nome)
	h.add(link)
	h.add(but)
	h.add(orizz)
	win.add(h)
	win.show_all()
	
def cancellacanaleconferma(widget,win,y,titolo,link,numfile):
	global homedir
	f = open (homedir+'canali'+str(numfile)+'.txt','r')
	t = f.readlines()
	f.close()
	
	f = open (homedir+'canali'+str(numfile)+'.txt','w')
	t.remove(titolo+'#'+link)
	f.writelines(t)
	f.close()
	win.destroy()
	

def cancellacanale(treeview, path, column,numfile):
	model = treeview.get_model()
	try:
		iter = model.get_iter(path)
		if model.get_value(iter,1)!=None:
			titolo = model.get_value(iter,1)
			link = model.get_value(iter,2)
			win = gtk.Window(gtk.WINDOW_TOPLEVEL)
			win.set_position(gtk.WIN_POS_MOUSE)
			win.set_default_size(250,100)
			win.set_title(trad("rimuovicanale"))
			nome = gtk.Label(trad("sicurorimuoverecanale")+titolo+"?")
			but = gtk.Button()
			but.set_label(trad("Conferma"))
			but.connect("clicked",cancellacanaleconferma,win,model.get_value(iter,0),titolo,link,numfile)
			h = gtk.VBox(2)
			h.add(nome)
			h.add(but)
			win.add(h)
			win.show_all()
	except ValueError:
		return		

def mostramessaggio(messaggio):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,gtk.BUTTONS_NONE, messaggio)
	dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
	dialog.run()
	dialog.destroy()
	
def aggiornaversione(messaggio,link):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,gtk.BUTTONS_NONE, messaggio)
	dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
	dialog.run()
	dialog.destroy()
	webbrowser.open(link)

#def showMenu():
	#global rai, mmode, versione,tgcom,icodir,homedir
	#allchannel = []
	#utente = []
	#if event.button == 1:
		#menu = gtk.Menu()

		#if os.path.exists(homedir+'versione.txt')==False:
			#download("http://ubuntuwin.altervista.org/fileadmin/user_upload/ubuntuwintv/versione.txt","Sto verificando l'esistenza di aggiornamenti","versione.txt")
			#r = open (homedir+'versione.txt','r')
			#rv = r.readlines()
			#r.close()
			#if rv[0].strip()!=versione:
				#aggiornaversione(trad("nuovaversionedisponibile")+" : "+rv[0],rv[1])

				####try:
		#if os.path.exists(homedir+"can.xml")==False:
			#download("http://ubuntuwin.altervista.org/fileadmin/user_upload/ubuntuwintv/can.xml","Sto scaricando i canali di UBUNTUWINTV","can.xml")
		#if os.path.exists(homedir+"can.xml")==True:
			#doc = xml.dom.minidom.parse(homedir+"can.xml")
			#for nodi in doc.getElementsByTagName("menu"):
				#nome = nodi.getAttribute("name")
				#flag = nodi.getAttribute("ico")
				#top = gtk.ImageMenuItem(nome)
				#top.set_image(loadico(flag))
				#menuitem = gtk.Menu()
				#for mitem in nodi.getElementsByTagName('menuitem'):
					#nc = mitem.getAttribute("name")
					#link = mitem.getAttribute("link")
					#label = mitem.getAttribute("label")
					#forza  = mitem.getAttribute("forza")
					#item = gtk.ImageMenuItem(nc)
					#item.connect("activate",scegli,link,nc,forza)
					#item.show()
					#menuitem.add(item)
					#top.set_submenu(menuitem)
					#top.show()
					#smenuitem = gtk.Menu()
					#for sitem in mitem.getElementsByTagName('submenu'):
						#snc = sitem.getAttribute("name")
						#slink = sitem.getAttribute("link")
						#slabel = sitem.getAttribute("label")
						#sforza  = sitem.getAttribute("forza")
						#smitem = gtk.ImageMenuItem(snc)
						#smitem.connect("activate",scegli,slink,snc,sforza)
						#allchannel.append((nome+" - "+nc,snc,slink))
						#smitem.show()
						#smenuitem.add(smitem)
						#item.set_submenu(smenuitem)
						#item.show()
						#umenuitem = gtk.Menu()
						#for uitem in sitem.getElementsByTagName('ultimo'):
							#unc = uitem.getAttribute("name")
							#ulink = uitem.getAttribute("link")
							#ulabel = uitem.getAttribute("label")
							#uforza  = uitem.getAttribute("forza")
							#umitem = gtk.ImageMenuItem(unc)
							#umitem.connect("activate",scegli,ulink,unc,uforza)
							#allchannel.append((nome+" - "+nc,unc,ulink))
							#umitem.show()
							#umenuitem.add(umitem)
							#smitem.set_submenu(umenuitem)
							#smitem.show()
					#if (nome=="ITALY") and (nc=="RADIO"):
							#if len(rai)<=0:
									#aggiornacanali(0)
							#ritem = gtk.ImageMenuItem(trad("programmiregistratirai"))
							#ritem.show()
							#ritem.connect("activate",visarray,rai,trad("programmiregistratirai"))
							#menuitem.add(ritem)
							#citem = gtk.ImageMenuItem(trad("creamostracatalogorai"), True)
							#citem.show()
							#citem.connect("activate",creacatalogo)
							#menuitem.add(citem)
							#pal = gtk.ImageMenuItem(trad("palinsesti"),True)
							#pal.show()
							#pal.connect("activate",apripalinsesti)
							#menuitem.add(pal)
			
				#menu.add(top)

			#for l in range(1,3):
				#if l==1 : titolo = trad("usertv")
				#if l==2 : titolo = trad("userradio")
				## aggiungi anche i canali utente
				#utente = []
				#try:
					#if (os.path.isfile(homedir+'canali'+repr(l)+'.txt')==False):
						#f = open (homedir+'canali'+repr(l)+'.txt','w')
						#f.write("")
						#f.close()
					#f = open (homedir+'canali'+repr(l)+'.txt','r')
					#canali = f.readlines()
					#f.close()
					#canali.sort()
					#for str in canali:
						#try:
							#(nome,indirizzo)=str.split('#')
							#utente.append((trad("canaleutente"),nome,indirizzo))
						#except:
							#pass
					##arr.sort()
					
					#menuutente = gtk.Menu()
					
					#menuitem = gtk.ImageMenuItem(titolo)
					#menuitem.set_image(loadico('user32'))
					
					#useritems = []
					
							
					#for menuItem in utente:
						#canitem = gtk.ImageMenuItem(menuItem[1].upper(), True)
						#canitem.connect("activate", scegli,menuItem[2],menuItem[1],'s')
						#useritems.append((menuItem[1],menuItem[2]))
						#allchannel.append((trad("usertv"),menuItem[1],menuItem[2]))
						#canitem.show()
						#menuutente.add(canitem)

					#sep = gtk.SeparatorMenuItem()
					#sep.show()
					#menuutente.add(sep)
					
					#aggitem = gtk.ImageMenuItem(trad("aggiungi"), True)
					#aggitem.show()
					#aggitem.connect( "activate", aggiungicanale, l)
					#menuutente.add(aggitem)
					
					#cancancitem = gtk.ImageMenuItem(trad("rimuovi"))
					#cancancitem.connect("activate",finestrarimuovicanale,useritems,"Doppio click sul canale da rimuovere",l)
					#cancancitem.show()
					#menuutente.add(cancancitem)
					
					
					#menuutente.show()
					#menuitem.show()
					##cmenuitem.show()
					#menuitem.set_submenu(menuutente)		
					#menu.add(menuitem)
				#except:
					#pass
			
			#can = gtk.ImageMenuItem(trad("aggiornacanali"),True)
			#can.show()
			#can.connect("activate",aggiornacanali)
			#menu.add(can)
			

			#cfg = gtk.ImageMenuItem("Config",True)
			#cfg.show()
			#cfg.connect("activate",config,"aaa")
			#menu.add(cfg)
			

					
			#telecomando = gtk.ImageMenuItem(trad("telecomando"),True)
			#telecomando.show()
			#telecomando.connect("activate",visarray,allchannel,trad("selezionaprogramma"))
			#menu.add(telecomando)
					
			
			
			#mmodem = gtk.CheckMenuItem("Move Mode",True)
			#mmodem.connect("toggled",procheck,"MMODE")
			#mmodem.show()
			#menu.add(mmodem)
			
			#sep = gtk.SeparatorMenuItem()
			#sep.show()
			#menu.add(sep)
			
			#about = gtk.ImageMenuItem("www.ubuntuwin.org",True)
			#about.connect("activate",showAboutDialog)
			#about.show()
			#menu.add(about)
			
			#if mmode==1:
				#mmodem.set_active(True)

			#menu.popup( None, None, None, event.button, event.time )
		
	#if event.button == 3:
		#widget.emit_stop_by_name("button_press_event")
		#create_menu(applet)

def menutelevideo():
	tel = gtk.ImageMenuItem(trad("Televideo"),True)
	telmenu = gtk.Menu()
	telmenuitem = gtk.ImageMenuItem("Indice")
	telmenuitem.connect("activate",televideo,"100")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Sport")
	telmenuitem.connect("activate",televideo,"200")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Borsa-Fondi")
	telmenuitem.connect("activate",televideo,"300")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Istituzioni")
	telmenuitem.connect("activate",televideo,"400")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Societa'")
	telmenuitem.connect("activate",televideo,"420")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Tv-Magazine")
	telmenuitem.connect("activate",televideo,"500")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Meteo-viaggi")
	telmenuitem.connect("activate",televideo,"600")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Sottotitoli")
	telmenuitem.connect("activate",televideo,"770")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Oggi-Flash")
	telmenuitem.connect("activate",televideo,"800")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Ultima Ora")
	telmenuitem.connect("activate",televideo,"102")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Primo Piano")
	telmenuitem.connect("activate",televideo,"110")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Politica")
	telmenuitem.connect("activate",televideo,"120")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Economia")
	telmenuitem.connect("activate",televideo,"130")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Dall'Italia")
	telmenuitem.connect("activate",televideo,"140")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Dal Mondo")
	telmenuitem.connect("activate",televideo,"150")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Culture")
	telmenuitem.connect("activate",televideo,"160")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Cittadini")
	telmenuitem.connect("activate",televideo,"170")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Speciale")
	telmenuitem.connect("activate",televideo,"180")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenuitem = gtk.ImageMenuItem("Motori")
	telmenuitem.connect("activate",televideo,"810")
	telmenuitem.show()
	telmenu.add(telmenuitem)
	telmenu.show()
	tel.set_submenu(telmenu)
	tel.show()
	return tel
	

def showMenu(widget,data=None):
	global rai, mmode, versione,tgcom,icodir,homedir
	allchannel = []
	utente = []
	menu = gtk.Menu()
	
	#questo scarica il file, ma va sostituito con una funzione che apra e basta. Pensavo di far salvare in un file can.xml nella home, come l'originale
	#if os.path.exists(homedir+'versione.txt')==False:
		#download("http://ubuntuwin.altervista.org/fileadmin/user_upload/ubuntuwintv/versione.txt","Sto verificando l'esistenza di aggiornamenti","versione.txt")
		#r = open (homedir+'versione.txt','r')
		#rv = r.readlines()
		#r.close()
		#if rv[0].strip()!=versione:
			#aggiornaversione(trad("nuovaversionedisponibile")+" : "+rv[0],rv[1])

			###try:
	if os.path.exists(homedir+"can.xml")==False:
		#download("http://ubuntuwin.altervista.org/fileadmin/user_upload/ubuntuwintv/can.xml","Sto scaricando i canali di UBUNTUWINTV","can.xml")
		print "Errore, inserire una file can.xml nella home directory"
		
	if os.path.exists(homedir+"can.xml")==True:
		doc = xml.dom.minidom.parse(homedir+"can.xml")
		for nodi in doc.getElementsByTagName("menu"):
			nome = nodi.getAttribute("name")
			flag = nodi.getAttribute("ico")
			top = gtk.ImageMenuItem(nome)
			top.set_image(loadico(flag))
			menuitem = gtk.Menu()
			for mitem in nodi.getElementsByTagName('menuitem'):
				nc = mitem.getAttribute("name")
				link = mitem.getAttribute("link")
				label = mitem.getAttribute("label")
				forza  = mitem.getAttribute("forza")
				item = gtk.ImageMenuItem(nc)
				item.connect("activate",scegli,link,nc,forza)
				item.show()
				menuitem.add(item)
				top.set_submenu(menuitem)
				top.show()
				smenuitem = gtk.Menu()
				for sitem in mitem.getElementsByTagName('submenu'):
					snc = sitem.getAttribute("name")
					slink = sitem.getAttribute("link")
					slabel = sitem.getAttribute("label")
					sforza  = sitem.getAttribute("forza")
					smitem = gtk.ImageMenuItem(snc)
					smitem.connect("activate",scegli,slink,snc,sforza)
					allchannel.append((nome+" - "+nc,snc,slink,sforza))
					smitem.show()
					smenuitem.add(smitem)
					item.set_submenu(smenuitem)
					item.show()
					umenuitem = gtk.Menu()
					for uitem in sitem.getElementsByTagName('ultimo'):
						unc = uitem.getAttribute("name")
						ulink = uitem.getAttribute("link")
						ulabel = uitem.getAttribute("label")
						uforza  = uitem.getAttribute("forza")
						umitem = gtk.ImageMenuItem(unc)
						umitem.connect("activate",scegli,ulink,unc,uforza)
						allchannel.append((nome+" - "+nc,unc,ulink,uforza))
						umitem.show()
						umenuitem.add(umitem)
						smitem.set_submenu(umenuitem)
						smitem.show()
				if (nome=="ITALY") and (nc=="RADIO"):
						if len(rai)<=0:
								aggiornacanali(0)
						ritem = gtk.ImageMenuItem(trad("programmiregistratirai"))
						ritem.show()
						ritem.connect("activate",visarray,rai,trad("programmiregistratirai"))
						menuitem.add(ritem)
						citem = gtk.ImageMenuItem(trad("creamostracatalogorai"), True)
						citem.show()
						citem.connect("activate",creacatalogo)
						menuitem.add(citem)
						pal = gtk.ImageMenuItem(trad("palinsesti"),True)
						pal.show()
						pal.connect("activate",apripalinsesti)
						menuitem.add(pal)
						tel = menutelevideo()
						menuitem.add(tel)
		
			menu.add(top)

		for l in range(1,3):
			if l==1 : titolo = trad("usertv")
			if l==2 : titolo = trad("userradio")
			# aggiungi anche i canali utente
			utente = []
			try:
				if (os.path.isfile(homedir+'canali'+repr(l)+'.txt')==False):
					f = open (homedir+'canali'+repr(l)+'.txt','w')
					f.write("")
					f.close()
				f = open (homedir+'canali'+repr(l)+'.txt','r')
				canali = f.readlines()
				f.close()
				canali.sort()
				for str in canali:
					try:
						(nome,indirizzo)=str.split('#')
						utente.append((trad("canaleutente"),nome,indirizzo))
					except:
						pass
				#arr.sort()
				
				menuutente = gtk.Menu()
				
				menuitem = gtk.ImageMenuItem(titolo)
				menuitem.set_image(loadico('user32'))
				
				useritems = []
				
						
				for menuItem in utente:
					canitem = gtk.ImageMenuItem(menuItem[1].upper(), True)
					canitem.connect("activate", scegli,menuItem[2],menuItem[1],'')
					useritems.append((menuItem[1],menuItem[2]))
					allchannel.append((trad("usertv"),menuItem[1],menuItem[2],''))
					canitem.show()
					menuutente.add(canitem)

				sep = gtk.SeparatorMenuItem()
				sep.show()
				menuutente.add(sep)
				
				aggitem = gtk.ImageMenuItem(trad("aggiungi"), True)
				aggitem.show()
				aggitem.connect( "activate", aggiungicanale, l)
				menuutente.add(aggitem)
				
				cancancitem = gtk.ImageMenuItem(trad("rimuovi"))
				cancancitem.connect("activate",finestrarimuovicanale,useritems,"Doppio click sul canale da rimuovere",l)
				cancancitem.show()
				menuutente.add(cancancitem)
				
				
				menuutente.show()
				menuitem.show()
				#cmenuitem.show()
				menuitem.set_submenu(menuutente)		
				menu.add(menuitem)
			except:
				pass
		
		can = gtk.ImageMenuItem(trad("aggiornacanali"),True)
		can.show()
		can.connect("activate",aggiornacanali)
		menu.add(can)
		

		cfg = gtk.ImageMenuItem("Config",True)
		cfg.show()
		cfg.connect("activate",config,"aaa")
		menu.add(cfg)
		

				
		telecomando = gtk.ImageMenuItem(trad("telecomando"),True)
		telecomando.show()
		telecomando.connect("activate",visarray,allchannel,trad("selezionaprogramma"))
		menu.add(telecomando)
				
		
		
		mmodem = gtk.CheckMenuItem("Move Mode",True)
		mmodem.connect("toggled",procheck,"MMODE")
		mmodem.show()
		menu.add(mmodem)
		
		sep = gtk.SeparatorMenuItem()
		sep.show()
		menu.add(sep)
		
		about = gtk.ImageMenuItem("About",True)
		about.connect("activate",showAboutDialog)
		about.show()
		menu.add(about)

		quit = gtk.ImageMenuItem(trad("quit"),True)
		quit.connect("activate",exit)
		quit.show()
		menu.add(quit)
		
		if mmode==1:
			mmodem.set_active(True)

		#menu.popup( None, None, None, event.button, event.time )
		menu.popup( None, None, None, 0, 0 )
		

def mostraimmagine(widget,parametro):
	Img = gtk.Image()
	downloadimage(parametro)
	win = gtk.Window()
	img = gtk.Image()
	img.set_from_file('/tmp/ubuntuwintvtemppng.png')
	win.add(img)
	win.show_all()


def canhook(nome,parametro):
	global homedir
	return parametro
	
def trad(txt):
	global homedir, lingua
	torna = txt
	f = open ('/usr/share/ubuntuwintvlingua_'+lingua+'.txt','r')
	
	arr = f.readlines()
	f.close
	
	for item in arr:
		el = item.split("=")
		if (txt==el[0]):
			titolo = el[1]
			torna = titolo[:-1]
	return torna 

def scegli(widget,parametro,nome,forza):
	global button
	global num, schermo, full,videotop,player
	#print nomepython
	parametro=canhook(nome,parametro);
	if (parametro.upper()!="NO"):
		num=num+1
		fullscreens=""
		videotops=""
		schermos=""
		#if (nome=='RAI UNO') or (nome=='RAI DUE') or (nome=='RAI TRE') or (nome=='RAI QUATTRO') or (nome=='RAI NEWS 24') or (nome=='RAI SPORT +') or (nome=='RAI EDU1') or (nome=='RAI STORIA') or (nome=='RAI SAT EXTRA') or (nome=='RAI SAT PREMIUM') or (nome=='RAI SAT CINEMA') or (nome=='RAI SAT YOYO') or (nome=='RAI SAT GULP'):
				#if parametro.find('mediapolis.rai.it')!=-1:
		#	forza='s'
		if (player=="vlc"):
			os.system("killall vlc")
			if (full==1):
				fullscreens=" -f "
			else:
				fullscreens=""
			if (videotop==1):
				videotops="  --video-on-top "
			else:
				videotops=""
			if (schermo==0):
				print forza
				print fullscreens
				print videotops
				print "uno "+parametro
				print "Forza : "+forza
				if forza!='s':
					subprocess.Popen("vlc "+fullscreens+videotops+parametro,shell=True)
				else:
					subprocess.Popen("python /usr/bin/rai.py "+parametro+" | vlc "+fullscreens+videotops+" - ",shell=True)
			else:
				subprocess.Popen("DISPLAY=:0.1 vlc "+videotops+parametro+fullscreens,shell=True)
		elif (player=="mplayer"):
			os.system("killall mplayer")
			if forza=='s': 
				forza='  -user-agent "Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6" '
			if (full==1) : fullscreens=" -fs "
			if (videotop==1): videotops=" -ontop "
			if (schermo==1): schermos="DISPLAY=:0.1 " 
			subprocess.Popen(schermos+'mplayer '+fullscreens+videotops+forza+parametro,shell=True)
		elif (player=="totem"):
			os.system("killall totem-xine")
			if forza=='s': forza='  -user-agent "Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6" '
			if (full==1) : fullscreens=" -fullscreen "
			if (videotop==1): videotops=" -ontop "
			if (schermo==1): schermos="DISPLAY=:0.1 " 
			subprocess.Popen(schermos+'totem-xine '+forza+parametro,shell=True)
		elif (player=="kaffeine"):
			os.system("killall kaffeine")
			if (full==1) : fullscreens=" -f"
			if (videotop==1): videotops=""
			if (schermo==1): schermos="DISPLAY=:0.1 " 
			subprocess.Popen(schermos+'kaffeine '+parametro,shell=True)


def sceglimplayer(widget,parametro):
	global button
	global num, schermo, full,videotop,mplayer
	
	os.system("killall vlc")
	os.system("killall mplayer")
	subprocess.Popen('mplayer '+parametro,shell=True)


def showAboutDialog(*arguments, **keywords):
        about('','')


avvia()


