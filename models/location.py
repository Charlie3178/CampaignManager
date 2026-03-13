class Location:
    def __init__(self, db_id, name, location_type, region, description, notes, parent_id=None):
        self.db_id = db_id
        self.name = name
        self.location_type = location_type
        self.region = region
        self.description = description
        self.notes = notes
        self.parent_id = parent_id  # This tells us if it's a sub-location
