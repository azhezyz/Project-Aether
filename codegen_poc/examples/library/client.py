from src_gen import Library, Book, Member, Loan, Author, Publisher, Copy, Librarian, Fine

lib = Library()
member = Member()

# Create book graph
book = Book()
pub = Publisher()
a1, a2 = Author(), Author()
copy1, copy2 = Copy(), Copy()

book.publishedby_publisher = pub
book.add_writtenby_author(a1)
book.add_writtenby_author(a2)

copy1.iscopyof_book = book
copy2.iscopyof_book = book

lib.add_stores_copy(copy1)
lib.add_stores_copy(copy2)

# Loan
loan = Loan()
loan.borrower__member = member
loan.forceps_copy = copy1
member.add_hasloan_loan(loan)

# Optional fine
fine = Fine()
loan.maycreate_fine = fine

print("Library copies:", len(lib.stores_copy))
print("Member loans:", len(member.hasloan_loan))
print("Book authors:", len(book.writtenby_author))
