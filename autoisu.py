import os
os.environ["KIVY_NO_ARGS"] = "1"
os.environ['KIVY_IMAGE'] = "pil,sdl2"
os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\glew\\bin')
os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\sdl2\\bin')
from tabulate import tabulate
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from kivy.clock import Clock
from kivymd.uix.fitimage import FitImage
import bcrypt
import time
import datetime
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivymd.uix.pickers import MDDatePicker
# ---------------------------------------MATPLOTLIB
import pandas as pd
import matplotlib.pyplot as plt
import re
# -------------------------------------WINDWOS MAXIMIZE
from kivy.core.window import Window
# -------------------------------------WINDWOS MAXIMIZE
# -------------------------------------CLOCK WIDGET
def clock_now():
	clock_now = datetime.datetime.utcnow()+datetime.timedelta(hours=3)
	clock_now_return = clock_now.strftime("%d-%m-%Y %H:%M:%S")
	return clock_now_return
def clock_now_DATE_VIEW():
	clock_now = datetime.datetime.utcnow()+datetime.timedelta(hours=3)
	clock_now_return_x = clock_now.strftime("%d-%m-%Y")
	return clock_now_return_x
# -------------------------------------CLOCK WIDGET




# Designate our .kv design file
class Pag1(Screen):

	def submit(self, *args):
		try:
			conn = sqlite3.connect("isu_db.db")

			# Create a Cursor
			c = conn.cursor()


			# PENTRU ADMINI --------------------------------------------------------------------------------------------------VERIFICARE
			if ".admin" in self.ids.user.text:
				c.execute("SELECT * FROM users_admin WHERE user_admin=:user_admin", {"user_admin": self.ids.user.text})


				# Verification step
				verification_step = c.fetchone()


				if verification_step[0] == self.ids.user.text and bcrypt.checkpw(bytes(self.ids.password.text,"utf-8"), bytes(verification_step[1],"utf-8")):

					admin_strip = self.ids.user.text.rsplit(".")

					self.ids.welcome_label.text = f"Welcome {admin_strip[0].capitalize()}!"
					Clock.schedule_once(self.next_screen_admin, 2) # TIMER

				else:
					self.ids.welcome_label.text = "Wrong Password!"


				# conn.commit()
				conn.close()




			# PENTRU USER SIMPLI --------------------------------------------------------------------------------------------------VERIFICARE
			else:
				c.execute("SELECT * FROM users WHERE user=:user", {"user": self.ids.user.text})


				# Verification step
				verification_step = c.fetchone()

				if verification_step[0] == self.ids.user.text and bcrypt.checkpw(bytes(self.ids.password.text,"utf-8"), bytes(verification_step[1],"utf-8")):


					self.ids.welcome_label.text = f"Welcome {self.ids.user.text.capitalize()}!"
					Clock.schedule_once(self.next_screen, 2) # TIMER

				else:
					self.ids.welcome_label.text = "Wrong Password!"


				# conn.commit()
				conn.close()

		# EROARE USERNAME DIN DATABASE --------------------------------------------------------------------------------------------------VERIFICARE
		except Exception as e:

			self.ids.welcome_label.text = "Wrong Username!"
			print("Error "+ str(e))


		# DELAY TRANSITIE PAGINA LOGIN--------------------------------------------------------------------------------------------------DELAY
	def next_screen(self, *args): # asta e pentru delay-ul acela pentru pagina de inceput
		self.manager.current = 'pag2'
		self.manager.transition.direction="left"
		# DELAY TRANSITIE PAGINA LOGIN ADMIN--------------------------------------------------------------------------------------------------DELAY ADMIN
	def next_screen_admin(self, *args): # asta e pentru delay-ul acela pentru pagina de inceput
		self.manager.current = 'pag3'
		self.manager.transition.direction="right"


#--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@--INTRODUCERE ID MASINI INTRARE @@@@@@@@@@@@@@
class Pag2(Screen):
#---------------------------------------------------------ADD VARIABLES!!!!!!!!!!!!!!!!!!!!!
	IDS_INTRARE = []
	IDS_IESIRE = []
	IDS_DATE_VIEW = []
	conn = sqlite3.connect("isu_db.db")

	# Create a Cursor
	c = conn.cursor()
	c.execute("SELECT * FROM IDS WHERE STATUS='STANDBY'")
	id_select = c.fetchall()
	for x in id_select:
		IDS_INTRARE.append(x[0])
		IDS_IESIRE.append(x[0])
		IDS_DATE_VIEW.append(x[0])


	values_list_spinner_INTRARE = ObjectProperty(IDS_IESIRE)

	values_list_spinner_IESIRE = ObjectProperty(IDS_INTRARE)

	values_list_spinner_DATE_VIEW = ObjectProperty(IDS_DATE_VIEW)

	conn.close()
