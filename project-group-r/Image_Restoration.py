import cv2
import tkinter
import tkinter.filedialog as tkFileDialog
import PIL.Image, PIL.ImageTk
import numpy as np
import Noise_Generator as ng
import Find_Filter as ff

def main():

    path = tkFileDialog.askopenfilename()
    input_image = cv2.imread(path, 0)

    #create window for images
    window = tkinter.Toplevel()
    window.title("Image Restoration")
    window.configure(background="white")
    width, height = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (width, height))

    #Frames to house each aspect of the window
    top_frame = tkinter.Frame(window, width=0, height=0, pady=0)
    top_frame.configure(background="white")
    input_frame = tkinter.Frame(window, width=width, height=height, pady=0)
    input_frame.configure(background="white")
    image_frame = tkinter.Frame(window, width=width, height=height, pady=0)
    image_frame.configure(background="white")
    image_frame_2 = tkinter.Frame(window, width=width, height=height, pady=0)
    image_frame_2.configure(background="white")
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)
    top_frame.grid(row=0, sticky="n")
    input_frame.grid(row=2, sticky="n")
    image_frame.grid(row=3, sticky="n")
    image_frame_2.grid(row=4, sticky="s")

    #Drop down menu for different noise types to add to the image
    noise_type = tkinter.StringVar(top_frame)
    noise_type.set("Periodic Noise")  # default value
    noise_menu = tkinter.OptionMenu(top_frame, noise_type, "Periodic Noise", "Gaussian Noise", "Salt and Pepper Noise", "Salt Noise", "Pepper Noise")

    #Drop down menu for the different filter types (Starts assuming that the default noise type is periodic)
    filter_type = tkinter.StringVar(top_frame)
    filter_type.set("Ideal Band Reject")  # default value
    filter_menu = tkinter.OptionMenu(top_frame, filter_type, "Ideal Band Reject", "Ideal Band Pass",
                                     "Gaussian Band Reject", "Gaussian Band Pass", "Butterworth Band Reject",
                                     "Butterworth Band Pass", "Ideal Notch Reject", "Ideal Notch Pass",
                                     "Gaussian Notch Reject", "Gaussian Notch Pass", "Butterworth Notch Reject",
                                     "Butterworth Notch Pass")

    # Text boxes for parameters of blurring images. Need to find out what parameters we need
    # I renamed width and window, because these variable names were already used!

    cutoff_label = tkinter.Label(input_frame, text='Cutoff:')
    cutoff_label.grid(row=2, column=0)
    cutoff_label.configure(background="white")
    cutoff_var = tkinter.IntVar()
    cutoff_var.set(17)  # changed this from 25 to 17
    cutoff = tkinter.Entry(input_frame, text=cutoff_var)
    cutoff.grid(row=2, column=1)

    width_label = tkinter.Label(input_frame, text='Width:')
    width_label.grid(row=2, column=2)
    width_label.configure(background="white")
    width_var = tkinter.IntVar()
    width_var.set(5)  # changed this from 10 to 5
    width_entry = tkinter.Entry(input_frame, text=width_var)
    width_entry.grid(row=2, column=3)

    order_label = tkinter.Label(input_frame, text='Order:')
    order_label.grid(row=2, column=4)
    order_label.configure(background="white")
    order_var = tkinter.IntVar()
    order_var.set(2)
    order = tkinter.Entry(input_frame, text=order_var)
    order.grid(row=2, column=5)

    notchx_label = tkinter.Label(input_frame, text='Notch_X:')
    notchx_label.grid(row=2, column=6)
    notchx_label.configure(background="white")
    notchx_var = tkinter.IntVar()
    notchx_var.set(17)
    notchx = tkinter.Entry(input_frame, text=notchx_var)
    notchx.grid(row=2, column=7)

    notchy_label = tkinter.Label(input_frame, text='Notch_Y:')
    notchy_label.grid(row=2, column=8)
    notchy_label.configure(background="white")
    notchy_var = tkinter.IntVar()
    notchy_var.set(0)
    notchy = tkinter.Entry(input_frame, text=notchy_var)
    notchy.grid(row=2, column=9)

    window_label = tkinter.Label(input_frame, text='Window Size:')
    window_label.grid(row=2, column=10)
    window_label.configure(background="white")
    window_var = tkinter.IntVar()
    window_var.set(3)
    window_entry = tkinter.Entry(input_frame, text=window_var)
    window_entry.grid(row=2, column=11)

    order.configure(state='disabled')
    notchx.configure(state='disabled')
    notchy.configure(state='disabled')
    window_entry.configure(state='disabled')

    # function that rewrites what is on the filter types drop down menu based on the type of noise added to the image

    def update_filter_dropdown(*args):
        # Get the menu portion of the drop down menu (Option menus are built from menu options and commands)
        m = filter_menu.children['menu']
        # Clear all the items in the drop down menu
        m.delete(0, 'end')
        # if we are working with periodic noise
        if noise_type.get() == "Periodic Noise":
            # Set the default filter to "Ideal Band Reject"
            filter_type.set("Ideal Band Reject")
            # All the filters that deal with periodic noise
            new_values = "Ideal Band Reject, Ideal Band Pass, Gaussian Band Reject, Gaussian Band Pass," \
                         " Butterworth Band Reject, Butterworth Band Pass, Ideal Notch Reject, Ideal Notch Pass, " \
                         "Gaussian Notch Reject, Gaussian Notch Pass, Butterworth Notch Reject, " \
                         "Butterworth Notch Pass".split(', ')
            # Add all the filters that deal with periodic noise to the drop down menu
            for val in new_values:
                m.add_command(label=val, command=lambda v=filter_type, l=val: v.set(l))
        else:
            # Set the default filter to "Arithmetic Mean Filter"
            filter_type.set("Arithmetic Mean Filter")
            # All the filters that deal with statistical noise
            new_values = "Arithmetic Mean Filter, Geometric Mean Filter, Harmonic Mean Filter, Max Filter," \
                         " Min Filter, Median Filter, Midpoint Filter, Alpha Trimmed Mean Filter," \
                         " Adaptive Filter".split(', ')
            # Add all the filters that deal with statistical noise to the drop down menu
            for val in new_values:
                m.add_command(label=val, command=lambda v=filter_type, l=val: v.set(l))

    # this function updates which entry fields are valid, so we can only enter into the ones needed for current filter
    def update_input_fields(*args):
        # disable all states, so we can just enable only the ones we need
        cutoff.configure(state='disabled')
        width_entry.configure(state='disabled')
        order.configure(state='disabled')
        notchx.configure(state='disabled')
        notchy.configure(state='disabled')
        window_entry.configure(state='disabled')

        # activate entry for band filters
        if filter_type.get() in "Ideal Band Reject, Ideal Band Pass, Gaussian Band Reject, Gaussian Band Pass," \
                                " Butterworth Band Reject, Butterworth Band Pass".split(', '):
            cutoff.configure(state='normal')
            width_entry.configure(state='normal')

            if filter_type.get() in "Butterworth Band Reject, Butterworth Band Pass".split(', '):
                order.configure(state='normal')

        # activate entry for notch filters
        if filter_type.get() in "Ideal Notch Reject, Ideal Notch Pass, Gaussian Notch Reject, Gaussian Notch Pass," \
                                " Butterworth Notch Reject, Butterworth Notch Pass".split(', '):
            cutoff.configure(state='normal')
            notchx.configure(state='normal')
            notchy.configure(state='normal')

            if filter_type.get() in "Butterworth Notch Reject, Butterworth Notch Pass".split(', '):
                order.configure(state='normal')

        # activate entry for windowed filters
        if filter_type.get() in "Arithmetic Mean Filter, Geometric Mean Filter, Harmonic Mean Filter, Max Filter," \
                                " Min Filter, Median Filter, Midpoint Filter, Alpha Trimmed Mean Filter," \
                                " Adaptive Filter".split(', '):
            window_entry.configure(state='normal')

    # Function that repaints the images once a button is pressed
    def onButton(*args):
        # global variable photo
        global photo
        global dft_photo
        # add noise to image
        noise_image = noise_obj.Identify_Noise_Type(noise_type.get(), input_image)
        # filter the image
        filter_image = filter_obj.Identify_Filter_Type(filter_type.get(), noise_image, int(cutoff_var.get()), int(width_var.get()), int(order_var.get()), int(notchx_var.get()), int(notchy_var.get()), int(window_var.get()))
        # Add all 3 images together as one image (Noise image, Filter Image, Target Image)
        numpy_horizontal = np.hstack((noise_image, filter_image, input_image))
        numpy_horizontal_dft = np.hstack((np.ones(input_image.shape[:2]) * 255, np.log(np.abs(np.fft.fftshift(np.fft.fft2(noise_image)))) * 10, np.ones(input_image.shape[:2]) * 255))
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(numpy_horizontal))
        dft_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(numpy_horizontal_dft))
        # Add a PhotoImage to the Canvas
        canvas.itemconfigure(image_on_canvas, image=photo)
        dft_canvas.itemconfigure(dft_on_canvas, image=dft_photo)
    # Trace the selection of the drop down menu
    filter_type.trace('w', update_input_fields)  # track when filter type is updated, update valid entry fields
    noise_type.trace('w', update_filter_dropdown)  # track when noise type is updated, update filter list

    # add noise to image
    noise_obj = ng.noise()
    noise_image = noise_obj.Identify_Noise_Type(noise_type.get(), input_image)

    # filter the image
    filter_obj = ff.filters()
    filter_image = filter_obj.Identify_Filter_Type(filter_type.get(), noise_image, int(cutoff_var.get()), int(width_var.get()), int(order_var.get()), int(notchx_var.get()), int(notchy_var.get()), int(window_var.get()))

    # Add all 3 images together as one image (Noise image, Filter Image, Target Image)
    numpy_horizontal = np.hstack((noise_image, filter_image, input_image))
    numpy_horizontal_dft = np.hstack((np.ones(input_image.shape[:2])*255, np.log(np.abs(np.fft.fftshift(np.fft.fft2(noise_image))))*10, np.ones(input_image.shape[:2])*255))

    # Get the images dimensions
    height, width = numpy_horizontal.shape[:2]

    # Create a canvas that can fit the above image
    canvas = tkinter.Canvas(image_frame, width=width, height=height)
    dft_canvas = tkinter.Canvas(image_frame_2, width=width, height=height)

    noise_label = tkinter.Label(top_frame, text='Noise Type:')
    filter_label = tkinter.Label(top_frame, text='Filter Type:')

    # Add the noise_menu drop down menu to the window
    noise_label.grid(row=0, column=0)
    noise_label.configure(background="white")
    noise_menu.grid(row=0, column=1)
    # Add the filter_menu drop down menu to the window
    filter_label.grid(row=0, column=2)
    filter_label.configure(background="white")
    filter_menu.grid(row=0, column=3)
    # Add the canvas to the window
    canvas.grid(row=0, column=0)
    canvas.configure(background="white")
    dft_canvas.grid(row=2, column=0)
    dft_canvas.configure(background="white")

    # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(numpy_horizontal))
    dft_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(numpy_horizontal_dft))

    # Add a PhotoImage to the Canvas
    image_on_canvas = canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    dft_on_canvas = dft_canvas.create_image(0, 0, image=dft_photo, anchor=tkinter.NW)
    # Create button that runs the onButton command (The command that repaints the images based on input from drop down menus)
    button = tkinter.Button(top_frame, text="    Filter    ", command=onButton)
    button.grid(row=1, column=2)

    # Run the window loop
    window.mainloop()


if __name__ == "__main__":
    main()
    # Command: python Image_Restoration.py
