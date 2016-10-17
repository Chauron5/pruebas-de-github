import gi 
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk, GLib 
from model import *
import gettext
import locale
import os

# Algunas cosas para gettext (para las traducciones)
APP='handler' #Dominio del programa-nombre de la traduccion
DIR='locale' #Directorio de traducciones

locale.setlocale(locale.LC_ALL, '')
LOCALE_DIR=os.path.join(os.path.dirname(__file__), "locale")

locale.bindtextdomain(APP, LOCALE_DIR)
# Esto permite traducir los textos escritos en el .py (no en glade)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)


# Y las siguientes 2 lineas permiten traducir los textos del Glade
#GLib.textdomain(APP)
#Gtk.Glade.bindtextdomain(APP, DIR)

# Y con esto podemos marcar las cadenas a traducir de la forma _("cadena")
_ = gettext.gettext

class  Handler():
     def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain(APP)
        
        # glade_file=join("."'view.glade')
        builder.add_from_file("view.glade")
        builder.connect_signals(self)

        # BAse de Datos
        self.model = Model()

        # ventanas
        self.w_principal = builder.get_object("main_window")

        # Dialogos
        self.w_anadir = builder.get_object("add_dialog")
        self.w_modificar = builder.get_object("modify_dialog")
        self.del_dialog = builder.get_object("del_dialog")

        # Objetos de la ventana principal
        self.btn_anadir = builder.get_object("btn_add")
        self.btn_modificar = builder.get_object("btn_modify")
        self.filter_by_label = builder.get_object("filter_by_label")
        self.filter_by_combobox = builder.get_object("filter_by_combobox")
        self.main_scroll = builder.get_object("main_scroll")
        self.main_tree = builder.get_object("main_tree")
        self.tree_selection = builder.get_object("tree_selection")
        self.btn_act = builder.get_object("btn_act")
        self.btn_del = builder.get_object("btn_del")


        # Objetos del dialogo anadir
        self.btn_aceptar_w_anadir = builder.get_object("add_dialog-btn_accept")
        self.btn_cancelar_w_anadir = builder.get_object("add_dialog-btn_cancel")
        self.entrada_titulo = builder.get_object("title_entry")
        self.entrada_director = builder.get_object("director_entry")
        self.entrada_duracion = builder.get_object("duration_entry")
        self.combobox_anadir_a = builder.get_object("add_dialog_comboboxtext")
        self.combobox_anadir_a_entrada = builder.get_object("add_dialog_comboboxtext-entry")
        self.notification_label = builder.get_object("notification_label")

         # Objetos de la ventana modificar
        self.btn_aceptar_w_modificar = builder.get_object("btn_aceptar_w_modificar")
        self.btn_cancelar_w_modificar = builder.get_object("btn_cancelar_w_modificar")
        self.modify_title = builder.get_object("modify-title_entry")
        self.modify_director = builder.get_object("modify-director_entry")
        self.modify_duration = builder.get_object("modify-duration_entry")
        self.modify_set_as = builder.get_object("modify_dialog-comboboxtext")
        self.modify_notification_label = builder.get_object("modify-notification_label")

        # Objetos de la ventana Borrar
        self.filmName = builder.get_object("filmName")
        self.cb_del = builder.get_object("cb_del")
        self.del_btn_accept = builder.get_object("del-dialog_btn_accept")
        self.del_btn_cancel = builder.get_object("del-dialog_btn_cancel")


        self.showDelDialog = True

         # Configuracion Lsita de Peliculas 
        self.filmsList = []
        self.filmsListStore = builder.get_object("filmsListStore")
        # self.filmsListStore = Gtk.ListStore(str, str, int, str)
        self.current_films_filter = None 
        self.films_filter = None
        self.selected_value = None

        # when a row is selected, it emits a signal
        # view.get_selection().connect("changed", self.on_changed)

        self.show_window(self.w_principal)
        self.actualizar_vista()



     # FUNCIONES DE LA CLASE VISTA

     def films_filter_func(self, model, iter, data):
        if self.current_films_filter is None or self.current_films_filter == _("Todas"):
            return True
        else:
            return _(model[iter][5]) in self.current_films_filter 

     def actualizar_vista(self):
        self.filmsList.clear()
        self.filmsListStore.clear()
        self.model.getAllFilms(self.filmsList)
        pos = 0
        for row in self.filmsList:
            self.filmsListStore.append([pos, row[0],row[1],row[2], row[3], row[4]])
            pos = pos + 1

        self.films_filter = self.filmsListStore.filter_new()
        self.films_filter.set_visible_func(self.films_filter_func)
        self.main_tree.set_model(self.films_filter)

     def onSelectionChanged(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            self.selected_value = (model.get_value(tree_iter,0))
            # print (value)


     def terminar_aplicacion(self, w):
        Gtk.main_quit()

     def show_window(self, window):
        window.show_all()

     # Si devolvemos FALSE en delete_event() (hide_window) 
     # se llamarA automaticamente a destroy
     def hide_window(self, widget, event , data=None):
        widget.hide()
        if widget == self.w_anadir:
            self.clear_w_anadir()
        return True


     def clear_w_anadir(self):
        self.entrada_titulo.set_text("")
        self.entrada_director.set_text("")
        self.entrada_duracion.set_text("")
        self.notification_label.set_text("")


     def validarDatos(self):
        if (self.entrada_titulo.get_text() != "" 
        and self.entrada_director.get_text() != ""
        and self.entrada_duracion.get_text() != ""
        and self.combobox_anadir_a.get_active_text() != ""):
            try:
                dur = int(self.entrada_duracion.get_text())
                return True
            except ValueError:
                self.notification_label.set_text(_("*Campo duracion con formato no valido"))
                return False 
        else:    
            self.notification_label.set_text(_("*Complete los campos para continuar"))
            return False

     def validarDatosModificados(self):
        if (self.modify_title.get_text() != ""
        and self.modify_director.get_text() != ""
        and self.modify_duration.get_text() != ""
        and self.modify_set_as.get_active_text() != ""):
            try:
                dur = int(self.modify_duration.get_text())
                return True
            except ValueError:
                self.modify_notification_label.set_text(_("*Campo duracion con formato no valido"))
                return False 
        else:    
            self.modify_notification_label.set_text(_("*Complete los campos para continuar"))
            return False

     def insertFilm(self):
        title = self.entrada_titulo.get_text() 
        director = self.entrada_director.get_text() 
        dur = self.entrada_duracion.get_text() 
        state = self.combobox_anadir_a.get_active_text()
        self.model.insert(title, director, dur, state)

     def modifyShowWindow(self):
        sel = self.filmsList[self.selected_value]
        self.modify_title.set_text(sel[1])
        self.modify_director.set_text(sel[2]) 
        self.modify_duration.set_text(str(sel[3])) 
        selCombo = None
        print(sel[4])
        if sel[4] == "Pendientes":
            selCombo=0
        elif sel[4] == "Vistas":
            selCombo=1
        elif sel[4] == "Favoritas":
            selCombo=2
        else: 
            selComb0=0
        self.modify_set_as.set_active(selCombo)
        self.w_modificar.run()

     def deleteShowWindow(self):
        sel = self.filmsList[self.selected_value]
        self.filmName.set_text(sel[1])
        self.del_dialog.run()

     def delete(self):
        sel = self.filmsList[self.selected_value]
        ID = int(sel[0])
        self.model.delete(ID)
        self.actualizar_vista()
        self.hide_window(self.del_dialog, None)

     def modify(self):
        sel = self.filmsList[self.selected_value]
        ID = int(sel[0])
        title = self.modify_title.get_text()
        direc = self.modify_director.get_text() 
        dur = int(self.modify_duration.get_text()) 
        state = self.modify_set_as.get_active_text()
        self.model.modify(ID, title, direc, dur, state)
        self.actualizar_vista()     

     def on_toggled(self, w):
        if self.showDelDialog:
            self.showDelDialog = False 
        else: 
            self.showDelDialog = True


     def on_click(self, widget):
        if widget == self.btn_anadir:
            self.w_anadir.run()
        elif widget == self.btn_cancelar_w_anadir:
            self.hide_window(self.w_anadir, None)
        elif widget == self.btn_act:
            self.actualizar_vista()
        elif widget == self.btn_del:
            if self.selected_value != None:
                if self.showDelDialog:
                    self.deleteShowWindow()
                else:
                    self.delete()
        elif widget == self.btn_modificar:
            if self.selected_value != None:
                self.modifyShowWindow()
        elif widget == self.filter_by_combobox:
            self.current_films_filter = widget.get_active_text()
            self.films_filter.refilter()
        elif widget == self.btn_aceptar_w_anadir:
            if self.validarDatos():
                self.insertFilm()
                self.hide_window(self.w_anadir, None)
                self.actualizar_vista()
        elif widget == self.btn_cancelar_w_modificar:
            self.hide_window(self.w_modificar, None)
        elif widget == self.btn_aceptar_w_modificar:
            if self.validarDatosModificados():
                self.modify()
                self.hide_window(self.w_modificar, None)
        elif widget == self.del_btn_accept:
            self.delete()
        elif widget == self.del_btn_cancel:
            self.hide_window(self.del_dialog, None)
        else:
            print("No conectado")




 


# Run Application
handler = Handler()
Gtk.main()