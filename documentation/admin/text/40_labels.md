
# Labels

To add or update labels, go to the Django default admin page at `<your url>/admin` (e.g. `https://www.example.com/admin`). Under the "Labelling" section, select "Labels." Here, you will see an overview of all existing labels, were you can add or modify labels as needed (see Figure \ref{fig:labels}).


![Admin view for labels \label{fig:labels}](resources/images/labels.png)


## Adding Labels

To add a new label, click the gray "ADD LABEL" button in the top right corner. This will take you to a screen where you can specify the label name, a shortcut key, and optionally, a color and order.

Within Tweeti, there are two types of buttons related to labels: "menu" buttons and "label" buttons. A "menu" button is a label without a parent label (and it will contain "label" buttons that use this label as their parent). A "label" button, on the other hand, can either have a parent label (appearing within a menu) or no parent label (appearing as a standalone "label" button).

As shown in Figure \ref{fig:labels}, you can place a label within a menu by selecting a "parent" label. This makes the label a submenu item under a menu button (see also Figure \ref{fig:menushow} for how users will see this). If no parent label is selected, the label will appear as a standalone label button without a menu (see Figure \ref{fig:labelsuser}).


### Add Label Button

When a user clicks on a label button, the label is added to the message (Figure \ref{fig:labelsuser}).

![This is how a user experiances a "label" button press, a label is shown under the messages. \label{fig:labelsuser}](resources/images/labelsuser.png)


### Add Menu Button

When a user clicks on a menu button, a menu appears with the associated label buttons (Figure \ref{fig:menushow}).

![This is how the user experiances an "parent" button, it shows a menu of "label" buttons when pressed. \label{fig:menushow}](resources/images/menushow.png)


### Example 1

If you want to create only three standalone labels—"Label A," "Label B," and "Label C"—without using menu buttons, create three labels without a parent label (order, color, and shortcut are optional) (see Figure \ref{fig:labelex1}).

![Example of a "label" button definition. \label{fig:labelex1}](resources/images/labelex1.png){ width=250px }


### Example 2

If you want to create a menu button called "Menu" that contains three labels—"Label A," "Label B," and "Label C"—first create the menu button (a label without a parent, named "Menu"; order, color, and shortcut are optional), see Figure \ref{fig:labelex2}. Then, create the three labels with the "menu" button as their parent label (order, color, and shortcut are optional, see Figure \ref{fig:labelex3}.

![Example of a "menu" button, containing label A, label B, and label C. \label{fig:labelex2}](resources/images/labelex2.png){ width=250px }

![Exmaple of a "label" button with a parent "menu" button. \label{fig:labelex3}](resources/images/labelex3.png){ width=250px }


## Modifying Labels

You can modify labels by selecting "Labels" on the admin page and clicking on the name of the label you want to edit.

When you click on the label name, the same input fields you used when creating the label will appear, allowing you to make changes.

At the bottom, you will see two non-editable fields, "Created at" and "Updated at," which show the date and time the label was created and last modified, respectively.



\newpage{}
