# Generated by Django 2.1.8 on 2019-05-01 02:08

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20180522_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceBookLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', wagtail.core.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'FaceBookLink',
            },
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='featured_section_2',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='featured_section_2_title',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='featured_section_3',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='featured_section_3_title',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='promo_image',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='promo_text',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='promo_title',
        ),
    ]
