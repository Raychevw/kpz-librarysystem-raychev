CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "email" varchar(255) UNIQUE NOT NULL,
  "password_hash" varchar(255) NOT NULL,
  "first_name" varchar(100),
  "last_name" varchar(100),
  "role" varchar(20) DEFAULT 'USER',
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "books" (
  "id" serial PRIMARY KEY,
  "title" varchar(255) NOT NULL,
  "author" varchar(150) NOT NULL,
  "isbn" varchar(20) UNIQUE,
  "description" text,
  "available" boolean DEFAULT true,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "borrowings" (
  "id" serial PRIMARY KEY,
  "book_id" int,
  "user_id" int,
  "borrow_date" date DEFAULT (now()),
  "due_date" date,
  "return_date" date,
  "status" varchar(20) DEFAULT 'ACTIVE'
);

CREATE TABLE "reviews" (
  "id" serial PRIMARY KEY,
  "book_id" int,
  "user_id" int,
  "rating" int,
  "comment" text,
  "created_at" timestamp DEFAULT (now())
);

COMMENT ON COLUMN "reviews"."rating" IS '1-5';

ALTER TABLE "borrowings" ADD FOREIGN KEY ("book_id") REFERENCES "books" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "borrowings" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reviews" ADD FOREIGN KEY ("book_id") REFERENCES "books" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reviews" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

-- Indexes

CREATE UNIQUE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn);

CREATE INDEX IF NOT EXISTS idx_books_author ON books(author);

CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);

CREATE INDEX IF NOT EXISTS idx_books_available ON books(available);

CREATE INDEX IF NOT EXISTS idx_borrowings_user_id ON borrowings(user_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_book_id ON borrowings(book_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_status ON borrowings(status);
CREATE INDEX IF NOT EXISTS idx_borrowings_due_date ON borrowings(due_date);

CREATE INDEX IF NOT EXISTS idx_reviews_book_id ON reviews(book_id);
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);

CREATE INDEX IF NOT EXISTS idx_borrowings_user_book ON borrowings(user_id, book_id);