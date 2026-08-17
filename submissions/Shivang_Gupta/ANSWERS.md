# Week 2 assignment — answers

**Seat:** seat-09

## Part 1 — order book

- Total orders in the book: 100
- Orders with status 'ready': 29
- Most ordered drink: latte (26 times)

## What surprised me

The /book endpoint is paginated — it only returns 50 orders per call even though `total` says 100, so book_report.py has to page through it with `offset` until it's collected all of them.
