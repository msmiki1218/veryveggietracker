import sqlite3

# to seed the database with initial data for Very Veggie Rules

# Connect to your database file
db = sqlite3.connect("veggie.db")
cursor = db.cursor()

# insert generations
generations = [
    #(name, color, career, aspiration, general_rules)
    ('Broccoli', '#556B2F', 'No formal career (run a small business selling your crafted goods)', 'Lord/Lady of the Knits', 'Start with $0 (Rags to Riches)'),
    ('Eggplant', '#4B0082', 'Romance Consultant', 'Villainous Valentine', 'Wear eggplant costume for every outfit as an adult'),
    ('Carrot', '#FF8C00', 'No formal career (earn your money through winning horse competitions)', 'Championship Rider', 'Max the Horse Riding Skill'),
    ('Squash', '#DAA520', 'University Student (your choice of major + career post graduation)', 'Academic AND Master Mentor', 'Successfully graduate university with at least a B grade'),
    ('Potato', '#C4A484', 'No formal career (earn money dumpster diving + as landlord)', 'Five-Star Property Owner', 'Become a 5-star property owner & have 3 units occupied by tenants'),
    ('Tomato', '#FF0000', 'Gardener (Floral Designer Branch)', 'Freelance Botanist AND Appliance Wiz', 'Grown tomato plants'),
    ('Cauliflower', '#D3D3D3', 'Undertaker', 'Ghost Historian', 'Complete your Souls Journey'),
    ('Radish', '#FFC0CB', 'Freelance Artist', 'Extreme Sports Enthusiast AND Jungle Explorer', 'Complete both aspirations'),
    ('Mushroom', '#D8CCC0', 'Conservationist (Environmental Manager branch)', 'Outdoor Enthusiast', 'Grow every mushroom variant from Cottage Living (Verdant, Charming, Mysterious, Lovely, Spicy, and Nightly mushrooms)'),
    ('Pea', '#90EE90', 'Actor', 'World Famous Celebrity', 'Refuse to ever cook, and only eat food prepared by other people. (Only eat "peas" quick meals from the fridge when another Sim has not cooked meals for you.)')
]

cursor.executemany("""
    INSERT INTO generations(name, color_code, career, aspiration, requirements)
    VALUES (?, ?, ?, ?, ?)
""", generations)

# insert Specific Goals (Linked by Generation ID)
# Gen 1: Broccoli (ID 1)
goals = [
    (1, 'Achieve a 5-star business'),
    (1, 'Max the wellness skill'),
    (1, 'Max 3 artistic skills (choose from painting, writing, photography, knitting, cross-stitching, pottery, tattooing, cooking/gourmet cooking, mixology, baking, DJ mixing, flower arranging, juice fizzing, fabrication, piano, pipe organ, violin, or guitar)'),
    # Gen 2: Eggplant (ID 2)
    (2, 'Grow giant eggplants'),
    (2, 'As an adult wear the eggplant costume for every outfit'),
    (2, 'Become a nectar connoisseur and maintain a nector cellar'),
    (2, 'Max the Romance, Fitness, Nectar Marking and Dancing skills'),
    # Gen 3: Carrot (ID 3)
    (3, 'Max the Horse Riding skill'),
    (3, 'Have 3 horses'),
    (3, 'Grow carrots'),
    (3, 'You can marry, but only after aging up to an Adult. It takes your Sim a long time to feel comfortable around new people'),
    # Gen 4: Squash (ID 4)
    (4, 'Successfully graduate university with at least a B grade'),
    (4, 'Complete both aspirations'),
    (4, 'Max the Logic, Video Gaming, and Research & Debate skills'),
    (4, 'Choose your own career benefitted by your degree, and max the career post graduation'),
    # Gen 5: Potato (ID 5)
    (5, 'Become a 5-Star Property Owner & have 3 units occupied by tenants'),
    (5, 'Befriend a Dust Bunny'),
    (5, 'Max the Fabrication, Baking, and Mischief skills'),
    (5, 'Decorate your home AND your rental units primarily with future obtained from a dumpster (or fabricated)'),
    # Gen 6: Tomato (ID 6)
    (6, 'Grow tomato plants'),
    (6, 'Max the Gardening, Cooking, and Gourmet Cooking skills'),
    (6, 'Get really into grilling (own a grill and have a dedicated outdoor kitchen)'),
    (6, 'Complete both aspirations'),
    # Gen 7: Cauliflower (ID 7)
    (7, 'Max the Thanatology, Gemology, Medium, and Writing skills'),
    (7, 'Complete your Souls Journey'),
    (7, 'Live in a Haunted House'),
    (7, 'Marry a ghost (kill your existing partner pre-marriage and choose to have kids first OR meet a new ghost and adopt with the ghost)'),
    # Gen 8: Radish (ID 8)
    (8, 'Complete both aspirations'),
    (8, 'Visit space (build your own rocket ship OR use one at GeekCon)'),
    (8, 'Max the Selvadoradian Culture and Archaeology Skills'),
    (8, 'Max the Skiing, Snowboarding, and Rock Climbing skills'),
    # Gen 9: Mushroom (ID 9)
    (9, 'Max the Fishing, Herbalism, Logic, and Handiness skills'),
    (9, 'Adopt a stray pet'),
    (9, 'Grow every mushroom variant from Cottage Living (Verdant, Charming, Mysterious, Lovely, Spicy, and Nightly mushrooms)'),
    # Gen 10: Pea (ID 10)
    (10, 'Become a 5-star celebrity'),
    (10, 'Have a house worth at least $250,000'),
    (10, 'Max the Piano, Violin, and Guitar skills'),
    (10, 'Refuse to ever cook, and only eat food prepared by other people. (Only eat "peas" quick meals from the fridge when another Sim has not cooked meals for you.)')
]

cursor.executemany("INSERT INTO goals (generation_id, description) VALUES (?,?)", goals)

db.commit()
db.close()
print("Success! Very Veggie Rules seeded.")