# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Permiso'
        db.create_table(u'administracion_permiso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'administracion', ['Permiso'])

        # Adding model 'Rol'
        db.create_table(u'administracion_rol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'administracion', ['Rol'])

        # Adding M2M table for field permisos on 'Rol'
        m2m_table_name = db.shorten_name(u'administracion_rol_permisos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rol', models.ForeignKey(orm[u'administracion.rol'], null=False)),
            ('permiso', models.ForeignKey(orm[u'administracion.permiso'], null=False))
        ))
        db.create_unique(m2m_table_name, ['rol_id', 'permiso_id'])


    def backwards(self, orm):
        # Deleting model 'Permiso'
        db.delete_table(u'administracion_permiso')

        # Deleting model 'Rol'
        db.delete_table(u'administracion_rol')

        # Removing M2M table for field permisos on 'Rol'
        db.delete_table(db.shorten_name(u'administracion_rol_permisos'))


    models = {
        u'administracion.permiso': {
            'Meta': {'object_name': 'Permiso'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'administracion.rol': {
            'Meta': {'object_name': 'Rol'},
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'permisos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['administracion.Permiso']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['administracion']