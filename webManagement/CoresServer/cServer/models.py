from django.db import models

class Computer(models.Model):
    name = models.CharField(max_length=20)
    ip = models.GenericIPAddressField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Thread(models.Model):
    name = models.CharField(max_length=20)
    computer = models.ForeignKey(Computer)
    active = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ("name", "computer")
    
    def __str__(self):
        return self.name + " (" + self.computer.name + ") - Active: " + str(self.active)
    
class File(models.Model):
    name = models.CharField(max_length=60)
    fetfile = models.FileField(upload_to='fetfiles/')
    
    def __str__(self):
        return self.name + " (" + str(self.fetfile) + ")"
    
class Assignment(models.Model):
    fetfile = models.ForeignKey(File)
    thread = models.ForeignKey(Thread, unique=True)
    
    def __str__(self):
        return self.thread.computer.name + " (" + self.thread.name + "): " + self.fetfile.name + " (" + self.fetfile.fetfile.path + ")"
        
class Result(models.Model):
    fetfile = models.ForeignKey(File)
    rfile = models.FileField(upload_to='results/')
    tfile = models.FileField(upload_to='results/')
    time = models.IntegerField(default=0)
    #teachers analisys...

    def __str__(self):
        return self.fetfile.name + " (" + str(self.time) + ")"