# All data related to events and membership
from datetime import date

all_events = []
all_members = {}
all_event_types = {}

def reset_event_data():
    global all_event_types, all_events, all_members
    all_events = []
    all_members = {}
    all_event_types = {}

# Adds an event type to the dictionary of all event types, and returns True on 
# a successful add
def add_event_type(type: str, cost: int):
    # Ensure the given type doesn't already have an EventType
    if type in all_event_types:
        return False
    
    all_event_types[type] = EventType(type, cost)
    return True

# Gets the EventType associated with the given type
def get_event_type(type: str):
    if type not in all_event_types:
        return None
    
    return all_event_types[type]

# Creates and returns a new event with the specified date
def add_event(name: str, date: date, type: str, sheet_id: str):
    event_type = get_event_type(type)
    if event_type == None:
        raise Exception("Invalid event type")
    
    new_event = Event(name, date, event_type, sheet_id)
    all_events.append(new_event)
    return new_event

# def get_event(index=-1, name=""):
#     if(index > -1):
#         if(index > len(all_events)):
#             raise Exception("Index out of bounds for event")
#         return all_events[index]

# Adds a new member to the dictionary of all members, and returns True on 
# a successful add
def add_member(
        first: str, 
        last: str, 
        id: str, 
        email: str, 
        phone: str, 
        position: str = "Member"):
    new_member = get_member(id)
    if new_member == None:
        new_member = Member(first, last, id, email, phone, position)
        all_members[id] = new_member
    
    return new_member

def get_member(id: str):
    if id not in all_members:
        return
    
    return all_members[id]

class Member:

    def __init__(
            self, 
            first: str, 
            last: str, 
            id: str, 
            email: str, 
            phone: str = "", 
            position: str = "Member"):        
        self.first_name = first
        self.last_name = last
        self.id = id
        self.email = email
        self.phone = phone
        self.position = position

        self.clear_event_data()
    
    # Returns True if the Member has attended the event
    def attended_event(self, event):
        if type(event) != Event:
            raise Exception("Incorrect argument type, expected Event")
        
        return event in self.events_attended
    
    # Clears all information about this member's events
    def clear_event_data(self):
        self.events_attended = []
        self.fall_points = 0
        self.spring_points = 0
        self.points = 0
    
    def add_event(self, event):
        if type(event) != Event:
            raise Exception("Incorrect argument type, expected Event")
        
        if self.attended_event(event) == False:
            self.events_attended.append(event)
            self.points += event.event_type().cost
    
    def __str__(self):
        return f"""[
    name: {self.first_name} {self.last_name}
    id: {self.id}
    email: {self.email}
    phone: {self.phone}
    position: {self.position}
    points: {self.points}
    fall sem points: {self.fall_points}
    spring sem points: {self.spring_points}
    attended events: {self.events_attended}
]"""
    
    def __repr__(self):
        return self.__str__()

class EventType:

    def __init__(self, type: str, cost: int):
        self.type = type
        self.cost = cost
    
    def __str__(self):
        return f"""[type: {self.type}, cost: {self.cost}]"""

class Event:

    def __init__(self, name: str, date: date, type: EventType, sheet_id: str):
        self.name = name
        self.date = date
        self.type = type
        self.sheet_id = sheet_id

        # Dictionary of attendees for this event (keys = ids of attendees, 
        # values = Member object of each attendee)
        self.attendees = {}

    # Returns True if attendee was successfully added to event, False
    # otherwise (attendee is already in event)
    def add_attendee(self, attendee):
        if type(attendee) != Member:
            raise Exception("Incorrect argument type, expected Event")
        
        # Ensure the attendee doesn't already have an entry in this Event
        if attendee.id in self.attendees:
            return False
        
        attendee.add_event(self)

        self.attendees[attendee.id] = attendee
        return True

    # Returns the EventType of this event
    def event_type(self):
        return self.type
    
    def __str__(self):
        return f"""[
    name: {self.name}
    date: {self.date}
    type: {self.type}
    attendees: {self.attendees}
]"""
    
    def __repr__(self):
        return self.name