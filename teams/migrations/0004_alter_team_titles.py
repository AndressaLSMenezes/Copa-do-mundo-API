# Generated by Django 4.1.6 on 2023-02-07 19:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teams", "0003_rename_top_score_team_top_scorer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="titles",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
