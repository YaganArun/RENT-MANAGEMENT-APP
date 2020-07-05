"""RentalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from Management.views import home_view , rent_view , rent_modify , personDetailsForm , delete_person_action ,delete_person
from Management.views import modify_person , rent_form , person_information , rental_delete , export_data_rent_current,export_data_person_all
from Management.views import export_data_home , export_data_rent_all,export_data_person_current,db_config_home ,person_csv_import , rent_csv_import
from Management.views import person_db_wipe , rent_db_wipe , reset_internal_db,old_rent_form , old_rent_form_modify ,old_rent_form_delete,extras_view
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$',home_view , name = 'home'),
    path('rent',rent_view , name='rentView'),
    path('details/<str:person_id>',rent_modify),
    path('personDetails',personDetailsForm , name='personDetailsForm'),
    path('deleteAction/<str:person_id>',delete_person_action),
    path('deleteAction/del/<str:person_id>',delete_person , name='del'),
    path('modify/<str:person_id>' ,modify_person),
    path('payRent/<str:person_id>',rent_form,name='rentPayment'),
    path('personInfo/<str:person_id>',person_information),
    path('details/deleteRental/<int:rent_id>',rental_delete),
    path('exportRentC',export_data_rent_current),
    path('exportRentA',export_data_rent_all),
    path('exportPersonC',export_data_person_current),
    path('exportPersonA',export_data_person_all),
    path('exportdata',export_data_home,name='exportDataHome'),
    path('dbConfig',db_config_home,name='dbConfigHome'),
    path('dbConfig/importPerson',person_csv_import),
    path('dbConfig/importRent',rent_csv_import),
    path('dbConfig/wipePerson',person_db_wipe),
    path('dbConfig/wipeRent',rent_db_wipe),
    path('dbConfig/resetInternal',reset_internal_db),
    re_path(r'^personInfo/oldRentForm/(?P<person_id>\w+)$',old_rent_form),
    re_path(r'^personInfo/(?P<person_id>\w+)/(?P<date>\d{4}-\d{1,2}-\d{1,2})$',old_rent_form_modify),
    re_path(r'^personInfo/oldRentFormDelete/(?P<person_id>\w+)/(?P<date>\d{4}-\d{1,2}-\d{1,2})$',old_rent_form_delete),
    path('extras',extras_view , name='documentation')

]
