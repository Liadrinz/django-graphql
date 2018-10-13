import os
import re
from project.settings import GQL_PAHT_NAME as gqlpn
from project.settings import GQL_URL as gqlurl

def strip_end(iterable):
    temp = iterable
    while temp[-1].replace(' ', '') == '':
        temp.pop()
    return temp

def getlines(filename):
    return ''.join(open(filename, 'r').readlines()).split('\n')

def setlines(filename, iterable):
    f = open(filename, 'w')
    for line in iterable:
        if '#todel' not in line:
            f.write(line + '\n')

def reset_project_pos(iterable):
    for i in range(0, len(project_url)):
        if 'urlpatterns=[' in project_url[i].replace(' ', ''):
            return i

def link(filename, keywords, content, offset, emsg):
    lines = getlines(filename)
    index = 0
    has = False
    for i in range(0, len(lines)):
        if keywords in lines[i]:
            index = i
            has = True
            if keywords == 'import Query':
                lines[i] = 'from data.%s.query import Query'%gqlpn
            break
    if not has:
        print(emsg)
        return False
    if content not in lines:
        lines.insert(index + offset, content)
    lines = strip_end(lines)
    setlines(filename, lines)

def flush(filename, start_str, end_str, mutations):
    lines = getlines(filename)
    s = 0
    e = 0
    for i in range(0, len(lines)):
        if start_str in lines[i]:
            s = i
        elif end_str != None:
            if  end_str.replace(' ', '') in lines[i].replace(' ', ''):
                e = i
                break
        elif end_str == None:
            e = len(lines)
            break
    for i in range(s + 1, e):
        if end_str == None or i != e - 1 or len(mutations) != 0:
            lines[i] = '#todel'
        else:
            lines[i] = '    pass\n'
    lines = strip_end(lines)
    setlines(filename, lines)

if __name__ == '__main__':

    project_url = getlines('./project/urls.py')
    urlpatternsIndex = reset_project_pos(project_url)
    if 'from graphene_django.views import GraphQLView' not in project_url:
        project_url.insert(urlpatternsIndex, 'from graphene_django.views import GraphQLView')
    urlpatternsIndex = reset_project_pos(project_url)
    if 'from project.schema import schema' not in project_url:
        project_url.insert(urlpatternsIndex, 'from project.schema import schema')
    urlpatternsIndex = reset_project_pos(project_url)
    if """    path('%s', GraphQLView.as_view(graphiql=True, schema=schema)),"""%gqlurl not in project_url:
        project_url.insert(urlpatternsIndex + 1, """    path('%s/', GraphQLView.as_view(graphiql=True, schema=schema)),"""%gqlpn)
    project_url = strip_end(project_url)
    setlines('./project/urls.py', project_url)

    mutations = []
    for item in os.walk('./data/%s/mutations/'%gqlpn):
        mutations = item[2]

    flush('./data/schema.py', 'import Query', None, mutations)
    flush('./project/schema.py', 'class Mutations', 'schema = graphene.Schema(query=Query, mutation=Mutations)', mutations)
    link('./data/schema.py', 'import Query', '', 1, 'No valid Query found!')
    for mutation in mutations:

        class_name = ''
        with open('./data/%s/mutations/'%gqlpn + mutation, 'r') as f:
            for line in f.readlines():
                for name in re.findall(r'class .*?\s*\(', line):
                    name = name.replace(' ', '')
                    class_name = name[5:-1]

        if class_name == '':
            print('No valid mutation class in some mutation file!')
            exit()

        mutation = mutation.replace('.py', '')
        origin_mutation = mutation
        camel = ''
        if re.match(r'(.*[a-z][A-Z].*)+', mutation):
            camel = mutation[0].upper() + mutation[1:]
            for peak in re.findall(r'[a-z][A-Z]', mutation):
                mutation = mutation.replace(peak, peak[0] + '_' + peak[1].lower())
            mutation = mutation[0].lower() + mutation[1:]
        else:
            for part in mutation.split('_'):
                part = part[0].upper() + part[1:]
                camel += part

        data_schema_import = 'from data.%s.mutations.%s import %s'%(gqlpn, origin_mutation, class_name)
        project_schema_register = '%s = data.schema.%s.Field()'%(mutation, class_name)

        link('./data/schema.py', 'import Query', data_schema_import, 1, 'No valid Query found!')
        link('./project/schema.py', 'class Mutations', '    ' + project_schema_register, 1, 'No class Mutations found or legally named')