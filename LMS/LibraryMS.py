import tkinter as tk
from tkinter import messagebox
import datetime


class LMS:
    def __init__(self, list_of_books, library_name):
        self.list_of_books = list_of_books
        self.library_name = library_name
        self.books_dict = {}
        Id = 101
        
        with open(self.list_of_books, "r") as bk:
            content = bk.readlines()
        for line in content:
            self.books_dict[str(Id)] = {
                "books_title": line.strip(),
                "lender_name": "",
                "Issue_date": "",
                "Status": "Available"
            }
            Id += 1

    def display_books(self):
        display_text = "Books ID\tTitle\t\t\tStatus\n" + "-" * 50 + "\n"
        for key, value in self.books_dict.items():
            display_text += f"{key}\t{value['books_title'][:20]:<20}\t[{value['Status']}]\n"
        return display_text

    def issue_books(self, books_id, lender_name):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if books_id in self.books_dict:
            if self.books_dict[books_id]["Status"] != "Available":
                return f"This book is already issued to {self.books_dict[books_id]['lender_name']} on {self.books_dict[books_id]['Issue_date']}."
            else:
                self.books_dict[books_id]["lender_name"] = lender_name
                self.books_dict[books_id]["Issue_date"] = current_date
                self.books_dict[books_id]["Status"] = "Issued"
                return "Book issued successfully!"
        else:
            return "Book ID not found!"

    def add_books(self, new_book):
        new_id = str(int(max(self.books_dict)) + 1)
        self.books_dict[new_id] = {
            "books_title": new_book,
            "lender_name": "",
            "Issue_date": "",
            "Status": "Available"
        }
        with open(self.list_of_books, "a") as bk:
            bk.write(f"{new_book}\n")
        return f"The book '{new_book}' has been added successfully!"

    def return_books(self, books_id):
        if books_id in self.books_dict:
            if self.books_dict[books_id]["Status"] == "Available":
                return "This book is already available in the library."
            else:
                self.books_dict[books_id]["lender_name"] = ""
                self.books_dict[books_id]["Issue_date"] = ""
                self.books_dict[books_id]["Status"] = "Available"
                return "Book returned successfully!"
        else:
            return "Book ID not found!"


class LMSApp:
    def __init__(self, root, lms):
        self.root = root
        self.lms = lms
        self.root.title(f"{self.lms.library_name} - Library Management System")
        self.root.geometry("600x500")
        self.root.config(bg="#F5F5DC")
        
        self.main_label = tk.Label(self.root, text=f"Welcome to {self.lms.library_name}", font=("Arial", 20, "bold"), bg="#F5F5DC", fg="#4B0082")
        self.main_label.pack(pady=20)

        self.display_button = tk.Button(self.root, text="Display Books", font=("Arial", 14), command=self.display_books, bg="#4B0082", fg="white")
        self.display_button.pack(pady=10)

        self.issue_button = tk.Button(self.root, text="Issue Book", font=("Arial", 14), command=self.issue_book, bg="#4B0082", fg="white")
        self.issue_button.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Book", font=("Arial", 14), command=self.add_book, bg="#4B0082", fg="white")
        self.add_button.pack(pady=10)

        self.return_button = tk.Button(self.root, text="Return Book", font=("Arial", 14), command=self.return_book, bg="#4B0082", fg="white")
        self.return_button.pack(pady=10)

    def display_books(self):
        books_list = self.lms.display_books()
        messagebox.showinfo("List of Books", books_list)

    def issue_book(self):
        def process_issue():
            book_id = book_id_entry.get()
            name = lender_name_entry.get()
            if book_id and name:
                result = self.lms.issue_books(book_id, name)
                messagebox.showinfo("Issue Book", result)
                issue_window.destroy()
            else:
                messagebox.showerror("Error", "Both fields are required!")

        issue_window = tk.Toplevel(self.root)
        issue_window.title("Issue Book")
        issue_window.geometry("300x200")

        tk.Label(issue_window, text="Book ID:").pack(pady=5)
        book_id_entry = tk.Entry(issue_window)
        book_id_entry.pack(pady=5)

        tk.Label(issue_window, text="Your Name:").pack(pady=5)
        lender_name_entry = tk.Entry(issue_window)
        lender_name_entry.pack(pady=5)

        tk.Button(issue_window, text="Issue", command=process_issue).pack(pady=10)

    def add_book(self):
        def process_add():
            new_book = new_book_entry.get()
            if new_book.strip():
                result = self.lms.add_books(new_book.strip())
                messagebox.showinfo("Add Book", result)
                add_window.destroy()
            else:
                messagebox.showerror("Error", "Book title cannot be empty!")

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Book")
        add_window.geometry("300x150")

        tk.Label(add_window, text="Book Title:").pack(pady=5)
        new_book_entry = tk.Entry(add_window)
        new_book_entry.pack(pady=5)

        tk.Button(add_window, text="Add", command=process_add).pack(pady=10)

    def return_book(self):
        def process_return():
            book_id = book_id_entry.get()
            if book_id:
                result = self.lms.return_books(book_id)
                messagebox.showinfo("Return Book", result)
                return_window.destroy()
            else:
                messagebox.showerror("Error", "Book ID is required!")

        return_window = tk.Toplevel(self.root)
        return_window.title("Return Book")
        return_window.geometry("300x150")

        tk.Label(return_window, text="Book ID:").pack(pady=5)
        book_id_entry = tk.Entry(return_window)
        book_id_entry.pack(pady=5)

        tk.Button(return_window, text="Return", command=process_return).pack(pady=10)


if __name__ == "__main__":
    lms = LMS("list_of_books.txt", "Python's Library")
    root = tk.Tk()
    app = LMSApp(root, lms)
    root.mainloop()
