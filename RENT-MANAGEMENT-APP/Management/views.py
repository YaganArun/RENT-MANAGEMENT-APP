import csv
import io
import matplotlib.pyplot as plt
import matplotlib
from django.http import HttpResponse

matplotlib.use('Agg')
import os
# django-web
from .forms import PersonForm, RentForm, RentFormOld
from django.forms import model_to_dict
from django.shortcuts import render
from django.db.models import Sum
from .models import Person, Rent, PersonTrack, Record
import datetime

filePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static/images')
print(filePath)


def home_view(request):
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    if len(Person.objects.all()) != PersonTrack.objects.get(id=1).length:
        generate_image(month)
        PersonTrack.objects.filter(id=1).update(length=len(Person.objects.all()))
        print("genrated")
    else:
        print("No changes in db")
    context = {
        'day': day,
        'month': datetime.date(year, month, 1).strftime('%B'),
        'year': year,
        'total_rooms_left': 30 - len(Person.objects.all()),
        'count_of_rooms': len(Person.objects.all()),
        'person_list': Person.objects.all().order_by('date'),
    }
    return render(request, 'home.html', context)


# rent section
def rent_view(request):
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    Notpaid = Person.objects.exclude(
        id__in=[tenant.person.id for tenant in Rent.objects.filter(paymentDate__month=month)])
    notPaidList = [person.id for person in Notpaid]
    print(notPaidList)
    context = {
        'person_list': Person.objects.all(),
        'month': datetime.date(year, month, 1).strftime('%B'),
        'notPaid': notPaidList,
        'totalIncome': Person.objects.all().aggregate(Sum('rent_Ammount'))['rent_Ammount__sum'],
        'currentIncome': Rent.objects.filter(paymentDate__month=month).aggregate(Sum('rent'))['rent__sum'],
        'paid': Rent,
        'len': len(Person.objects.all()),
    }
    return render(request, 'rent_view.html', context)


def rent_form(request, person_id):
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            client = Person.objects.get(id=person_id)
            date = datetime.datetime.today().date()
            data = form.cleaned_data
            data.update({'person': client})
            data.update({'paymentDate': date})
            print(data)
            Rent.objects.create(**data)
            return render(request, 'message.html', {'action': 1, 'name': client.first_name + " " + client.last_name})
        else:
            form = RentForm()
            return render(request, 'rentForm.html', {'form': form})
    else:
        form = RentForm()
        return render(request, 'rentForm.html', {'form': form})


def rent_modify(request, person_id):
    client = Person.objects.get(id=person_id)
    clientRentInfo = Rent.objects.filter(person=client, paymentDate__month=datetime.datetime.today().month)
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            clientRentInfo.update(**data)
            return render(request, 'message.html', {'action': 2, 'name': client.first_name + " " + client.last_name})
        else:
            form = RentForm(model_to_dict(clientRentInfo[0]))
            return render(request, 'details.html', {'form': form, 'rent_id': clientRentInfo[0].id})
    else:
        form = RentForm(model_to_dict(clientRentInfo[0]))
        return render(request, 'details.html', {'form': form, 'rent_id': clientRentInfo[0].id})


def rental_delete(request, rent_id):
    client = Rent.objects.get(id=rent_id).person
    print(client)
    Rent.objects.get(id=rent_id).delete()
    return render(request, 'message.html', {'action': 3, 'name': client.first_name + " " + client.last_name})


