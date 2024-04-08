from pandas import read_csv, to_datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_patients_number():
    """Return the number of patients had their last cholestrol checkup more than 3.5 
    years ago from the date: 12 Nov 2023."""

    file_path = 'PreprocessingDataset4.csv'
    #read the the csv file
    df = read_csv(file_path)
    #start date mentioned in the question
    from_date_str = '12 Nov 2023'
    from_date_object = datetime.strptime(from_date_str, '%d %b %Y')
    #When to pickup start from
    start_picking = from_date_object - relativedelta(years=3, months=6)
    #filter out the data which is required and then count the number of patients
    filtered_patients = df[to_datetime(df['LastCholCheckupDate']) < start_picking]

    return len(filtered_patients)

print("--------------Task 2-----------")
message = "Patients had their last cholestrol checkup more than 3.5 years ago from the date: 12 Nov 2023"
print(f"{message} - {get_patients_number()}")
print("--------------End Task 2-----------")
