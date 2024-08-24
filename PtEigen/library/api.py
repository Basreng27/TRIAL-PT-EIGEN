from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Member, Book, BorrowRecord
from datetime import timedelta
from .schema import BookSchema, MemberSchema
from typing import List

api = NinjaAPI()

@api.get("books")
def list_books(request):
    books = Book.objects.filter(stock__gt=0)
    
    return list(books.values())

@api.post("book")
def create_book(request, payload:List[BookSchema]):
    books_to_create = [
        Book(
            code=book.code,
            title=book.title,
            author=book.author,
            stock=book.stock
        )
        for book in payload
    ]
    
    created_books = Book.objects.bulk_create(books_to_create)

    return [
        {
            'code': book.code,
            'title': book.title,
            'author': book.author,
            'stock': book.stock,
        }
        for book in created_books
    ]

@api.get("members")
def list_members(request):
    members = Member.objects.all()
    result = []
    
    for member in members:
        borrowed_books = BorrowRecord.objects.filter(member=member, return_date__isnull=True).count()
        result.append({"code": member.code, "name": member.name, "borrowed_books": borrowed_books})
    
    return result

@api.post("member")
def create_member(request, payload:List[MemberSchema]):
    members_to_create = [
        Member(
            code=member.code,
            name=member.name,
            penalty_until=member.penalty_until,
        )
        for member in payload
    ]
    
    created_member = Member.objects.bulk_create(members_to_create)
    
    return [
        {
            "code":member.code,
            "name":member.name,
            "penalty_until":member.penalty_until,
        }
        for member in created_member
    ]

@api.post("borrow")
def borrow_book(request, member_code: str, book_code: str):
    member = get_object_or_404(Member, code=member_code)
    book = get_object_or_404(Book, code=book_code)

    if member.is_penalized():
        return {"error": "Member is penalized and cannot borrow books"}

    if BorrowRecord.objects.filter(member=member, return_date__isnull=True).count() >= 2:
        return {"error": "Member cannot borrow more than 2 books"}

    if BorrowRecord.objects.filter(book=book, return_date__isnull=True).exists():
        return {"error": "Book is already borrowed"}

    if book.stock < 1:
        return {"error": "Book is out of stock"}

    BorrowRecord.objects.create(member=member, book=book)
    book.stock -= 1
    book.save()

    return {"success": f"Book '{book.title}' borrowed successfully"}

@api.post("return")
def return_book(request, member_code: str, book_code: str):
    member = get_object_or_404(Member, code=member_code)
    book = get_object_or_404(Book, code=book_code)

    borrow_record = get_object_or_404(BorrowRecord, member=member, book=book, return_date__isnull=True)
    borrow_record.return_date = timezone.now()
    borrow_record.save()

    if borrow_record.is_overdue():
        member.penalty_until = timezone.now() + timedelta(days=3)
        member.save()

    book.stock += 1
    book.save()

    return {"success": f"Book '{book.title}' returned successfully"}
