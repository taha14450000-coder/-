import tkinter as tk
import tkinter.font as tkFont
import math
import re # برای پردازش sqrt

# --- تنظیمات ظاهری ---
BACKGROUND_COLOR = "#f0f0f0"  # رنگ پس‌زمینه کلی: خاکستری روشن
ENTRY_RESULT_COLOR = "#f1c40f" # زرد برای نمایشگر (همانند قبل)
ENTRY_TEXT_COLOR = "#000000"   # متن نمایشگر: سیاه

BUTTON_COLOR_OPERATOR = "#ffffff" # سفید برای دکمه های عددی و عملیاتی پایه
BUTTON_COLOR_OPERATOR_ACTIVE = "#e0e0e0" # رنگ فعال تر برای دکمه های عملیاتی

BUTTON_COLOR_MAIN_OPS = "#ff9500"  # نارنجی تیره برای عملیات اصلی (+, -, *, /)
BUTTON_COLOR_EQUALS = "#00c853"    # سبز برای دکمه مساوی
BUTTON_COLOR_CLEAR = "#ff4444"    # قرمز برای دکمه پاک کردن
BUTTON_COLOR_RADICAL = "#ff9500" # نارنجی تیره برای رادیکال

TEXT_COLOR_DARK = "#212121"      # متن تیره برای دکمه های روشن
TEXT_COLOR_LIGHT = "#ffffff"     # متن روشن برای دکمه های رنگی

SECONDARY_BG_COLOR = "#cccccc" # رنگ پس‌زمینه برای پنجره جدید (کمی تیره تر از اصلی)
SIGNATURE_TEXT_COLOR = "#212121" # متن امضا: تیره

FONT_FAMILY = "Arial"

# --- توابع ماشین حساب ---
expression = ""

def press(num):
    global expression
    # اگر آخرین ورودی یک خطا بود، آن را پاک کن
    if equation.get() == " error " or equation.get() == " invalid input ":
        expression = ""
        equation.set("")

    expression = expression + str(num)
    equation.set(expression)

def equalpress():
    try:
        global expression
        # اگر عبارت شامل رادیکال باشد، باید محاسبه شود
        if 'sqrt(' in expression:
            # استفاده از re برای پیدا کردن و جایگزینی تمام موارد sqrt()
            # این بخش برای اطمینان از پردازش صحیح عبارت‌های پیچیده‌تر است
            processed_expression = expression
            while 'sqrt(' in processed_expression:
                start = processed_expression.find('sqrt(')
                end = start + len('sqrt(')
                paren_count = 1
                for i in range(end, len(processed_expression)):
                    if processed_expression[i] == '(':
                        paren_count += 1
                    elif processed_expression[i] == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            num_str = processed_expression[end:i]
                            try:
                                num = float(num_str)
                                radical_result = math.sqrt(num)
                                processed_expression = processed_expression[:start] + str(radical_result) + processed_expression[i+1:]
                            except ValueError:
                                equation.set(" invalid input ")
                                expression = ""
                                return
                            break
                    if i == len(processed_expression) - 1: # اگر پرانتز بسته نشد
                        equation.set(" invalid input ")
                        expression = ""
                        return

            expression = processed_expression # به‌روزرسانی عبارت اصلی با نتایج جذر

        total = str(eval(expression))
        equation.set(total)
        expression = ""
    except ZeroDivisionError:
        equation.set(" Cannot divide by zero ")
        expression = ""
    except Exception as e:
        print(f"Error during evaluation: {e}") # برای دیباگ
        equation.set(" error ")
        expression = ""

def clear():
    global expression
    expression = ""
    equation.set("")

def add_radical():
    global expression
    if equation.get() == " error " or equation.get() == " invalid input ":
        expression = ""
        equation.set("")
    expression += "sqrt("
    equation.set(expression)
    
def add_parenthesis(type):
    global expression
    if equation.get() == " error " or equation.get() == " invalid input ":
        expression = ""
        equation.set("")
    expression += type
    equation.set(expression)

def percentage():
    global expression
    try:
        # محاسبه درصد به صورت 100/number یا number/100 بسته به موقعیت
        # این بخش ممکن است نیاز به منطق پیچیده‌تری داشته باشد
        # در حال حاضر، فرض می‌کنیم کاربر عدد را وارد کرده و می‌خواهد درصد بگیرد
        if expression:
            num = float(expression)
            expression = str(num / 100)
            equation.set(expression)
    except Exception as e:
        print(f"Error in percentage: {e}")
        equation.set(" error ")
        expression = ""

