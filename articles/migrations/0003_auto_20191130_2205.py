# Generated by Django 2.2.6 on 2019-11-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-pk',)},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete='models.CASCADE', related_name='comments', to='articles.Article')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
