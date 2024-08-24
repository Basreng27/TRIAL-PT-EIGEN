from django.test import TestCase
from django.utils import timezone
from .models import Member, Book, BorrowRecord
from datetime import timedelta

class MemberTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(code='M001', name='Angga')

    def test_is_penalized(self):
        self.member.penalty_until = timezone.now() + timedelta(days=1)
        self.member.save()
        self.assertTrue(self.member.is_penalized())

class BookTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(code='JK-45', title='Harry Potter', author='J.K Rowling', stock=1)

    def test_book_str(self):
        self.assertEqual(str(self.book), 'Harry Potter')

class BorrowRecordTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(code='M001', name='Angga')
        self.book = Book.objects.create(code='JK-45', title='Harry Potter', author='J.K Rowling', stock=1)
        self.borrow_record = BorrowRecord.objects.create(member=self.member, book=self.book)

    def test_is_overdue(self):
        self.borrow_record.return_date = self.borrow_record.borrow_date + timedelta(days=8)
        self.borrow_record.save()
        self.assertTrue(self.borrow_record.is_overdue())

    def test_book_stock_decrease_on_borrow(self):
        initial_stock = self.book.stock
        self.borrow_record.book.stock -= 1
        self.borrow_record.book.save()
        self.assertEqual(self.book.stock, initial_stock - 1)
