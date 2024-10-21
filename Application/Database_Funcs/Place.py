from Application.Models import Place

# Function to retrieve all places from the database
def get_places():
    return Place.query.all()

# Function to add a new place to the database
def add_place(place_name, place_type, price, amenities, rating, campus_distance):
    try:
        new_place = Place(
            place_name=place_name,
            type=place_type,
            price=price,
            amenities=amenities,
            rating=rating,
            campus_distance=campus_distance
        )
        db.session.add(new_place)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error adding place: {e}")
        db.session.rollback()
        return False