#---------------------------------------------------------INTRARI SPINNER---#---------------------------------------------------------IESIRI SPINNER

	def clean_errors(self,*args):
		self.ids.error_submit_intrare.text = ""
		self.ids.error_submit_iesire.text = ""
		self.ids.search_label.text = ""
#---------------------------------------------------------ADD VARIABLES!!!!!!!!!!!!!!!!!!!!
	def back_btn(self,*args):
		self.manager.current = 'pag1'
		self.manager.transition.direction="right"
		self.clean_errors()
	def clear_btn_errors(self,*args):
		self.ids.error_submit_intrare.text = ""
		self.ids.error_submit_iesire.text = ""
		self.ids.search_label.text = ""
	def clean_btn_chart(self,*args):
		self.ids.search_label.text = ""
		self.ids.date_view_label.text = ""
	#---------------------------------------------------CLOCK WIDGET
	def on_pre_enter(self, *args):
		Clock.schedule_interval(self.update, 1)
		Clock.schedule_interval(self.view_intrari, 1)
		Clock.schedule_interval(self.view_iesiri, 1)
		Clock.schedule_interval(self.update_lists_of_values_spinner_INTRARE, 1)
		Clock.schedule_interval(self.update_lists_of_values_spinner_IESIRE, 1)
		self.update_lists_of_values_spinner_DATE_VIEW()
	def update(self, *args):
		self.ids.timex.text = clock_now()
	#---------------------------------------------------CLOCK WIDGET
	
	#---------------------------------------------------------SPINNER VARIABLES
	def update_lists_of_values_spinner_INTRARE(self,*args):
		IDS_INTRARE = []
		conn = sqlite3.connect("isu_db.db")
		# Create a Cursor
		c = conn.cursor()

		c.execute("SELECT * FROM IDS WHERE STATUS='INTRARE' or STATUS='STANDBY'")
		cdc = c.fetchall()
		for x in cdc:
			IDS_INTRARE.append(x[0])

		conn.close()
		IDS_INTRARE.sort()
		self.values_list_spinner_INTRARE = IDS_INTRARE
	def update_lists_of_values_spinner_IESIRE(self,*args):
		IDS_IESIRE = []
		conn = sqlite3.connect("isu_db.db")

		# Create a Cursor
		c = conn.cursor()
		c.execute("SELECT * FROM IDS WHERE STATUS='IESIRE'")
		cdc = c.fetchall()
		for x in cdc:
			IDS_IESIRE.append(x[0])
		conn.close()
		IDS_IESIRE.sort()
		self.values_list_spinner_IESIRE = IDS_IESIRE
	def update_lists_of_values_spinner_DATE_VIEW(self,*args):
		IDS_DATE_VIEW = []
		conn = sqlite3.connect("isu_db.db")

		# Create a Cursor
		c = conn.cursor()
		c.execute("SELECT * FROM IDS")
		cdc = c.fetchall()
		for x in cdc:
			IDS_DATE_VIEW.append(x[0])
		conn.close()
		IDS_DATE_VIEW.sort()
		self.values_list_spinner_DATE_VIEW = IDS_DATE_VIEW
	#---------------------------------------------------------SPINNER VAIABLES

	#-----------------------------------------------------------------------------------------------------------------------------------------SUBMIT INTRARI VANZARI
	def spinner_intrare(self,value):
		try:

			if value == "Alege IDs":

				self.ids.error_submit_intrare.text = "[color=#FF0000]Eroare: [/color]Lipsa valori"

			else:

				conn = sqlite3.connect("isu_db.db")
				id_unique_name_split = re.split(r"-| ", value)
				# Create a Cursor
				c = conn.cursor()
				c.execute("INSERT INTO chart_view VALUES (:INTRARE, :ID, :DATA)", {'INTRARE': 'INTRARE', 'ID': id_unique_name_split[0], 'DATA': clock_now()})
				c.execute("INSERT INTO "+ id_unique_name_split[0] +" VALUES (:INTRARE, :ID, :DATA, :DATA_VIEW)", {'INTRARE': 'INTRARE', 'ID': value, 'DATA': clock_now(),'DATA_VIEW': clock_now_DATE_VIEW()})	


				c.execute("UPDATE iesiri_intrari_vizualizare_app SET TIP =?, ID=?, DATA=?, SIMPLE_ID=? WHERE ID=?", ('INTRARE',value, clock_now(),id_unique_name_split[0],value))
				c.execute("UPDATE IDS SET STATUS =? WHERE ID=?", ('INTRARE',value))

				conn.commit()
				conn.close()

				self.ids.error_submit_intrare.text = f"[color=#3e8079]{value}[/color] a [color=#08d442]INTRAT[/color] in unitate."
				self.ids.spinner_id_intrare.text = "Alege IDs"


		except Exception as e:
			self.ids.error_submit_intrare.text = "[color=#FF0000]Eroare: [/color]adaugare ID SQL"
			print("Error "+ str(e))


	def spinner_iesire(self,value):
		try:

			if value == "Alege IDs":

				self.ids.error_submit_iesire.text = "[color=#FF0000]Eroare: [/color]Lipsa valori"

			else:

				conn = sqlite3.connect("isu_db.db")
				id_unique_name_split = re.split(r"-| ", value)
				# Create a Cursor
				c = conn.cursor()
				c.execute("INSERT INTO chart_view VALUES (:IESIRE, :ID, :DATA)", {'IESIRE': 'IESIRE', 'ID': id_unique_name_split[0], 'DATA': clock_now()})
				c.execute("INSERT INTO "+ id_unique_name_split[0] +" VALUES (:IESIRE, :ID, :DATA, :DATA_VIEW)", {'IESIRE': 'IESIRE', 'ID': value, 'DATA': clock_now(), 'DATA_VIEW': clock_now_DATE_VIEW()})
				c.execute("UPDATE iesiri_intrari_vizualizare_app SET TIP =?, ID=?, DATA=?, SIMPLE_ID=? WHERE ID=?", ('IESIRE',value, clock_now(),id_unique_name_split[0],value))
				c.execute("UPDATE IDS SET STATUS =? WHERE ID=?", ('IESIRE',value))
				conn.commit()
				conn.close()

				self.ids.error_submit_iesire.text = f"[color=#3e8079]{value}[/color] a [color=#FF0000]IESIT[/color] din unitate."
				self.ids.spinner_id_iesire.text = "Alege IDs"
		except Exception as e:
			self.ids.error_submit_iesire.text = "[color=#FF0000]Eroare: [/color]adaugare ID SQL"
			print("Error "+ str(e))
	#-----------------------------------------------------------------------------------------------------------------------------------------SUBMIT INTRARI VANZARI