# --- تابع برای نمایش پنجره امضا ---
def show_signature_window():
    signature_win = tk.Toplevel(root)
    signature_win.title("About")
    signature_win.geometry("450x200")
    signature_win.configure(background=SECONDARY_BG_COLOR)
    signature_win.transient(root)
    signature_win.grab_set()

    signature_font_very_large = tkFont.Font(family=FONT_FAMILY, size=24, weight="bold")

    signature_label = tk.Label(signature_win, text="Sakhte Shode Tavsot Taha", font=signature_font_very_large, bg=SECONDARY_BG_COLOR, fg=SIGNATURE_TEXT_COLOR)
    signature_label.pack(expand=True, pady=30)

    close_button = tk.Button(signature_win, text="OK", command=signature_win.destroy, font=default_font, bg=BUTTON_COLOR_OPERATOR, fg=TEXT_COLOR_DARK, width=10, relief=tk.RAISED)
    close_button.pack(pady=10)

    signature_win.update_idletasks()
    main_window_x = root.winfo_x()
    main_window_y = root.winfo_y()
    main_window_width = root.winfo_width()
    main_window_height = root.winfo_height()
    new_window_width = signature_win.winfo_width()
    new_window_height = signature_win.winfo_height()
    x = main_window_x + (main_window_width // 2) - (new_window_width // 2)
    y = main_window_y + (main_window_height // 2) - (new_window_height // 2)
    signature_win.geometry(f'+{x}+{y}')

    root.wait_window(signature_win)

# --- ساخت پنجره اصلی ---
root = tk.Tk()
root.configure(background=BACKGROUND_COLOR)
root.title("Pro Calculator")
root.geometry("400x550") # کمی بزرگتر برای جای دادن دکمه ها

# --- فونت سفارشی ---
default_font = tkFont.Font(family=FONT_FAMILY, size=12)
button_font = tkFont.Font(family=FONT_FAMILY, size=18, weight="bold")
entry_font = tkFont.Font(family=FONT_FAMILY, size=28) # فونت بزرگتر برای نمایشگر

# --- نمایشگر ماشین حساب ---
equation = tk.StringVar()
# تنظیمات نمایشگر با رنگ زرد و متن سیاه
expression_field = tk.Entry(root, textvariable=equation, font=entry_font, bd=10, insertwidth=2, width=14, borderwidth=4, justify='right', bg=ENTRY_RESULT_COLOR, fg=ENTRY_TEXT_COLOR, relief=tk.FLAT)
expression_field.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=15, sticky="nsew")

# --- پیکربندی گرید برای مقیاس‌پذیری ---
for i in range(6): # افزایش تعداد ردیف ها
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(0, weight=2) # ردیف نمایشگر وزن بیشتری دارد

# --- تعریف دکمه ها و چیدمان آنها ---
# دکمه های ردیف بالا
tk.Button(root, text='C', fg=TEXT_COLOR_LIGHT, bg=BUTTON_COLOR_CLEAR, font=button_font, height=2, width=4, command=clear, relief=tk.RAISED).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='()', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: add_parenthesis('()'), relief=tk.RAISED).grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='%', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=percentage, relief=tk.RAISED).grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='÷', fg=TEXT_COLOR_LIGHT, bg=BUTTON_COLOR_MAIN_OPS, font=button_font, height=2, width=4, command=lambda: press('/'), relief=tk.RAISED).grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

# دکمه های ردیف دوم (اعداد 7, 8, 9 و ضرب)
tk.Button(root, text='7', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('7'), relief=tk.RAISED).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='8', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('8'), relief=tk.RAISED).grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='9', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('9'), relief=tk.RAISED).grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='×', fg=TEXT_COLOR_LIGHT, bg=BUTTON_COLOR_MAIN_OPS, font=button_font, height=2, width=4, command=lambda: press('*'), relief=tk.RAISED).grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

# دکمه های ردیف سوم (اعداد 4, 5, 6 و تفریق)
tk.Button(root, text='4', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('4'), relief=tk.RAISED).grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='5', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('5'), relief=tk.RAISED).grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='6', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('6'), relief=tk.RAISED).grid(row=3, column=2, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='-', fg=TEXT_COLOR_LIGHT, bg=BUTTON_COLOR_MAIN_OPS, font=button_font, height=2, width=4, command=lambda: press('-'), relief=tk.RAISED).grid(row=3, column=3, padx=5, pady=5, sticky="nsew")

# دکمه های ردیف چهارم (اعداد 1, 2, 3 و جمع)
tk.Button(root, text='1', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('1'), relief=tk.RAISED).grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='2', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('2'), relief=tk.RAISED).grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='3', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('3'), relief=tk.RAISED).grid(row=4, column=2, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='+', fg=TEXT_COLOR_LIGHT, bg=BUTTON_COLOR_MAIN_OPS, font=button_font, height=2, width=4, command=lambda: press('+'), relief=tk.RAISED).grid(row=4, column=3, padx=5, pady=5, sticky="nsew")

# دکمه های ردیف پنجم (0, . , = و √ )
tk.Button(root, text='0', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('0'), relief=tk.RAISED).grid(row=5, column=0, columnspan=1, padx=5, pady=5, sticky="nsew")
tk.Button(root, text='.', fg=TEXT_COLOR_DARK, bg=BUTTON_COLOR_OPERATOR, font=button_font, height=2, width=4, command=lambda: press('.'), relief=tk.RAISED).grid(row=5, column=1, padx=5, pady=5, sticky="nsew")
# دکمه √ (رادیکال)
tk.Button(root, text="√", fg=TEXT_COLOR_LIGHT, bg=BUTTON_COLOR_RADICAL, font=button_font, height=2, width=4, command=add_radical, relief=tk.RAISED).grid(row=5, column=2, padx=5, pady=5, sticky="nsew")
# دکمه مساوی (=) که بزرگتر است
tk.Button(root, text='=', fg=TEXT_COLOR_LIGHT, bg=BUTTON_COLOR_EQUALS, font=button_font, height=2, width=4, command=equalpress, relief=tk.RAISED).grid(row=5, column=3, padx=5, pady=5, sticky="nsew")


# --- منوی همبرگری ---
menubar = tk.Menu(root, bg=BACKGROUND_COLOR, fg=TEXT_COLOR_DARK, font=default_font, relief=tk.RAISED)
root.config(menu=menubar)

# منوی کشویی
hamburger_menu = tk.Menu(menubar, tearoff=0, bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR_DARK)
menubar.add_cascade(label="☰", menu=hamburger_menu)

# آیتم منو برای امضا
hamburger_menu.add_command(label="Saznde-Taha", command=show_signature_window, font=default_font)

# --- اجرای برنامه ---
root.mainloop()
