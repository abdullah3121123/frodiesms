import os
import time
import tkinter as tk
from tkinter import filedialog


# Klasör seçimi
def select_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select a folder")


# Dosya seçimi
def select_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])


# Küçük/büyük harf farkı gözetmeyen arama fonksiyonu
def case_insensitive_search(term, line):
    return term.lower() in line.lower()


# Klasörde arama ve sonuçları kaydetme
def search_and_save(folder_path, search_term):
    search_term = search_term.replace('/', '_')  # Geçersiz karakterleri düzenleme
    result_file_path = os.path.join(os.getcwd(), f"{search_term.replace(' ', '_')}.txt")
    found_lines = 0
    start_time = time.time()

    try:
        with open(result_file_path, 'w', encoding='utf-8') as result_file:
            for root_dir, _, files in os.walk(folder_path):
                for file_name in files:
                    if file_name.endswith('.txt'):
                        file_path = os.path.join(root_dir, file_name)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                for line in file:
                                    if case_insensitive_search(search_term, line):
                                        result_file.write(line)
                                        found_lines += 1
                        except UnicodeDecodeError:
                            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                                for line in file:
                                    if case_insensitive_search(search_term, line):
                                        result_file.write(line)
                                        found_lines += 1

        elapsed_time = time.time() - start_time
        print(f"Search results saved to '{result_file_path}'")
        print(f"Total lines found: {found_lines}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
    except Exception as e:
        print(f"An error occurred: {e}")


# Mail:Pass temizleyici
def clear_and_format(file_path):
    formatted_lines = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                cleaned_line = line.strip()
                if '://' in cleaned_line:
                    cleaned_line = cleaned_line.split(' ')[-1]

                parts = cleaned_line.split(':')
                if len(parts) >= 2:
                    username = parts[-2].strip()
                    password = parts[-1].strip()
                    if username and password and '@' in username:
                        formatted_lines.add(f"{username}:{password}")

        output_file_path = os.path.splitext(file_path)[0] + '_formatted.txt'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for formatted_line in formatted_lines:
                output_file.write(formatted_line + '\n')

        print(f"Cleaned data saved to '{output_file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")


# Full Cleaner (Mail:Pass formatlayıcı, kullanıcıya özel bir düzenleme eklenebilir)
def clear_and_format_user_pass(file_path):
    formatted_lines = set()
    try:
        with open(file_path, 'r', encoding='latin-1') as file:
            for line in file:
                cleaned_line = line.strip()
                if '://' in cleaned_line:
                    cleaned_line = cleaned_line.split(' ')[-1]
                cleaned_line = cleaned_line.replace('|', ':')
                parts = cleaned_line.split(':')
                if len(parts) >= 2:
                    username = parts[-2].strip()
                    password = parts[-1].strip()
                    if username and password:
                        formatted_lines.add(f"{username}:{password}")

        output_file_path = os.path.splitext(file_path)[0] + '_formatted_user_pass.txt'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for formatted_line in formatted_lines:
                output_file.write(formatted_line + '\n')

        print(f"Cleaned data saved to '{output_file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")


# Bir dosya içeriğine göre arama yapma
def search_from_file(search_terms_file, folder_path):
    start_time = time.time()
    output_folder = os.path.join(os.getcwd(), "SearchResults")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        with open(search_terms_file, 'r', encoding='latin-1') as search_file:
            terms = search_file.read().splitlines()

        for term in terms:
            term = term.strip()
            if term:
                term_result_file_path = os.path.join(output_folder, f'{term}.txt')
                with open(term_result_file_path, 'w', encoding='latin-1') as term_result_file:
                    for root_dir, _, files in os.walk(folder_path):
                        for file_name in files:
                            if file_name.endswith('.txt'):
                                file_path = os.path.join(root_dir, file_name)
                                try:
                                    with open(file_path, 'r', encoding='latin-1') as file:
                                        for line in file:
                                            if term in line:
                                                term_result_file.write(line)
                                except Exception as e:
                                    print(f"Error in file {file_name}: {e}")

        elapsed_time = time.time() - start_time
        print(f"Search completed in {elapsed_time:.2f} seconds")
    except Exception as e:
        print(f"An error occurred: {e}")


# Kullanıcıların terminalde renkli metin görmesi için
def print_colored_text(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")


def main_menu():
    folder_path = None

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_colored_text("""
██╗     ██╗ ██████╗ ██╗  ██╗████████╗███╗   ██╗██╗███╗   ██╗ ██████╗ 
██║     ██║██╔════╝ ██║  ██║╚══██╔══╝████╗  ██║██║████╗  ██║██╔════╝ 
██║     ██║██║  ███╗███████║   ██║   ██╔██╗ ██║██║██╔██╗ ██║██║  ███╗
██║     ██║██║   ██║██╔══██║   ██║   ██║╚██╗██║██║██║╚██╗██║██║   ██║
███████╗██║╚██████╔╝██║  ██║   ██║   ██║ ╚████║██║██║ ╚████║╚██████╔╝
╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝  v1.0
                                                                                        
┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│   [1] DATABASE LOAD             │   [2] SEARCHER                  │   [3] QUIT                      │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│   [4] MAIL:PASS CLEANER         │   [5] FULL CLEANER              │   [6] ALL SEARCHER              │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│   [7] RAR FULL SEARCHER         │   [8] RAR TARGET SEARCHER       │   [9] QUIT                      │
└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
""", "36")  # Cyan color (changed from blue)

        choice = input("\n⚡ Choose an option (1-9): ")

        # Rest of the function remains the same

        choice = input("Choose an option (1-12): ")

        if choice == '1':
            folder_path = select_folder()
            if folder_path:
                print(f"'{folder_path}' folder selected.")
            else:
                print("No folder selected.")
        elif choice == '2':
            if not folder_path:
                print("You need to select a folder first.")
            else:
                search_term = input("Enter the search term: ")
                if search_term.strip():
                    search_and_save(folder_path, search_term)
                else:
                    print("Search term cannot be empty.")
        elif choice == '3':
            print("Exiting.")
            break
        elif choice == '4':
            file_path = select_file()
            if file_path:
                clear_and_format(file_path)
            else:
                print("No file selected.")
        elif choice == '5':
            file_path = select_file()
            if file_path:
                clear_and_format_user_pass(file_path)
            else:
                print("No file selected.")
        elif choice == '6':
            if not folder_path:
                print("You need to select a folder first.")
            else:
                file_path = select_file()
                if file_path:
                    search_from_file(file_path, folder_path)
                else:
                    print("No file selected.")
        else:
            print_colored_text("Invalid choice, please try again.", "31")  # Red color code
        time.sleep(2)


if __name__ == "__main__":
    main_menu()