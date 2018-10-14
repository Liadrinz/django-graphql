# django-graphql

Use for Django GraphQL Server development

## Why

#### Modular development with GraphQL

  In some simple Django GraphQL projects, all the query and mutation operations are in the same module called schema. But if your project needs large amount of GraphQL operations, it's a good choice to separate each query and mutation<br><br>
   The GraphQL part is separated into the following pieces:
   
```shell
mutations/  # contains all mutation operations
queries/    # contains all query operations
inputs.py   # contains all formatted inputs for mutation operations
types.py    # contains all GraphQL Types

```
<br>

  How do the project know you've created a new mutation operation?
  
```shell
python3 link.py # just run link.py, this will apply all queries and mutations to schema.py
```
<br><br>
## How to start<br>

#### 0. Install requirements

```shell
pip3 install -r requirements.txt
```
<br>

#### 1. Build your django models in ./data/models.py

##### e.g.
```python
# ./data/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    # Create your user profile model here.
    pass
    
class Author(models.Model):
  name = models.CharField(max_length=1000)
  nationality = models.CharField(max_length=1000)

class Book(models.Model):
  name = models.CharField(max_length=1000)
  author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
 
```
<br>

#### 2. Create GraphQL Types for your models

##### e.g.
```python
# ./data/graphql/types.py
from graphene_django.types import DjangoObjectType
from data.models import Author, Book

class AuthorType(DjangoObjectType):
  class Meta:
    model = Author


class BookType(DjangoObjectType):
  class Meta:
    model = Book
    
```
<br>

#### 3. Create query operations

Create files in ./data/graphql/queries/ for query classes

```shell
cd ./data/graphql/queries/
touch query_author.py
touch query_book.py
```

Create query class in the new files

##### e.g.
```python
# ./data/graphql/queries/query_author.py
import graphene
from data.models import Author
from data.graphql.types import AuthorType

class QueryAuthor(object):
  
  # operations
  all_authors = graphene.List(AuthorType)   # return all authors
  get_authors_by_name = graphene.List(AuthorType, name=graphene.String())   # return authors whose name is equal to the "name" argument
  get_author_by_id = graphene.Field(AuthorType, id=graphene.Int())  # return the author whose id is equal to the "id" argument
  
  # methods must be named "resolve_" + operation_name
  def resolve_all_authors(self, info, **kwargs):
    return Author.objects.all()
  
  def resolve_get_authors_by_name(self, info, **kwargs):
    author_name = kwargs['name']
    return Author.objects.filter(name=author_name)
  
  def resolve_get_author_by_id(self, info, **kwargs):
    author_id = kwargs['id']
    return Author.objects.get(pk=author_id)
```

```python
# ./data/graphql/queries/query_book.py
import graphene
from data.models import Book
from data.graphql.types import BookType

class QueryBook(object):
  
  # operations
  all_books = graphene.List(BookType)   # return all books
  get_books_by_name = graphene.List(BookType, name=graphene.String())   # return books whose name is equal to the "name" argument
  get_book_by_id = graphene.Field(BookType, id=graphene.Int())  # return the book whose id is equal to the "id" argument
  
  # methods must be named "resolve_" + operation_name
  def resolve_all_books(self, info, **kwargs):
    return Book.objects.all()
  
  def resolve_get_books_by_name(self, info, **kwargs):
    book_name = kwargs['name']
    return Book.objects.filter(name=book_name)
  
  def resolve_get_book_by_id(self, info, **kwargs):
    book_id = kwargs['id']
    return Book.objects.get(pk=book_id)
```

<br>

#### 4. Create mutation inputs

##### e.g.
```python
# ./data/graphql/inputs.py
import graphene

class AuthorCreationInput(graphene.InputObjectType):
  name = graphene.String(required=True)
  nationality = graphene.String(required=True)
  

class BookCreationInput(graphene.InputObjectType):
  name = graphene.String(required=True)
  author_id = graphene.Int(required=True)
```
<br>

#### 5. Create mutation operations

Create files in ./data/graphql/mutations/ for mutation classes

```shell
cd ./data/graphql/mutations/
touch create_author.py
touch create_book.py
```

Create mutation class in the new files

##### e.g.
```python
# ./data/graphql/mutations/create_author.py
import graphene
from data.models import Author
from data.graphql.types import AuthorType
from data.graphql.inputs import AuthorCreationInput

class CreateAuthor(graphene.Mutation):

  class Arguments:
    author_data = AuthorCreationInput(required=True)
  
  ok = graphene.Boolean()
  author = graphene.Field(AuthorType)
  
  def mutate(self, info, author_data):
    name = author_data['name']
    nationality = author_data['nationality']
    author = Author.objects.create(name=name, nationality=nationality)
    return CreateAuthor(ok=True, author=author)
  
```

```python
# ./data/graphql/mutations/create_book.py
import graphene
from data.models import Book
from data.graphql.types import BookType
from data.graphql.inputs import BookCreationInput

class CreateBook(graphene.Mutation):

  class Arguments:
    book_data = BookCreationInput(required=True)
  
  ok = graphene.Boolean()
  book = graphene.Field(BookType)
  
  def mutate(self, info, book_data):
    name = book_data['name']
    author_id = book_data['author_id']
    book = Book.objects.create(name=name, author_id=author_id)
    return CreateBook(ok=True, book=book)
    
```
<br>

#### 6. Link and Migrate

link.py will apply your queries and mutations to the project before migrate your models to database

```shell
python3 link.py
python3 manage.py makemigrations
python3 manage.py migrate
```

link.py help to merge queries and mutations into schema.py. See the following gif <br> 
(On windows it's python while on linux it's python3): <br>

![link.py](https://github.com/Liadrinz/django-graphql/blob/master/link.gif)

<br>

#### 7. Run

```shell
python3 manage.py runserver 0:8000
```

Then, visit http://localhost:8000/graphql/  and enjoy your GraphQL requests! <br><br>


Demo: <br>

![demo](https://github.com/Liadrinz/django-graphql/blob/master/run.gif)


