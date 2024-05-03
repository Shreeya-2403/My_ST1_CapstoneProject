import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import tkinter as tk
from tkinter import messagebox

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('Medical_insurance.csv')

# Preprocess the data
# For simplicity, let's assume you only want to use 'children', 'smoker', 'region', and 'age' as predictors
X = df[['children', 'smoker', 'region', 'age']]
y = df['charges']

# Convert categorical variables into dummy/indicator variables
X = pd.get_dummies(X, drop_first=True)

# Train the KNN model
knn_model = KNeighborsRegressor(n_neighbors=5)
knn_model.fit(X, y)


# Create a simple GUI using tkinter
def predict_insurance_charges():
    # Get the input values from the entry widgets
    children = int(children_entry.get())
    smoker = int(smoker_entry.get())
    age = int(age_entry.get())

    # Get the state of region checkboxes
    northeast = int(northeast_var.get())
    northwest = int(northwest_var.get())
    southeast = int(southeast_var.get())
    southwest = int(southwest_var.get())

    # Create a dictionary with all possible region values
    region_values = {
        'region_northeast': northeast,
        'region_northwest': northwest,
        'region_southeast': southeast,
        'region_southwest': southwest
    }

    # Convert the input values into a format suitable for making predictions
    input_data = pd.DataFrame({
        'children': [children],
        'smoker_yes': [smoker],
        'age': [age],
        **region_values  # Include all region values
    })

    # Reorder columns to match the order used during training
    input_data = input_data.reindex(columns=X.columns, fill_value=0)

    # Make a prediction
    predicted_charge = knn_model.predict(input_data)

    # Display the predicted insurance charge
    messagebox.showinfo("Prediction", f"The predicted insurance charge is: ${predicted_charge[0]:.2f}")


# Create the main window
window = tk.Tk()
window.title("Insurance Charges Prediction")

# Create labels and entry widgets for input variables
children_label = tk.Label(window, text="Children:")
children_label.grid(row=0, column=0)
children_entry = tk.Entry(window)
children_entry.grid(row=0, column=1)

smoker_label = tk.Label(window, text="Smoker (0 for No, 1 for Yes):")
smoker_label.grid(row=1, column=0)
smoker_entry = tk.Entry(window)
smoker_entry.grid(row=1, column=1)

region_label = tk.Label(window, text="Region:")
region_label.grid(row=2, column=0)
northeast_var = tk.IntVar()
northwest_var = tk.IntVar()
southeast_var = tk.IntVar()
southwest_var = tk.IntVar()
northeast_checkbox = tk.Checkbutton(window, text="Northeast", variable=northeast_var)
northeast_checkbox.grid(row=2, column=1)
northwest_checkbox = tk.Checkbutton(window, text="Northwest", variable=northwest_var)
northwest_checkbox.grid(row=2, column=2)
southeast_checkbox = tk.Checkbutton(window, text="Southeast", variable=southeast_var)
southeast_checkbox.grid(row=2, column=3)
southwest_checkbox = tk.Checkbutton(window, text="Southwest", variable=southwest_var)
southwest_checkbox.grid(row=2, column=4)

age_label = tk.Label(window, text="Age:")
age_label.grid(row=3, column=0)
age_entry = tk.Entry(window)
age_entry.grid(row=3, column=1)

# Create a button to trigger the prediction
predict_button = tk.Button(window, text="Predict Insurance Charges", command=predict_insurance_charges)
predict_button.grid(row=4, column=0, columnspan=2)

# Run the GUI application
window.mainloop()