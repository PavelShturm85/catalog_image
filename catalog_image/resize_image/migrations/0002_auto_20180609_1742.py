# Generated by Django 2.0.6 on 2018-06-09 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resize_image', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='name_image',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Название изображения'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='img',
            field=models.ImageField(upload_to='uploads'),
        ),
    ]
