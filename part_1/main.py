from mongoengine import connect

from models import Author, Quote

connect(db='web14', host="mongodb+srv://boridka:654123@cluster0.8nz8els.mongodb.net/?retryWrites=true&w=majority")


def find_all_quotes_author(author):
    result = []
    author = Author.objects(fullname=author).first()

    if author:
        quotes = Quote.objects(author=author.id).all()
        for quote in quotes:
            result.append(quote.quote)

        return result
    

def find_all_quotes_for_tag(tag):
    result = []
    quotes = Quote.objects(tags=tag)

    for quote in quotes:
        result.append(quote.quote)

    return result


def find_all_quotes_for_tags(tags):
    tags = tags.split(',')
    list_tags =[]
    result = []
    for tag in tags:
        list_tags.append(tag)
    print(list_tags)

    quotes = Quote.objects(tags__in=list_tags)
    for quote in quotes:
        result.append(quote.quote)

    return result


def main():
    while True:
        action = input('Enter command: ')

        if action.startswith('exit'):
            break
        elif action.startswith('name:'):
            parse = action.split(':')
            print(find_all_quotes_author(parse[1].strip()))
        elif action.startswith('tag:'):
            parse = action.split(':')
            print(find_all_quotes_for_tag(parse[1].strip()))
        elif action.startswith('tags:'):
            parse = action.split(':')
            print(find_all_quotes_for_tags(parse[1].strip()))
        else:
            print("Wrong command")


if __name__ == "__main__":
    main()