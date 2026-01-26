import sqlite3

db = sqlite3.connect("veggie.db")
cursor = db.cursor()

# 1. THE WIPE (Prevents duplicates)
cursor.execute("DROP TABLE IF EXISTS user_progress")
cursor.execute("DROP TABLE IF EXISTS goals")
cursor.execute("DROP TABLE IF EXISTS generations")
cursor.execute("DROP TABLE IF EXISTS users")

# 2. THE SETUP (Re-creates the empty tables)
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE generations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    color_code TEXT,
    career TEXT,
    aspiration TEXT,
    traits TEXT
)""")

cursor.execute("""
CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generation_id INTEGER,
    description TEXT NOT NULL,
    FOREIGN KEY (generation_id) REFERENCES generations(id)
)""")

cursor.execute("""
CREATE TABLE user_progress (
    user_id INTEGER,
    goal_id INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    aspiration_completed BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (user_id, goal_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (goal_id) REFERENCES goals(id)
)""")

# insert generations
generations = [
    #(name, color, career, aspiration, traits)
    ('Broccoli', '#556B2F', 'No formal career (run a small business selling your crafted goods)', 'Lord/Lady of the Knits', 'Creative, Art Lover, High Maintenance'),
    ('Eggplant', '#4B0082', 'Romance Consultant', 'Villainous Valentine', 'Evil, Romantic, Bro'),
    ('Carrot', '#FF8C00', 'No formal career (earn your money through winning horse competitions)', 'Championship Rider', 'Horse Lover, Unflirty, Loner'),
    ('Squash', '#DAA520', 'University Student (your choice of major + career post graduation)', 'Academic AND Master Mentor', 'Ambitious, Hates Children, Geek'),
    ('Potato', '#C4A484', 'No formal career (earn money dumpster diving + as landlord)', 'Five-Star Property Owner', 'Freegan, Nosy, Slob'),
    ('Tomato', '#FF0000', 'Gardener (Floral Designer Branch)', 'Freelance Botanist AND Appliance Wiz', 'Socially Awkward, Hot-Headed, Overachiever'),
    ('Cauliflower', '#D3D3D3', 'Undertaker', 'Ghost Historian', 'Paranoid, Bookworm, Skeptical'),
    ('Radish', '#FFC0CB', 'Freelance Artist', 'Extreme Sports Enthusiast AND Jungle Explorer', 'Adventurous, Chased By Death, Active'),
    ('Mushroom', '#D8CCC0', 'Conservationist (Environmental Manager branch)', 'Outdoor Enthusiast', 'Vegetarian, Loves the Outdoors, Dog/Cat Lover'),
    ('Pea', '#90EE90', 'Actor', 'World Famous Celebrity', 'Self-Absorbed, Materialistic, Music Lover')
]

cursor.executemany("""
    INSERT INTO generations(name, color_code, career, aspiration, traits )
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
    (2, 'Max the Romance Skill'),
    (2, 'Max the Fitness Skill'),
    (2, 'Max the Nectar Making Skill'),
    (2, 'Max the Dancing Skill'),
    # Gen 3: Carrot (ID 3)
    (3, 'Max the Horse Riding skill'),
    (3, 'Have 3 horses'),
    (3, 'Grow carrots'),
    (3, 'You can marry, but only after aging up to an Adult. It takes your Sim a long time to feel comfortable around new people'),
    # Gen 4: Squash (ID 4)
    (4, 'Successfully graduate university with at least a B grade'),
    (4, 'Complete both aspirations'),
    (4, 'Max the Logic skill'),
    (4, 'Max the Video Gaming skill'),
    (4, 'Max the Research & Debate skill'),
    (4, 'Choose your own career benefitted by your degree, and max the career post graduation'),
    # Gen 5: Potato (ID 5)
    (5, 'Become a 5-Star Property Owner & have 3 units occupied by tenants'),
    (5, 'Befriend a Dust Bunny'),
    (5, 'Max the Fabrication skill'),
    (5, 'Max the Baking skill'),
    (5, 'Max the Mischief skill'),
    (5, 'Decorate your home AND your rental units primarily with future obtained from a dumpster (or fabricated)'),
    # Gen 6: Tomato (ID 6)
    (6, 'Grow tomato plants'),
    (6, 'Max the Gardening skill'),
    (6, 'Max the Cooking skill'),
    (6, 'Max the Gourmet Cooking skill'),
    (6, 'Get really into grilling (own a grill and have a dedicated outdoor kitchen)'),
    (6, 'Complete both aspirations'),
    # Gen 7: Cauliflower (ID 7)
    (7, 'Max the Thanatology, Gemology, Medium, and Writing skills'),
    (7, 'Max the Geomology skill'),
    (7, 'Max the Medium skill'),
    (7, 'Max the Writing skill'),
    (7, 'Complete your Soul\'s Journey'),
    (7, 'Live in a Haunted House'),
    (7, 'Marry a ghost (kill your existing partner pre-marriage and choose to have kids first OR meet a new ghost and adopt with the ghost)'),
    # Gen 8: Radish (ID 8)
    (8, 'Complete both aspirations'),
    (8, 'Visit space (build your own rocket ship OR use one at GeekCon)'),
    (8, 'Max the Selvadoradian Culture skill'),
    (8, 'Max the Archaeology skill'),
    (8, 'Max the Skiing skill'),
    (8, 'Max the Snowboarding skill'),
    (8, 'Max the Rock Climbing skill'),
    # Gen 9: Mushroom (ID 9)
    (9, 'Max the Fishing skill'),
    (9, 'Max the Herbalism skill'),
    (9, 'Max the Logic skill'),
    (9, 'Max the Handiness skill'),
    (9, 'Adopt a stray pet'),
    (9, 'Grow every mushroom variant from Cottage Living (Verdant, Charming, Mysterious, Lovely, Spicy, and Nightly mushrooms)'),
    # Gen 10: Pea (ID 10)
    (10, 'Become a 5-star celebrity'),
    (10, 'Have a house worth at least $250,000'),
    (10, 'Max the Piano, Violin, and Guitar skills'),
    (10, 'Max the Violin skill'),
    (10, 'Max the Guitar skill'),
    (10, 'Refuse to ever cook, and only eat food prepared by other people. (Only eat "peas" quick meals from the fridge when another Sim has not cooked meals for you.)')
]

cursor.executemany("INSERT INTO goals (generation_id, description) VALUES (?,?)", goals)

db.commit()
db.close()
print("Success! Very Veggie Rules seeded.")