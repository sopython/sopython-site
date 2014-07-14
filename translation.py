from collections import OrderedDict

salad = ["Cabbage", "Rhubarb", "rbrb", "cbg", "Potato?", "Sprouts", "Banana",
"Bananas", "Bean", "Beans", "Yam", "Tomato", "Melon", "Watermelon",
"Peaches", "Pears", "Mushrooms", "Mushroom", "Avocado", "Carrot", 
"Asparagus", "[Black Eyed] Peas", "Lettuce?", "Artichoke?"]

english = ["Hello", "Goodbye", "brb/afk", "hi/back", "How are you?", "Sorry", 
"Good", "Awesome", "Bad", "Horrible", "Fuck", "Bitch", "Thank you", "You're welcome", 
"Ladies", "Gentlemen", "I don't know", "Dunno", "I agree / I like it / yes", 
"I disagree / I don't like it / no", "Assistance / help",
"Brain Fart / Writers Block / Confusion / Confused / Makes No Sense",
"What? / What do you mean?",
"Are you joking? / Are you kidding? / Are you serious? / dafuq?"]

translation = OrderedDict(zip(salad, english))
