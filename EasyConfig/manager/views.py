import os,threading
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from .models import Project, Device, Interface
from .services import get_project_name,get_project_devices
from .automation import configuration_router,ssh_conection,vpcs_configuration, funct_ping
from .serializers import InterfaceSerializer




def members(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def show_projects(request):
    get_project_name(request.user)

    proiecte = Project.objects.filter(user = request.user)
    return render(request, 'My_project.html', {'proiecte' : proiecte})

def show_projects_devices(request, project_id):
    get_project_devices(project_id)

    devices = Device.objects.filter(project_id = project_id).prefetch_related('interfaces')
    return render(request, 'Project_page.html',{'devices' : devices})

@api_view(['POST'])
def save_interface_config(request):
    data = request.data 
    print(request.data)
    device_id = data.get('device_id')
    interface_name = data.get('interface_name')
    print("--- DATE PRIMITE DIN FRONTEND ---")
    print(f"Device ID primit: '{device_id}' (Tip: {type(device_id)})")
    print(f"Nume Interfață primit: '{interface_name}'")


    try:
        interface_obj = Interface.objects.get(device_id = device_id, name = interface_name)
    except Interface.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Interfata nu a fost gasita in baza de date!'
        })
    serializer = InterfaceSerializer(interface_obj, data=data, partial = True)
    if serializer.is_valid():
        instance = serializer.save()

        instance.is_configured = False
        instance.save()
        print(f"Configuratia s-a salvat in baza de date pentru {interface_name}")
        if 'vpcs' in instance.device.device_type.strip().lower():
            thread1 = threading.Thread(target=vpcs_configuration, args= (instance.device.device_id,instance.device.console_port,instance.device.name,instance.name,instance.ip_address, instance.mask, instance.gateway))
        elif instance.device.device_type == 'router':
            thread1 = threading.Thread(target=configuration_router, args=(instance.device.device_id,instance.device.console_port,instance.device.name,instance.name,instance.ip_address, instance.mask))
        
        thread1.daemon= True
        thread1.start()
        
        return Response({
            'status': 'in_progress', 
            'message': 'Configurația se aplică în fundal în GNS3...'
        })
    return Response({
        'status': 'error', 
        'message': serializer.errors
    })

@api_view(['POST'])
def check_interface_status(request):
    data = request.data
    device_id = data.get('device_id')
    interface = data.get('interface_name')
    try:
        interface_obj = Interface.objects.get(device_id= device_id, name = interface)
        print(interface_obj.is_configured)
        return Response({
            'is_configured': interface_obj.is_configured
        },status=status.HTTP_200_OK)
    except Interface.DoesNotExist:

        return Response({
            'is_configured': False
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def run_device_ping(request):
    data = request.data
    device_id = data.get('device_id')
    interface = data.get('interface_name')
    try: 
        interface_obj = Interface.objects.get(device_id= device_id, name = interface)
        rezultat_ping = funct_ping(interface_obj.ip_address)
        return Response(rezultat_ping, status=status.HTTP_200_OK)
    except Interface.DoesNotExist:

        return Response({
            'is_configured': False
        }, status=status.HTTP_404_NOT_FOUND)
