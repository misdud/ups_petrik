You can apply a Style to your ttk.widget

first you need to create an Instance of the ttk Style Class e.g. like this:

style = ttk.Style()

and then you have multiple options:

you can either apply a set style to all widgets of that type, like that:

style.configure('Treeview.Heading', foreground = 'red')

or you can create your own 'sub-Styles' to apply that manually:

style.configure('custom.TLabel', foreground = 'red')
style.configure('other.TLabel', foreground = 'yellow')

which you than apply when creating the widget like:

myLabel = ttk.Label(parent, text = 'I have a custom Style', style = 'custom.TLabel')
label2 = ttk.Label(parent, text = 'I have a different Style', style = 'other.TLabel')
