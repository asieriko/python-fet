import os

def populate():
    for j in range(1,13):
        comp = add_computer('c'+str(j))    
        for i in range(1,5):
            add_thread(computer=comp,name="t"+str(i))

    # Print out what we have added to the user.
    for c in Computer.objects.all():
        for p in Thread.objects.filter(computer=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_computer(name):
    c = Computer.objects.get_or_create(name=name)[0]
    return c

def add_thread(computer,name):
    t = Thread.objects.get_or_create(computer=computer,name=name)[0]
    return t


def add_superuser():
    from django.contrib.auth.models import User
    user=User.objects.create_user('fet', password='secreto')
    user.is_superuser=True
    user.is_staff=True
    user.save()

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coresServer.settings')
    django.setup()
    from cServer.models import Computer,Thread
    populate()