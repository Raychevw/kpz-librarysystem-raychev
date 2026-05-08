import sqlite3
import hashlib


def validate_email(email: str) -> bool:
   return '@' in email


class UserRepository:

   def __init__(self, db_connection):
      self.conn = db_connection

   def save(self, user):
      cursor = self.conn.cursor()
      cursor.execute(
            "INSERT INTO users(email, password, name) VALUES (?, ?, ?)",
            (user["email"], user["password"], user["name"])
      )
      self.conn.commit()

   def update(self, user_id, data):
      cursor = self.conn.cursor()
      cursor.execute(
            "UPDATE users SET email=?, name=? WHERE id=?",
            (data["email"], data["name"], user_id)
      )
      self.conn.commit()

   def delete(self, user_id):
      cursor = self.conn.cursor()
      cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
      self.conn.commit()

   def get_all(self) -> list:
      cursor = self.conn.cursor()
      return cursor.execute("SELECT * FROM users").fetchall()


class EmailService:

   def send_welcome(self, user):
      import smtplib

      server = smtplib.SMTP('smtp.gmail.com', 587)

      message = f"Subject: Welcome!\n\nHello {user['name']}"

      server.sendmail(
            'from@gmail.com',
            user["email"],
            message
      )

      server.quit()


class ReportService:

   def generate_new_user_report(self, user):
      with open("report.txt", "a") as f:
            f.write(f"New user: {user['email']}\n")


class UserService:

   def __init__(self, repo: UserRepository, email_svc: EmailService, report_svc: ReportService):
      self.repo = repo
      self.email_svc = email_svc
      self.report_svc = report_svc

   def register(self, email, password, name):

      if not validate_email(email):
            return False

      if len(password) < 8:
            return False

      hashed_password = hashlib.sha256(password.encode()).hexdigest()

      user = {
            "email": email,
            "password": hashed_password,
            "name": name
      }

      self.repo.save(user)
      self.email_svc.send_welcome(user)
      self.report_svc.generate_new_user_report(user)

      return True

   def update(self, user_id, data):

      if "email" in data and not validate_email(data["email"]):
            return False

      self.repo.update(user_id, data)
      return True

   def delete(self, user_id):
      self.repo.delete(user_id)

   def get_all_users(self):
      return self.repo.get_all()


connection = sqlite3.connect("users.db")

repo = UserRepository(connection)
email_service = EmailService()
report_service = ReportService()

user_service = UserService(repo, email_service, report_service)