#--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@--INTRODUCERE ID MASINI IESIRE @@@@@@@@@@@@@@

#--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@--SCREEN 2 VIZUALIZARE DATE @@@@@@@@@@@@@@

	def view_intrari(self,*args):
		try:
			conn = sqlite3.connect("isu_db.db")
			df = pd.read_sql_query("SELECT * from iesiri_intrari_vizualizare_app", conn)

			string_view = df.loc[df['TIP']=='INTRARE']

			specific_cols = string_view[['ID']]
			specific_cols1 = string_view[['DATA']]


			df = specific_cols.to_string(index=False,header=False)
			df1 = specific_cols1.to_string(index=False,header=False)

			if 'Empty DataFrame' in df:
				self.ids.intrari_view_id.text = ''
				self.ids.intrari_view_data.text = ''
			else:
				self.ids.intrari_view_id.text = f"""
[b][color=#08d442]{df}[/color][/b]
"""	
				self.ids.intrari_view_data.text = f"""
{df1}
"""			
			conn.close()
		except Exception as e:
			print("Error "+ str(e))





	def view_iesiri(self,*args):
		try:
			conn = sqlite3.connect("isu_db.db")
			df = pd.read_sql_query("SELECT * from iesiri_intrari_vizualizare_app", conn)

			string_view = df.loc[df['TIP']=='IESIRE']
			specific_cols = string_view[['ID']]
			specific_cols1 = string_view[['DATA']]


			df = specific_cols.to_string(index=False,header=False)
			df1 = specific_cols1.to_string(index=False,header=False)
			if 'Empty DataFrame' in df:
				self.ids.iesiri_view_id.text = ''
				self.ids.iesiri_view_data.text = ''
			else:
				self.ids.iesiri_view_id.text = f"""
[b][color=#FF0000]{df}[/color][/b]
"""	
				self.ids.iesiri_view_data.text = f"""
{df1}
"""		
			conn.close()

		except Exception as e:
			print("Error "+ str(e))
#--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@--SCREEN 2 VIZUALIZARE DATE @@@@@@@@@@@@@@


