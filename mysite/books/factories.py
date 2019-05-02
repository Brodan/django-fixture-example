import factory

from books.models import Author, Book, Publisher


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Faker('company')


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker('first_name_female')
    last_name = factory.Faker('last_name_female')


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    publisher = factory.SubFactory(PublisherFactory)
    publication_date = factory.Faker('date_time')
    isbn = factory.Faker('isbn13', separator="-")

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for author in extracted:
                self.authors.add(author)
