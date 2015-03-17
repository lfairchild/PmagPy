#!/usr/bin/env python

import matplotlib
#matplotlib.use('WXAgg')
import pmag
import wx
import copy
import os

#============================================================================================
# LOG HEADER:
#  
# Dialogs boxes for demag_gui.py
#
#============================================================================================
#
# 3/10/2014 Version 0.1 (beta) by Ron Shaar
#
#
#============================================================================================


#--------------------------------------------------------------    
#--------------------------------------------------------------


#--------------------------------------------------------------    
# MagIc results tables dialog
#--------------------------------------------------------------

class magic_pmag_tables_dialog(wx.Dialog):
    def __init__(self,parent,WD,Data,Data_info):
        super(magic_pmag_tables_dialog, self).__init__(parent, title="MagIC results table Dialog")
        self.InitUI()
        

    def InitUI(self):

        pnl1 = wx.Panel(self)
        vbox = wx.StaticBoxSizer(wx.StaticBox( pnl1, wx.ID_ANY, "MagIC result tables options" ), wx.VERTICAL)        

        #---------------------
        # Acceptance criteria
        #---------------------
        #self.acceptance_criteria_text=wx.StaticText(pnl1,label="apply acceptance criteria from pmag_criteria.txt:",style=wx.TE_CENTER)        
        self.cb_acceptance_criteria= wx.CheckBox(pnl1, -1, 'apply acceptance criteria from pmag_criteria.txt', (10, 30))

        #---------------------
        # choose coordinate system
        #---------------------
        self.coor_text=wx.StaticText(pnl1,label="coordinate system:",style=wx.TE_CENTER)
        self.rb_spec_coor = wx.RadioButton(pnl1, -1, 'specimen', (10, 10), style=wx.RB_GROUP)
        self.rb_geo_coor = wx.RadioButton(pnl1, -1, 'geographic', (10, 30))
        self.rb_tilt_coor = wx.RadioButton(pnl1, -1, 'tilt-corrected', (10, 30))
        self.rb_geo_tilt_coor = wx.RadioButton(pnl1, -1, 'geographic and tilt-corrected', (10, 30))
        
        self.rb_geo_coor.SetValue(True)
        coordinates_window = wx.GridSizer(1, 4, 6, 6)
        coordinates_window.AddMany( [(self.rb_spec_coor),            
            (self.rb_geo_coor),
            (self.rb_tilt_coor),
            (self.rb_geo_tilt_coor)])

        #---------------------
        # default age
        #---------------------
        self.default_age_text=wx.StaticText(pnl1,label="default age if site age does not exist in er_ages.txt:",style=wx.TE_CENTER)        
        self.cb_default_age = wx.CheckBox(pnl1, -1, 'use default age', (10, 30))

        self.default_age_min=wx.TextCtrl(pnl1,style=wx.TE_CENTER,size=(50,20))
        self.default_age_max=wx.TextCtrl(pnl1,style=wx.TE_CENTER,size=(50,20))
        age_unit_choices=['Years Cal BP','Years Cal AD (+/-)','Years BP','Years AD (+/-)','Ma','Ka','Ga']
        self.default_age_unit=wx.ComboBox(pnl1, -1,size=(150, -1), value = '', choices=age_unit_choices, style=wx.CB_READONLY)
        
        default_age_window = wx.GridSizer(2, 4, 6, 6)
        default_age_window.AddMany( [(wx.StaticText(pnl1,label="",style=wx.TE_CENTER), wx.EXPAND),            
            (wx.StaticText(pnl1,label="younger bound",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="older bound",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="units",style=wx.TE_CENTER), wx.EXPAND),
            (self.cb_default_age,wx.EXPAND),
            (self.default_age_min,wx.EXPAND),
            (self.default_age_max,wx.EXPAND),
            (self.default_age_unit,wx.EXPAND)])
            
        
        #---------------------
        # sample 
        #---------------------
        self.cb_sample_mean=wx.CheckBox(pnl1, -1, 'calculate sample mean  ', (10, 30))
        self.cb_sample_mean.SetValue(False)  
        sample_mean_choices=['specimens']
        self.combo_sample_mean=wx.ComboBox(pnl1, -1,size=(150, -1), value = 'specimens', choices=sample_mean_choices, style=wx.CB_READONLY)
        sample_mean_types=['Fisher']
        self.combo_sample_type=wx.ComboBox(pnl1, -1,size=(150, -1), value = 'Fisher', choices=sample_mean_types, style=wx.CB_READONLY)
        self.cb_sample_mean_VGP=wx.CheckBox(pnl1, -1, 'calculate sample VGP', (10, 30))
        self.cb_sample_mean_VGP.SetValue(False)  
        self.Bind(wx.EVT_CHECKBOX,self.on_change_cb_sample_mean_VGP,self.cb_sample_mean_VGP)
   
        sample_mean_window = wx.GridSizer(2, 4, 6, 6)
        sample_mean_window.AddMany( [(wx.StaticText(pnl1,label="",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="average sample by:",style=wx.TE_CENTER), wx.EXPAND),            
            (wx.StaticText(pnl1,label="calculation type",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="",style=wx.TE_CENTER), wx.EXPAND),
            (self.cb_sample_mean,wx.EXPAND),            
            (self.combo_sample_mean,wx.EXPAND),
            (self.combo_sample_type,wx.EXPAND),
            (self.cb_sample_mean_VGP,wx.EXPAND)])

        #---------------------
        # site 
        #---------------------
        self.cb_site_mean=wx.CheckBox(pnl1, -1, 'calculate site mean    ', (10, 30))
        self.cb_site_mean.SetValue(True)         
        site_mean_choices=['specimens','samples']
        self.combo_site_mean=wx.ComboBox(pnl1, -1,size=(150, -1), value = 'specimens', choices=site_mean_choices, style=wx.CB_READONLY)
        site_mean_types=['Fisher']
        self.combo_site_type=wx.ComboBox(pnl1, -1,size=(150, -1), value = 'Fisher', choices=site_mean_types, style=wx.CB_READONLY)
        self.cb_site_mean_VGP=wx.CheckBox(pnl1, -1, 'calculate site VGP', (10, 30))
        self.cb_site_mean_VGP.SetValue(True)         
        self.Bind(wx.EVT_CHECKBOX,self.on_change_cb_site_mean_VGP,self.cb_site_mean_VGP)

        site_mean_window = wx.GridSizer(2, 4, 6, 6)
        site_mean_window.AddMany( [(wx.StaticText(pnl1,label="",style=wx.TE_CENTER), wx.EXPAND), 
            (wx.StaticText(pnl1,label="average site by:",style=wx.TE_CENTER), wx.EXPAND),           
            (wx.StaticText(pnl1,label="calculation type",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="",style=wx.TE_CENTER), wx.EXPAND),
            (self.cb_site_mean,wx.EXPAND),
            (self.combo_site_mean,wx.EXPAND),
            (self.combo_site_type,wx.EXPAND),
            (self.cb_site_mean_VGP,wx.EXPAND)])

        #---------------------
        # location 
        #---------------------
        self.cb_location_mean=wx.CheckBox(pnl1, -1, 'calculate location mean', (10, 30))
        self.cb_location_mean.SetValue(False)
        location_mean_choices=['sites']
        self.combo_location_mean=wx.ComboBox(pnl1, -1,size=(150, -1), value = 'sites', choices=location_mean_choices, style=wx.CB_READONLY)
        location_mean_types=['Fisher-separate polarities']
        self.combo_loction_type=wx.ComboBox(pnl1, -1,size=(150, -1), value = 'Fisher-separate polarities', choices=location_mean_types, style=wx.CB_READONLY)
        self.cb_location_mean_VGP=wx.CheckBox(pnl1, -1, 'calculate location VGP', (10, 30))
        self.cb_location_mean_VGP.SetValue(True)
        #self.Bind(wx.EVT_CHECKBOX,self.on_change_cb_location_mean_VGP,self.cb_location_mean_VGP)
   
         
        loaction_mean_window = wx.GridSizer(2, 4, 6, 6)
        loaction_mean_window.AddMany( [(wx.StaticText(pnl1,label="",style=wx.TE_CENTER), wx.EXPAND), 
            (wx.StaticText(pnl1,label="average location by:",style=wx.TE_CENTER), wx.EXPAND),            
            (wx.StaticText(pnl1,label="calculation type",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="",style=wx.TE_CENTER), wx.EXPAND),
            (self.cb_location_mean,wx.EXPAND),
            (self.combo_location_mean,wx.EXPAND),
            (self.combo_loction_type,wx.EXPAND),
            (self.cb_location_mean_VGP,wx.EXPAND)])

        #---------------------
        # OK/Cancel buttons 
        #---------------------
                
        hboxok = wx.BoxSizer(wx.HORIZONTAL)
        self.okButton = wx.Button(pnl1, wx.ID_OK, "&OK")
        self.cancelButton = wx.Button(pnl1, wx.ID_CANCEL, '&Cancel')
        hboxok.Add(self.okButton)
        hboxok.AddSpacer(20)
        hboxok.Add(self.cancelButton )
                
        #---------------------

        vbox.Add(wx.StaticLine(pnl1), 0, wx.ALL|wx.EXPAND, 5)  
        vbox.AddSpacer(10)

        vbox.Add(self.cb_acceptance_criteria,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(pnl1), 0, wx.ALL|wx.EXPAND, 5)  
        vbox.AddSpacer(10)
        
        vbox.Add(self.coor_text,flag=wx.ALIGN_CENTER_HORIZONTAL, border=100)
        vbox.AddSpacer(10)
        vbox.Add(coordinates_window,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(pnl1), 0, wx.ALL|wx.EXPAND, 5)  
        vbox.AddSpacer(10)

        vbox.Add(self.default_age_text,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(default_age_window,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(pnl1), 0, wx.ALL|wx.EXPAND, 5)  
        vbox.AddSpacer(10)


        vbox.Add(sample_mean_window,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(pnl1), 0, wx.ALL|wx.EXPAND, 5)  
        vbox.AddSpacer(10)

        vbox.Add(site_mean_window,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(pnl1), 0, wx.ALL|wx.EXPAND, 5)  
        vbox.AddSpacer(10)

        vbox.Add(loaction_mean_window,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticLine(pnl1), 0, wx.ALL|wx.EXPAND, 5)  
        vbox.AddSpacer(10)

        #-------------
        vbox1=wx.BoxSizer(wx.VERTICAL)
        vbox1.AddSpacer(10)
        vbox1.Add(vbox)
        vbox1.AddSpacer(10)
        vbox1.Add(hboxok,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox1.AddSpacer(10)


        pnl1.SetSizer(vbox1)
        vbox1.Fit(self)

    
            
    def on_change_cb_sample_mean_VGP(self,event):
        if self.cb_sample_mean_VGP.GetValue()==True:
            self.cb_site_mean_VGP.SetValue(False)

    def on_change_cb_site_mean_VGP(self,event):
        if self.cb_site_mean_VGP.GetValue()==True:
            self.cb_sample_mean_VGP.SetValue(False)
        
    def on_change_cb_location_mean_VGP(self,event):
        if self.cb_location_mean_VGP.GetValue()==True:
            self.cb_location_mean_VGP.SetValue(False)

#--------------------------------------------------------------    
# MagIc results tables dialog
#--------------------------------------------------------------

#--------------------------------------------------------------    
# MagIC generic files conversion
#--------------------------------------------------------------


class convert_generic_files_to_MagIC(wx.Frame):
    """"""
    title = "PmagPy Thellier GUI generic file conversion"

    def __init__(self,WD):
        wx.Frame.__init__(self, None, wx.ID_ANY, self.title)
        self.panel = wx.Panel(self)
        #self.MakeModal(True) 
        self.max_files=10
        self.WD=WD
        self.InitUI()
        self.END=False
    def InitUI(self):

        pnl = self.panel

        #---sizer infor ----
        TEXT=[]
        TEXT.append("A generic file is a tab-delimited file with the following headers:\n")
        TEXT.append("specimen  treatment step moment dec_s inc_s dec_g inc_g dec_t inc_t \n")
        TEXT.append("treatment: N [NRM], A[AF] T[Thermal].\n")
        TEXT.append("step: if treatment=N: should be 0.\n")
        TEXT.append("step: if treatment=A: peak field in mT.\n")
        TEXT.append("step: if treatment=T: Temperature in C.\n")  
        TEXT.append("step: if treatment=N: peak field in mT.\n")  
        TEXT.append("moment: magnetic moment in units of emu.\n")  
        TEXT.append("dec_s inc_s: declination/inclination in specimen coordinates\n" ) 
        TEXT.append("dec_g inc_g: declination/inclination in geographic coordinates\n")  
        TEXT.append("dec_t inc_t: declination/inclination in tilt corrected coordinates\n")          
        TEXT.append("\n At least one set of dec/inc is required.\n")
        TEXT.append("\n The order of the columns is not important.\n")
        

        STRING="".join(TEXT) 
        bSizer_info = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "" ), wx.HORIZONTAL )
        bSizer_info.Add(wx.StaticText(pnl,label=STRING),wx.ALIGN_LEFT)
            

        #---sizer 0 ----
        TEXT="file:\n choose measurement file\n no spaces are allowed in path"
        bSizer0 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "" ), wx.VERTICAL )
        bSizer0.Add(wx.StaticText(pnl,label=TEXT),wx.ALIGN_TOP)
        bSizer0.AddSpacer(5)
        for i in range(self.max_files):
            command= "self.file_path_%i = wx.TextCtrl(self.panel, id=-1, size=(200,25), style=wx.TE_READONLY)"%i
            exec command
            command= "self.add_file_button_%i =  wx.Button(self.panel, id=-1, label='add',name='add_%i')"%(i,i)
            exec command
            command= "self.Bind(wx.EVT_BUTTON, self.on_add_file_button_i, self.add_file_button_%i)"%i
            #print command
            exec command            
            command="bSizer0_%i = wx.BoxSizer(wx.HORIZONTAL)"%i
            exec command
            command="bSizer0_%i.Add(wx.StaticText(pnl,label=('%i  '[:2])),wx.ALIGN_LEFT)"%(i,i+1)
            exec command
            
            command="bSizer0_%i.Add(self.file_path_%i,wx.ALIGN_LEFT)" %(i,i)
            exec command
            command="bSizer0_%i.Add(self.add_file_button_%i,wx.ALIGN_LEFT)" %(i,i)
            exec command
            command="bSizer0.Add(bSizer0_%i,wx.ALIGN_TOP)" %i
            exec command
            bSizer0.AddSpacer(5)
              