#--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-- SEARCH ID @@@@@@@@@@@@@@
	def search_id(self,value):
		try:
			conn = sqlite3.connect("isu_db.db")
			# Create a Cursor
			c = conn.cursor()

			c.execute("SELECT * FROM iesiri_intrari_vizualizare_app WHERE ID=:ID", {"ID": value})
			verification_step = c.fetchone()
			if verification_step[0] == "INTRARE":
				self.ids.search_label.text = f"Masina cu ID: -- [b]{verification_step[1]}[/b] -- Status: [color=#08d442]{verification_step[0]}[/color] " + "\n" + f"Data: {verification_step[2]}"
			else:
				self.ids.search_label.text = f"Masina cu ID: -- [b]{verification_step[1]}[/b] -- Status: [color=#FF0000]{verification_step[0]}[/color] " + "\n" + f"Data: {verification_step[2]}"

			#PARTEA DE VIZALIZARE DATE 

			id_unique_DATE_VIEW = re.split(r"-| ", value)
			query = "SELECT * from {}".format(id_unique_DATE_VIEW[0])
			df = pd.read_sql_query(query, conn)
			string_view = df.loc[df['DATA_VIEW'] == self.ids.data_picker_show.text]
			df = string_view[['TIP','ID','DATA']].to_string(index=False)

			if "Select Date" == self.ids.data_picker_show.text:
				self.ids.date_view_label.text = f"""[color=#FF0000]Error:  [/color]--[b]{value}[/b]-- 
You need to select a date --[b]{self.ids.data_picker_show.text}[/b]--."""
			elif 'Empty DataFrame' in df:
				self.ids.date_view_label.text = f"""[color=#FF0000]Error:  [/color]--[b]{value}[/b]-- 
nu are inregistrari pe data de --[b]{self.ids.data_picker_show.text}[/b]--."""
			else:
				self.ids.date_view_label.text = f"""{df}"""
			conn.close()

		except Exception as e:
			self.ids.search_label.text = f"[color=#FF0000]Error:  [/color]--[b]LIPSA VALORI SQL.[/b]--"
			print("Error "+ str(e))


	def show_date_picker(self,*args):
		date_dialog = MDDatePicker()

		date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)

		date_dialog.open()

	# CLICK SAVE DATE
	def on_save(self,instance,value,date_range):
		self.ids.data_picker_show.text = str(value.strftime("%d-%m-%Y"))

	# CLIK CANCEL DATE
	def on_cancel(self,instance,value):
		pass
#--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-- SEARCH ID @@@@@@@@@@@@@@

######################################## MATPLOTLIB -----------------------------------------------------------------
	def matplotlib_first(self,*args):
		try:
			conn = sqlite3.connect("isu_db.db")
			df = pd.read_sql_query("SELECT * from chart_view", conn)

			results = df.groupby('ID')['TIP'].count().sort_values(ascending=False)
			results = results.iloc[:8]

			values = [x for x in results]

			fig, ax = plt.subplots(figsize=(10,5))

			ax.bar(results.index,values)

			plt.xticks(results.index)
			ax.tick_params(axis='x', colors='red')
			ax.tick_params(axis='y', colors='red')


			ax.xaxis.label.set_color('red')
			ax.yaxis.label.set_color('red')
			fig.patch.set_facecolor('xkcd:sage green')
			plt.ylabel("IESIRI/INTRARI")
			plt.xlabel("ID")
			plt.title("Situatie ID/INTRARI-IESIRI")
			plt.savefig('ID_cars_intrari_iesiri.png')
			conn.close()
			self.ids.box.reload()
		except Exception as e:
			print("Error "+ str(e))
######################################## MATPLOTLIB -----------------------------------------------------------------




class Pag3(Screen):
	def clean_errors(self,*args):
		self.ids.error_add.text = ""
		self.ids.error_add_admin.text = ""
		self.ids.error_ids.text = ""
	def back_btn_admin(self,*args):
		self.manager.current = 'pag1'
		self.manager.transition.direction="left"