def old_rent_form(request, person_id):
    client = Person.objects.get(id=person_id)
    if request.method == 'POST':
        form = RentFormOld(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.update({'person': client})
            Rent.objects.create(**data)
            return render(request, 'message.html', {'action': 9, 'name': client.first_name + " " + client.last_name})
        else:
            form = RentFormOld()
            return render(request, 'rentForm.html', {'action': 1, 'form': form})
    else:
        form = RentFormOld()
        return render(request, 'rentForm.html', {'action': 1, 'form': form})


def old_rent_form_modify(request, person_id, date):
    client = Person.objects.get(id=person_id)
    rentClient = Rent.objects.get(person=client, paymentDate=date)
    print(rentClient)
    if request.method == 'POST':
        form = RentFormOld(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Rent.objects.filter(person=client, paymentDate=date).update(**data)
            return render(request, 'message.html', {'action': 10, 'name': client.first_name + " " + client.last_name})
        else:
            form = RentFormOld(model_to_dict(rentClient))
            return render(request, 'rentForm.html', {'action': 2, 'form': form})

    else:
        form = RentFormOld(model_to_dict(rentClient))
        return render(request, 'rentForm.html', {'action': 2, 'form': form})


def old_rent_form_delete(request, person_id, date):
    client = Person.objects.get(id=person_id)
    rentClient = Rent.objects.filter(person=client, paymentDate=date)[0]
    print(rentClient)
    rentClient.delete()
    return render(request, 'message.html', {'action': 11, 'name': client.first_name + " " + client.last_name})


# person section
def personDetailsForm(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.update({'id': data['first_name'].lower() + data['room_no']})
            print(data)
            sum = Record.objects.get(actionMonth=data['date'].month).count
            Record.objects.filter(actionMonth=data['date'].month).update(count=sum + 1)
            print(sum)
            Person.objects.create(**data)
            return render(request, 'message.html', {'action': 12})
        else:
            form = PersonForm()
            return render(request, 'personDetailsForm.html', {'form': form})
    else:
        form = PersonForm()
        return render(request, 'personDetailsForm.html', {'form': form})


def delete_person_action(request, person_id):
    user = Person.objects.get(id=person_id)
    context = {
        'type': 'DELETED',
        'action': 1,
        'name': user.first_name + " " + user.last_name,
        'id': user.id,
        'rent': user.rent_Ammount,
        'dateRented': user.date,
        'currentDate': datetime.datetime.today().date(),
        'contact_no': user.contact_no,
        'room_no': user.room_no,
    }
    return render(request, 'personDetails.html', context)


def delete_person(request, person_id):
    month = datetime.datetime.now().month
    rec = Record.objects.get(actionMonth=month)
    user = Person.objects.get(id=person_id)
    if rec.count < 0:
        Record.objects.filter(actionMonth=month).update(count=0)
    Record.objects.filter(actionMonth=month).update(count=rec.count - 1)
    user.delete()
    return render(request, 'message.html', {'action': 0, 'name': user.first_name + " " + user.last_name})


def modify_person(request, person_id):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            client = Person.objects.filter(id=person_id)[0]
            name = client.first_name + " " + client.last_name
            data.update({'id': data['first_name'].lower() + data['room_no']})
            client.delete()
            Person.objects.create(**data)
            return render(request, 'message.html', {'type': 'updated', 'name': name})
        else:
            form = PersonForm(model_to_dict(Person.objects.get(id=person_id)))
            return render(request, 'modifyPerson.html', {'form': form})
    else:
        form = PersonForm(model_to_dict(Person.objects.get(id=person_id)))
        return render(request, 'modifyPerson.html', {'form': form})


def person_information(request, person_id):
    person_ = Person.objects.get(id=person_id)
    rentDetailsList = Rent.objects.filter(person=person_).order_by('paymentDate')
    context = {
        'person': person_,
        'rentInfoList': rentDetailsList,
        'len': len(rentDetailsList),
    }
    return render(request, 'personInfo.html', context)


# export data
def export_data_rent_current(request):
    month = datetime.datetime.today().month
    fname = '{}-{}RentDetails.csv'.format(datetime.date(2000, month, 1).strftime('%b'), datetime.datetime.today().year)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename = {}'.format(fname)
    writer = csv.writer(response)
    writer.writerow(['ID', 'Rent', 'Electric Bill', 'Maintanace_charge', 'Payment Date'])
    for row in Rent.objects.filter(paymentDate__month=month).values_list('person', 'rent', 'electric_bill',
                                                                         'Maintanace_charge', 'paymentDate'):
        writer.writerow(row)
    return response


def export_data_rent_all(request):
    fname = "AllRentDetails.csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename = {}'.format(fname)
    writer = csv.writer(response)
    writer.writerow(['ID', 'Rent', 'Electric Bill', 'Maintanace_charge', 'Payment Date'])
    for row in Rent.objects.all().values_list('person', 'rent', 'electric_bill', 'Maintanace_charge', 'paymentDate'):
        writer.writerow(row)
    return response


def export_data_person_all(request):
    fname = 'AllPersonDetails.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename = {}'.format(fname)
    writer = csv.writer(response)
    writer.writerow(
        ['First Name', 'Last Name', 'Age', 'Designation', 'Room Number', 'ID', 'Rent Amount', 'Advance Amount',
         'Contact Number', 'Date Rented'])
    for row in Person.objects.all().values_list('first_name', 'last_name', 'age', 'designation', 'room_no', 'id',
                                                'rent_Ammount', 'advance_Ammount', 'contact_no', 'date'):
        writer.writerow(row)
    return response


def export_data_person_current(request):
    month = datetime.datetime.today().month
    fname = '{}-{}PersonDetails.csv'.format(datetime.date(2000, month, 1).strftime('%b'),
                                            datetime.datetime.today().year)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename = {}'.format(fname)
    writer = csv.writer(response)
    writer.writerow(
        ['First Name', 'Last Name', 'Age', 'Designation', 'Room Number', 'ID', 'Rent Amount', 'Advance Amount',
         'Contact Number', 'Date Rented'])
    for row in Person.objects.filter(date__month=month).values_list('first_name', 'last_name', 'age', 'designation',
                                                                    'room_no', 'id', 'rent_Ammount', 'advance_Ammount',
                                                                    'contact_no', 'date'):
        writer.writerow(row)
    return response


def export_data_home(request):
    return render(request, 'exportHome.html', {})


# db config
def db_config_home(request):
    return render(request, 'dbConfigHome.html', {})


def person_csv_import(request):
    if request.method == 'GET':
        return render(request, 'csvImport.html', {'type': 1})
    else:
        file = request.FILES['file']
        dataset = file.read().decode('UTF-8')
        print(dataset)
        ioString = io.StringIO(dataset)
        next(ioString)  # skips the head of csv
        for col in csv.reader(ioString, delimiter=',', quotechar='|'):
            print(len(col))
            if len(col) != 10:
                return render(request, 'message.html', {'action': 14})

            print(len(Person.objects.filter(id=col[5])))
            if len(Person.objects.filter(id=col[5])):
                Person.objects.filter(id=col[5])[0].delete()
            Person.objects.update_or_create(
                first_name=col[0],
                last_name=col[1],
                age=col[2],
                designation=col[3],
                room_no=col[4],
                id=col[5],
                rent_Ammount=col[6],
                advance_Ammount=col[7],
                contact_no=col[8],
                date=col[9]
            )
            currentPerson = Person.objects.get(id=col[5])
            sum = Record.objects.get(actionMonth=currentPerson.date.month).count
            Record.objects.filter(actionMonth=currentPerson.date.month).update(count=sum + 1)
        return render(request, 'message.html', {'action': 4})


def person_db_wipe(request):
    Person.objects.all().delete()
    month = datetime.datetime.now().month
    Record.objects.all().delete()
    PersonTrack.objects.all().delete()
    for action in range(1, 13):
        Record.objects.create(actionMonth=action)
    PersonTrack.objects.create(id=1, length=1)
    return render(request, 'message.html', {'action': 6})


def rent_csv_import(request):
    if request.method == 'GET':
        if len(Person.objects.all()) == 0:
            print('cant import')
            return render(request, 'csvImport.html', {'type': 3})
        else:
            return render(request, 'csvImport.html', {'type': 2})
    else:
        file = request.FILES['file']
        dataset = file.read().decode('UTF-8')
        print(dataset)
        ioString = io.StringIO(dataset)
        next(ioString)  # skips the head of csv
        for col in csv.reader(ioString, delimiter=',', quotechar='|'):
            if len(col) > 5:
                return render(request, 'message.html', {'action': 13})
            Rent.objects.create(
                person=Person.objects.get(id=col[0]),
                rent=col[1],
                electric_bill=col[2],
                Maintanace_charge=col[3],
                paymentDate=col[4],
            )
        return render(request, 'message.html', {'action': 5})


def rent_db_wipe(request):
    Rent.objects.all().delete()
    return render(request, 'message.html', {'action': 7})


def reset_internal_db(request):
    month = datetime.datetime.now().month
    Record.objects.all().delete()
    PersonTrack.objects.all().delete()
    for action in range(1, 13):
        Record.objects.create(actionMonth=action)
    generate_image(month)
    PersonTrack.objects.create(id=1, length=1)
    return render(request, 'message.html', {'action': 8})


def extras_view(request):
    return render(request, 'extra.html', {})


# graph
def generate_image(mon):
    actionMonthList = []
    countRecord = 0
    for rec in Record.objects.all():
        if countRecord >= mon:
            break
        actionMonthList.append(datetime.date(2012, rec.actionMonth, 1).strftime('%b'))  # getting months appended
        countRecord += 1

    countRecordList = 0
    countList = []
    sum = 0
    for rec in Record.objects.all():
        if countRecordList >= mon:
            break
        sum += rec.count
        countList.append(sum)
        countRecordList += 1
    print(actionMonthList)
    print(countList)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.bar(actionMonthList, countList, color=(0.2, 0.4, 0.6, 0.6))
    plt.xlabel("Month")
    plt.ylabel("Person Count")
    plt.xticks(rotation=40)
    plt.savefig('{}/graph.png'.format(filePath), dpi=300)
    plt.close()
