from dataclasses import dataclass


EMAIL_MIN_LENGTH = 5
NAME_MIN_LENGTH = 2


def validate_email(email: str) -> bool:
   return '@' in email and len(email) >= EMAIL_MIN_LENGTH


def validate_name(name: str) -> bool:
   return len(name) >= NAME_MIN_LENGTH


@dataclass
class User:
   id: int
   email: str
   name: str


class UserRepository:

   def __init__(self, db_connection):
      self.conn = db_connection

   def save(self, user: User):
      cursor = self.conn.cursor()
      cursor.execute(
         "INSERT INTO users(id, email, name) VALUES (?, ?, ?)",
         (user.id, user.email, user.name)
      )
      self.conn.commit()

   def get_all(self):
      cursor = self.conn.cursor()
      return cursor.execute("SELECT id, email, name FROM users").fetchall()


class EmailService:

   def __init__(self, email_sender):
      self.sender = email_sender

   def send_welcome(self, email: str, name: str):
      message = f"Welcome {name}"
      self.sender.send(email, message)


class UserService:

   def __init__(self, repo: UserRepository, email_service: EmailService):
      self.repo = repo
      self.email_service = email_service

   def create_user(self, user_id: int, email: str, name: str):

      if not validate_email(email):
         return False

      if not validate_name(name):
         return False

      user = User(user_id, email, name)

      self.repo.save(user)
      self.email_service.send_welcome(email, name)

      return True

   def list_users(self):
      return self.repo.get_all()