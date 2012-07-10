# -*- coding: utf-8 -*-
# Copyright (c) 2012 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
from optparse import make_option

from django.core.management.base import BaseCommand
from django_detect_cyclic.apps_dependence import create_graph_apps_dependence
from django_detect_cyclic.exceptions import InvalidOptions
from django_detect_cyclic.utils import SCOPE_GLOBAL


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
            make_option('-i', '--include-apps', dest='include_apps',
                    help='Only use these applications to the graph (separated by commas)'),
            make_option('-e', '--exclude-apps', dest='exclude_apps',
                    help='Exclude these apps to the graph (separated by commas)'),
            make_option('-f', '--file-name', dest='file_name', default='detect.svg',
                    help='Exclude these apps to the graph (separated by commas)'),
            make_option('-p', '--exclude-packages', dest='exclude_packages',
                    help='Exclude the next packages. For example migrations,templatetags (separated by commas)'),
            make_option('-r', '--remove-isolate-nodes', dest='remove_isolate_nodes',  action="store_true",
                    help='Remove the isolate nodes'),
            make_option('-k', '--remove-sink-nodes', dest='remove_sink_nodes',  action="store_true",
                    help='Remove the sink nodes'),
            make_option('-a', '--remove-source-nodes', dest='remove_source_nodes',  action="store_true",
                    help='Remove the source nodes'),
            make_option('-o', '--only-cyclic', dest='only_cyclic',  action="store_true",
                    help='Remove the nodes without cyclic'),
            make_option('-s', '--show-modules', dest='show_modules',  action="store_true",
                    help='The nodes now are the modules (by default are the applications)'),
            make_option('-g', '--scope-global', dest='scope_global',  action="store_true",
                    help='The imports into the functions are ignored'),
            make_option('-c', '--force-colors', dest='force_colors',  action="store_true",
                    help='You can use this option when the format are not svg'),
            make_option('-d', '--dotted-scope-local', dest='dotted_scope_local',  action="store_true",
                    help='The imports into the functions are printing with dotted line'),
    )

    def handle(self, *args, **options):
        include_apps = exclude_apps = exclude_packages = None
        if options['include_apps']:
            include_apps = options['include_apps'].split(',')
        if options['exclude_apps']:
            exclude_apps = options['exclude_apps'].split(',')
        if options['exclude_packages']:
            exclude_packages = options['exclude_packages'].split(',')
        verbosity = int(options['verbosity'])
        remove_isolate_nodes = options['remove_isolate_nodes']
        remove_sink_nodes = options['remove_sink_nodes']
        remove_source_nodes = options['remove_source_nodes']
        only_cyclic = options['only_cyclic']
        if only_cyclic:
            remove_isolate_nodes = True
        show_modules = options['show_modules']
        file_name = options['file_name']
        force_colors = options['force_colors']
        dotted_scope_local = options['dotted_scope_local']
        scope = options['scope_global'] and SCOPE_GLOBAL or None
        if dotted_scope_local and scope == SCOPE_GLOBAL:
            raise InvalidOptions("The dotted-scope-local and scope-global are incompatibles")
        create_graph_apps_dependence(file_name=file_name,
                                     include_apps=include_apps,
                                     exclude_apps=exclude_apps,
                                     exclude_packages=exclude_packages,
                                     verbosity=verbosity,
                                     show_modules=show_modules,
                                     remove_isolate_nodes=remove_isolate_nodes,
                                     remove_sink_nodes=remove_sink_nodes,
                                     remove_source_nodes=remove_source_nodes,
                                     only_cyclic=only_cyclic,
                                     scope=scope,
                                     force_colors=force_colors,
                                     dotted_scope_local=dotted_scope_local)