#        #---sizer 1 ----
#
#        TEXT="\n\nExperiment:"
#        bSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "" ), wx.VERTICAL )
#        bSizer1.Add(wx.StaticText(pnl,label=TEXT),wx.ALIGN_TOP)
#        self.experiments_names=['IZZI','IZ','ZI','ATRM 6 positions','cooling rate','NLT']
#        bSizer1.AddSpacer(5)
#        for i in range(self.max_files):
#            command="self.protocol_info_%i = wx.ComboBox(self.panel, -1, self.experiments_names[0], size=(100,25), choices=self.experiments_names, style=wx.CB_DROPDOWN)"%i
#            #command="self.protocol_info_%i = wx.TextCtrl(self.panel, id=-1, size=(100,20), style=wx.TE_MULTILINE | wx.HSCROLL)"%i
#            #print command
#            exec command
#            command="bSizer1.Add(self.protocol_info_%i,wx.ALIGN_TOP)"%i        
#            exec command
#            bSizer1.AddSpacer(5)

        #---sizer 2 ----

        #TEXT="Blab:\n(microT dec inc)\nexample: 40 0 -90 "
        #bSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "" ), wx.VERTICAL )
        #bSizer2.Add(wx.StaticText(pnl,label=TEXT),wx.ALIGN_TOP)
        #bSizer2.AddSpacer(5)
        #for i in range(self.max_files):
        #    command= "self.file_info_Blab_%i = wx.TextCtrl(self.panel, id=-1, size=(40,25))"%i
        #    exec command
        #    command= "self.file_info_Blab_dec_%i = wx.TextCtrl(self.panel, id=-1, size=(40,25))"%i
        #    exec command
        #    command= "self.file_info_Blab_inc_%i = wx.TextCtrl(self.panel, id=-1, size=(40,25))"%i
        #    exec command          
        #    command="bSizer2_%i = wx.BoxSizer(wx.HORIZONTAL)"%i
        #    exec command
        #    command="bSizer2_%i.Add(self.file_info_Blab_%i ,wx.ALIGN_LEFT)" %(i,i)
        #    exec command
        #    command="bSizer2_%i.Add(self.file_info_Blab_dec_%i,wx.ALIGN_LEFT)" %(i,i)
        #    exec command
        #    command="bSizer2_%i.Add(self.file_info_Blab_inc_%i,wx.ALIGN_LEFT)" %(i,i)
        #    exec command
        #    command="bSizer2.Add(bSizer2_%i,wx.ALIGN_TOP)" %i
        #    exec command
        #    bSizer2.AddSpacer(5)


        #self.blab_info = wx.TextCtrl(self.panel, id=-1, size=(80,250), style=wx.TE_MULTILINE | wx.HSCROLL)
        #bSizer2.Add(self.blab_info,wx.ALIGN_TOP)        

        #---sizer 3 ----

        TEXT="\nUser\nname:"
        bSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "" ), wx.VERTICAL )
        bSizer3.Add(wx.StaticText(pnl,label=TEXT),wx.ALIGN_TOP)
        bSizer3.AddSpacer(5)
        for i in range(self.max_files):
            command= "self.file_info_user_%i = wx.TextCtrl(self.panel, id=-1, size=(60,25))"%i
            exec command
            command="bSizer3.Add(self.file_info_user_%i,wx.ALIGN_TOP)" %i
            exec command
            bSizer3.AddSpacer(5)

        #---sizer 4 ----

        TEXT="\nsample-specimen\nnaming convention:"
        bSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "" ), wx.VERTICAL )
        bSizer4.Add(wx.StaticText(pnl,label=TEXT),wx.ALIGN_TOP)
        self.sample_naming_conventions=['sample=specimen','no. of terminate characters','charceter delimited']
        bSizer4.AddSpacer(5)
        for i in range(self.max_files):
            command="self.sample_naming_convention_%i = wx.ComboBox(self.panel, -1, self.sample_naming_conventions[0], size=(180,25), choices=self.sample_naming_conventions, style=wx.CB_DROPDOWN)"%i
            exec command            
            command="self.sample_naming_convention_char_%i = wx.TextCtrl(self.panel, id=-1, size=(40,25))"%i
            exec command
            command="bSizer4_%i = wx.BoxSizer(wx.HORIZONTAL)"%i
            exec command
            command="bSizer4_%i.Add(self.sample_naming_convention_%i,wx.ALIGN_LEFT)" %(i,i)
            exec command
            command="bSizer4_%i.Add(self.sample_naming_convention_char_%i,wx.ALIGN_LEFT)" %(i,i)
            exec command
            command="bSizer4.Add(bSizer4_%i,wx.ALIGN_TOP)"%i        
            exec command

            bSizer4.AddSpacer(5)

        #---sizer 5 ----

        TEXT="\nsite-sample\nnaming convention:"
        bSizer5 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "" ), wx.VERTICAL )
        bSizer5.Add(wx.StaticText(pnl,label=TEXT),wx.ALIGN_TOP)
        self.site_naming_conventions=['site=sample','no. of terminate characters','charceter delimited']
        bSizer5.AddSpacer(5)
        for i in range(self.max_files):
            command="self.site_naming_convention_char_%i = wx.TextCtrl(self.panel, id=-1, size=(40,25))"%i
            exec command
            command="self.site_naming_convention_%i = wx.ComboBox(self.panel, -1, self.site_naming_conventions[0], size=(180,25), choices=self.site_naming_conventions, style=wx.CB_DROPDOWN)"%i
            exec command
            command="bSizer5_%i = wx.BoxSizer(wx.HORIZONTAL)"%i
            exec command
            command="bSizer5_%i.Add(self.site_naming_convention_%i,wx.ALIGN_LEFT)" %(i,i)
            exec command
            command="bSizer5_%i.Add(self.site_naming_convention_char_%i,wx.ALIGN_LEFT)" %(i,i)
            exec command
            command="bSizer5.Add(bSizer5_%i,wx.ALIGN_TOP)"%i        
            exec command
            bSizer5.AddSpacer(5)

        #---sizer 6 ----

        TEXT="\n\nlocation:"
        bSizer6 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "" ), wx.VERTICAL )
        bSizer6.Add(wx.StaticText(pnl,label=TEXT),wx.ALIGN_TOP)
        bSizer6.AddSpacer(5)
        for i in range(self.max_files):
            command= "self.file_info_location_%i = wx.TextCtrl(self.panel, id=-1, size=(60,25))"%i
            exec command
            command="bSizer6.Add(self.file_info_location_%i,wx.ALIGN_TOP)" %i
            exec command
            bSizer6.AddSpacer(5)



        #------------------

        #self.add_file_button =  wx.Button(self.panel, id=-1, label='add file')
        #self.Bind(wx.EVT_BUTTON, self.on_add_file_button, self.add_file_button)

        #self.remove_file_button =  wx.Button(self.panel, id=-1, label='remove file')

                     
        self.okButton = wx.Button(self.panel, wx.ID_OK, "&OK")
        self.Bind(wx.EVT_BUTTON, self.on_okButton, self.okButton)

        self.cancelButton = wx.Button(self.panel, wx.ID_CANCEL, '&Cancel')
        self.Bind(wx.EVT_BUTTON, self.on_cancelButton, self.cancelButton)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
        #hbox1.Add(self.add_file_button)
        #hbox1.Add(self.remove_file_button )

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)        
        hbox2.Add(self.okButton)
        hbox2.Add(self.cancelButton )

        #------

        vbox=wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(5)
        hbox.Add(bSizer0, flag=wx.ALIGN_LEFT)        
        hbox.AddSpacer(5)
        #hbox.Add(bSizer1, flag=wx.ALIGN_LEFT)        
        #hbox.AddSpacer(5)
        #hbox.Add(bSizer2, flag=wx.ALIGN_LEFT)        
        #hbox.AddSpacer(5)
        hbox.Add(bSizer3, flag=wx.ALIGN_LEFT)        
        hbox.AddSpacer(5)
        hbox.Add(bSizer4, flag=wx.ALIGN_LEFT)        
        hbox.AddSpacer(5)
        hbox.Add(bSizer5, flag=wx.ALIGN_LEFT)        
        hbox.AddSpacer(5)
        hbox.Add(bSizer6, flag=wx.ALIGN_LEFT)        
        hbox.AddSpacer(5)

        #-----
        
        vbox.AddSpacer(20)
        vbox.Add(bSizer_info,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(20)        
        vbox.Add(hbox)
        vbox.AddSpacer(20)
        vbox.Add(hbox1,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(20)
        vbox.Add(hbox2,flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(20)
        
        self.panel.SetSizer(vbox)
        vbox.Fit(self)
        self.Show()
        self.Centre()

    def on_add_file_button(self,event):

        dlg = wx.FileDialog(
            None,message="choose file to convert to MagIC",
            defaultDir=self.WD, 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )        
        if dlg.ShowModal() == wx.ID_OK:
            FILE = dlg.GetPath()
        # fin=open(FILE,'rU')
        self.file_path.AppendText(FILE+"\n")
        self.protocol_info.AppendText("IZZI"+"\n")


    def on_add_file_button_i(self,event):

        dlg = wx.FileDialog(
            None,message="choose file to convert to MagIC",
            defaultDir="./", 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )        
        if dlg.ShowModal() == wx.ID_OK:
            FILE = dlg.GetPath()
        # fin=open(FILE,'rU')
        button = event.GetEventObject()
        name=button.GetName()
        i=int((name).split("_")[-1])
        #print "The button's name is " + button.GetName()
        
        command="self.file_path_%i.SetValue(FILE)"%i
        exec command

        #self.file_path.AppendText(FILE)
        #self.protocol_info.AppendText("IZZI"+"\n")



    def read_generic_file(self,path):
        Data={}
        if str(path)=="":
            return ({})
        Fin=open(str(path),'rU')
        header=Fin.readline().strip('\n').split('\t')
        
        for line in Fin.readlines():
            tmp_data={}
            l=line.strip('\n').split('\t')
            if len(l)<len(header):
                continue
            else:
                for i in range(len(header)):
                    tmp_data[header[i]]=l[i]
                specimen=tmp_data['specimen']
                if specimen not in Data.keys():
                    Data[specimen]=[]
                # check dupliactes
                if len(Data[specimen]) >0:
                    if tmp_data['treatment']==Data[specimen][-1]['treatment']:
                        if tmp_data['step']==Data[specimen][-1]['step']:
                            print "-W- WARNING: duplicate measurements specimen %s, Treatment %s:%s. keeping onlt the last one"%(tmp_data['specimen'],tmp_data['treatment'],tmp_data['step'])
                            Data[specimen].pop()
                        
                Data[specimen].append(tmp_data)
        return(Data)               

    def on_okButton(self,event):


        #-----------------------------------
        # Prepare MagIC measurement file
        #-----------------------------------

        # prepare output file
        #magic_headers=['er_citation_names','er_specimen_name',"er_sample_name","er_site_name",'er_location_name','er_analyst_mail_names',\
        #               "magic_instrument_codes","measurement_flag","measurement_standard","magic_experiment_name","magic_method_codes","measurement_number",'treatment_temp',"measurement_dec","measurement_inc",\
        #               "measurement_magn_moment","measurement_temp","treatment_dc_field","treatment_dc_field_phi","treatment_dc_field_theta"]             

        #fout=open("magic_measurements.txt",'w')        
        #fout.write("tab\tmagic_measurements\n")
        #header_string=""
        #for i in range(len(magic_headers)):
        #    header_string=header_string+magic_headers[i]+"\t"
        #fout.write(header_string[:-1]+"\n")

        #-----------------------------------
        os.chdir(self.WD)
        Data={}
        header_codes=[]
        ERROR=""
        datafiles=[]
        MagRecs=[]
        self.er_sample_data={}
        try:
            self.er_sample_data=self.read_magic_file(os.path.join(self.WD, "er_samples.txt"), 'er_sample_name')
        except:
            print "-W- WARNING: Cant find er_samples.txt table"
            
        for i in range(self.max_files):

            # read data from generic file
            datafile=""
            command="datafile=self.file_path_%i.GetValue()"%i
            exec command
            #if datafile!="":
            #    try:
            #        this_file_data= self.read_generic_file(datafile)
            #    except:
            #        print "-E- Cant read file %s" %datafile                
            #else:
            #    continue
            this_file_data= self.read_generic_file(datafile)
            #print "datafile",datafile
            #print "this_file_data",this_file_data
                
            # get experiment
            #command="experiment=self.protocol_info_%i.GetValue()"%i
            #exec command

            # get Blab
            #labfield=["0","-1","-1"]
            #command="labfield[0]=self.file_info_Blab_%i.GetValue()"%i
            #exec command
            #command="labfield[1]=self.file_info_Blab_dec_%i.GetValue()"%i
            #exec command
            #command="labfield[2]=self.file_info_Blab_inc_%i.GetValue()"%i
            #exec command
            
            # get User_name
            user_name=""
            command="user_name=self.file_info_user_%i.GetValue()"%i
            exec command
            
            # get sample-specimen naming convention

            sample_naming_convenstion=["",""]
            command="sample_naming_convenstion[0]=self.sample_naming_convention_%i.GetValue()"%i
            exec command
            command="sample_naming_convenstion[1]=self.sample_naming_convention_char_%i.GetValue()"%i
            exec command
            
            # get site-sample naming convention

            site_naming_convenstion=["",""]
            command="site_naming_convenstion[0]=self.site_naming_convention_%i.GetValue()"%i
            exec command
            command="site_naming_convenstion[1]=self.site_naming_convention_char_%i.GetValue()"%i
            exec command

            # get location
            location_name=""
            command="location_name=self.file_info_location_%i.GetValue()"%i
            exec command

            
            # read er_samples.txt
            # to check for sample orientation data and tilt-corrected data
            ErSamplesRecs=[]
            for specimen in this_file_data.keys():
                measurement_running_number=0
                this_specimen_LT=[]
                this_specimen_LP=[]
                MagRecs_this_specimen=[]
                for meas_line in this_file_data[specimen]:
                    MagRec={}
                    #
                    MagRec["er_specimen_name"]=meas_line['specimen']
                    MagRec['er_citation_names']="This study"
                    MagRec["er_sample_name"]=self.get_sample_name(MagRec["er_specimen_name"],sample_naming_convenstion)
                    MagRec["er_site_name"]=self.get_site_name(MagRec["er_sample_name"],site_naming_convenstion)
                    MagRec["er_location_name"]=location_name
                    MagRec['er_analyst_mail_names']=user_name 
                    MagRec["magic_instrument_codes"]="" 
                    MagRec["measurement_flag"]='g'
                    MagRec["measurement_number"]="%i"%measurement_running_number
                    MagRec["measurement_temp"]='273.' # room temp in kelvin
                    MagRec["measurement_standard"]="u"
                    #-----
                    MagRec["measurement_magn_moment"]='%10.3e'%(float(meas_line["moment"])*1e-3) # convert to Am^2
                    
                    # see if core azimuth and tilt-corrected data are in er_samples.txt
                    sample=MagRec["er_sample_name"]
                    found_sample_azimuth,found_sample_dip,found_sample_bed_dip_direction,found_sample_bed_dip=False,False,False,False
                    if sample in self.er_sample_data.keys():
                        if "sample_azimuth" in self.er_sample_data[sample].keys() and self.er_sample_data[sample]['sample_azimuth'] !="":
                            sample_azimuth=float(self.er_sample_data[sample]['sample_azimuth'])
                            found_sample_azimuth=True
                        if "sample_dip" in self.er_sample_data[sample].keys() and self.er_sample_data[sample]['sample_dip']!="":
                            sample_dip=float(self.er_sample_data[sample]['sample_dip'])
                            found_sample_dip=True
                        if "sample_bed_dip_direction" in self.er_sample_data[sample].keys() and self.er_sample_data[sample]['sample_bed_dip_direction']!="":
                            sample_bed_dip_direction=float(self.er_sample_data[sample]['sample_bed_dip_direction'])
                            found_sample_bed_dip_direction=True
                        if "sample_bed_dip" in self.er_sample_data[sample].keys() and self.er_sample_data[sample]['sample_bed_dip']!="":
                            sample_bed_dip=float(self.er_sample_data[sample]['sample_bed_dip'])
                            found_sample_bed_dip=True
                    else:
                        self.er_sample_data[sample]={}
                    
                    #--------------------
                    # deal with sample orientation
                    #--------------------

                    found_s,found_geo,found_tilt=False,False,False
                    if "dec_s" in meas_line.keys() and "inc_s" in meas_line.keys():
                        found_s=True
                        MagRec["measurement_dec"]=meas_line["dec_s"]
                        MagRec["measurement_inc"]=meas_line["inc_s"]
                    if "dec_g" in meas_line.keys() and "inc_g" in meas_line.keys():
                        found_geo=True
                    if "dec_t" in meas_line.keys() and "inc_t" in meas_line.keys():
                        found_tilt=True
                        
                    #-----------------------------                    
                    # specimen coordinates: no
                    # geographic coordinates: yes
                    #-----------------------------                    
                    
                    if found_geo and not found_s:
                        MagRec["measurement_dec"]=meas_line["dec_g"]
                        MagRec["measurement_inc"]=meas_line["inc_g"]
                        
                        # core azimuth/plunge is not in er_samples.txt
                        if not found_sample_dip or not found_sample_azimuth:
                            self.er_sample_data[sample]['sample_azimuth']="0"
                            self.er_sample_data[sample]['sample_dip']="0"

                        # core azimuth/plunge is in er_samples.txt                        
                        else:
                            sample_azimuth=float(self.er_sample_data[sample]['sample_azimuth'])  
                            sample_dip=float(self.er_sample_data[sample]['sample_dip'])   
                            if sample_azimuth!=0 and sample_dip!=0:
                                print "-W- WARNING: delete core azimuth/plunge in er_samples.txt\n\
                                becasue dec_s and inc_s are not avaialable" 

                    #-----------------------------                                                
                    # specimen coordinates: no
                    # geographic coordinates: no
                    #-----------------------------                    
                    if not found_geo and not found_s:
                        print "-E- ERROR: sample %s does not have dec_s/inc_s or dec_g/inc_g. Ignore specimen %s "%(sample,specimen)
                        break
                           
                    #-----------------------------                                                
                    # specimen coordinates: yes
                    # geographic coordinates: yes
                    #
                    # commant: Ron, this need to be tested !!
                    #-----------------------------                    
                    if found_geo and found_s:
                        
                        cdec,cinc=float(meas_line["dec_s"]),float(meas_line["inc_s"])
                        gdec,ginc=float(meas_line["dec_g"]),float(meas_line["inc_g"])
                        az,pl=pmag.get_azpl(cdec,cinc,gdec,ginc)

                        # core azimuth/plunge is not in er_samples.txt:
                        # calculate core az/pl and add it to er_samples.txt
                        if not found_sample_dip or not found_sample_azimuth:
                            self.er_sample_data[sample]['sample_azimuth']="%.1f"%az
                            self.er_sample_data[sample]['sample_dip']="%.1f"%pl
                        
                        # core azimuth/plunge is in er_samples.txt
                        else:
                            if float(self.er_sample_data[sample]['sample_azimuth'])!= az:
                                print "-E- ERROR in sample_azimuth sample %s. Check it! using the value in er_samples.txt"%sample
                                
                            if float(self.er_sample_data[sample]['sample_dip'])!= pl:
                                print "-E- ERROR in sample_dip sample %s. Check it! using the value in er_samples.txt"%sample
                            
                    #-----------------------------                                                
                    # specimen coordinates: yes
                    # geographic coordinates: no
                    #-----------------------------                    
                    if found_geo and found_s:
                        if found_sample_dip and found_sample_azimuth:
                            pass
                            # (nothing to do)
                        else:
                            print "-E- ERROR: missing sample_dip or sample_azimuth for sample %s.ignoring specimens "%sample
                            break 
 
                    #-----------------------------                                                
                    # tilt-corrected coordinates: yes
                    # geographic coordinates: no
                    #-----------------------------                    
                    if found_tilt and not found_geo:
                            print "-E- ERROR: missing geographic data for sample %s. Ignoring tilt-corrected data "%sample
                    if found_tilt and found_geo:
                        dec_geo,inc_geo=float(meas_line["dec_g"]),float(meas_line["inc_g"])
                        dec_tilt,inc_tilt=float(meas_line["dec_t"]),float(meas_line["inc_t"])
                        if dec_geo==dec_tilt and inc_geo==inc_tilt:
                           DipDir,Dip=0.,0. 
                        else:
                           DipDir,Dip=pmag.get_tilt(dec_geo,inc_geo,dec_tilt,inc_tilt)
                            
                        if not found_sample_bed_dip_direction or not found_sample_bed_dip:
                            print "-I- calculating dip and dip direction used for tilt correction sample %s. results are put in er_samples.txt"%sample
                            self.er_sample_data[sample]['sample_bed_dip_direction']="%.1f"%DipDir
                            self.er_sample_data[sample]['sample_bed_dip']="%.1f"%Dip

                    #-----------------------------                                                
                    # er_samples method codes
                    # geographic coordinates: no
                    #-----------------------------                    
                    if found_tilt or found_geo:
                        self.er_sample_data[sample]['magic_method_codes']="SO-NO"               
                    #-----                    
                    # Lab treatments and MagIC methods
                    #-----                    
                    if meas_line['treatment']=="N":
                        LT="LT-NO"
                        LP="" 
                        MagRec["treatment_temp"]="273."                        
                        #MagRec["treatment_temp"]
                    elif meas_line['treatment']=="A":
                        LT="LT-AF-Z" 
                        LP="LP-DIR-AF"
                        MagRec["treatment_ac_field"]="%.4f"%(float(meas_line['step'])*1e-3)
                        MagRec["treatment_temp"]="273."                        
                        #print MagRec["treatment_ac_field"],"treatment_ac_field"
                    elif meas_line['treatment']=="T":
                        LT="LT-T-Z" 
                        LP="LP-DIR-T"
                        MagRec["treatment_temp"]="%.1f"%(float(meas_line['step'])+273.)
                        #print MagRec["treatment_temp"],"treatment_temp"

                    #if LT not in this_specimen_LT:
                    #    this_specimen_LT.append(LT)
                    if LP!="" and LP not in this_specimen_LP:
                        this_specimen_LP.append(LP)
                                                                                            
                    #MagRec["magic_experiment_name"]=MagRec["er_specimen_name"]+":"+":".join(this_specimen_LP)
                    MagRec["magic_method_codes"]=LT#+":"+":".join(this_specimen_LP)
                    MagRecs_this_specimen.append(MagRec)
                    
                    #-----------------
                    # er_samples_data
                    #
                    if sample in self.er_sample_data.keys():
                        self.er_sample_data[sample]['er_sample_name']=sample
                        self.er_sample_data[sample]['er_site_name']=MagRec["er_site_name"]
                        self.er_sample_data[sample]['er_location_name']=MagRec["er_location_name"]
                        
                        
                    measurement_running_number+=1
                
                # add magic_experiment_name and magic_method_codes to magic_measurements.txt
                for MagRec in MagRecs_this_specimen:
                    MagRec["magic_experiment_name"]=MagRec["er_specimen_name"]+":"+":".join(this_specimen_LP)
                    MagRec["magic_method_codes"]=MagRec["magic_method_codes"]+":"+":".join(this_specimen_LP)
                    MagRecs.append(MagRec)   
        #--
        # write magic_measurements.txt
        #--
        MagRecs_fixed=self.merge_pmag_recs(MagRecs)
        pmag.magic_write(os.path.join(self.WD, "magic_measurements.txt"), MagRecs_fixed, 'magic_measurements')

        #--
        # write er_samples.txt
        #--
        ErSamplesRecs=[]
        samples=self.er_sample_data.keys()
        for sample in samples:
            ErSamplesRecs.append(self.er_sample_data[sample])
        ErSamplesRecs_fixed=self.merge_pmag_recs(ErSamplesRecs)
        pmag.magic_write(os.path.join(self.WD, "er_samples.txt"), ErSamplesRecs_fixed, 'er_samples')
        
                    
                        
        
        MSG=" Files converted to MagIC format and merged into two files:\n\
        magic_measurements.txt and er_samples.txt.\n\
        Files saved in the current MagIC directory.\n\
        Quit the GUI and restart it to view the data."            
        dlg1 = wx.MessageDialog(None,caption="Message:", message=MSG ,style=wx.OK|wx.ICON_INFORMATION)
        dlg1.ShowModal()
        dlg1.Destroy()
        self.END=True
        self.Destroy()

    def merge_pmag_recs(self,old_recs):
        # fix the headers of pmag recs
        recs={}
        recs=copy.deepcopy(old_recs)
        headers=[]
        for rec in recs:
            for key in rec.keys():
                if key not in headers:
                    headers.append(key)
        for rec in recs:
            for header in headers:
                if header not in rec.keys():
                    rec[header]=""
        return recs

    def on_cancelButton(self,event):
        self.Destroy()

    def get_sample_name(self,specimen,sample_naming_convenstion):
        if sample_naming_convenstion[0]=="sample=specimen":
            sample=specimen
        elif sample_naming_convenstion[0]=="no. of terminate characters":
            n=int(sample_naming_convenstion[1])*-1
            sample=specimen[:n]
        elif sample_naming_convenstion[0]=="charceter delimited":
            d=sample_naming_convenstion[1]
            sample_splitted=specimen.split(d)
            if len(sample_splitted)==1:
                sample=sample_splitted[0]
            else:
                sample=d.join(sample_splitted[:-1])
        return sample
                            
    def get_site_name(self,sample,site_naming_convenstion):
        if site_naming_convenstion[0]=="site=sample":
            site=sample
        elif site_naming_convenstion[0]=="no. of terminate characters":
            n=int(site_naming_convenstion[1])*-1
            site=sample[:n]
        elif site_naming_convenstion[0]=="charceter delimited":
            d=site_naming_convenstion[1]
            site_splitted=sample.split(d)
            if len(site_splitted)==1:
                site=site_splitted[0]
            else:
                site=d.join(site_splitted[:-1])
        #print "d",d
        #print "sample",sample
        #print "site_splitted",site_splitted
        #print "site",site
        return site
            
    def read_magic_file(self,path,sort_by_this_name):
        DATA={}
        fin=open(path,'rU')
        fin.readline()
        line=fin.readline()
        header=line.strip('\n').split('\t')
        for line in fin.readlines():
            tmp_data={}
            tmp_line=line.strip('\n').split('\t')
            for i in range(len(tmp_line)):
                tmp_data[header[i]]=tmp_line[i]
            if tmp_data[sort_by_this_name] in DATA.keys():
                print "-E- ERROR: magic file %s has more than one line for %s %s\n"%(path,sort_by_this_name,tmp_data[sort_by_this_name])
            DATA[tmp_data[sort_by_this_name]]=tmp_data
        fin.close()        
        return(DATA)


#--------------------------------------------------------------    
# Popupmenu
#--------------------------------------------------------------

class GBPopupMenu(wx.Menu):
    def __init__(self,Data,magic_file,mag_meas_data,s,g_index,position):
        self.g_index=g_index
        self.s=s
        self.Data=Data
        self.mag_meas_data=mag_meas_data
        self.magic_file=magic_file
        #self.measurement_flag=measurement_flag
        wx.Menu.__init__(self)
        item = wx.MenuItem(self, wx.NewId(), "'good measurement'")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItemGood, item)
        item = wx.MenuItem(self, wx.NewId(),"'bad measurement'")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItemBad, item)

    def OnItemGood(self, event):
        #print "good"
        index=self.Data[self.s]['mag_meas_data_index'][self.g_index]
        #print self.mag_meas_data[index]
        self.mag_meas_data[index]['measurement_flag']='g'
        self.write_good_bad_magic_measurements()
        
        
     
    def OnItemBad(self, event):
        #print "bad"
        index=self.Data[self.s]['mag_meas_data_index'][self.g_index]
        #print self.mag_meas_data[index]
        self.mag_meas_data[index]['measurement_flag']='b'
        self.write_good_bad_magic_measurements()
        
    def write_good_bad_magic_measurements(self):
        #print "write_good_bad_magic_measurements"
        print "self.magic_file",self.magic_file
        pmag.magic_write(self.magic_file,self.mag_meas_data,"magic_measurements")
                


#--------------------------------------------------------------    
# Change Acceptance criteria dialog
#--------------------------------------------------------------


class demag_criteria_dialog(wx.Dialog):

    def __init__(self, parent, acceptance_criteria,title):
        style =  wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER  
        super(demag_criteria_dialog, self).__init__(parent, title=title,style=style)
        self.acceptance_criteria=acceptance_criteria
        self.InitUI(acceptance_criteria)
        #self.SetSize((250, 200))

    def InitUI(self,acceptance_criteria):

        pnl1 = wx.Panel(self)

        #----------- 
        # specimen criteria
        #-----------                

        vbox = wx.BoxSizer(wx.VERTICAL)
        bSizer1 = wx.StaticBoxSizer( wx.StaticBox( pnl1, wx.ID_ANY, "specimen acceptance criteria" ), wx.HORIZONTAL )

        # Specimen criteria

        window_list_specimens=['specimen_n','specimen_mad','specimen_dang','specimen_alpha95']
        for key in window_list_specimens:
            command="self.set_%s=wx.TextCtrl(pnl1,style=wx.TE_CENTER,size=(50,20))"%key
            exec command
        criteria_specimen_window = wx.GridSizer(2, len(window_list_specimens), 10, 10)
        criteria_specimen_window.AddMany( [(wx.StaticText(pnl1,label="n",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="MAD",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="DANG",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="alpha95",style=wx.TE_CENTER), wx.EXPAND),
            (self.set_specimen_n),
            (self.set_specimen_mad),
            (self.set_specimen_dang),
            (self.set_specimen_alpha95)])
                                           
        bSizer1.Add( criteria_specimen_window, 0, wx.ALIGN_LEFT|wx.ALL, 5 )


        #----------- 
        # sample criteria
        #-----------                


        bSizer2 = wx.StaticBoxSizer( wx.StaticBox( pnl1, wx.ID_ANY, "sample acceptance criteria" ), wx.HORIZONTAL )
    
        #self.set_average_by_sample_or_site=wx.ComboBox(pnl1, -1,size=(150, -1), value = 'sample', choices=['sample','site'], style=wx.CB_READONLY)
        
        # Sample criteria
        window_list_samples=['sample_n','sample_n_lines','sample_n_planes','sample_k','sample_r','sample_alpha95']
        for key in window_list_samples:
            command="self.set_%s=wx.TextCtrl(pnl1,style=wx.TE_CENTER,size=(50,20))"%key
            exec command
        criteria_sample_window = wx.GridSizer(2, len(window_list_samples), 10, 10)
        criteria_sample_window.AddMany( [(wx.StaticText(pnl1,label="n",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="n lines",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="n planes",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="k",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="r",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="alpha95",style=wx.TE_CENTER), wx.EXPAND),
            (self.set_sample_n),            
            (self.set_sample_n_lines),            
            (self.set_sample_n_planes),            
            (self.set_sample_k),
            (self.set_sample_r),
            (self.set_sample_alpha95)])

        bSizer2.Add( criteria_sample_window, 0, wx.ALIGN_LEFT|wx.ALL, 5 )


        #----------- 
        # site criteria
        #-----------                


        bSizer3 = wx.StaticBoxSizer( wx.StaticBox( pnl1, wx.ID_ANY, "site acceptance criteria" ), wx.HORIZONTAL )
            
        # Site criteria
        window_list_sites=['site_n','site_n_lines','site_n_planes','site_k','site_r','site_alpha95']
        for key in window_list_sites:
            command="self.set_%s=wx.TextCtrl(pnl1,style=wx.TE_CENTER,size=(50,20))"%key
            exec command
        criteria_site_window = wx.GridSizer(2, len(window_list_sites), 10, 10)
        criteria_site_window.AddMany( [(wx.StaticText(pnl1,label="n",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="n lines",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="n planes",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="k",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="r",style=wx.TE_CENTER), wx.EXPAND),
            (wx.StaticText(pnl1,label="alpha95",style=wx.TE_CENTER), wx.EXPAND),
            (self.set_site_n),            
            (self.set_site_n_lines),            
            (self.set_site_n_planes),            
            (self.set_site_k),
            (self.set_site_r),
            (self.set_site_alpha95)])

        bSizer3.Add( criteria_site_window, 0, wx.ALIGN_LEFT|wx.ALL, 5 )



        #-----------        

        #ok_sizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.okButton = wx.Button(pnl1, wx.ID_OK, "&OK")
        self.cancelButton = wx.Button(pnl1, wx.ID_CANCEL, '&Cancel')
        hbox3.Add(self.okButton)
        hbox3.AddSpacer(10)
        hbox3.Add(self.cancelButton )
        #self.okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        #-----------

        
        supported_crit=window_list_specimens+window_list_samples+window_list_sites
        
        # initialize value:
        for crit in supported_crit:
            if crit not in acceptance_criteria.keys():
                continue
            if acceptance_criteria[crit]['value']!="":
                value=float(acceptance_criteria[crit]['value'])
                if value!=-999:                                   
                    decimal_points=acceptance_criteria[crit]['decimal_points']
                    command="self.set_%s.SetValue('%%.%if'%%(value))"%(crit,int(decimal_points))
                    exec command
        
        #----------------------  
        vbox.AddSpacer(10)
        vbox.Add(bSizer1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(bSizer2, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(bSizer3, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER_HORIZONTAL)
        vbox.AddSpacer(10)
               
        hbox_top=wx.BoxSizer(wx.HORIZONTAL)
        hbox_top.AddSpacer(50)   
        hbox_top.Add(vbox)                      
        hbox_top.AddSpacer(50)              
        pnl1.SetSizer(hbox_top)
        hbox_top.Fit(self)



#class MyFrame(wx.Frame):
#    def __init__(self, parent, id, title):
#        wx.Frame.__init__(self, parent, id, title, size=(500,500))
#
#        panel = wx.Panel(self, -1)
#        wx.Button(panel, 1, 'Show Custom Dialog', (100,100))
#        self.Bind (wx.EVT_BUTTON, self.OnShowCustomDialog, id=1)
#
#    def OnShowCustomDialog(self, event):
#        #dia = MyDialog(self, -1, 'buttons')
#                
#        dia=demag_criteria_dialog(None, {},title='Set Acceptance Criteria')
#        dia.Center()        
#        dia.ShowModal()
#        dia.Destroy()
#
#class MyApp(wx.App):
#    def OnInit(self):
#        frame = MyFrame(None, -1, 'customdialog1.py')
#        frame.Show(True)
#        frame.Centre()
#        return True
##
#app = MyApp(0)
#app.MainLoop()


#if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    app.frame = demag_criteria_dialog(None, {},title='Set Acceptance Criteria')
#    app.frame.Show()
#    app.frame.Center()
#    app.MainLoop()

 
#if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    app.frame = magic_pmag_tables_dialog(None,"./",{},{})
#    app.frame.Center()
#    #alignToTop(app.frame)
#    #dw, dh = wx.DisplaySize() 
#    #w, h = app.frame.GetSize()
#    #print 'display 2', dw, dh
#    #print "gui 2", w, h
#    app.frame.Show()
#    app.MainLoop()
