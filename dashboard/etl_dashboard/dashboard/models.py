from django.db import models

# Create your models here.



class Etl_table(models.Model):
    table_name = models.CharField(max_length=200)
    def __str__(self):
        return str(self.table_name)

class Etl_load(models.Model):
    table_name = models.ForeignKey(Etl_table, on_delete=models.CASCADE)
    parquete_file =models.CharField(max_length=200)
    min_id = models.IntegerField()
    max_id = models.IntegerField()

class Etl_table_property(models.Model):
    table_name = models.ForeignKey(Etl_table, on_delete=models.CASCADE)
    record_sizes = models.IntegerField()
    record_count = models.IntegerField()
