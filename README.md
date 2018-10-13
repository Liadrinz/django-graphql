# django-graphql

Use for Django GraphQL Server development

## Why

#### Modular development with GraphQL

  In some simple Django GraphQL projects, all the query and mutation operations are in the same module called schema. But if your project needs large amount of GraphQL operations, it's a good choice to separate query and mutation, even each mutation. (The function for mutation operation are often much larger than that for query, so mutations are more necessary to be separated than queries)<br><br>
   The GraphQL part is separated into the following pieces:
   
```shell
mutations/  # contains all mutation operations
inputs.py   # contains all formatted inputs for mutation operations
query.py    # contains all query operations
types.py    # contains all GraphQL Types

```
<br>

  How do the project know you've created a new mutation operation?
  
```shell
python3 link.py # just run link.py, this will apply all mutations to schema.py
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
from django.db import models

class Author(models.Model):
  name = models.CharField(max_length=1000)
  nationality = models.CharField(max_length=1000)

class Book(models.Model):
  name = models.CharField(max_length=1000)
  author = models.ForeignKey(Author, related_name='books')
 
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

Add attrs for class Query as query operations

##### e.g.
```python
# ./data/graphql/query.py
import graphene
from data.graphql.types import AuthorType, BookType
from data.models import Author, Book

class Query(object):
  
  all_authors = graphene.List(AuthorType)
  all_books = graphene.List(BookType)
  
  def resolve_all_authors(self, info, **kwargs):
    return Author.objects.all()
  
  def resolve_all_books(self, info, **kwargs):
    return Book.objects.all()

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
from data.graphql.input import AuthorCreationInput

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
from data.graphql.input import BookCreationInput

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

#### 6. Link your mutations to the project

This step will apply your mutations to the project by import it to ./project/schema.py

```shell
python3 link.py
```