################################################################################################---USERS
	def add_users(self,*args):
		try:

			if self.ids.password_x.text == "" and self.ids.user_name_x.text == "":
				self.ids.error_add.text = f"[color=#FF0000]Error:  [/color][b]Lipsa valori[/b]"
			else:
				conn = sqlite3.connect("isu_db.db")

				# Create a Cursor
				c = conn.cursor()
				passwd = bytes(self.ids.password_x.text,'utf-8')

				salt = bcrypt.gensalt()
				hashed = bcrypt.hashpw(passwd, salt)

				c.execute("INSERT INTO users VALUES (:user, :password)", {'user': self.ids.user_name_x.text, 'password': hashed.decode()})
				conn.commit()
				conn.close()

				self.ids.error_add.text = f"User [b]{self.ids.user_name_x_admin.text}[/b] adaugat cu succes."
				self.ids.password_x.text = ''
				self.ids.user_name_x.text = ''
		except Exception as e:
			self.ids.error_add.text = f"[color=#FF0000]Error:  [/color]--[b]SQL[/b]--"
			print("Error "+ str(e))
	def add_users_admin(self,*args):
		try:

			if self.ids.password_x_admin.text == "" and self.ids.user_name_x_admin.text == "":
				self.ids.error_add_admin.text = f"[color=#FF0000]Error:  [/color][b]Lipsa valori[/b]"
			else:
				conn = sqlite3.connect("isu_db.db")

				# Create a Cursor
				c = conn.cursor()
				passwd = bytes(self.ids.password_x_admin.text,'utf-8')

				salt = bcrypt.gensalt()
				hashed = bcrypt.hashpw(passwd, salt)

				c.execute("INSERT INTO users_admin VALUES (:user_admin, :password_admin)", {'user_admin': f"{self.ids.user_name_x_admin.text}.admin", 'password_admin': hashed.decode()})
				conn.commit()
				conn.close()

				self.ids.error_add_admin.text = f"User [b]{self.ids.user_name_x_admin.text}.admin[/b] adaugat cu succes."
				self.ids.password_x_admin.text = ''
				self.ids.user_name_x_admin.text = ''
		except Exception as e:
			self.ids.error_add_admin.text = f"[color=#FF0000]Error:  [/color]--[b]SQL[/b]--"
			print("Error "+ str(e))
################################################################################################---USERS

################################################################################################---IDS ADD
	def add_ids(self,*args):
		try:
			if self.ids.ids_add.text == "":
				self.ids.error_ids.text = f"[color=#FF0000]Error:  [/color][b]Lipsa valori[/b]"
			else:
				conn = sqlite3.connect("isu_db.db")

				# Create a Cursor
				c = conn.cursor()
				id_unique_table_split = re.split(r"-| ", self.ids.ids_add.text)
				query_unique_tables = "CREATE TABLE if not exists {} (TIP text, ID text, DATA text, DATA_VIEW text)".format(id_unique_table_split[0].upper())
				c.execute(query_unique_tables)

				c.execute("SELECT * FROM IDS WHERE SIMPLE_ID=:SIMPLE_ID", {"SIMPLE_ID": id_unique_table_split[0].upper()})
				find_duplicate = c.fetchone()
				if find_duplicate == None:
					c.execute("INSERT INTO iesiri_intrari_vizualizare_app VALUES (:TIP, :ID, :DATA, :SIMPLE_ID)", {'TIP': 'STANDBY', 'ID': self.ids.ids_add.text.upper(), 'DATA': clock_now(), "SIMPLE_ID":id_unique_table_split[0].upper()})
					c.execute("INSERT INTO IDS VALUES (:ID, :STATUS, :SIMPLE_ID)", {'ID': self.ids.ids_add.text.upper(), "STATUS":"STANDBY", "SIMPLE_ID":id_unique_table_split[0].upper()})
					self.ids.error_ids.text = f'IDs [color=#08d442]{self.ids.ids_add.text.upper()}[/color] a fost adaugat cu succes.'
				else:
					self.ids.error_ids.text = f'IDs [color=#08d442]{self.ids.ids_add.text.upper()}[/color][color=#FF0000] Error:  DUPLICAT[/color]'	

				conn.commit()
				conn.close()

				self.ids.ids_add.text = ''

		except Exception as e:
			self.ids.error_ids.text = f"[color=#FF0000]Error:  [/color]--[b]-SQL-[/b]--"
			print("Error "+ str(e))
################################################################################################---IDS ADD

	
class WindowManager(ScreenManager):
    pass



class AutoISUApp(MDApp):
	def build(self):
		# WINDOW
		Window.clearcolor = (1,1,1,1)
		Window.maximize()
		# WINDOW

		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"




		# Create DATABASE or Connect to one
		conn = sqlite3.connect("isu_db.db")

		c = conn.cursor()


		# Create a Table
		c.execute("""CREATE TABLE if not exists users( user text, password text)""")
		c.execute("""CREATE TABLE if not exists users_admin( user_admin text, password_admin text)""")
		c.execute("""CREATE TABLE if not exists iesiri_intrari_vizualizare_app(TIP text, ID text , DATA text, SIMPLE_ID text unique)""")
		c.execute("""CREATE TABLE if not exists chart_view(TIP text, ID text, DATA text)""")
		c.execute("""CREATE TABLE if not exists IDS(ID text, STATUS text, SIMPLE_ID unique)""")

		conn.commit()
		conn.close()

		return Builder.load_file("design_isu.kv")


if __name__ == "__main__":
	AutoISUApp().run()
