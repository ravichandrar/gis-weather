#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gtk
import os

def create_gtk_city_id(window, city_id, city_id_add, APP_PATH):
    dialog = gtk.Dialog(_('Location'), window)
    dialog.resize(300, 100)
    dialog.add_buttons(_('Add'), gtk.RESPONSE_OK,
        _('Close'), gtk.RESPONSE_CANCEL,
        _('Remove selected'), gtk.RESPONSE_ACCEPT)
    dialog.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))

    hbox = gtk.HBox(False, 8)
    hbox.set_border_width(8)
    dialog.vbox.pack_start(hbox, False, False, 0)
    table = gtk.Table(2, 3)
    table.set_row_spacings(4)
    table.set_col_spacings(4)
    hbox.pack_start(table, True, True, 0)

    entrybox = gtk.Entry()
    entrybox.set_text(str(city_id))
    text = _("""Choose your city on <a href='http://www.gismeteo.com'> http://www.gismeteo.com </a>
and copy number at the end of reference
For example <u><span foreground='blue'>http://www.gismeteo.ru/city/daily/<b>1234</b>/</span></u>
City code<b>1234</b>""")
    
    label = gtk.Label()
    label.set_markup(text)

    bar_err = gtk.InfoBar()
    bar_err.set_message_type(gtk.MESSAGE_ERROR)
    bar_err.get_content_area().pack_start(
        gtk.Label(_('Invalid location code')))
    table.attach(bar_err, 0, 1, 2, 3)

    bar_ok = gtk.InfoBar()
    bar_ok.set_message_type(gtk.MESSAGE_INFO)
    bar_label = gtk.Label(_('Added'))
    bar_ok.get_content_area().pack_start(
        bar_label)
    table.attach(bar_ok, 0, 1, 2, 3)

    label_err = gtk.Label('\n')
    table.attach(label, 0, 1, 0, 1)
    table.attach(entrybox, 0, 1, 1, 2)
    table.attach(label_err, 0, 1, 2, 3)

    sw = gtk.ScrolledWindow()
    sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

    store = create_model(city_id_add)
    treeView = gtk.TreeView(store)
    sw.add(treeView)
    create_columns(treeView)
    table.attach(sw, 1, 2, 0, 3)
    return dialog, entrybox, treeView, bar_err, bar_ok, bar_label

def create_model(city_id_add):
    store = gtk.ListStore(str, str)

    for item in city_id_add:
        store.append([item.split(';')[0], item.split(';')[1]])
    return store


def create_columns(treeView):

    rendererText = gtk.CellRendererText()
    column = gtk.TreeViewColumn(_('Code'), rendererText, text=0)
    treeView.append_column(column)
    
    rendererText = gtk.CellRendererText()
    column = gtk.TreeViewColumn(_('Place'), rendererText, text=1)
    treeView.append_column(column)