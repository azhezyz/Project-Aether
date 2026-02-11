from src_gen import Library, Book, Member, Loan, Author, Publisher, Copy, Librarian, Fine

lib = Library()
member = Member()

# Create book graph
book = Book()
pub = Publisher()
a1, a2 = Author(), Author()
copy1, copy2 = Copy(), Copy()

book.publishedby__publisher = pub
book.add_writtenby__author(a1)
book.add_writtenby__author(a2)

copy1.iscopyof__book = book
copy2.iscopyof__book = book

lib.add_stores__copy(copy1)
lib.add_stores__copy(copy2)

# Loan
loan = Loan()
loan.borrower__member = member
loan.forcopy__copy = copy1
member.add_hasloan__loan(loan)

# Optional fine
fine = Fine()
loan.maycreate__fine = fine

print("Library copies:", len(lib.stores__copy))
print("Member loans:", len(member.hasloan__loan))
print("Book authors:", len(book.writtenby__author))
