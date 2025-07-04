# Generated by Django 5.2 on 2025-06-17 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0005_anexo'),
    ]

    operations = [
        migrations.AddField(
            model_name='anexo',
            name='comentario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='anexos', to='chamados.comentario'),
        ),
        migrations.AlterField(
            model_name='anexo',
            name='chamado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='anexos', to='chamados.chamado'),
        ),
        migrations.AddConstraint(
            model_name='anexo',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('chamado__isnull', False), ('comentario__isnull', True)), models.Q(('chamado__isnull', True), ('comentario__isnull', False)), _connector='OR'), name='anexo_apenas_um_pai'),
        ),
    ]
