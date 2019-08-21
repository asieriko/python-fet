from django.db import models

class Computer(models.Model):
    name = models.CharField(max_length=20)
    ip = models.GenericIPAddressField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Thread(models.Model):
    name = models.CharField(max_length=20)
    computer = models.ForeignKey(Computer,on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    lastping = models.DateTimeField(blank=True)
    
    class Meta:
        unique_together = ("name", "computer")
    
    def __str__(self):
        return self.computer.name + "-" + self.name + " - Active: " + str(self.active)
    
class File(models.Model):
    name = models.CharField(max_length=60)
    fetfile = models.FileField(upload_to='fetfiles/')
    
    def __str__(self):
        return self.name + " (" + str(self.fetfile) + ")"
    
class Assignment(models.Model):
    fetfile = models.ForeignKey(File,on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, unique=True,blank=True,null=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.thread.computer.name + " (" + self.thread.name + "): " + self.fetfile.name + " (" + self.fetfile.fetfile.path + ")"
        
class Result(models.Model):
    fetfile = models.ForeignKey(File,blank=True,null=True,on_delete=models.SET_NULL)
    rfile = models.FileField(upload_to='results/')
    tfile = models.FileField(upload_to='results/')
    time = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True, blank=True)
    computer = models.ForeignKey(Computer,blank=True,null=True,on_delete=models.SET_NULL)
    assignment = models.ForeignKey(Assignment,blank=True,null=True,on_delete=models.SET_NULL)
    stats = models.TextField(blank=True,null=True) #Better individual fields?
    #teachers analisys...

    def __str__(self):
        return self.fetfile.name + " (" + str(self.time) + ")"
