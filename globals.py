import tkinter as tk

window = tk.Tk()
cur = 0
updated = False
finished_updating = False


def center(win):
    """
    Centers a tkinter window

    :param win: the window to center
    :return: None
    """
    global window

    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = int(window.winfo_rootx() + (window.winfo_width() // 2) - (width // 2))
    y = int(window.winfo_rooty() + (window.winfo_height() // 2) - (height // 2))
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


# [{Bonus Name}, {Uncollected = 0/Collected = 1}]
bonuses = [['Bird of Prey', 0], ['Combo King', 0], ['Juggler', 0], ['Backstabber', 0], ['Sweeper', 0],
           ['Clean Sweep', 0], ['Meteor Smash', 0], ['Meteor Clear', 0], ['Meteor Master', 0],
           ['Meteor Survivor', 0], ['Flying Meteor', 0], ['Exceptional Aim', 0], ['Perfect Aim', 0],
           ['All Ground', 0], ['All Aerial', 0], ['All Variations', 0], ['All on One', 0],
           ['Lethal Weapon', 0], ['Berserker', 0], ['Smash King', 0], ['Smash Maniac', 0],
           ['Smash-less', 0], ['Specialist', 0], ['Dedicated Specialist', 0], ['One-Two Punch', 0],
           ['First Strike', 0], ['150% Damage', 0], ['200% Damage', 0], ['250% Damage', 0], ['300% Damage', 0],
           ['350% Damage', 0], ['Heavy Damage', 0], ['Sniper', 0], ['Brawler', 0], ['Precise Aim', 0],
           ['Pitcher', 0], ['Butterfingers', 0], ['All Thumbs', 0], ['Cuddly Bear', 0], ['Compass Tosser', 0],
           ['Throw Down', 0], ['Pummeler', 0], ['Fists of Fury', 0], ['Close Call', 0], ['Opportunist', 0],
           ['Spectator', 0], ['Statue', 0], ['Never Look Back', 0], ['Stiff Knees', 0], ["Run, Don't Walk", 0],
           ['Ambler', 0], ['No Hurry', 0], ['Marathon Man', 0], ['Eagle', 0], ['Aerialist', 0], ['Acrobat', 0],
           ['Cement Shoes', 0], ['Head Banger', 0], ['Elbow Room', 0], ['Power Shielder', 0], ['Shield Buster', 0],
           ['Shattered Shield', 0], ['Shield Stupidity', 0], ['Shield Saver', 0], ['Skid Master', 0],
           ['Rock Climber', 0], ['Edge Hog', 0], ['Cliffhanger', 0], ['Life on the Edge', 0], ['Poser', 0],
           ['Poser Poseur', 0], ['Poser Power', 0], ['Pose Breaker', 0], ['Instant Poser', 0], ['Control Freak', 0],
           ['Button Masher', 0], ['Button Holder', 0], ['Rock Steady', 0], ['Pratfaller', 0], ['Face Planter', 0],
           ['Twinkle Toes', 0], ['Floor Diver', 0], ['No R 4 U', 0], ['Climactic Clash', 0], ['Floored', 0],
           ['Punching Bag', 0], ['Stale Moves', 0], ['Blind Eye', 0], ['Crowd Favorite', 0],
           ['Master of Suspense', 0], ['Lost in Space', 0], ['Lost Luggage', 0], ['Half-Minute Man', 0],
           ['Pacifist', 0], ['Peaceful Warrior', 0], ['Moment of Silence', 0], ['Impervious', 0], ['Immortal', 0],
           ['Switzerland', 0], ['Predator', 0], ['Down, But Not Out', 0], ['Solar Being', 0], ['Stalker', 0],
           ['Bully', 0], ['Coward', 0], ['In the Fray', 0], ['Friendly Foe', 0], ['Center Stage', 0],
           ['Merciful Master', 0], ['Star KO', 0], ['Rocket KO', 0], ['Wimpy KO', 0], ['Bulls-eye KO', 0],
           ['Poser KO', 0], ['Cheap KO', 0], ['Bank-Shot KO', 0], ['Timely KO', 0], ['Special KO', 0],
           ["Hangman's KO", 0], ['KO 64', 0], ['Bubble-Blast KO', 0], ['Sacrificial KO', 0],
           ['Avenger KO', 0], ['Double KO', 0], ['Triple KO', 0], ['Quadruple KO', 0], ['Quintuple KO', 0],
           ['Dead-Weight KO', 0], ['Kiss-the-Floor KO', 0], ['Assisted KO', 0], ['Foresight', 0], ['First to Fall', 0],
           ['Cliff Diver', 0], ['Quitter', 0], ['Shameful Fall', 0], ['World Traveler', 0], ['Ground Pounded', 0],
           ['Environmental Hazard', 0], ['Angelic', 0], ['Magnified Finish', 0], ['Fighter Stance', 0], ['Mystic', 0],
           ['Shooting Star', 0], ['Lucky Number Seven', 0], ['Last Second', 0], ['Lucky Threes', 0], ['Jackpot', 0],
           ['Full Power', 0], ['Item-less', 0], ['Item Specialist', 0], ['Item Chucker', 0], ['Item Smasher', 0],
           ['Capsule KO', 0], ['Carrier KO', 0], ['Weight Lifter', 0], ['Item Catcher', 0], ['Reciprocator', 0],
           ['Item Self-Destruct', 0], ['Triple Items', 0], ['Minimalist', 0], ['Materialist', 0], ['Item Hog', 0],
           ['Item Collector', 0], ['Connoisseur', 0], ['Gourmet', 0], ['Battering Ram', 0], ['Straight Shooter', 0],
           ['Wimp', 0], ['Shape Shifter', 0], ['Chuck Wagon', 0], ['Parasol Finish', 0], ['Gardener Finish', 0],
           ['Flower Finish', 0], ['Super Scoper', 0], ['Screwed Up', 0], ['Screw Attack KO', 0], ['Warp Star KO', 0],
           ['Mycologist', 0], ['Mario Maniac', 0], ['Metal KO', 0], ['Freezie KO', 0], ['Flipper KO', 0],
           ['Mr. Saturn Fan', 0], ['Mrs. Saturn', 0], ['Saturn Siblings', 0], ['Saturn Ringer', 0], ['Giant KO', 0],
           ['Tiny KO', 0], ['Invisible KO', 0], ['Bunny-Hood Blast', 0], ['Vegetarian', 0], ['Heartthrob', 0],
           ['Invincible Finish', 0], ['Invincible KO', 0], ['Beam Swordsman', 0], ['Home-Run King', 0],
           ['Laser Marksman', 0], ['Flame Thrower', 0], ['Hammer Throw', 0], ['Headless Hammer', 0], ['Super Spy', 0],
           ["Bob-omb's Away", 0], ['Bob-omb Squad', 0], ['Pokémon KO', 0], ['Mew Catcher', 0], ['Celebi Catcher', 0],
           ['Goomba KO', 0], ['Koopa KO', 0], ['Paratroopa KO', 0], ['ReDead KO', 0], ['Like Like KO', 0],
           ['Octorok KO', 0], ['Topi KO', 0], ['Polar Bear KO', 0], ['Shy Guy KO', 0], ['First Place', 0],
           ['Last Place', 0], ['Wire to Wire', 0], ['Whipping Boy', 0], ['KO Artist', 0], ['KO Master', 0],
           ['Offensive Artist', 0], ['Offensive Master', 0], ['Frequent Faller', 0], ['Fall Guy', 0],
           ['Self-Destructor', 0], ['Master of Disaster', 0], ['KOs', 0], ['Falls', 0], ['SDs', 0],
           ['Target Master', 0], ['Hobbyist', 0], ['Collector', 0], ['No-Damage Clear', 0], ['No-Miss Clear', 0],
           ['Continuation', 0], ['Speedster', 0], ['Speed Demon', 0], ['Melee Master', 0], ['Classic Clear', 0],
           ['Adventure Clear', 0], ['All-Star Clear', 0], ['Very-Hard Clear', 0], ['Crazy Hand KO', 0], ['Luigi KO', 0],
           ['Link Master', 0], ['Giant Kirby KO', 0], ['Metal Bros. KO', 0], ['Giga Bowser KO', 0]]

# [{Trophy Name}, {Uncollected = 0/Collected = 1}, {1P only = 0, 1P + Lotto = 1, Lotto = 2}, {Bucket}]
trophies = [['Freezie', 0, 0, 'Item'], ['Parasol', 0, 0, 'Item'], ['Screw Attack', 0, 0, 'Item'],
            ['Bucket', 0, 1, 'Item'], ['Capsule', 0, 1, 'Item'], ['Egg', 0, 1, 'Item'], ['Fan', 0, 1, 'Item'],
            ['Flipper', 0, 1, 'Item'], ['Home-Run Bat', 0, 1, 'Item'], ['Megavitamins', 0, 1, 'Item'],
            ['Mr. Saturn', 0, 1, 'Item'], ['Poison Mushroom', 0, 1, 'Item'], ['Star Rod', 0, 1, 'Item'],
            ['Super Mushroom', 0, 1, 'Item'], ['Super Scope', 0, 1, 'Item'], ['Toad', 0, 1, 'Item'],
            ['Vegetable', 0, 0, 'Container'], ['Warp Star', 0, 0, 'Container'], ['Barrel', 0, 1, 'Container'],
            ['Crate', 0, 1, 'Container'], ['Party Ball', 0, 1, 'Container'], ['Starman 64', 0, 1, 'Container'],
            ['Green Shell', 0, 0, 'Shell'], ['Bob-omb', 0, 1, 'Shell'], ['Cloaking Device', 0, 1, 'Shell'],
            ['Coin', 0, 1, 'Shell'], ['Fire Flower', 0, 1, 'Shell'], ['Ray Gun', 0, 1, 'Shell'],
            ['Beam Sword', 0, 0, 'Paula BS'], ['Paula', 0, 0, 'Paula BS'], ['Charizard', 0, 0, 'Starzard'],
            ['Staryu', 0, 0, 'Starzard'], ['Chikorita', 0, 1, 'Starzard'], ['Crobat', 0, 1, 'Starzard'],
            ['Goldeen', 0, 1, 'Starzard'], ['Heracross', 0, 1, 'Starzard'], ['Poliwhirl', 0, 1, 'Starzard'],
            ['Scizor', 0, 1, 'Starzard'], ['Snorlax', 0, 1, 'Starzard'], ['Cleffa', 0, 0, 'Cletrodema'],
            ['Electrode', 0, 0, 'Cletrodema'], ['Marill', 0, 0, 'Cletrodema'],
            ['Bellossom', 0, 1, 'Cletrodema'], ['Blastoise', 0, 1, 'Cletrodema'], ['Bulbasaur', 0, 1, 'Cletrodema'],
            ['Clefairy', 0, 1, 'Cletrodema'], ['Cyndaquil', 0, 1, 'Cletrodema'], ['Igglybuff', 0, 1, 'Cletrodema'],
            ['Lugia', 0, 1, 'Cletrodema'], ['Porygon2', 0, 1, 'Cletrodema'], ['Squirtle', 0, 1, 'Cletrodema'],
            ['Togepi', 0, 1, 'Cletrodema'], ['Totodile', 0, 1, 'Cletrodema'], ['Weezing', 0, 1, 'Cletrodema'],
            ['Steelix', 0, 1, 'Steelix'], ['Wobbuffet', 0, 1, 'Wobbuffet'], ['Fire Kirby', 0, 0, 'Kirby'],
            ['Baby Bowser', 0, 1, 'Kirby'], ['Ball Kirby', 0, 1, 'Kirby'], ['Metroid', 0, 1, 'Kirby'],
            ['Raphael Raven', 0, 1, 'Kirby'], ['Rick', 0, 1, 'Kirby'], ['Slippy Toad', 0, 1, 'Kirby'],
            ['Waddle Dee', 0, 1, 'Kirby'], ['Banzai Bill', 0, 0, 'Enemies'], ['Koopa Paratroopa', 0, 0, 'Enemies'],
            ['Klap Trap', 0, 1, 'Enemies'], ['Koopa Troopa', 0, 1, 'Enemies'], ['Thwomp', 0, 1, 'Enemies'],
            ['Topi', 0, 1, 'Enemies'], ['Pit', 0, 0, 'Wheels'], ['Annie', 0, 1, 'Wheels'],
            ['Donbe & Hikari', 0, 1, 'Wheels'], ['Excitebike', 0, 1, 'Wheels'], ['Monster', 0, 1, 'Wheels'],
            ['Ryota Hayami', 0, 1, 'Wheels'], ['ZERO-ONE', 0, 1, 'Wheels'], ['Ayumi Tachibana', 0, 0, 'D Bucket'],
            ['Love Giant', 0, 0, 'D Bucket'], ['Daisy', 0, 1, 'D Bucket'], ['Dr. Wright', 0, 1, 'D Bucket'],
            ['Ducks', 0, 1, 'D Bucket'], ['Plum', 0, 0, 'Characters'], ['Lakitu', 0, 1, 'Characters'],
            ['Peppy Hare', 0, 1, 'Characters'], ['Starman EB', 0, 1, 'Characters'], ['Goron', 0, 0, 'Zelda'],
            ['Master Sword', 0, 0, 'Zelda'], ['Balloon Fighter', 0, 1, 'Zelda'], ['Kensuke Kimachi', 0, 1, 'Zelda'],
            ['Kirby Hat 3', 0, 1, 'Zelda'], ['Stanley', 0, 1, 'Zelda'], ['Like Like', 0, 0, 'Birdo'],
            ['ReDead', 0, 0, 'Birdo'], ['Birdo', 0, 1, 'Birdo'], ['Polar Bear', 0, 1, 'Birdo'],
            ['Four Giants', 0, 0, 'Giants'], ['Barrel Cannon', 0, 1, 'Giants'], ['Octorok', 0, 0, 'Octorok'],
            ['Viruses', 0, 0, 'Sick'], ['Heririn', 0, 1, 'Sick'], ['Racing Kart', 0, 1, 'Sick'],
            ['Dr. Stewart', 0, 1, 'Hats'], ['Kirby Hat 1', 0, 1, 'Hats'], ['Kirby Hat 2', 0, 1, 'Hats'],
            ['Metal Mario', 0, 1, 'Hats'], ['Andross', 0, 1, 'Villains'], ['Andross 64', 0, 1, 'Villains'],
            ['Jody Summer', 0, 1, 'Villains'], ['Meta-Knight', 0, 1, 'Villains'], ['Poo', 0, 1, 'Villains'],
            ['Ridley', 0, 1, 'Villains'], ['Samurai Goroh', 0, 1, 'Villains'], ['Vacuum Luigi', 0, 1, 'Vacuum Luigi'],
            ['Totakeke', 0, 1, 'Dog'], ['Alpha', 0, 2, 'Lotto'], ['Articuno', 0, 2, 'Lotto'], ['Arwing', 0, 2, 'Lotto'],
            ['Baby Mario', 0, 2, 'Lotto'], ['Bayonette', 0, 2, 'Lotto'], ['Boo', 0, 2, 'Lotto'],
            ['Bubbles', 0, 2, 'Lotto'], ['Chansey', 0, 2, 'Lotto'], ['Chozo Statue', 0, 2, 'Lotto'],
            ['Ditto', 0, 2, 'Lotto'], ['Dixie Kong', 0, 2, 'Lotto'], ['Eevee', 0, 2, 'Lotto'],
            ['Eggplant Man', 0, 2, 'Lotto'], ['Fighter Kirby', 0, 2, 'Lotto'], ['Fountain of Dreams', 0, 2, 'Lotto'],
            ['GCN', 0, 2, 'Lotto'], ['Gooey', 0, 2, 'Lotto'], ['Great Fox', 0, 2, 'Lotto'], ['Hammer', 0, 2, 'Lotto'],
            ['Hate Giant', 0, 2, 'Lotto'], ['Ho-Oh', 0, 2, 'Lotto'], ['Jeff', 0, 2, 'Lotto'],
            ['King Dedede', 0, 2, 'Lotto'], ['King K. Rool', 0, 2, 'Lotto'], ['Koopa Clown Car', 0, 2, 'Lotto'],
            ['Maruo Maruhige', 0, 2, 'Lotto'], ['Misty', 0, 2, 'Lotto'], ['Moltres', 0, 2, 'Lotto'],
            ['Moon', 0, 2, 'Lotto'], ['Ocarina of Time', 0, 2, 'Lotto'], ['Pak E. Derm', 0, 2, 'Lotto'],
            ['Pidgit', 0, 2, 'Lotto'], ['Pikmin', 0, 2, 'Lotto'], ['Poké Ball', 0, 2, 'Lotto'],
            ['Pokémon Stadium', 0, 2, 'Lotto'], ["Princess Peach's Castle", 0, 2, 'Lotto'],
            ['Professor Oak', 0, 2, 'Lotto'], ['Raccoon Mario', 0, 2, 'Lotto'], ['Raikou', 0, 2, 'Lotto'],
            ['Ray Mk II', 0, 2, 'Lotto'], ['Red Shell', 0, 2, 'Lotto'], ['Shy Guys', 0, 2, 'Lotto'],
            ['Suicune', 0, 2, 'Lotto'], ['Tingle', 0, 2, 'Lotto'], ['Turtle', 0, 2, 'Lotto'],
            ['Venusaur', 0, 2, 'Lotto'], ['Waluigi', 0, 2, 'Lotto'], ['Whispy Woods', 0, 2, 'Lotto'],
            ['Zapdos', 0, 2, 'Lotto']]

TAGS = ['AAAA', '1DER', '2BIT', '2L8', '2PAY', '401K', '4BDN', '4BY4', '4EVA', '7HVN', 'AOK', 'ARCH', 'ARN', 'ASH',
        'BAST', 'BBBB', 'BCUZ', 'BETA', 'BOBO', 'BOMB', 'BONE', 'BOO', 'BORT', 'BOZO', 'BUB', 'BUD', 'BUZZ', 'BYRN',
        'CHUM', 'COOP', 'CUBE', 'CUD', 'DAYZ', 'DIRT', 'DIVA', 'DNCR', 'DUCK', 'DUD', 'DUFF', 'DV8', 'ED', 'ELBO',
        'FAMI', 'FIDO', 'FILO', 'FIRE', 'FLAV', 'FLEA', 'FLYN', 'GBA', 'GCN', 'GLUV', 'GR8', 'GRIT', 'GRRL', 'GUST',
        'GUT', 'HAMB', 'HAND', 'HELA', 'HEYU', 'HI5', 'HIKU', 'HOOD', 'HYDE', 'IGGY', 'IKE', 'IMPA', 'JAZZ', 'JEKL',
        'JOJO', 'JUNK', 'KEY', 'KILA', 'KITY', 'KLOB', 'KNEE', 'L33T', 'L8ER', 'LCD', 'LOKI', 'LULU', 'MAC', 'MAMA',
        'ME', 'MILO', 'MIST', 'MOJO', 'MOSH', 'NADA', 'ZZZZ', 'NAVI', 'NELL', 'NEWT', 'NOOK', 'NEWB', 'ODIN', 'OLAF',
        'OOPS', 'OPUS', 'PAPA', 'PIT', 'POP', 'PKMN', 'QTPI', 'RAM', 'RNDM', 'ROBN', 'ROT8', 'RUTO', 'SAMI', 'SET',
        'SETI', 'SHIG', 'SK8R', 'SLIM', 'SMOK', 'SNES', 'SNTA', 'SPUD', 'STAR', 'THOR', 'THUG', 'TIRE', 'TLOZ', 'TNDO',
        'TOAD', 'TOMM', 'UNO', 'VIVI', 'WALK', 'WART', 'WARZ', 'WITH', 'YETI', 'YNOT', 'ZAXO', 'ZETA', 'ZOD', 'ZOE',
        'WORM', 'GEEK', 'DUDE', 'WYRN', 'BLOB']
