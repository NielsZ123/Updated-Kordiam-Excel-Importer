import pandas as pd
from datetime import datetime, timedelta

# Create sample data that matches the successful Kordiam API structure
# Only includes fields that were actually used in the working payload
data = {
    # Basic element fields (only the ones used in successful payload)
    'Title': [
        'Breaking: Local Election Results',
        'Weather Update: Storm Warning',
        'Sports: Championship Game Tonight'
    ],
    'Slug': [
        'local-election-results-2024',
        'storm-warning-march-15',
        'championship-game-tonight'
    ],
    'Element Status': [2, 2, 2],
    
    # Task fields (only the ones used in successful payload)
    'Task Status ID': [2, 2, 2],
    'Task Format ID': [18, 18, 18],
    'Assigned User ID': [10126151, 10126151, 10126151],
    'Task Deadline': [
        datetime(2024, 3, 15, 16, 0),
        datetime(2024, 3, 15, 8, 0),
        datetime(2024, 3, 15, 22, 0)
    ],
    'Confirmation Status': [-2, -2, -2],
    
    # Publication fields (only the ones used in successful payload)
    'Platform ID': [9413781, 9413781, 9413781],
    'Publication Date': [
        datetime(2024, 3, 15, 18, 0),
        datetime(2024, 3, 15, 6, 0),
        datetime(2024, 3, 15, 22, 0)  # Changed from 2024-03-16 to 2024-03-15
    ],
    'Task Assignments': ['true', 'true', 'true'],
    
    # Group fields
    'Group IDs': [9455121, 9455121, 9455121],
    
    # Event fields (optional - only if you need events)
    'Event Start Date': [
        datetime(2024, 3, 15, 19, 0),
        None,
        datetime(2024, 3, 15, 19, 30)
    ],
    'Event Start Time': [
        datetime(2024, 3, 15, 19, 0),
        None,
        datetime(2024, 3, 15, 19, 30)
    ],
    'Event End Date': [
        datetime(2024, 3, 15, 21, 0),
        None,
        datetime(2024, 3, 15, 21, 30)  # Adjusted to match the new publication date
    ],
    'Event End Time': [
        datetime(2024, 3, 15, 21, 0),
        None,
        datetime(2024, 3, 15, 22, 0)
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel with proper formatting
with pd.ExcelWriter('kordiam_example_clean.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Elements', index=False)
    
    # Get the workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Elements']
    
    # Auto-adjust column widths
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width

print("Kordiam clean example Excel file 'kordiam_example_clean.xlsx' created successfully!")
print("\nThis file contains only the essential fields that were successfully tested:")
print("- Basic element fields (title, slug, elementStatus)")
print("- Task information (status, format, user, deadline, confirmationStatus)")
print("- Publication details (platform, publication date, assignments)")
print("- Group information")
print("- Event information (optional)")
print("\nUse this as a template for your own data import.")
print("\nTo use this with the clean mapping:")
print("python kordiam_excel_importer.py kordiam_example_clean.xlsx --mapping kordiam_mapping_clean.json --dry-run") 