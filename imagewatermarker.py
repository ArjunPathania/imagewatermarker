import tkinter as tk
from tkinter import filedialog, colorchooser, font, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
from matplotlib import font_manager
import os


class ImageWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermark App")
        self.root.config(padx=50, pady=50)

        # Initialize variables
        self.files = []
        self.preview_file_path = ""
        self.print_font_fill = (0, 0, 0)  # Default black color
        self.print_watermark_font = "Arial"
        self.print_watermark_size = 10
        self.watermark_angle = 0  # New variable for rotation angle
        self.cached_image = None

        # Create UI components
        self.create_widgets()
        self.set_fonts()

    def create_widgets(self):
        """Create all the widgets for the application"""
        self.create_main_frame()
        self.create_canvas()
        self.create_file_frame()
        self.create_watermark_frame()
        self.create_save_frame()

    def create_main_frame(self):
        """Create the main frame container"""
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0)

    def create_canvas(self):
        """Create the preview canvas"""
        self.canvas = tk.Canvas(self.frame, width=700, height=800, bd=1)
        self.canvas.grid(row=0, column=1, rowspan=15, padx=10, sticky=tk.E)
        self.canvas.config(relief="sunken")

        # Default canvas image
        self.background_img = self.canvas.create_image(0, 0, image="")

        # Default text
        self.preview_text = self.canvas.create_text(
            350, 400, text="Preview..", fill="black", font=("Arial", 10)
        )

        # Watermark text positions
        self.watermark_items = {
            "upper_left": self.canvas.create_text(10, 30, text="", font=("Arial", 10), anchor=tk.W, angle=0),
            "top_center": self.canvas.create_text(350, 30, text="", font=("Arial", 10), angle=0),
            "upper_right": self.canvas.create_text(600, 30, text="", font=("Arial", 10), angle=0),
            "mid_left": self.canvas.create_text(10, 400, text="", font=("Arial", 10), angle=0),
            "mid_center": self.canvas.create_text(350, 400, text="", font=("Arial", 10), angle=0),
            "mid_right": self.canvas.create_text(600, 400, text="", font=("Arial", 10), anchor=tk.W, angle=0),
            "bottom_left": self.canvas.create_text(10, 750, text="", font=("Arial", 10), anchor=tk.W, angle=0),
            "bottom_center": self.canvas.create_text(350, 750, text="", font=("Arial", 10), angle=0),
            "bottom_right": self.canvas.create_text(600, 750, text="", font=("Arial", 10), anchor=tk.W, angle=0),
        }

    def create_file_frame(self):
        """Create the file selection frame"""
        file_frame = tk.LabelFrame(self.frame, text="Add File", font=("Arial", 10, "bold"))
        file_frame.grid(row=2, column=0, sticky=tk.W, padx=1)

        # Labels
        tk.Label(file_frame, text="Select a file:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=10)
        tk.Label(file_frame, text='Uploaded files:', font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, padx=10)
        tk.Label(file_frame, text="*.jpg, .jpeg, .png", font=("Arial", 8)).grid(row=0, column=2, sticky=tk.SW)

        # Listbox for files
        self.listbox = tk.Listbox(file_frame, height=5, width=70, exportselection=False)
        self.listbox.grid(row=1, column=1, columnspan=3, padx=13, pady=10, sticky="news")
        self.listbox.bind("<<ListboxSelect>>", self.select_item)

        # Buttons
        tk.Button(file_frame, text="Browse File", font=("Arial", 9), command=self.add_file).grid(
            row=0, column=1, padx=10, pady=5, sticky=tk.EW
        )
        tk.Button(file_frame, text="Clear Files", font=("Arial", 9), command=self.clear_listbox).grid(
            row=0, column=3, padx=10, pady=5, sticky=tk.EW
        )

    def create_watermark_frame(self):
        """Create the watermark customization frame"""
        watermark_frame = tk.LabelFrame(self.frame, text="Add Watermark", font=("Arial", 10, "bold"))
        watermark_frame.grid(row=3, column=0, pady=10, sticky=tk.W)

        # General labels
        tk.Label(watermark_frame, text="Compose watermark:", font=("Arial", 10)).grid(
            row=1, column=0, padx=10, sticky=tk.W
        )
        tk.Label(watermark_frame, text="Placing options:", font=("Arial", 10)).grid(
            row=2, column=0, rowspan=3, sticky=tk.W, padx=10
        )
        tk.Label(watermark_frame, text="Choose font:", font=("Arial", 10)).grid(row=5, column=0, padx=10, sticky=tk.W)
        tk.Label(watermark_frame, text="Choose watermark size:", font=("Arial", 10)).grid(
            row=7, column=0, sticky=tk.W, padx=10
        )
        tk.Label(watermark_frame, text="Choose color:", font=("Arial", 10)).grid(row=8, column=0, sticky=tk.W, padx=10)
        tk.Label(watermark_frame, text="Rotation angle:", font=("Arial", 10)).grid(row=9, column=0, sticky=tk.W, padx=10)

        # Watermark text entry
        self.watermark_text = tk.Entry(watermark_frame, width=60)
        self.watermark_text.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=10)

        # Font listbox
        self.font_listbox = tk.Listbox(
            watermark_frame, selectmode=tk.SINGLE, height=5, width=50, highlightthickness=0, exportselection=False
        )
        self.font_listbox.grid(row=5, column=1, columnspan=3, padx=10, pady=10, sticky="news")
        self.font_listbox.bind("<ButtonRelease-1>", self.select_font)

        # Font size slider
        self.font_size_button = tk.Scale(
            watermark_frame, from_=0, to=50, orient=tk.HORIZONTAL, sliderlength=30, command=self.font_size
        )
        self.font_size_button.grid(row=7, column=1, columnspan=3, sticky=tk.EW, padx=8)

        # Rotation angle slider
        self.rotation_slider = tk.Scale(
            watermark_frame, from_=0, to=360, orient=tk.HORIZONTAL, sliderlength=30, command=self.set_rotation
        )
        self.rotation_slider.grid(row=9, column=1, columnspan=3, sticky=tk.EW, padx=8)

        # Color and reset buttons
        tk.Button(watermark_frame, text='Color', command=self.get_color).grid(row=8, column=1, padx=10, pady=10, sticky=tk.W)
        tk.Button(watermark_frame, text='Reset Watermark', command=self.reset_watermark).grid(
            row=10, column=1, columnspan=3, padx=10, pady=10, sticky=tk.EW
        )

        # Placing options frame
        self.create_placing_options_frame(watermark_frame)

    def set_rotation(self, angle):
        """Set the rotation angle for the watermark"""
        try:
            self.watermark_angle = int(angle)
            self.place_watermark()  # Update the watermark with new rotation
        except ValueError as e:
            self.show_error(f"Invalid rotation angle: {str(e)}")

    def create_placing_options_frame(self, parent):
        """Create the frame for watermark placement options"""
        placing_options_frame = tk.LabelFrame(parent, text="Options", font=("Arial", 10, "bold"))
        placing_options_frame.grid(row=2, column=1, columnspan=3, pady=10, padx=10, sticky=tk.EW)

        # Checkbutton variables
        self.placement_vars = {
            "upper_left": tk.IntVar(),
            "top_center": tk.IntVar(),
            "upper_right": tk.IntVar(),
            "mid_left": tk.IntVar(),
            "mid_center": tk.IntVar(),
            "mid_right": tk.IntVar(),
            "bottom_left": tk.IntVar(),
            "bottom_center": tk.IntVar(),
            "bottom_right": tk.IntVar(),
        }

        # Create checkbuttons
        options = [
            ("Top Left", "upper_left", 2, 1),
            ("Top Center", "top_center", 2, 2),
            ("Top Right", "upper_right", 2, 3),
            ("Center Left", "mid_left", 3, 1),
            ("Center Middle", "mid_center", 3, 2),
            ("Center Right", "mid_right", 3, 3),
            ("Bottom Left", "bottom_left", 4, 1),
            ("Bottom Center", "bottom_center", 4, 2),
            ("Bottom Right", "bottom_right", 4, 3),
        ]

        for text, var_name, row, col in options:
            tk.Checkbutton(
                placing_options_frame,
                text=text,
                onvalue=1,
                offvalue=0,
                variable=self.placement_vars[var_name],
                command=self.place_watermark,
            ).grid(row=row, column=col, sticky=tk.W)

    def create_save_frame(self):
        """Create the save frame"""
        save_frame = tk.LabelFrame(self.frame, text="Save Your Work", font=("Arial", 10, "bold"))
        save_frame.grid(row=4, column=0, pady=10, sticky=tk.W)

        tk.Label(save_frame, text="...here you go!", font=("Arial", 10, "italic", "bold")).grid(row=1, column=0)
        tk.Button(save_frame, text='Save!', font=("Arial", 10), command=self.save).grid(
            row=1, column=1, sticky="news", columnspan=3, pady=10, padx=10
        )

    def set_fonts(self):
        """Populate the font listbox with available fonts"""
        self.font_listbox.delete(0, tk.END)
        for f in font_manager.get_font_names():
            self.font_listbox.insert(tk.END, f)

    def add_file(self):
        """Add a file to the listbox"""
        try:
            file_path = filedialog.askopenfilename(
                initialdir=os.path.join(os.path.dirname(__file__), "assets"),
                title="Select a file!",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
            )
            
            if not file_path:  # User canceled the dialog
                return
                
            if file_path not in self.files:
                self.files.append(file_path)
                self.listbox.insert(tk.END, file_path)
        except Exception as e:
            self.show_error(f"Error adding file: {str(e)}")

    def clear_listbox(self):
        """Clear the listbox and reset file list"""
        self.listbox.delete(0, tk.END)
        self.files.clear()
        self.canvas.itemconfig(self.background_img, anchor=tk.NW, image="")
        self.canvas.itemconfig(self.preview_text, text="Preview..")

    def select_item(self, event):
        """Handle item selection in the listbox"""
        try:
            selection = self.listbox.curselection()
            if not selection:  # No selection
                return
                
            self.preview_file_path = self.listbox.get(selection)
            self.canvas.itemconfig(self.preview_text, text="")
            self.preview_imgs()
        except Exception as e:
            self.show_error(f"Error selecting item: {str(e)}")

    def preview_imgs(self):
        """Preview the selected image"""
        try:
            if not self.preview_file_path:
                return
                
            with Image.open(self.preview_file_path) as image:
                resized_img = image.resize((700, 800), Image.Resampling.LANCZOS)
                selected_image = ImageTk.PhotoImage(resized_img)
                
                self.canvas.itemconfig(self.preview_text, text="")
                self.canvas.itemconfig(self.background_img, anchor=tk.NW, image=selected_image)
                
                # Prevent garbage collection
                self.cached_image = selected_image
        except Exception as e:
            self.show_error(f"Error previewing image: {str(e)}")
            self.canvas.itemconfig(self.preview_text, text="Preview Error")

    def get_color(self):
        """Get color from color chooser"""
        try:
            color = colorchooser.askcolor()
            if color[1] is None:  # User canceled
                return
                
            self.print_font_fill = color[0]
            
            # Update all watermark items with new color
            for item in self.watermark_items.values():
                self.canvas.itemconfig(item, fill=color[1])
        except Exception as e:
            self.show_error(f"Error selecting color: {str(e)}")

    def select_font(self, event):
        """Handle font selection"""
        try:
            selection = self.font_listbox.curselection()
            if not selection:  # No selection
                return
                
            self.print_watermark_font = self.font_listbox.get(selection)
            
            # Update font for all watermark items
            for item in self.watermark_items.values():
                self.canvas.itemconfig(item, font=(self.print_watermark_font, self.print_watermark_size))
        except Exception as e:
            self.show_error(f"Error selecting font: {str(e)}")

    def font_size(self, value):
        """Handle font size change"""
        try:
            self.print_watermark_size = 10 + int(value)
            
            # Update font size for all watermark items
            for item in self.watermark_items.values():
                self.canvas.itemconfig(item, font=(self.print_watermark_font, self.print_watermark_size))
        except ValueError as e:
            self.show_error(f"Invalid font size: {str(e)}")

    def save(self):
        """Save the watermarked image"""
        try:
            if not self.preview_file_path:
                self.show_error("No image selected to save")
                return
                
            if not self.watermark_text.get():
                self.show_error("No watermark text provided")
                return
                
            save_path = filedialog.asksaveasfilename(
                confirmoverwrite=True,
                defaultextension=".png",
                filetypes=[
                    ("JPEG", ".jpg"),
                    ("PNG", ".png"),
                    ("Bitmap", ".bmp"),
                    ("GIF", ".gif")
                ]
            )
            
            if not save_path:  # User canceled
                return
                
            with Image.open(self.preview_file_path).convert("RGB") as base:
                resized_img = base.resize((700, 800), Image.Resampling.LANCZOS)
                font_file = font_manager.findfont(self.print_watermark_font)
                fnt = ImageFont.truetype(font_file, self.print_watermark_size)
                draw = ImageDraw.Draw(resized_img)
                
                # Apply all selected watermarks with rotation
                positions = {
                    "upper_left": (10, 30),
                    "top_center": (350, 30),
                    "upper_right": (600, 30),
                    "mid_left": (10, 400),
                    "mid_center": (350, 400),
                    "mid_right": (600, 400),
                    "bottom_left": (10, 750),
                    "bottom_center": (350, 750),
                    "bottom_right": (600, 750),
                }
                
                for position, var in self.placement_vars.items():
                    if var.get():
                        # Create a temporary image for the text to rotate
                        txt_img = Image.new('RGBA', (500, 100), (255, 255, 255, 0))
                        txt_draw = ImageDraw.Draw(txt_img)
                        txt_draw.text((0, 0), self.watermark_text.get(), font=fnt, fill=self.print_font_fill)
                        
                        # Rotate the text image
                        rotated_txt = txt_img.rotate(self.watermark_angle, expand=1, resample=Image.BICUBIC)
                        
                        # Paste the rotated text onto the main image
                        x, y = positions[position]
                        resized_img.paste(rotated_txt, (x, y), rotated_txt)
                
                resized_img.save(save_path)
        except Exception as e:
            self.show_error(f"Error saving image: {str(e)}")

    def place_watermark(self):
        """Place the watermark on the preview canvas"""
        try:
            self.canvas.itemconfig(self.preview_text, text="")
            text = self.watermark_text.get()
            
            # Update all watermark positions based on checkboxes
            for position, var in self.placement_vars.items():
                if var.get():
                    self.canvas.itemconfig(self.watermark_items[position], text=text, angle=self.watermark_angle)
                else:
                    self.canvas.itemconfig(self.watermark_items[position], text="", angle=0)
        except Exception as e:
            self.show_error(f"Error placing watermark: {str(e)}")

    def reset_watermark(self):
        """Reset all watermark settings"""
        try:
            # Clear all watermark text
            for item in self.watermark_items.values():
                self.canvas.itemconfig(item, text="", fill="#000000", angle=0)
                
            # Reset checkboxes
            for var in self.placement_vars.values():
                var.set(0)
                
            # Reset font settings
            self.font_size_button.set(0)
            self.print_watermark_font = "Arial"
            self.print_watermark_size = 10
            
            # Reset rotation
            self.rotation_slider.set(0)
            self.watermark_angle = 0
            
            # Reset text entry
            self.watermark_text.delete(0, tk.END)
            
            # Update font for all watermark items
            for item in self.watermark_items.values():
                self.canvas.itemconfig(item, font=(self.print_watermark_font, self.print_watermark_size))
        except Exception as e:
            self.show_error(f"Error resetting watermark: {str(e)}")

    def show_error(self, message):
        """Show an error message to the user"""
        messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageWatermarkApp(root)
    root.mainloop()