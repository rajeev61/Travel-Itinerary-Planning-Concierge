from models import TravelOption

# Illustrative academic demo prices; these are NOT live quotes.
FLIGHTS = [
    ("F1", "IndiGo Saver Return", 8200, "Sample return economy fare"),
    ("F2", "Air India Economy Return", 10400, "Sample return economy fare"),
    ("F3", "Premium Flex Return", 14800, "Sample flexible return fare"),
]
HOTELS = [
    ("H1", "City Comfort Hotel", 2200, "Budget", "Simple centrally located stay"),
    ("H2", "Heritage Inn", 3400, "Standard", "Heritage-style hotel near attractions"),
    ("H3", "Royal Palace Stay", 5900, "Premium", "Upscale stay with breakfast"),
]
ACTIVITIES = [
    ("A1", "Amber Fort", 550, ["history", "culture"], "2–3 hours"),
    ("A2", "City Palace", 500, ["history", "culture"], "1–2 hours"),
    ("A3", "Hawa Mahal & old city walk", 250, ["history", "culture", "photography"], "1–2 hours"),
    ("A4", "Jaipur street-food trail", 900, ["food", "culture"], "2 hours"),
    ("A5", "Jantar Mantar", 300, ["history", "science"], "1 hour"),
    ("A6", "Nahargarh sunset viewpoint", 400, ["nature", "photography"], "2 hours"),
    ("A7", "Local craft market", 350, ["shopping", "culture"], "1–2 hours"),
    ("A8", "Garden and lakeside visit", 200, ["nature", "relaxation"], "1–2 hours"),
]

def flight_options(origin, destination):
    return [TravelOption(id=i, category="flight", name=n,
        description=f"{d} · {origin} ↔ {destination}", cost=float(c))
        for i, n, c, d in sorted(FLIGHTS, key=lambda x: x[2])]

def hotel_options(destination, days, category):
    nights = max(days - 1, 1)
    ordered = sorted(HOTELS, key=lambda x: (x[3] != category, x[2]))
    return [TravelOption(id=i, category="hotel", name=n,
        description=f"{d} · {destination} · {nights} night(s)",
        cost=float(price * nights), location=destination)
        for i, n, price, cat, d in ordered]

def activity_options(interests):
    wanted = {x.lower().strip() for x in interests}
    found = []
    for i, n, c, tags, duration in ACTIVITIES:
        overlap = wanted.intersection(tags)
        if overlap:
            found.append(TravelOption(id=i, category="activity", name=n,
                description=f"{duration} · matches {', '.join(sorted(overlap))}", cost=float(c)))
    if not found:
        found = [TravelOption(id="A8", category="activity", name="Garden and lakeside visit",
                  description="1–2 hours · general sightseeing", cost=200)]
    return sorted(found, key=lambda x: x.cost)
