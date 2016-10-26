# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-10 14:26
from __future__ import unicode_literals

from django.db import migrations
from django.db.models.expressions import Q, F

from pages.models import Page


def get_page_model_manager(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    return apps.get_model('pages', 'Page').objects.using(db_alias)


def generate_related_model_names(apps, schema_editor):
    PageManager = get_page_model_manager(apps, schema_editor)

    pages = PageManager.filter(Q(type='shopelectro_category') | Q(type='shopelectro_product'))
    pages.update(type=Page.MODEL_TYPE, related_model_name=F('type'))


def restore_pages_relationships(apps, schema_editor):
    PageManager = get_page_model_manager(apps, schema_editor)

    pages = PageManager.exclude(_parent=None)
    pages.update(parent=F('_parent'))


def create_correct_slug_fields_for_custom_pages(apps, schema_editor):
    PageManager = get_page_model_manager(apps, schema_editor)

    slugs_data = {
        'index': '',
        'category_tree': 'catalog',
    }

    for old_slug, new_slug in slugs_data.items():
        page = PageManager.filter(type=Page.CUSTOM_TYPE, slug=old_slug)
        page.update(slug=new_slug)


def delete_redundant_model_page(apps, schema_editor):
    model_pages = get_page_model_manager(apps, schema_editor).filter(type=Page.MODEL_TYPE)
    for page in model_pages:
        related_model = getattr(page, page.related_model_name, None)
        if related_model is None:
            page.delete()


def generate_parents_for_model_pages(apps, schema_editor):
    PageManager = get_page_model_manager(apps, schema_editor)

    category_tree_page = PageManager.filter(type=Page.CUSTOM_TYPE, slug='catalog').first()

    if category_tree_page:
        PageManager.filter(type=Page.MODEL_TYPE, parent=None).update(parent=category_tree_page)


class Migration(migrations.Migration):

    dependencies = [
        ('shopelectro', '0006_pages_db_refactor'),
    ]

    run_before = [
        ('pages', '0006_remove_redundant_fields'),
    ]

    operations = [
        migrations.RunPython(generate_related_model_names),
        migrations.RunPython(restore_pages_relationships),
        migrations.RunPython(create_correct_slug_fields_for_custom_pages),
        migrations.RunPython(delete_redundant_model_page),
        migrations.RunPython(generate_parents_for_model_pages),
    ]
