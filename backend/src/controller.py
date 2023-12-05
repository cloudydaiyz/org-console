# Controller that interfaces between program data and external APIs
import event_data

from datetime import datetime
from google_data import get_spreadsheet_range, update_spreadsheet_range, clear_spreadsheet_range, get_files_in_folder
from settings import settings, gid_settings, range_settings

log_sheet_id = gid_settings["membership_log_id"]
event_drive_id = gid_settings["root_drive_id"]

# 1. Update the membership logs
def update_membership_logs():
    event_data.reset_event_data()
    
    try:
        pull_existing_data()
        pull_event_data()
        push_event_data()
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
    return True

# Retrieve existing member information from the membership logs
def pull_existing_data():
    global log_sheet_id

    # Populate the event types
    vals = get_spreadsheet_range(
        log_sheet_id, 
        range_settings["point_calcs"])
    
    if vals != None:
        vals_width = len(vals[0])
        for row in vals:
            print(f"Event Type Added: {row[0]} ({int(row[vals_width - 1])} pts)")
            event_data.add_event_type(row[0], int(row[vals_width - 1]))
        
    # (DEPRECATED): Populate the existing events
    # vals = get_spreadsheet_range(
    #     log_sheet_id, 
    #     range_settings["event_log"])
    
    # if vals != None:
    #     for row in vals:
    #         try:
    #             parsed_date = datetime.strptime(row[3], "%m/%d/%Y").date()
    #             event_data.add_event(row[1], parsed_date, row[2], row[4])
    #         except:
    #             pass

    # Populate the existing members with the events they attended
    vals = get_spreadsheet_range(
        log_sheet_id,
        range_settings["membership_log"]
    )

    if vals != None:
        for row in vals:
            event_data.add_member(row[0], row[1], row[2], row[3], row[4], row[5])
    print(event_data.all_members)

# Retrieve event data from the sign in folder
def pull_event_data():
    global event_drive_id

    # Go through each folder in the root drive folder
    files = get_files_in_folder(event_drive_id)
    if files == None:
        return
    
    for file in files:
        print(file)
        file_name = file["name"]
        file_id = file["id"]

        # If the name of the event type folder is valid, go through the folder
        if event_data.get_event_type(file_name) == None:
            print(f"Invalid event type: {file_name}")
        else:
            sheets = get_files_in_folder(file_id)

            # Get event information from sheets in folder
            if sheets != None:
                for sheet in sheets:
                    populate_event(sheet["name"], sheet["id"], file_name)

# Retrieve all of the event info from the spreadsheet
def populate_event(event_sheet_name, event_sheet_id, event_type):
    # Create event information
    split_index = event_sheet_name.index(" ")
    date_str = event_sheet_name[:split_index]
    event_date = datetime.strptime(date_str, "%m/%d/%Y").date()
    event_name = event_sheet_name[split_index+1:]

    event = event_data.add_event(event_name, event_date, event_type, event_sheet_id)

    # Get members from the sheet and add them to the event
    vals = get_spreadsheet_range(
        event_sheet_id, 
        range_settings["sign_in_info"])
    
    if vals == None:
        print("No vals")
    else:
        for row in vals:
            populate_member_from_event(event, row[1:])

# Create a new member or update an existing member's information from an Event
def populate_member_from_event(event, values):
    id = values[2]
    member = event_data.get_member(id)

    if member == None:
        first = values[0]
        last = values[1]
        email = values[3]
        phone = values[4] if len(values) >= 5 else None
        member = event_data.add_member(first, last, id, email, phone)
    
    event.add_attendee(member)

# Push event data back to the spreadsheet based off of what information
# we currently have
def push_event_data():
    print("push event data")

    # Clear the previous data in the logs
    clear_spreadsheet_range(
        log_sheet_id, 
        range_settings["event_log"])
    clear_spreadsheet_range(
        log_sheet_id,
        range_settings["membership_log"])
    clear_spreadsheet_range(
        log_sheet_id,
        range_settings["event_labels"])

    # Make sure all events are sorted based on date
    event_data.all_events.sort(key = lambda event: event.date)

    # Update the logs with the new values
    event_log_vals = []
    for i in range(len(event_data.all_events)):
        event = event_data.all_events[i]
        val = [
            i,
            event.name, 
            event.event_type().type, 
            event.date.strftime("%m/%d/%Y"),
            event.sheet_id
        ]
        event_log_vals.append(val)
    update_spreadsheet_range(
        log_sheet_id,
        range_settings["event_log"],
        event_log_vals)

    membership_log_vals = []
    for id, member in event_data.all_members.items():
        if type(member) != event_data.Member:
            raise Exception()
        val = [
            member.first_name,
            member.last_name,
            member.id,
            member.email,
            member.phone,
            member.position,
            member.fall_points,
            member.spring_points,
            member.points
        ]
        membership_log_vals.append(val)

        # Add an X for each event the member attended
        for event in event_data.all_events:
            if(member.attended_event(event)):
                val.append("X")
            else:
                val.append("")

    update_spreadsheet_range(
        log_sheet_id,
        range_settings["membership_log"],
        membership_log_vals)

    event_labels_vals = [ list(range(len(event_data.all_events))) ]
    
    update_spreadsheet_range(
        log_sheet_id,
        range_settings["event_labels"],
        event_labels_vals)

# 2. Schedule technical assistant emails
def schedule_leadership_update():
    pass

# 2a. Schedule technical assistant follow up
#   - NOTE: Only have this option if a technical assistant email
#           has already been scheduled previously
#   - NOTE: Can create a /data directory, and create .json file
#           keeping track of info regarding scheduled emails

if __name__ == "__main__":
    update_membership_logs()