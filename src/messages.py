'''
    messages.py
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2020 Jacob Wharton.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

'''
    tags in {} are substituted with the following.
    tag   - substituted with:
    pct     PC title
    pcn     PC name
    pcc     PC class
    pcgg    PC gender - generic ("man", "woman")
    pcgp    PC gender - polite ("sir", "madam")
    pcgs    PC gender - subject ("he", "she")
    pcgo    PC gender - object ("him", "her")
    pcgi    PC gender - object2 ("guy", "girl")
    npct    NPC title
    npcn    NPC name
    npcc    NPC class
    npcgg   NPC gender - generic
    nc      name calling
    anc     a(n) + nc
    ncs     name calling plural
    cuss    exclamation
    slur    curse
    slurs   slur plural
    aslur   a(n) + slur
    flirt   flirt word ("baby", "cutie", "hot stuff", "",)
    tod     time of day
    tof     term of friendship
    toe     term of endearment
    gcomp   generic compliment
    comp    compliment
    wcomp   whacky over the top compliment
    icomp   item of a compliment (something you are wearing or holding or carrying)
    insult  generic 
    
    
    * capitalized first letter indicates the need to capitalize the word
        that is substituted.
'''

TERM_OF_FLIRTATION={
    "male" : ("hot stuff","cutie","babe","sexy",),
    "female" : ("babe","baby","cutie","pretty lady",),
}

TERM_OF_FRIENDSHIP={
    "male" : ("bro","dude","man",),
    "female" : ("girl","babe","woman",),
}

TERM_OF_ENDEARMENT=(
    "darling", "dear", "love", "dear friend",
)

TERM_OF_ATTRACTION=(
    "sweety", "honey", "darling",
)

CUSS=("fuck", "shit", "damn", "hell",)

SLUR=(
    # singular
    ("jackass", "cuntface", "dick", "bitch", "motherfucker", "human trash",
     "wretch", "cur", "devil", "douchebag",),
    # plural
    ("jackasses", "cuntfaces", "dicks", "bitches", "motherfuckers", "human trash",
     "wretches", "curs", "devils", "douchebags",),
)

NAMECALLING=(
    # singular
    ("ninny", "twit", "loser", "asshole", "jerk", "imbecile", "simp",
     "simpleton", "fool", "ass", "asshat", "cunt", "donkey",),
    # plural
    ("ninnies", "twits", "losers", "assholes", "jerks", "imbeciles", "simps",
     "simpletons", "fools", "asses", "asshats", "cunts", "donkeys",),
)

COMPLIMENT=(
    "you have beautiful eyes",
    "I dig your style",
)

COMPLIMENT_GENERIC=(
    "I like your hair",
    "lookin' good",
    "nice outfit",
    "looking sharp",
)

COMPLIMENT_WHACKY=(
    "what a splendid day it is that I should stumble upon the likes of your glorious person",
    "well aren't you a sight for sore eyes",
    "your presence is divine, like the rays of the Sun",
    "my, what a beautiful face you have",
)

PHRASE_QUIRKY=(
    "well slap me sideways and call me Sally",
)

PHRASE_WHY=(
    "well kick me in the gut and pull my intestines out from my prolapsed anus",
)

INSULT=(
    "you reek of codfish and your mother speaks Cantonese",
)

    #----------#
    # messages #
    #----------#

# Introductions -- on first meeting someone #

INTRODUCTION={
"generic" : {
    0: ("I don't care who you are. Just leave me alone.",),
    0.1:("Whoever you are, just mind your own business.",),
    0.2:("Good to meet you.",),
    0.3:("Nice to meet you. The name's {npcn}.",),
    0.4:("{npcn}. Nice to meet you.",),
    0.5:("Pleased to meet you, {pcn}. I'm {npcn}.",),
    0.6:("So very nice to meet you, {pcn}. My name is {npcn}.",),
    0.7:("I feel like we've met before.",),
    0.8:("You remind me of an old friend. I think we'll get along very well.",),
    0.9:("Oh, yes, {pcn}, I am very pleased to make your acquaintance. My name is {npcn}. I hope we will be seeing a lot more of each other.",),
    },
}

# Greetings #

REJECTION={ # conversation rejection
"generic" : {
    0  :("I'm sick of you. Go away, and don't ever come back.",
         "I hate you.",
         "Leave. Now.",
         "Piss off.",
         "*no response*",),
    0.1:("Get lost.",
         "Go away.",
         "Shut up.",
         "Stop.",
         "Stop it.",),
    0.2:("I'm busy.",
         "I'm sorry, I can't help you.",
         "I'm sorry, I'm too busy right now. Come back later.",),
    0.3:("Sorry, I've got a lot of work to do. I can't help you now.",
         "Unfortunately, I've got my hands full. Sorry.",),
    0.4:("I'd like to help you, {pcn}, but I'm very busy.",),
    0.5:("As much as I'd like to help, I'm afraid I can't right now. I'll make it up to you.",),
    0.6:("Hey, {pcn}. I wish I had time to chat, but I have to concentate. See you later.",),
    0.7:("Oh, hey, {pcn}! I'm sorry, I can't talk with you right now, but come back again sometime soon.",),
    0.8:("Hello, sweet {pcn}. I'm sorry, I have a lot of work to do at the moment.",),
    0.9:("As much as it pains me to say it, dear {pcn}, I'm too busy to talk at the moment.",),
    },
"motivated" : {
    0  :("I do not have time for you. Now or ever.",
         "No, no time. Not for you.",),
    0.1:("No, {pcgp}.",),
    0.2:("Excuse me, I'm busy; please let me finish my work.",),
    0.3:("I'm sorry, {pcgp}{pcc}, I'm very busy at the moment, but come back shortly.",),
    },
"outgoing" : {
    100 : ("Forgive me. I must be going.",),
    },
"proactive" : {
    100 : ("I'm sorry, I don't talk to {slurs} like you.",),
    },
}

GREETING={ # conversation acceptance
"generic" : {
    0  :("I wish you would be quiet.",
         "Please just go away.",
         "You again? What do you want?",),
    0.1:("Yea? What?",
         "Not you again.",
         "What? What do you want from me?",),
    0.2:("Yea?",
         "Yes, {pcc}?",
         "Yes, {pcc}? What do you want?",
         "What do you want?",),
    0.3:("Mm-hmm?",
         "Yes, {pct}{pcn}?",
         "What can I do for you?",
         "Can I help you?",),
    0.4:("Yes, {pcn}?",
         "Hello.",
         "What's up?",
         "What is it, {pcn}?",
         "How can I help, {pcc}?",),
    0.5:("Hello again.",
         "Hello again, {pcn}.",
         "Hello, friend.",
         "Nice to see you again.",
         "What are you up to today?",
         "What is it, dear {pcn}?",),
    0.6:("Yes, sweet {pcn}?",
         "It's nice to see you, {pcn}.",
         "Hey {tof}, what are your plans for the weekend?",
         "Hello again {pcn}, I pray you're doing well. What's on your mind?",),
    0.7:("Great to see you again.",
         "It's always good to see you, {pcn}.",
         "Hello again, {toe}.",),
    0.8:("Hello, love.",
         "Hello, darling, what can I do you for?",
         "Is there something I can do to help? Anything at all, just ask.",
         "It's great to see you again.",),
    0.9:("And for what purpose am I blessed to be in your presence?",
         "Hey {pcn}! It's so great to see you.",
         "I've missed you, {pcn}.",
         "Hello, my love.",
         "Hello again, my darling.",),
    1.0:("Hello, my dearest {pcn}.",
         "I've missed you -- you should come around more often.",
         "I've really missed you a lot.",),
    },
"proud" : { # happy, high opinion of self, family man/woman, helpful, not dependable
    0  :("What is it, person who is inferior to me in every way?",
         "Just walk away, you miserable dog.",
         "Piss off, you wretched creature.",),
    0.1:("Hey, {pcc}, is it true you pissed your bed until you were eight?",
         "Horrible creature.",
         "I saw a muckrat the other day.",),
    0.2:("What do *you* want?",
         "Well if it isn't you again.",
         "I suppose I could spare a moment or two for someone less fortunate than myself.",),
    0.3:("Hey, good to see you.",
         "Hello, {pcc}. I hope you won't take up too much of my time.",
         "Have you come to bask in my glorious presence? Can't say I blame you.",),
    0.4:("Hey, {pcn}, good to see you.",
         "What can I do for you, {pcc}?",
         "It's your lucky day! It appears I've got a moment to spare for you.",),
    0.5:("I'd be glad to help.",
         "It would be my pleasure.",
         "I'm glad you're still alive.",),
    0.6:("Let me know if there's anything I can do to help. I'd be glad to do what I can.",
         "It's so good to see you. Anything I can do, just say the word.",
         "Great to see you're doing all right.",),
    0.7:("Hello {pcn}. You know, I'm proud to call you my friend. What can I do for you?",
         "What a nice thing to say. It's good to see you, friend.",),
    0.8:("Hello, my dear {pcn}. Anything you need, don't hesitate to ask.",
         "Oh, please, you're too kind.",),
    0.9:("I'm so glad to see you.",
         "Oh, it's good to see you're all right. Us upperclassmen have got to stick together.",),
    1.0:("Oh, {pcn}, how I've missed you! It's so good to see you're still in one piece.",),
    },
"low-self-esteem" : { # sad, low opinion of self, a downer, hates all weather, always having a "shitty" day, flaky, unreliable, but kind
    0  :("Great, just what I deserved. It's you.",
         "Just when things were starting to look slightly less shitty. You show up.",),
    0.1:("Not you again. Just my luck.",
         "I may deserve every ounce of pain you're going to cause me, but I beg you, have mercy.",),
    0.2:("...Yes?",
         "Hello there.",
         "Yo.",),
    0.3:("Hi.",
         "Oh, it's you again. Hello.",
         "Whassup?",
         "Yo, whassup?",
         "'Sup?",),
    0.4:("Yo, what's hangin'.",
         "Hope you've been doin' better than I have.",
         "What's shakin'?",),
    0.5:("How've you been? Better than me, I hope.",
         "Well, they say the grass is always greener...",),
    0.6:("Hi, {pcn}!",
         "I'm glad you're doing OK.",),
    0.7:("To what do I owe the pleasure?",),
    0.8:("Hello there, {pcn}, I'm so glad to see you.",),
    0.9:("I've been looking forward to you coming to visit, {pcn}.",),
    1.0:("You're so wonderful... I don't deserve you.",),
    },
"argumentative" : { # opinionated, slurs a lot, loves arguing/fighting, helpful, dependable, friendly, rude, insulting
    0  :("Hey, {slur}.",
         "Yea, I know your mother gives free handies, and like I told you before, I'm straight.",
         "Go fall in a hole and die.",
         "Not you. Anyone but you, please, for the love of God.",
         "Hello again, {slur}. It's so great to see you. Oh no, please, feel free to be an absolute fucking {slur}. Be my guest.",),
    0.1:("Looking for a fight?",
        "Hey, ...you.",
         "Whassup, {slur}.",
         "Ugh.",
         "Not you. Get lost or hit me like a {pcgg}, {slur}.",
         "Whatever you're looking for, I'm sure I don't know how to find it.",),
    0.2:("You're not the person I was hoping to see.",
         "Can I *help* you?",),
    0.3:("Hey {pcn}, you agree that socialism is the same thing as naziism, right?",
         "Yea? Can I help you?",),
    0.4:("George Hepburn is the stupidest god-damn president of all time. Try to change my mind.",
         "Wow, I still can't believe he said that. *laughs*",),
    0.5:("What do you think of the illuminati?",
         "I'm telling you, mountain stew is, bar-none, the best MRE in the history of mankind.",),
    0.6:("Where do you think we go when we die?",),
    0.7:("Hello my friend. Looking for a right beating in a good ol' game of fless?",
         "Oh no, not you again. *chuckles* Good to see you, you son of a bitch. How've you been?",),
    0.8:("Hey, I need you to break a tie. No matter which way you shake it, The Shobbit films are just *so* vastly much better produced than the Lord of the Kings. Right?",),
    0.9:("There's no-one I'd rather see. What's new?",),
    1.0:("There's my {pcn}. No-one could ever beat you in a fight!",),
    },
"non-confrontational" : { # agreeable, dry, shallow, boring
    0  :("*no response*",
         "*exasperated expression*",),
    0.1:("I'd really rather you not.",
         "Could you just... not?",
         "*annoyed expression*",),
    0.2:("Hm.",
         "*sharp exhale*",
         "Well, what is it?",),
    0.3:("Yep?",
         "Yes? Do you need something?",),
    0.4:("Uh-huh?",
         "Oh, it's just you. Hello.",),
    0.5:("Hi, how are you?",),
    0.6:("*smiles*",),
    0.7:("Hello friend, lovely weather we're having.",),
    0.8:("Great to see you again. Is there anything I can do for you?",),
    0.9:("Oh, hello, sweet {pcn}. How have you been?",),
    1.0:("Will I get to see you tomorrow, {pcn}?",),
    },
"outgoing" : { # compliments a lot. Very intense. Uses goofy words/phrases.
    0  :("No!!! God. No! God, please, no. No! No! Noooo!!!!!",
         "What the hell do you want?",
         "What do you want, {slur}?",
         "God, just go. Go away, and don't come back.",),
    0.1:("Make it quick or hit the road.",
         "I don't like you.",),
    0.2:("I'm sure there's someone else you can bother.",),
    0.3:("Hey, {pcn}. {Gcomp}.",
         "Yo, {tof}, what's up.",
         "Hey, buddy.",),
    0.4:("Yea, {pcc}? Do you have a question?",
         "{Gcomp}, {pcn}. What's up?",
         "What's up, {tof}?",
         "Hey, buddy!",),
    0.5:("What's happenin'?",
         "What's shakin', bacon?",
         "What's cookin', my shooken?",
         "Niiice {icomp}, {tof}.",
         "Heya, pal.",),
    0.6:("What's up, brohammer?",
         "{pcn}! Yo, I love that {icomp}!",
         "Heya, pal!",),
    0.7:("'Sup, {pcn}! Sick {icomp}!",
         "Hey there, {pcn}! {Comp}.",
         "Hey! Good on ya, {tof}!",
         "Hey, friend.",),
    0.8:("Hey, {tof}! {Comp}.",
         "What's up, {tof}? Great to see you! {Comp}.",
         "Hello, sweet {toe}. What can I do for you on this fine day?",
         "Oh, {tof}, it's good to see you! Put 'er there!",
         "Hey, friend!",),
    0.9:("I'm so glad to see you again, {pcn}! I hope you've been well. Is there anything I can do for you? Anything at all?",
         "Friend!",),
    1.0:("Oh, my dear {pcn}, how are you?",
         "Oh! {pcn}, what a surprise! I'm so happy to see you. How have you been?",),
    },
"shy" : { # weeb. Likes video games. says um, uh, mm-hm a lot. Uses terse responses. Conservative in speech. Often hugs people they love the most.
    0  :("Um... so, I would appreciate it if you would leave.",),
    0.1:("Oh, hello...",),
    0.2:("Hi, {pcn}.",
         "Hello, {pcn}.",
         "Hello...",
         "Yea.",),
    0.3:("Hello {pcn}.",
         "Hello.",
         "Yea?",),
    0.4:("Hi, {pcn}!",
         "Oh! Hi, {pcn}.",
         "Yes.",),
    0.5:("*smiles*",
         "Yes?",),
    0.6:("Uh! Well, it's...! Oh, nevermind.",
         "*grins*",
         "Mm-hmm.",),
    0.7:("Mm-hmm...?",
         "Nice to see you!",),
    0.8:("Mm-hmm!",
         "Hello!",
         "Hi again!",),
    0.9:("Hey, {pcn}. How are you doing? I've missed you! *hugs*",
         "*glances at you coyly*",),
    1.0:("Hello, {toe}! I love you! *hugs*",
         "*smiles coyly*",),
    },
"independent" : { # against "vendors", doesn't open up very much
    0  :("I don't want whatever you're selling.",
         "Just leave me and my family alone.",
         "Whatever you're after, leave me out of it.",),
    0.1:("I'm fine, thanks.",
         "Hey?",
         "*silently looks you in the eyes*",),
    0.2:("Hey, there, {pcc}.",
         "Hey, you.",),
    0.3:("No, thank you. Oh -- it's just you; I thought you were a vendor. *shudders*",),
    0.4:("Hello, {pcn}. {Gcomp}.",),
    0.5:("Hello you.",),
    0.6:("Hi {pcn}!",
         "Hi!",),
    0.7:("Hey, you!",),
    0.8:("Hey you!",),
    0.9:("Hey you! *smiles*",
         "How are you! *smiles*",),
    1.0:("Hey, you! *grins*",
         "*cute smile*",
         "Dear {toe}, how have you been?",),
    },
"codependent" : { # Needy. Helpful. Dependable. Somewhat selfish.
    0  :("I don't want you. I don't need you. Just get out of my life.",
         "Go away, and don't ever come back.",),
    0.1:("You again? What is it this time?",),
    0.2:("Hey there, {pcgp} {pcc}.",),
    0.3:("Hey, {pcn}. What's up?",),
    0.4:("Maybe we can help each other.",),
    0.5:("I'm looking forward to dealing more with you in the future.",
         "Can I help?",),
    0.6:("What do you need?",
         "Yes, dear {pcn}? What can I do for you?",),
    0.7:("Dear {pcn}, is there something I can do for you?",
         "Hello, my sweet {pcn}, how can I serve you?",
         "It's always good to see you, dear {pcn}. What do you need?",),
    0.8:("Hello {toe}, {comp}. What's new?",
         "{Gcomp}, {pcn}! Need something?",
         "Sweet {pcn}, can I help with something?",),
    0.9:("Oh, dearest {pcn}! {Wcomp}.",
         "How can I assist you my love?",
         "Hey, {pcn}! Boy, do I have a lot to tell you!",),
    1.0:("Lovely {pcn}, {wcomp}.",
         "*big smile*",
         "Hello best friend!",
         "How are you my {toe}?",),
    },
"bubbly" : { # friendly, quirky, smily, does a lot of gesturing. Hugs a lot. Screams "rape!" when threatened.
    0  :("Just get it over with, {slur}!",
         "Hey, {slur}! {Gcomp}.",
         "Oh, hi, {slur}. I always love when you come, because I get to look forward to you leaving.",
         "Ooh, I love that {icomp}. It really highlights what a {slur} you are.",),
    0.1:("Sorry, but not sorry.",
         "Gross. It's {pcn}.",
         "Ew.",),
    0.2:("Hey, {gcomp}, {pcgg}.",),
    0.3:("Hey, it's {pcn} again!",
         "Hey again!",),
    0.4:("Hello again {pcn}! Good {tod}.",
         "Hey {pcn}, {gcomp}.",),
    0.5:("Hey there! *punches you in the arm*",
         "Hi!!",
         "Hey! Nice {icomp}.",),
    0.6:("Well, hi again, {pcn}. So nice to see you.",
         "Yo! *high-fives*",
         "Hi, {pcn}! I love that {icomp}!",),
    0.7:("Heya! *does a little dance*",
         "Yao! {pcn}! Did I ever tell you {comp}?",
         "Hi! *hugs*",),
    0.8:("Squee! It's {pcn}...! *hugs*",
         "*grins, hugs* Hey, {pcn}!",
         "Well if it isn't my {toe}, {pcn}. Don't hesitate to ask if there's anything I can do for you.",),
    0.9:("Hey!! Guess what? I love you!",
         "*freaks out in excited delight*",
         "*hugs extremely tightly*",
         "Wow! That {icomp} looks so good on you! *hugs*",),
    1.0:("*big smile*",
         "Aw, {pcn}! How lucky can I be?",
         "It's {pcn}!! {Comp}. I can't get over it.",
         "Hey! *smiles, hugs*",),
    },
"low-energy" : { # quick, to-the-point, lazy, speaks slowly, very loving to people with highest disposition. acts high.
    0  :("*long, exasperated sigh*",
         "Eat shit, {slur}.",),
    0.1:("They don't pay me enough to deal with {slur}s like you.",),
    0.2:("Oh. It's only you. What?",),
    0.3:("Yea? Something you need?",),
    0.4:("Hm? What is it?",
         "Warm day to you.",),
    0.5:("Hey. Good to see you.",
         "Warm day to you, friend.",),
    0.6:("Hey, how are you doin'?",
         "Live long and prosper.",),
    0.7:("What's goin' on?",
         "Heeeeyyy.",),
    0.8:("Yo, good to see you!",
         "*smiles with love*",),
    0.9:("Hi there, how are you doing?",
         "Love. *hugs*",),
    1.0:("Hey... How are you?",
         "*hugs*",),
    },
"motivated" : { # says "great {pcgp}" a lot, talks about stocks, their work, uses polite, old-fashioned speech. Hugs people they love the most
    0  :("What could possibly be worth my time, coming from a {slur} like you?",
         "Suck my dick, you fuckhead.",),
    0.1:("What do you want? I'm very busy.",
         "Just one more, and make it quick.",),
    0.2:("Yes? If it's nothing important, I'll be going now.",
         "What is it now?",),
    0.3:("Good {tod}.",
         "Yes, {pcgp}? Make it quick, I'm very busy.",
         "Is there something I can do for you? If not, please leave me to my work.",
         "Yes, {pcn}. {Gcomp}.",),
    0.4:("Good day, {pcgp}.",
         "Hello, {pcn}. {Gcomp}.",),
    0.5:("Good day, {pcgp}!",
         "Good {tod}. {Comp}.",),
    0.6:("Great {pcgp}, what can I do for you?"
         "Hello again, great {pcgp}!",
         "Great {pcgp}. So wonderful to see you.",),
    0.7:("Great {pcgp}, it is wonderful to see you again. I'd quite like to do so more often, but I'm afraid time is not on my side, you see.",
         "Hello, {pcn}. {Comp}.",
         "Well, {pcn}! I can always make time for you. What can I do you for?",),
    0.8:("Hello, {pcn}. {Wcomp}.",
         "{pcn}! So great to see you! {Gcomp}, as always!",
         "Salutations, {toe}.",),
    0.9:("Hello, beautiful.",
         "You're looking wonderful this {tod}.",),
    1.0:("I'm very glad to see you, {toe}. *hugs*",
         "{pcn}! I've missed you. *hugs*",),
    },
"unmotivated" : { # lazy, chill, cool, nice, terse.
    0  :("Oof. Not you again.",
         "*sighs*",),
    0.1:("Ooohh... *groans*",
         "*sighs* Yea?",),
    0.2:("I don't have the energy for you today.",),
    0.3:("Hey.",
         "'Sup.",
         "*nods head in greeting*",),
    0.4:("Well if it isn't {pcn}.",
         "*raises head in greeting*",),
    0.5:("Hi, trusted {pcn}.",
         "*smiles slightly*",
         "Hey-yo.",),
    0.6:("*singing badly* What's goin' on?",
         "All-right.",),
    0.7:("*finger guns*",
         "All-right!",),
    0.8:("Hey there, {pcn}. I'm glad you're all right.",
         "*singing badly* Hello, hello! I don't know why you say goodbye, I say hello.",
         "Arright!",),
    0.9:("Well it's very nice to see you, {pcn}.",
         "Arrigght!!",),
    1.0:("Hello, {toe}.",
         "{Toe}, hello again.",),
    },
"relaxed" : { # chill, talks about UFOs, aliens, acts like tripping, hippy-ish. Hugs people they love.
    0  :("Listen, you need to leave me alone.",
         "Listen, {slur}. You're ruining my {tod}.",
         "You are scum.",
         "God have mercy.",
         "{Slur}.",),
    0.1:("Dang, what a drag.",
         "Oh. {pcn}. I thought it was something important. *picks nose*",
         "Not you.",
         "I fart in your general direction.",),
    0.2:("Huh. Oh, it's only {pcn} again. Yea?",
         "Mm-hmm? What is it now, {pcc}?",
         "Oh. You.",),
    0.3:("Uh-huh? What is it?",
         "Oh, hey {pcn}. What's up?",
         "Oh, it's {pcn}.",),
    0.4:("Heyy.",
         "Hey, {pcgg}. What's hangin'? I mean -- how's it hangin'?",),
    0.5:("Yo, {pcn}. {Gcomp}.",
         "Dude, you're never going to believe this, but I saw a UFO the other day.",),
    0.6:("Hey, {pcn}. Good to see you, {pcgg}. What have you been up to?",
         "UFOs are real. I've seen one with my own eyes. They're real. Aliens are real.",),
    0.7:("Aw, yea. It's my friend, {pcn}.",
         "Yo, {pcgg}. You want a beer?",
         "What's up, {pcgg}? You feelin' cool?",),
    0.8:("'Eyyy, how've you been, {pcgg}?",
         "Hey! So good to see you! *hugs*",
         "I promise you there are aliens out there, somewhere. It's just logical. I mean, think about it. Space is so vast, and there are so many planets with the necessary conditions for life.",),
    0.9:("{pcn}! Just the person I was hoping to see.",
         "Hello again, {toe}. *hugs*",
         "Hey, {pcn}. *smiles*",),
    1.0:("Heyyyy... how's it goin', my {toe}?",
         "Friend...! How nice you could come by. *hugs*",
         "*small but sincere smile*",),
    },
"uptight" : { # God-fearing, polite, kind, strict
    0  :("God will punish you.",
         "Jesus help you.",
         "Burn in hell, you wretched cur.",
         "You are the worst type of person.",
         "Yea, I know, you're a {slur}; everybody already knows, so you can just go home now. Bye.",),
    0.1:("Nobody likes you; nobody needs you.",
         "What is it? Can't you go bother someone else?",
         "I don't have the time nor the energy for you right now, {pcn}.",
         "I don't care for you. I don't know why I should help you, except that I'm just a saint.",),
    0.2:("Hmm. What is it? I do hope it will be quick.",
         "Yes, {pcc}?",
         "What is it, {pcgg}?",
         "Yes, {pct}{pcn}?",),
    0.3:("Yes, {pct}{pcn}? Is there something you need?",
         "Great {pcgp}.",
         "Oh, {pcn}. How are you.",),
    0.4:("What do you need?",
         "Great {pcgp}, are you in need of my assistance?",),
    0.5:("Greetings!",
         "Bonjour, great {pcgp}.",
         "A pleasure.",
         "Hello, {pcn}. So nice to see you on this fine {tod}.",),
    0.6:("Salutations.",
         "Greetings and salutations!",
         "An honor to be sure.",),
    0.7:("I am most honored, {pcn}. Please, the pleasure is mine.",
         "A pleasure to serve you.",),
    0.8:("How very nice to see you. I do hope that everything is all right.",
         "Most excellent.",),
    0.9:("Dear {pcn}, what a lovely encounter.",
         "Hello, {toe}. What brings you this way on this fine {tod}?",),
    1.0:("Hello, my lovely {pcn}. It's so wonderful to see you. {Comp}.",
         "Oh, hi, sweet {toe}. What a lovely visit. You can stay as long as you like.",
         "Oh, please, stay a while. I do ever so love when you come to visit.",),
    },
"proactive" : { # environmental advocate, outspoken, stubborn, opinionated. Hugs people they love the most
    0  :("People like you are the reason this country has gone to shit.",
         "Go back to kissing the president's ass, ass-kisser.",
         "I don't have time for anything else from you.",
         "You're a piece of shit human being.",
         "I'm sorry you had a shitty childhood, {pcgg}, but that's no excuse for being a complete {slur} all the time.",),
    0.1:("What gives you the right?",
         "What the hell is it now?",
         "Yes? I'm busy.",),
    0.2:("What is it, {pct}{pcn}?",
         "Mmm?",
         "Got something for me?",),
    0.3:("Mm? What is it, {pcn}?",
         "Oh, {pcn}. How are you this {tod}?",
         "Learn anything new?",),
    0.4:("What's goin' on? Any news?",
         "Hey {pcn}! What's new?",
         "Got anything new for me?",),
    0.5:("Hey, {pcgg}. Anything new?",
         "What's the news?",),
    0.6:("Hey, friend! How've you been lately?",
         "Hey {pcn}, what's new with you?",),
    0.7:("Hello, {toe}. Heard anything interesting lately?",
         "What's going on, {pcn}? *high fives*",),
    0.8:("Yo, {pcn}! I love your {icomp}. Where did you get it?",
         "What's new, {toe}?",
         "Hey there, {pcn}, what's the news?",),
    0.9:("Any news, {toe}? No? You just came to chat? That's OK. I've got time.",
         "Yay, it's my friend, {pcn}! *hugs*",),
    1.0:("Hi!! *hugs*",
         "It's so good to see you again, {pcn}! What have you been up to lately?",),
    },
"apathetic" : { # doesn't give much of a fuck
    0  :("*scowls in digust*",
         "*gives you the finger*",
         "Eat dogshit!",
         "What the fuck do you want?",
         "Fuck you.",),
    0.1:("What? What?",
         "What do *you* want? *scowls*",
         "What?",
         "*glances at you, then looks away*",),
    0.2:("Huh?",
         "Yea?",
         "Uh-huh?",
         "Yep?",),
    0.3:("Yea, {pcn}?",
         "Hey, {pcn}.",
         "Hey.",),
    0.4:("Yes?",
         "What is it?",
         "Hello.",),
    0.5:("Hey!",
         "Hello, {pcn}.",
         "'Sup, {pcgg}?",),
    0.6:("Hello!",
         "Hello, {pcn}!",
         "Hey, {pcn}!",
         "Yo, what's up?",
         "Hey, {pcgg}. What's going on?",),
    0.7:("Hey. Anything new?",
         "Hello, there.",
         "Hi. *smiles*",),
    0.8:("Hi, {pcn}!",
         "Hello! *smiles*",),
    0.9:("Heya, {pcn}. Good to see you.",
         "Yo, what's up, {pcgg}? *fist bumps*",),
    1.0:("Heya, {pcn}! Good to see you.",
         "How've you been?",
         "*fist bumps*",),
    },
}


    #------------#
    # Persuasion #
    #------------#

# small talk -- idle chit-chat between two people, generally acquaintances rather than close friends #

SMALLTALK_SUCCESS={ # could work differently than other messages:
            # all options are always available as long as you have >= the disposition requirement
"generic" : {
    0  :("That was strange.",
         "Oh, yeah. Right. That's good.",),
    0.1:("Yes, it's not bad.",
         "Good. And you?",),
    0.2:("MREs used to be a lot better.",
         "We live in strange times.",
         "Arright.",),
    0.3:("Nice weather we're having.",
         "I'm doing well, thanks. And you?",
         "Cool.",),
    0.4:("Water keeps getting more and more expensive.",
         "That's weird, I thought I left it right here...",
         "Great.",),
    0.5:("This is going to be a bad year for crops.",
         "Oh, good to hear.",),
    0.6:("It's a good day today.",
         "I didn't know that, that is something.",),
    0.7:("What a lovely day it's turned out to be.",
         "The weather's been feeling better these days, hm?",),
    0.8:("It's shaping up to be a wonderful {tod}.",
         "Well, that's very interesting.",),
    0.9:("I'm glad you came to chat. I've been looking forward to it.",
         "That's great to hear. I'm doing well, thank you.",),
    1.0:("Oh, I do enjoy our conversations. Please stay a while.",
         "So nice to hear it, {toe}. I've been doing well.",
         "Thanks for the update, {toe}.",
         "Oh, how nice.",),
    },
"proud" : {
    0  :("Reeeally.",),
    0.2:("Yes, I'm fine. Thanks.",
         "Yes, I'm doing very well. Thanks for your concern.",),
    0.4:("Good to hear. Yes, I'm doing well, as always.",),
    0.6:("Look at this picture of my dog. Isn't {she} so precious?",),
    0.8:("Look at this picture of my daughter. Isn't she so precious?",
         "Look at this picture of my newborn son. Isn't he so precious?",),
    1.0:("Look at this picture of my family. Aren't they just so precious?",),
    },
"low-self-esteem" : {
    0  :("Shitty day as usual.",),
    0.2:("Another day another nickel.",),
    0.4:("Yep, shitty weather as always.",),
    0.6:("I've been through the ringer this year, but I'm feeling a little better lately.",),
    0.8:("Shitty day. I'm feeling all right now, though.",),
    1.0:("I'm feeling a lot better now that you're here.",),
    },
"argumentative" : {
    0  :("Nah, it's definitely the complete opposite.",
         "Yeah, shitty day, all right.",
         "Yeah, I guess. Not really but sure.",
         "Whatever!",),
    0.4:("Oh no way. No way. *laughs*",
         "Well, I'm sure I could find something wrong with that statement.",),
    0.6:("I disagree, but that's an interesting opinion.",
         "It's not too bad, I suppose.",),
    0.8:("Yeah, today is all right, but you should have seen yesterday.",),         
    },
"non-confrontational" : {
    0  :("Ah..",
         "Yeah, that's right, all right.",),
    0.2:("Oh... I see, I see.",
         "Oh, for sure.",),
    0.4:("Hm... Interesting...",
         "Oh, absolutely.",
         "Indeed.",),
    0.6:("Indubitably.",),
    0.8:("You're absolutely right about that, {pcgg}.",),
    },
"outgoing" : {
    0.2:("Huh! That's something, all right.",),
    0.4:("Yes, I agree. It is nice.",
         "Oh yeah, I am excited about it.",),
    0.6:("Oh, how nice to hear, {pcn}.",),
    },
"shy" : {
    0  :("Oh, OK...",),
    0.2:("Oh, that's... nice.",),
    0.6:("I do enjoy the rain.",),
    1.0:("Yesterday I saw a deer.",),
    },
"independent" : {
    },
"codependent" : {
    },
"bubbly" : {
    },
"low-energy" : {
    0.4:("Lovely weather.",),
    0.6:("Indeed, {pcn}.",),
    },
"motivated" : {
    0.2:("I'm hype.",),
    0.4:("Corn stocks are *still* dropping. Can you believe it?",),
    0.6:("This is going to be a good decade for entrepreneurs.",),
    0.8:("I might be on to something.",),
    },
"unmotivated" : {
    },
"relaxed" : {
    0.4:("Hey {pcn}, you believe in aliens, right?",),
    0.6:("I wonder if that was a UFO I saw the other day...",),
    0.8:("What do you think it's like to be an alien? Like, would they feel the same kinds of emotions we do?",),
    },
"uptight" : {
    },
"proactive" : {
    0.4:("Well, more and more rivers are running dry these days. It's because the mega-corporations keep building more and more dams. It's terrible.",),
    0.6:("That's good news.",),
    },
"apathetic" : {
    },
}

SMALLTALK_FAILURE={
"generic" : {
    0  :("I don't want to talk to you.",
         "You're bothering me.",),
    0.2:("Let's just be quiet for a while.",
         "Ok.",),
    0.3:("Oh. Yea.",
         "Ah, hm.",),
    0.4:("Mm...hm.",
         "Ah. I see.",),
    0.6:("Oh. Wow.",
         "Hmmm. Is that right.",),
    0.8:("Huh. That's pretty cool.",),
    1.0:("Oh, that's super interesting.",),
    },
"argumentative" : {
    0  :("Who gives a shit?",
         "*laughs* You {nc}.",
         "Listen, {tof}. You and I are not pals. Give it up already.",),
    0.2:("No. Wrong.",
         "Well, whatever, who cares anyway?",
         "Who cares?",
         "Yeah. You're right, all right.",),
    0.4:("No disrespect, but that's demonstrably false.",
         "No, sorry, {tof}. That's wrong.",
         "Get your facts straight.",
         "I respect your right to your wrong opinion.",),
    0.6:("That's... not quite right.",
         "That isn't right.",
         "That's not what I remember, check your sources.",),
    },
"motivated" : {
    0  :("Shoo, fly.",
         "Shoo, fly, before I swat you.",
         "Shoo, shoo.",),
    0.2:("Who's got the time for that?",),
    },
"proactive" : {
    0.2:("Well, it'd be much nicer of a day if our own government didn't poison our air with mind-control gas.",),
    },
"relaxed" : {
    0.4:("Aliens are definitely real, {pcgg}.",
         "Did you read your horoscope for the week?",),
    0.6:("Have you ever felt anything... weird... in your... you know what, nevermind.",),
    },
}

# gossip -- like small talk, but slightly more intense and friendly #

GOSSIP_SUCCESS={
"generic" : {
    0  :("Ha. That's a good one.",
         "I'll remember that.",),
    0.2:("Mm, is that so?",
         "Well, that's pretty interesting.",),
    0.4:("Huh. Very interesting.",
         "Wow, I didn't know that.",),
    0.6:("Oh, really? *laughs*",
         "Ooh, that's juicy.",),
    0.8:("Oh my God, you're kidding!",
         "Oh, no...",),
    1.0:("What? She did what?!",),
    },
"shy" : {
    0.4:("No, you're kidding!",),
    0.6:("How awful!",),
    0.8:("*laughs* That's so funny, {pcn}.",),
    },
"uptight" : {
    0.2:("What has this country come to?",),
    0.4:("Well, I can't say I'm surprised.",),
    0.6:("What? Little Ms. Sally's girl? I knew their family would go downhill when they stopped going to Church on Sundays, but I never imagined it would come to this.",),
    0.8:("How very sad. What has become of our once great nation?",
         "My aunt Shirley has that same kind of thing. We visited her last summer, and she brought it out while everybody was eating at the dinner table. Uncle Morey would not stop laughing.",),
    },
}

GOSSIP_FAILURE={
"generic" : {
    0  :("Everybody already knows that, {slur}.",
         "Who gives a damn?",),
    0.2:("Nobody cares, {pcn}.",
         "That's none of my concern, nor yours for that matter.",),
    0.4:("What are you talking about?",
         "That's disgusting!",
         "Oh, {pcgg}, I heard an even better one just the other {tod}.",),
    0.6:("Wow. I didn't know you would stoop so low.",
         "Gross, {pcn}.",
         "That's nobody's business but their own.",),
    0.8:("You should just mind your own business.",
         "Oh, sorry, I don't like to talk about people behind their backs.",),
    },
"proactive" : {
    0  :("You ape.",
         "Barbarian.",),
    0.2:("What two grown men do in their own home is none of your business!",
         "I don't wanna hear about that. Not from you, anyway.",),
    0.4:("Oh, {pcgg}. That's just messed up.",),
    0.6:("How... how do you even know about that?",),
    0.8:("That's my sister you're talking about, {pcgg}.",),
    },
"relaxed" : {
    0.2:("Just keep your nose out of other people's shit!",),
    },
}

# ask question -- try to gain information about location, entity, entity class, etc. #

QUESTION_SUCCESS={
"generic" : {
    0  :("Fine, I'll tell you, {slur}.",),
    0.2:("I guess it wouldn't hurt to tell you.",),
    0.4:("OK, I'll tell you just this once.",),
    0.6:("No problem, I'd be glad to answer any questions you have.",),
    0.8:("Any more questions? Ask away.",),
    1.0:("Anything else, dear {pcn}?",),
    },
}

QUESTION_FAILURE={
"generic" : {
    0  :("Why on earth should I tell you that?",
         "I'll never tell, you {slur}.",
         "Give it up.",),
    0.2:("I'm not going to tell you that.",
         "Sorry, I can't tell you that.",),
    0.4:("Sorry, that's really not my place to say.",
         "I'm afraid I don't know the answer.",),
    0.6:("No, I can't tell you. I'm sorry.",),
    0.8:("I'm sorry, {pcn}. It's just something I can't say.",),
    1.0:("I'm terribly sorry, {toe}. I promised I wouldn't tell.",),
    },
}

# interrogate -- like questioning but more intense, more serious #

INTERROGATE_SUCCESS={
"generic" : {
    0  :("Fine! Fine! I'll sing!",),
    0.2:("All right, you got me.",),
    0.4:("I'll tell you whatever you need to know.",),
    0.6:("I'll tell you. You don't need to make such a big deal about it.",),
    0.8:("Calm down, {pcgg}. I'll answer your questions.",),
    1.0:("Oh, {pcn}, I wish you would ask nicely.",),
    },
}

INTERROGATE_FAILURE={
"generic" : {
    0  :("I'll never tell you in a million years.",
         "Get fucked.",
         "*spits on you*",),
    0.2:("No, I'm not gonna talk.",
         "You're gonna have to do a lot better than that.",),
    0.4:("Forget it, {pcc}.",
         "No, it's not going to happen.",),
    0.6:("I won't spill it.",),
    0.8:("I'm sorry, I just can't.",),
    1.0:("You're making me upset, {pcn}. Just calm down and let's think about this rationally.",),
    },
}

# torture -- threaten pain to get information or get them to do what you want #

TORTURE_SUCCESS={
"generic" : {
    0  :("*crying* Fine... I'll tell you. Just please, stop. I can't take it anymore.",
         "I'll tell you everything. Just don't hurt my family.",),
    0.2:("Yes! OK! I'll tell you, just promise you'll leave me alone if I do!",),
    0.4:("I can't believe you'd go to such measures. I'll tell you. Just stop.",),
    0.6:("I'll tell! I'll tell! Christ!",),
    0.8:("I can't take it anymore. Whatever you need me to do, I'll do it.",),
    },
}

TORTURE_FAILURE={
"generic" : {
    0  :("*sobbing* I don't know.",
         "Just please, stop.",
         "I can't take it.",
         "I think my heart is going to give out.",),
    0.2:("Never. I'll never tell.",
         "I'm not going to rat my friends out.",),
    0.4:("I can't tell you, so just give up.",
         "No. I won't tell you; not now or ever.",),
    0.6:("Why would you do this?",),
    0.8:("How could you do this to me?",),
    },
"motivated" : {
    0  :("You'll give out before I do.",),
    },
}

# ask favor -- ask someone to do something for you #

ASKFAVOR_SUCCESS={
"generic" : {
    0  :("I'll do it. But then I don't ever want to see you again.",),
    0.1:("This is the last time I'll ever help you.",),
    0.2:("Don't make me regret helping you.",
         "OK, but I'm not happy about it.",),
    0.3:("OK, I'll do it.",
         "Fine.",),
    0.4:("All right.",
         "Sure.",
         "Yep.",),
    0.5:("Sure, that's fine.",
         "Yes, I can do that.",),
    0.6:("OK, friend.",),
    0.7:("Yes.",),
    0.8:("I'll get it done right away.",),
    0.9:("That'll be easy.",),
    1.0:("I'll do it as soon as I can.",),
    },
"proud" : {
    0.2:("Don't make me regret taking pity on you.",),
    },
"unmotivated" : {
    0  :("What a drag.",),
    0.2:("Ugh, fine. Hold on...",),
    0.4:("Fine...",),
    },
"relaxed" : {
    0.2:("Eh, all right. Give me a second.",),
    0.4:("Yeah, no problem.",
         "Yeah.",),
    },
"bubbly" : {
    0.6:("Absofruitly.",),
    },
         
}

ASKFAVOR_FAILURE={
"generic" : {
    0  :("No. I won't do that.",
         "Not for you. Get lost.",),
    0.1:("Why would I do that for you?",
         "Come again? Who are you now?",),
    0.2:("You want me to do what?",),
    0.3:("No, I'm not going to do that for you.",
         "No. Sorry, but that's kind of innappropriate of you.",),
    0.4:("No, I won't do that.",
         "Sorry, that's something I'm not going to do.",),
    0.5:("Sorry, I can't do that for you.",),
    0.6:("No, sorry, {pcn}.",),
    0.7:("Oh, I'm sorry, I can't help you with that, {pcn}.",),
    0.8:("Oh, I can't. I'm really sorry...",
         "For my own sake, I can't help you with that.",),
    0.9:("Well I would love to help, but I really can't. Please forgive me.",
         "I care deeply for you, {pcn}, but I can't do that for you.",),
    1.0:("I don't think you could ever get me to do that, no matter what you did.",
         "I'm truly sorry, {pcn}. I can't.",),
    },
}

# beg -- like asking favor, but much more intense and needy #

BEG_SUCCESS={
"generic" : {
    0  :("Oh, what a pitiful creature. Get yourself some clean clothes.",),
    0.1:("*hands you a gift, avoiding eye contact*",),
    0.2:("Very well, you poor thing.",),
    0.3:("All right, I can see you are in desperate need.",),
    0.4:("OK, then. I can tell you're really out and out.",),
    0.5:("Damn, {pcgg}, you've had a rough {tod}, haven't you?",),
    0.6:("All right, all right. It's not a big deal.",),
    0.7:("Yes, I'll lend you a hand, {pcn}.",),
    0.8:("Yes, {pcn}, I can help you out.",),
    0.9:("OK, I'll do what I can.",),
    1.0:("Very well, dear {toe}.",),
    },
"motivated" : {
    0.5:("Sure, I can give you a loan if you need it.",),
    },
"codependent" : {
    0.5:("Hey, hey. You didn't have to beg.",),
    },
}

BEG_FAILURE={
"generic" : {
    0  :("*firmly* No.",),
    0.1:("No.",),
    0.2:("Sorry, no.",),
    0.3:("Sorry.",),
    0.4:("I can't, sorry.",),
    0.5:("Sorry, {pcgg}.",),
    0.6:("I'm afraid I can't swing it.",),
    0.7:("I'm really sorry, I simply can't.",),
    0.8:("I'm sorry, {pcn}. Not today.",),
    0.9:("I can't, {pcn}. I care about you, but I can't give you that.",),
    1.0:("I'm truly sorry.",),
    },
"proud" : {
    0  :("Pitiful. Just pitiful.",
         "Why would I give that to you?",),
    0.2:("How shameful.",
         "Do you have no shame?",
         "Only pathetic creatures beg in such an unsightly manor. Pathetic creatures are not fit to survive. They need to die out and make room for the strong.",),
    0.4:("How sad, that you would stoop to begging.",
         "What a sad little {pcc} you are.",),
    0.6:("{pcn}, you're acting so shamefully! Get a hold of yourself!",
         "Are you feeling all right, {pcn}? Perhaps you should see a doctor.",),
    0.8:("Listen, {pcn}... I care about you, and I'm willing to help you. But not like this. Don't beg. It's so shameful.",),
    },
"low-self-esteem" : {
    0  :("*pretends you don't exist*",),
    0.2:("*becomes noticeably uncomfortable*",
         "I don't have any to spare.",),
    0.4:("Oh, no, I'm poor myself.",
         "If you're like me, you probably deserve being so poor, anyway.",),
    0.6:("I feel terrible, but I simply can't...",),
    },
"argumentative" : {
    0  :("What's in it for me?",),
    0.2:("I wish, {pcgg}. Damn president fucked our economy so hard, I'll be lucky if I'm not on the streets begging just like you within the year.",),
    0.4:("No, {pcc}, sorry. There's not enough to go around these days.",),
    0.6:("Huh. So even you've been fucked by this new system of so-called leadership.",),
    },
"non-confrontational" : {
    0  :("*shuffles nervously away*",),
    0.2:("Oh, no...",),
    0.4:("Oh... I'm... I don't have any, sorry.",),
    },
"outgoing" : {
    0  :("Don't have it.",),
    0.2:("I can't. I wish I could.",),
    0.4:("Nah. Sorry, {pcgg}.",),
    },
"shy" : {
    0  :("*becomes extremely uncomfortable*",),
    0.2:("*quietly* Sorry.",
         "*quickly* No.",),
    0.4:("Oh... no, sorry...",),
    0.6:("I'm so sorry.",),
    0.8:("So sorry.",),
    },
"independent" : {
    0  :("Ugh, how very pathetic.",),
    0.2:("Get your own.",
         "Why? So you can buy another hit of morphine off the street?",),
    0.4:("I worked hard for this! I'm not just going to give it to you.",),
    },
"codependent" : {
    0.2:("I'd be glad to help, but I don't have enough for myself.",),
    },
"bubbly" : {
    0.6:("Ahh, I'm sorry!",),
    0.6:("Ahh, I'm sorry!",),
    0.8:("I'm really sorry, {pcn}.",),
    },
"low-energy" : {
    0  :("Aw man, I do not have the energy for this.",),
    0.2:("*sighs* I knew I shouldn't have skipped breakfast.",),
    0.4:("Yeah, and are you gonna work out these knots in my shoulders in exchange?",),
    0.6:("Aw, nah. Nah, sorry.",
         "Sorry, {pcn}. Really, sorry.",),
    },
"motivated" : {
    0  :("So pitiful.",),
    0.2:("Oh, no. Come on. Up you get.",
         "You've got to work for things in life, {pcc}.",
         "Would you steal food from my family's table?",),
    0.4:("Great {pcgp}, you're embarrassing yourself.",
         "Chin up, chap.",),
    0.6:("I have faith that you can get out of this yourself.",),
    0.8:("*sighs* The economy's taking a toll on everyone, {pcn}.",),
    },
"unmotivated" : {
    0.8:("So sorry.",),
    },
"relaxed" : {
    0  :("Take it easy, {tof}.",),
    0.2:("Chill, {tof}.",),
    0.4:("Relax, dude, everything's gonna be all right.",),
    0.6:("*singing* Don't worry / about a thing / 'Cuz every little thing / is gonna be all right",),
    0.8:("Aw, man. You're looking rough, {tof}.",),
    },
"uptight" : {
    0  :("Oh, how incredibly sad. Look at {pcgo}.",
         "Absolutely not.",),
    0.2:("I will pray for you.",
         "Poor cretin, what a terrible hand the world has dealt you.",),
    0.4:("I pray your situation improves, {pcc}.",
         "No, I can't do that, sorry, {pcc}. I pray you'll get through this.",),
    0.6:("It pains me to say it, but I have to decline.",),
    },
"proactive" : {
    0.2:("I'm sorry the system has beaten you down so hard, {tof}.",),
    0.4:("You didn't even do anything wrong. It's that damn government.",),
    0.6:("Oh, poor {pcn}. The man just beats you down at every turn. If I were a politician, I'd make some changes in this country!",),
    0.8:("Poor, pitiful {pcn}. It's so sad to see the best of {pcggs} succumb to this economy.",),
    },
"apathetic" : {
    0  :("Uh-uh.",),
    0.2:("Lazy {slur}.",),
    0.4:("Why should I help you?",
         "Who cares, {pcgg}?",),
    0.6:("Ugh. What a drag...",),
    0.8:("Man, what a pain.",),
    },
}

# barter -- buy / sell / trade / ask for gift #

BARTER_SUCCESS={
"generic" : {
    0  :("OK.",
         "*silently accepts the deal*",
         "*weak smile, nods*",),
    0.2:("All right, then.",
         "I suppose I can do that.",),
    0.4:("Very well, {pcc}.",
         "That will suffice, {pcc}.",
         "Very well, {pcn}.",
         "All right, then. Let's shake on it.",),
    0.8:("*smiles* It's a deal.",
         "Sounds like a deal to me.",),
    1.0:("Thank you kindly, dear {pcn}.",),
    },
}

BARTER_FAILURE={ # range: as long as disp >= value, can display msg (like taunt and smalltalk)
"generic" : {
    0  :("*laughs* Do you take me for a fool?",
         "*laughs uproariously*",
         "*laughs* No.",
         "*laughs* Absolutely not.",
         "What an absurd offer.",
         "Are you mad?",
         "Would you have my family starve?",
         "You insult me with such an offer.",
         "How insulting!",
         "No way!",
         "Ridiculous.",
         "My family will go hungry with trades like that!",),
    0.4:("Not going to happen, {pcc}.",
         "*exhales sharply* Good one. No.",),
    0.6:("Are you all right in the head, {pcn}?",),
    0.8:("No, {pcn}. I can do half that.",),
    },
"bubbly" : {
    0.8:("No! No matter how much I like you, I can't do a deal like that.",),
    },
"argumentative" : {
    0  :("Hell no!",
         "Hell no.",
         "Fuck no.",
         "No way, absolutely not.",
         "I guess I will kick your teeth in if you really want me to so badly. That's what you were thinking would make that transaction even, right?",),
    0.2:("Outrageous!",),
    },
"outgoing" : {
    0.4:("I'd never make a deal like that!",),
    },
"motivated" : {
    0  :("You must be mad, {pcgg}.",
         "You've lost your marbles!",
         "Great {pcgp}, you will put my entire family out of business.",
         "*laughs heartily* That is a funny joke, {pcgp}.",
         "You would steal the bread right from my kid brother's tounge if given the chance!",),
    },
}

# charm -- temporarily increase disposition #

CHARM_SUCCESS={
"generic" : {
    0  :("Oh, that is nice.",
         "Thanks.",),
    0.1:("Well, how thoughtful.",
         "Oh. Thank you.",),
    0.2:("That's very nice.",
         "Hm. Well, thanks.",),
    0.3:("Thank you, {pct}{pcc}.",
         "Thanks.",),
    0.4:("Thanks, {pcn}. That's very kind.",
         "Oh. Thanks.",
         "Thanks, {gcomp}.",),
    0.5:("Oh, thank you, I like your {icomp}.",
         "Thank you, {pcn}.",
         "You're not looking half bad, yourself.",
         "Thanks. I like your {icomp}.",),
    0.6:("Please, you're too kind.",
         "Aw, thank you.",
         "*smiles* Oh, thanks for noticing.",
         "Thanks, I like your {icomp}!",),
    0.7:("Oh, thank you so much, {pcn}, I like it too.",
         "Yes, it's my favorite, too.",
         "Oh thanks! Yours is also great.",
         "Thanks! I love your {icomp}.",),
    0.8:("Oh, {pcn}, thank you.",
         "Thanks! I love your {icomp}!",),
    0.9:("Oh, well thank you, dear {pcn}.",
         "Thanks, sweet {pcn}. {comp}.",),
    1.0:("Thank you, my dearest {pcn}.",
         "*smiles widely*",),
    },
"proud" : {
    0  :("*standing up straight* Oh, please. You're too kind.",),
    0.4:("*proudly* Oh, stop. You're embarrassing me!",),
    0.6:("*smiling* Oh, no, that's too much. Too much.",),
    },
"low-self-esteem" : {
    },
"argumentative" : {
    },
"non-confrontational" : {
    },
"outgoing" : {
    0.6:("*smiling* Oh, quit it, you.",),  
    },
"shy" : {
    0.2:("Thank... you.",),
    0.4:("Thanks, um... {pcn}.",),
    0.6:("Oh, {pcn}... Thank you...!",),
    0.8:("Thank you, {pcn}! You're so sweet.",),
    },
"independent" : {
    },
"codependent" : {
    },
"bubbly" : {
    0.6:("Aww, thank you so much! *hugs*",),
    },
"low-energy" : {
    },
"motivated" : {
    0.6:("Absolutely!",),
    },
"unmotivated" : {
    },
"relaxed" : {
    },
"uptight" : {
    0  :("Perhaps I misjudged you.",),
    0.4:("My, aren't you charming?",),
    },
"proactive" : {
    },
"apathetic" : {
    },
}

CHARM_FAILURE={
"generic" : {
    0  :("*nauseous expression*",),
    0.1:("Gross.",),
    0.2:("Ew.",),
    0.3:("*shuffles uncomfortably*",),
    0.4:("*bares teeth*",),
    0.5:("*cringes*",),
    0.6:("*shivers in embarrassment*",),
    0.7:("Stop, {pcn}. You're embarrassing me.",),
    0.8:("Really, {pcn}?",),
    0.9:("Oh, cut it out.",),
    },
"proud" : {
    0  :("Oh, please. That's not even close to my best feature.",
         "You're embarrassing yourself, {toe}.",),
    0.2:("Ha! *That's* what you chose to compliment? Says a lot about who *you* are.",
         "Oh, {toe}, stop.",),
    0.4:("Pff, please!",
         "What?",
         "Come again? Did you really just say that?",),
    0.6:("Bitch, please!",),
    },
"low-self-esteem" : {
    0  :("Stop. You're lying.",
         "I know you don't mean that.",
         "That's a big lie and you know it.",
         "Liar!",
         "Stop lying to me.",
         "I can't stand people lying to me all the time. Just stop.",),
    },
"argumentative" : {
    0  :("Wow, that was just sad.",),
    0.2:("Oh, man. What a blunder, {tof}.",),
    },
"non-confrontational" : {
    },
"outgoing" : {
    },
"shy" : {
    },
"independent" : {
    0  :("Blech. You trying to give me diabetes?",),
    },
"codependent" : {
    },
"bubbly" : {
    0  :("*imitates gag reflex*",),
    },
"low-energy" : {
    },
"motivated" : {
    },
"unmotivated" : {
    },
"relaxed" : {
    },
"uptight" : {
    },
"proactive" : {
    },
"apathetic" : {
    },
}

# boast -- temporarily increase disposition #

BOAST_SUCCESS={
"generic" : {
    0  :("*listens intently*",),
    0.1:("Hm.",),
    0.2:("Cool.",),
    0.3:("Oh, OK. Good for you.",),
    0.4:("Hm, that is pretty cool.",),
    0.5:("You've got good genes.",),
    0.6:("That's impressive.",),
    0.7:("Wow, seriously? Dang.",),
    0.8:("Woah. You're amazing.",),
    0.9:("Wow! I'm amazed.",),
    1.0:("I'm seriously impressed. You're extremely talented.",),
    },
"outgoing" : {
    0.4:("That's so great!",),
    0.6:("What?? *high-fives* that's awesome, {pcgg}!",),
    0.8:("I knew you could do it, {pcn}!",),
    },
"shy" : {
    0.4:("How nice, {pcn}.",
         "Keep going...",),
    0.6:("I'm so happy for you, {pcn}!",
         "That's awesome!",
         "Sugoi!",),
    0.8:("Amazing!",
         "You're amazing!",
         "Ah, sugoi...!",),
    },
"bubbly" : {
    0.4:("Cool! I can't believe you did that.",),
    0.6:("Wow, you're so cool!",),
    0.8:("Oh, {pcn}, you're just the coolest!",),
    },
}

BOAST_FAILURE={
"generic" : {
    0  :("Yeah, right. You?",),
    0.1:("Don't make me laugh.",),
    0.2:("You didn't do that.",),
    0.3:("I don't believe you.",),
    0.4:("I don't believe that for a minute.",),
    0.5:("Hm, that's... pretty unbelievable. As in, I don't believe it.",),
    0.6:("I don't think you could do that!",),
    0.7:("No way, you liar.",),
    0.8:("You're a liar! I know that isn't true.",),
    0.9:("I know you well enough to know that's a lie.",),
    1.0:("You're great, but not that great, I'm afraid.",),
    },
}

# bribe -- offer a gift in exchange for improved disposition #

BRIBERY_SUCCESS={
"generic" : {
    0  :("*quietly accepts the gift*",),
    0.1:("That will do, {pcc}.",),
    0.2:("Thank you, {pct}{pcc}.",),
    0.3:("Thank you, {pcn}.",),
    0.4:("Very well, {pcn}. I'll accept it.",
         "Thank you very much.",),
    0.5:("That's so nice. Thank you, {pcn}.",
         "That's very kind of you, {pcn}.",),
    0.6:("Wow, thanks, {pcn}. I owe you.",),
    0.7:("Thank you so much, {pcn}. I'll pay you back.",),
    0.8:("Thanks a bundle!",),
    0.9:("Thank you very much, {pcn}.",),
    1.0:("*grins* Thank you.",),
    },
"outgoing" : {
    0  :("Maybe you're not as bad as I thought you were.",),
    0.2:("You did me a solid. I owe you.",),
    0.4:("I owe you one. Thanks.",),
    },
"shy" : {
    0.2:("Well, I guess it wouldn't hurt just this once.",),
    0.4:("Um... OK.",),
    0.6:("Oh, um... Thanks, {pcn}...! *smiles nervously*",),
    0.8:("Oh... Thanks! *smiles shyly*",),
    },
"motivated" : {
    0.4:("Perhaps we can work something out after all.",),
    0.6:("Thanks a million!",),
    0.8:("Thank you kindly, great {pcgp}. I shall pay you back in earnest.",),
    },
}

BRIBERY_FAILURE={
"generic" : {
    0  :("What kind of {npcgg} do you think I am?",),
    0.1:("No way I'd accept that from you.",),
    0.2:("No, thank you.",
         "No. *puts hand up in a 'stop' sign*",),
    0.3:("No, I don't want it.",),
    0.4:("No. I don't need it.",),
    0.5:("Sorry, I don't have need for that.",),
    0.6:("No, {pcn}. I can't accept that.",),
    0.7:("I'm sorry, but I can't take that.",),
    0.8:("No, you keep that.",),
    0.9:("Oh no. Keep your valuables, I can manage.",),
    1.0:("No, no. It's too much to accept, {pcn}.",),
    },
"motivated" : {
    0.2:("I am not a charity case!",),
    0.4:("I do not need your pity.",),
    },
"uptight" : {
    0.2:("No. I refuse.",),
    0.4:("I refuse to accept that, {pct}{pcc}.",),
    0.6:("No, {pcn}. It's very kind, but no.",),
    0.8:("You've done more than enough for me already.",
         "You're very kind, but I have to decline, and that's final.",),
    },
}

# intimidate -- scare using IDN stat to raise disposition,
# but also gives the Mistreated component,
#   which makes them quick to turn on you if given the opportunity.
#   (unless they have the Masochist component)

INTIMIDATION_SUCCESS={ # disp >= value: displays (like pester, smalltalk, barter, intimidation, taunt)
"generic" : {
    0  :("*screams*",
         "No, please, don't hurt me!",
         "Oh, {cuss}!",),
    0.2:("No!",
         "No, don't!",),
    0.4:("Why?!",
         "{Tof}! Ah, {cuss}!",),
    0.6:("*shrinks away in terror*",
         "No! Why are you doing this?",),
    },
"bubbly" : {
    0  :("*screams* Ahhhhhh!! I'm being raped!",),
    },
"proud" : {
    0  :("I'll make you eat those words!",),
    },
"outgoing" : {
    0.6:("*screaming* {pcn}! You {slur}!",
         "Damn you, {pcn}!",),
    },
"shy" : {
    0  :("*whimpers in terror*",
         "*shaking, backing away*",
         "*crying*",),
    0.6:("*screaming* You're so scary!",),
    },
}

INTIMIDATION_FAILURE={
"generic" : {
    0  :("You don't scare me.",
         "*ignoring you*",),
    0.2:("*visibly annoyed*",
         "Stop!",),
    0.4:("Don't do that!",
         "Ah, {slur}.",),
    0.6:("*half-hearted yelp*",
         "*startled*",),
    0.8:("Stop, {pcn}!",
         "{pcn}!",
         "No!",),
    },
"proud" : {
    0  :("As if I could ever be bested by the likes of you!",
         "You're comparing yourself to me? Ha! You're not even good enough to be my fake.",
         "Boooo!",
         "You suck!",),
    },
"low-self-esteem" : {
    0  :("I'm not afraid of you!",),
    },
"argumentative" : {
    0  :("Wow, you should work in haunted houses.",
         "Oh, you're soooo scary. I'm soooo scared.",
         "Oh, I pissed my pants, ah.",
         "Ooooh, so spoopy.",),
    },
"non-confrontational" : {
    0  :("*looks at you with wide eyes, looks away*",
         "*aggressively ignoring you*",),
    },
"outgoing" : {
    0  :("I'm not afraid, {slur}.",
         "Blah, blah, blah.",
         "Yeah, yeah.",
         "Go on, I'm listening.",
         "Keep talking.",
         "Prick.",),
    },
"shy" : {
    0  :("Stop... you're scaring me...",
         "*tears in eyes* Quit it...!",
         "Leave me alone!",),
    },
"independent" : {
    0  :("Ho. That scared me good, all right.",),
    },
"codependent" : {
    0  :("Total {slur}.",),
    0.4:("Aw, why would you do that?",),
    },
"bubbly" : {
    0  :("*screams* Help me, this {pcgg}'s trying to rape me!",),
    0.6:("*twitches, slaps you*",),
    },
"low-energy" : {
    0  :("Bruh...",),
    },
"motivated" : {
    0  :("Did you think I would submit so easily?",
         "You're no match for me!",
         "I will not be bested by the likes of you, great {pcgp}.",),
    },
"unmotivated" : {
    0  :("Dude, what's your problem?",),
    },
"relaxed" : {
    0  :("Aliens are scarier than you.",),
    },
"uptight" : {
    0  :("*standing up straight, looking you in the eye*",
         "HA!",
         "Just try it.",
         "You think I would fall for that? You must think I'm pretty naive.",),
    },
"proactive" : {
    0  :("*sneers*",),
    },
"apathetic" : {
    0  :("Oh fuck. I can't believe you've done this.",),
    },
}

# debate -- argue; talk about something possibly intense to try and raise disposition #

DEBATE_SUCCESS={
"generic" : {
    0  :("You're not wrong. You're just {aslur}.",),
    0.1:("Well, whatever.",),
    0.2:("OK, I guess you're right.",),
    0.3:("Oh. All right, then.",),
    0.4:("Huh. You learn something new every day.",),
    0.5:("Well, what do you know about that?",),
    0.6:("That's funny. Well, I learned something new.",),
    0.7:("Hmm... Is that right?",),
    0.8:("Well, I stand corrected.",),
    0.9:("You're right, {toe}.",),
    },
"outgoing" : {
    0.1:("I agree that you're {aslur}.",),
    },
"uptight" : {
    0  :("Hmph!",
         "Argh...",),
    0.4:("Is that so?",),
    0.6:("Well, maybe I'm not remembering it correctly.",),
    },
}

DEBATE_FAILURE={
"generic" : {
    0  :("I'm not going to waste any more of my time with you.",),
    0.1:("Liar.",
         "You're wrong.",),
    0.2:("That's not true.",
         "Nope.",
         "That's not even an argument.",),
    0.3:("You're just splitting hairs.",
         "That's a boldface lie.",),
    0.4:("That doesn't sound right.",
         "Ah. Well, I learned it differently.",
         "Well, I can see you're not going to budge on this.",),
    0.5:("I don't believe a word you're saying.",
         "Uh... really? I don't think so.",
         "You're just arguing semantics.",),
    0.6:("Yeah, right, {pcgg}!",
         "*dubiously* Mm... Mm-mm.",
         "That's not true and you know it.",),
    0.7:("That's not what I heard.",
         "*shakes head*",),
    0.8:("We'll just have to agree to disagree.",
         "*facepalm*",),
    0.9:("Well, you might be right. But I'm not changing my mind.",
         "Oh, come on!",),
    },
"proud" : {
    0  :("Ha! You {nc}, you should have just kept your mouth shut. Then you wouldn't look like such {anc}.",
         "I'm embarrassed for you, {tof}.",
         "You're making such a fool of yourself, {pct}{pcc}.",
         "What a joke.",
         "*laughs at you*",
         "Man, you're so smart.",
         "Can you believe this {pcgi}? Who does {pcgs} think {pcgs} is?",
         "Ah. I see your preschool has prepared you well for debating with me, who has earned a Ph.D in rhetoric.",),
    },
"low-self-esteem" : {
    0  :("All right. You win. {Slur}."),
    },
"argumentative" : {
    0  :("No. Wrong.",
         "Well, whatever, who cares anyway?",
         "Who cares?",
         "Yeah. You're right, all right.",
         "You complete {nc}, arguing with you is a waste of time.",
         "Ah. I see. So you're an intellectual, are you.",),
    0.4:("That's a weak defense at best.",
         "No disrespect, but that's demonstrably false.",
         "No, sorry, {tof}. That's wrong.",
         "Get your facts straight.",
         "I respect your right to your wrong opinion.",
         "That's a logical fallacy.",),
    0.6:("That's... not quite right.",
         "That isn't right.",
         "That's not what I remember, check your sources.",),
    },
"non-confrontational" : {
    0  :("Right. OK. No, yeah, you're right.",
         "Ah. I see.",
         "Yeah yeah. Whatever you say...",),
    0.2:("*dubiously averts eyes*",
         "Whatever you say.",),
    0.4:("OK, sure...",
         "Whatever.",),
    },
"outgoing" : {
    0  :("What a load of horseshit.",
         "*rolls eyes*",
         "Bullshit.",),
    0.4:("Oh, please, {pcn}. You're so full of shit.",
         "*laughs, rolls eyes*",),
    0.6:("*rolls eyes* Please!",
         "*laughs* Good one, {pcn}.",),
    },
"shy" : {
    0  :("Oh... Um... Well, you see... Oh! Nevermind...",
         "I think... Um, that's not exactly right...",),
    0.4:("Oh no, that's not true...",),
    0.6:("No... I disagree...",),
    },
"independent" : {
    0  :("That's it, I'm done.",
         "I don't need this.",
         "You're completely backwards.",),
    0.2:("I don't have time for this.",),
    },
"codependent" : {
    0  :("That's not true, {slur}.",),
    0.4:("You're so full of shit, your eyes are brown.",),
    },
"bubbly" : {
    0  :("That's bullshit, you liar.",
         "Bullshit.",),
    0.2:("Don't lie.",),
    0.4:("Don't lie, {pcn}.",),
    0.6:("*sarcastically* OK. You're right, {pcn}.",
         "Don't lie to me.",),
    0.8:("*sarcastically* You're right, {toe}.",
         "Don't lie to me!",),
    },
"low-energy" : {
    0  :("*falls backward in exasperation*",
         "What a load.",),
    0.2:("Whatever, {tof}.",
         "Where did you hear that?",),
    0.4:("All right, sure. We'll go with that.",),
    },
"motivated" : {
    0  :("Good day to you, {pcgp}.",
         "Well, I never.",),
    0.2:("Great {pcgp}, I do believe you are mistaken.",
         "That is quite untrue.",
         "Quite the falsehood, indeed.",),
    0.4:("You must be mistaken, old chap. There are actually two different ways to go about the business, you see...",),
    },
"unmotivated" : {
    0  :("K.",
         "Ah.",
         "Cool.",
         "*raises eyebrows*",),
    0.2:("Hmmm. 'That right.",),
    0.4:("*feigns interest*",),
    },
"relaxed" : {
    0  :("Dude, no need to get so worked up about it.",
         "All right, {tof}. It's not that big a deal.",),
    0.2:("I would have come to a similar conclusion if I was in your shoes.",),
    0.4:("It sounds reasonable, but there's a flaw in your logic.",),
    0.6:("Duuude. That was like, so far gone, man.",),
    },
"uptight" : {
    0  :("*scoffs* Well! I never!",
         "*scoffs, raises eyebrows*",),
    0.2:("What on Earth gave you that idea?",),
    },
"proactive" : {
    0  :("{Tof}, did you even go to college?",
         "That's just crock of donkey shit.",
         "How far up your own ass did you have to climb to find that nugget of gold?",),
    0.2:("No. Sorry, that's false.",
         "Mercury in our fish.",
         "Fish. Mercury.",),
    0.4:("Well no, that's been disproven.",
         "We should totally just stab Caesar!",),
    0.6:("It's the damn government releasing chem trails into our air, making all our kids autistic.",),
    },
"apathetic" : {
    0  :("Who cares.",
         "Doesn't matter anyway.",
         "We're all going to die anyway, so what does it matter?",
         "Nothing matters at the end of the day.",
         "It's not worth it.",
         "*sighs, shakes head*",),
    },
}

# pester -- annoy someone in an effort to make them dislike you or lose temper. Always results in loss of disposition. #

PESTER={ # range: >= (like taunt, smalltalk, etc.)
"generic" : {
    0  :("*ignoring you*",),
    0.2:("How bothersome.",
         "Stop that.",
         "Quit doing that.",),
    0.4:("How annoying!",
         "Stop.",
         "Stop it.",
         "Stop doing that.",),
    0.6:("Man, you are annoying.",
         "Why do you do the things that you do?",),
    0.8:("Are you trying to make me hate you? Because it might be working.",),
    },
"proud" : {
    0.2:("*simmering*",),
    0.4:("*blood boiling*",),
    0.6:("*visibly losing temper*",),
    0.8:("Oh man, I'm so ashamed to know you right now.",
         "*laughs* You're {aslur}.",),
    },
"low-self-esteem" : {
    0  :("Yep. I deserve this.",
         "I hate you.",),
    0.2:("*tries to ignore you*",
         "*frowns*",),
    0.4:("Yeah it'd be about 20% cooler if you would stop. But you know, it's up to you.",),
    0.6:("Please stop.",),
    },
"argumentative" : {
    0  :("Were you dropped on your head as an infant?",
         "Did your mother feed you bleach instead of baby formula?",
         "Why are you the way that you are? I hate so much about the things that you choose to be.",
         "{Slur}!",
         "{Slur}.",),
    0.2:("You {slur}!",
         "You fucking {slur}.",),
    0.4:("Shut up, {slur}.",
         "{Tof}, shut up, {pcn}, you god damn {nc}.",),
    0.6:("Stop it, {tof}. Come on.",),
    0.8:("Come on, man!",
         "Really!?",),
    },
"non-confrontational" : {
    0  :("*quietly* ...Quit...",
         "*mumbling*",),
    0.2:("...Please, don't.",),
    0.4:("*mumbling* I wish you would... Not do that...",),
    0.6:("Why?",),
    0.8:("What do you gain from this?",),
    },
"outgoing" : {
    0  :("Ugh!",
         "Cut it out, seriously.",
         "Cut it out, {pcgg}.",),
    0.2:("Oof.",
         "Please stop, {pcn}.",),
    0.4:("Quit it, {tof}.",),
    0.6:("{Tof}! Quit!",),
    0.8:("Agh! I hate it when you do that!",),
    },
"shy" : {
    0  :("...",
         "Uh...",
         "Please, go away...",),
    0.2:("Um... Please, stop...",
         "*trying hard to ignore you*",
         "*frowns deeply*",),
    0.4:("...Stop, {pcn}.",),
    0.6:("Stop... You're bothering me.",),
    0.8:("You're going to make me cry.",
         "Quit it, {pcn}, you're gonna make me cry...",),
    },
"independent" : {
    0  :("Buzz off.",
         "Eat my shit.",),
    0.2:("I don't need this.",
         "OK. We get it. You're a {slur}.",),
    0.4:("You can go now, {pcc}.",
         "I'd appreciate if you would leave.",),
    0.6:("I'd appreciate if you would leave, {pcn}.",),
    0.8:("{pcn}. What are you doing.",),
    },
"codependent" : {
    0  :("...God.",
         "*smiles* Jesus Christ.",
         "*laughs* Fucking hell.",),
    0.2:("*laughs* You're such a fucking weirdo.",
         "*laughs* Gross.",),
    0.4:("Ew. You showed your true colors again. Put that away, {tof}.",),
    },
"bubbly" : {
    0  :("*extremely drawn out sigh*",
         "*exaggerated angry expression*",),
    0.2:("Stop, {tof}.",
         "No.",
         "Ughhh.",),
    0.4:("Nooo!!!",
         "No!! Quit it!",
         "*suicide gesture*",
         "{pcn}!",
         "{tof}!",),
    0.6:("{pcn}, I'm going to slap you silly if you don't stop doing that.",
         "Cut it out, {tof}! I mean it!",),
    0.8:("Stop, {pcn}! I love you but you're driving me up the wall!",),
    },
"low-energy" : {
    0  :("You {nc}.",
         "{Insult}.",
         "{Slur}.",),
    0.2:("Dude, what is your problem?",
         "What is wrong with you?",
         "*exaggerated facepalm*",),
    0.4:("What is your major malfunction, {tof}.",
         "I already woke up with a headache this morning.",
         "God have mercy.",),
    0.6:("Ughhh. Not again.",),
    0.8:("{pcn}, I really don't have the energy for this.",),
    },
"motivated" : {
    0  :("Gentlemen, this is democracy manifest.",
         "Get your hand off my penis!",
         "What is the charge? Eating a meal? A succulent Chinese meal?",
         "Oh, that's a nice headlock, {pcgp}!",
         "Ahhh yes -- I see that you know your Judo well.",
         "And you, {pcgp}? Are you waiting to receive my limp penis?",),
    0.2:("Great {pcgp}, I implore you, desist.",
         "What a great {nc} you are!",),
    0.4:("Great {pcgp}. It appears you have been possessed by some imp.",
         "Oh, do go on, great {pcgp}! I will ever so enjoy smashing your face in.",),
    },
"unmotivated" : {
    0  :("I can't deal with this shit today.",),
    0.2:("Ugh, man. What a drag.",),
    0.4:("What a pain!",),
    0.6:("Bother, bother.",),
    },
"relaxed" : {
    0  :("Duuude.",
         "What the fuck, {tof}?",
         "Bruh.",),
    0.2:("You can't make me lose my temper. I'm like a Shaolin monk.",
         "See I can take the punches, man; I'll outlast you.",),
    0.4:("I'm not falling for it, {tof}.",
         "Bro, chill the fuck out.",),
    0.6:("Nah, {tof}. Just nah.",),
    },
"uptight" : {
    0  :("You're naught but a burden.",
         "Buzz, buzz, bothersome fly.",
         "Curse you, cur!",),
    0.2:("Bothersome creature."
         "A curse upon you.",
         "You pest!",
         "What on God's green Earth are you doing, {pcgg}?",),
    0.4:("Cut it out, {pcn}.",
         "{Pcgg}, cut that shit out. It's a bad habit.",
         "Curse you, {pcn}.",
         "Burdensome pest!",),
    0.6:("What's gotten into you?",
         "Are you feeling all right?",
         "Curse you, {pcn}, you pest!",),
    },
"proactive" : {
    0  :("Help, help! I'm being oppressed!",),
    0.2:("I don't need this.",),
    0.4:("Stop now.",),
    0.6:("You can stop now.",),
    0.8:("I'd really appreciate it if you didn't do that, {pcn}.",
         "Please, stop.",),
    },
"apathetic" : {
    0  :("*no reaction*",),
    0.2:("*stares at you*",),
    0.4:("{Slur}.",),
    0.6:("*laughs* You {slur}.",),
    0.8:("{Insult}.",),
    },
}

# taunt -- try to make them lose temper so they will fight you. Success results in loss of disposition. Failure may also lose disposition. #

TAUNT_SUCCESS={
"generic" : {
    0  :("Let's take this outside.",
         "I'll make you regret this!",
         "Do you want to die, {slur}?",
         "{Slur}!",),
    0.2:("You {slur}!",),
    0.4:("If you're looking for a fight, you've found one.",),
    0.6:("Sure, I'll kick your ass for you.",),
    0.8:("You're asking for it.",),
    },
"proud" : {
    0:  ("Die!",),
    0.2:("That's it. I'm gonna knock your teeth in.",),
    },
"low-self-esteem" : {
    0  :("{Slur}! Fucking {slur}! Fuck you!",),
    },
"argumentative" : {
    0  :("I'll kill you!",
         "I am going to kick your ass.",),
    0.2:("I'll teach you a lesson you won't forget, little kid.",
         "{Slur}. You think you can beat me?",),
    0.4:("You little {slur}, I'll kill you!",),
    },
"non-confrontational" : {
    0.2:("I'm not going to enjoy kicking your ass.",),
    0.4:("I take no pleasure in this.",),
    0.6:("*sighs* you total {nc}.",),
    },
"outgoing" : {
    0.2:("Let's go. You ready, {slur}?",),
    },
"shy" : {
    0  :("*quietly enters a combat stance*",),
    },
"independent" : {
    0  :("Argh! That's it, I'm going to destroy you!",),
    },
"codependent" : {
    0.2:("So, you want a fight, huh? I'll abide.",),
    },
"bubbly" : {
    0.2:("*grinding teeth* You're going to raise my blood pressure!",),
    0.4:("Aghh! You {slur}!",),
    0.6:("I'm so going to hurt you!",),
    },
"low-energy" : {
    0  :("You're a {slur}.",),
    0.4:("Meanie.",
         "Jerk!",),
    },
"motivated" : {
    0  :("You have crossed the line, {pcgp}.",),
    0.2:("I will kick you in time to resume my studies!",
         "I take exception to that.",),
    0.4:("I am always ready for a friendly tussle, my great {pcgp}. *unrolling sleeves gesture*",),
    },
"unmotivated" : {
    0  :("Oh, man. What a drag. Looks like I'm going to have to bust some ass.",),
    0.4:("I'll slap you silly!",),
    0.6:("You {nc}. {Insult}.",),
    },
"relaxed" : {
    0  :("*sighs, enters combat stance* All right, let's make this quick.",),
    0.2:("That's the line, {pcgg}.",
         "All right, {tof}. Let's do this.",),
    0.4:("I'll make this quick.",
         "Don't worry, this won't hurt a bit.",),
    },
"uptight" : {
    0  :("All right then. Have at you, {slur}!",),
    0.2:("Well then, great {pcgp}, prepare yourself!",),
    0.4:("I'll not pull my punches!",),
    0.6:("By jove, you've gone mad. I'll knock some sense into you.",),
    },
"proactive" : {
    0  :("So this is what it's come to.",),
    0.2:("You {slur}! Do you think I'll let you get away with this?",),
    0.4:("I'll never forgive you for this!",),
    },
"apathetic" : {
    0  :("Let's see what you're made of.",
         "*sighs* I guess I have no choice.",
         "*deadpan enters combat stance*",),
    },
}

TAUNT_FAILURE={ # taunt is different: as long as disposition >= ratio, then message can appear
"generic" : {
    0  :("What a {slur}.",
         "*ignoring you*",),
    0.2:("Stop it. Now.",
         "Please stop.",),
    0.4:("*annoyed expression*",
         "Ugh. Leave me alone, {pcgg}.",
         "Stop it!",),
    0.6:("Leave me alone, {pcn}.",
         "Quit it!",),
    0.8:("Quit, {pcn}!",
         "*angry expression*",
         "Why are you like this?",),
    },
"proud" : {
    0  :("*laughs* Wow, you're such a {nc}.",
         "*scoffs*",
         "You're shit.",),
    0.2:("*laughs* Look at you. {Nc}.",
         "Guys, look at this fuckin' {nc}. {Pcgs} should be in a circus.",),
    0.4:("You're embarassing yourself.",),
    },
"low-self-esteem" : {
    0  :("Thanks for making my {tod} even worse.",
         "{Slur}.",),
    0.2:("You're mean.",
         "I know you are but what am I?",),
    0.4:("I know, but you don't have to be such a {slur} about it.",),
    },
"argumentative" : {
    0  :("Are you running for the biggest {slur} of the year award? You've got my vote.",),
    0.2:("If you continue I will be forced to use my power against you.",),
    0.4:("You're going to regret this, {pcn}. Back out while you still can.",),
    },
"non-confrontational" : {
    0  :("*ignoring you agressively*",),
    },
"outgoing" : {
    0  :("Piss off.",),
    0.2:("*stares in disbelief*",),
    0.4:("Why are you this way?",),
    },
"shy" : {
    0.2:("*whimpers*",),
    },
"independent" : {
    0  :("Ha, what a {nc}. Look at this guy.",),
    },
"codependent" : {
    0  :("No! Stop that!",
         "Quit!!!",
         "...!!!",),
    },
"bubbly" : {
    0  :("Jerk! What's your problem?",
         "Ugh!",),
    0.2:("*appears frustrated*",),
    0.4:("Don't do that, {pcn}.",
         "I want you to stop that.",),
    0.6:("Don't do that anymore!",
         "Don't do that again.",),
    },
"low-energy" : {
    0  :("What? What do you want from me, {pcc}?",
         "Just stop. It's not going to work.",),
    0.2:("*sighs*",),
    },
"motivated" : {
    0  :("Stop! Halt! Desist!",),
    0.2:("Great {pcgp}, please, desist!",),
    0.4:("Please, I implore you, great {pcgp}, ",),
    },
"unmotivated" : {
    0  :("Aughhh...",
         "*long, drawn out sigh*",),
    0.2:("What a bother.",
         "Geez. What a pain.",),
    },
"relaxed" : {
    0.2:("Woah, there, horsey.",),
    0.4:("Woah, just take it easy, man.",
         "Calm down, dude.",),
    0.6:("Woaah dude. Take like, a chill pill, {tof}.",
         "Chill, {tof}, chill!",
         "{pcn}, chill the fuck out.",),
    },
"uptight" : {
    0  :("Buzz off, bothersome pest.",),
    0.2:("By God, I am a good Christian {npcgg}, but I am not above teaching you a lesson now.",),
    0.4:("Do you kiss your mother with that mouth?",),
    },
"proactive" : {
    0  :("I'll beat your ass. I'm not afraid of you.",
         "What have you got?",),
    0.4:("Why are you trying to pick a fight?",),
    },
"apathetic" : {
    0  :("*very little reaction*",
         "*glances at you*",),
    },
}

# Flattery -- admiring, complimenting, etc. #

FLATTERY_SUCCESS={
"generic" : {
    0  :("Thanks.",
         "Mm-hm.",
         "Yep.",),
    0.1:("You're too kind.",
         "Thanks, {pct}",
         "That's nice.",),
    0.2:("Thanks, that's really nice.",
         "Thank you, {pcc}.",
         "Thank you.",
         "Thanks.",),
    0.3:("Well, thanks!",
         "How nice.",
         "Thanks!",),
    0.4:("Why, thank you!",
         "That's so nice, thanks.",
         "How nice! Thanks.",
         "Thank you.",),
    0.5:("You're such a sweetheart.",
         "That's very nice.",
         "Thanks, that means a lot.",
         "Oh, thank you! How very nice.",
         "Thank you!",),
    0.6:("Oh, I'm glad you think so.",
         "How nice. Thank you, {pcn}.",
         "Yes, I worked hard on it. Thanks for noticing.",),
    0.7:("Thanks, {toe}.",
         "Wow, thanks, {pcn}! You're looking good, too!",
         "I'm glad you think so.",),
    0.8:("What a wonderful compliment. Thank you, {pcn}.",
         "Thank you, my dear {pcn}.",
         "Thanks, {toe}. You're too kind.",),
    0.9:("Aw, thanks, {toe}!",
         "That's wonderful. Thank you, sweet {pcn}.",),
    1.0:("That means so much coming from you. Thank you, dearest {pcn}.",
         "I'm so happy you like it.",),
    },
"proud" : {
    0.2:("Well, it's about time someone noticed.",),
    },
"low-self-esteem" : {
    0  :("Are you my own personal hell manifest?",),
    0.1:("Yea, right. Don't make me laugh...",),
    0.2:("That's not true. But thank you.",),
    0.3:("No, I'm not that great. Thanks anyway.",
         "Oh, please. Give me a break.",),
    0.4:("Stop, you're exaggerating.",
         "No, really -- you're too much.",),
    0.5:("No, I don't deserve that praise. But thanks.",
         "Really, you're too much.",),
    0.6:("*weak smile*",
         "Thanks...",),
    0.7:("*starts, then pauses* Oh... thanks.",
         "It's too much, {pcn}. Thanks for the thought, though.",),
    0.8:("Thanks, that means a lot coming from you.",
         "I'm glad you like it!",),
    0.9:("I'm really glad you see it that way. I just wish I felt the same way about it.",),
    1.0:("What a lovely thing to say.",
         "Oh, thank you, {pcn}. Thanks so much.",),
    },
"motivated" : {
    0  :("Coming from you, that means nothing.",),
    0.1:("Yes, you are right. I am fabulous.",),
    },
}

FLATTERY_FAILURE={
"generic" : {
    0  :("Just quit it.",
          "*scowl*",
          "Ugh!",
          "Enough!",
          "I've had enough! Get lost!",),
    0.1:("Cool.",
          "Good for you.",
          "I don't care.",
          "*raises, then lowers eyebrows*",
          "Enough.",
          "Uh...",
          "I don't want to hear that from you.",),
    0.2:("Thanks but I don't need to hear that coming from you.",
          "*false smile*",
          "Ok, that's enough.",
          "I don't need to hear that from you.",),
    0.3:("Well, that's nice of you.",
          "Oh... thanks.",
          "Stop. You're too much, really.",
          "*grimaces*",
          "That's enough, now.",),
    0.4:("*frowns*",
          "Oh. Well, I can't say I agree with you on that one.",
          "I know you mean well, but now you're making me uncomfortable.",
          "Ok, you've said your fill. Let's change the subject.",),
    0.5:("I don't want to talk about this.",
          "Ok. Let's change the subject.",
          "*confused / upset expression*",),
    0.6:("*uncomfortable, forced smile*",
          "All right, {pcn}.",
          "K. Thanks.",
          "Well that's very nice, {pcn}. Anyway, is there something else you needed?",),
    0.7:("Hm. Ok.",
          "Ok, that's enough, please, let's talk about something different now.",
          "I have to disagree with you about that.",
          "I'm really not that great.",),
    0.8:("That's nice of you, {pcn}. But I'd rather you didn't say things like that.",
          "Right. Anyways.",),
    0.9:("Well I'm glad you like it, but let's get back to what we were talking about before.",),
    1.0:("Oh. Thank you... {pcn}.",),
    },
"low-self-esteem" : {
    0  :("*crying* I can't take any more of your lies.",
         "*crying* You're so mean!",
         "*sobbing*",
         "You're just evil.",),
    0.1:("Don't try to make me laugh.",
         "No. That's never been true.",),
    0.2:("Yeah, right. You just made that up.",
         "Hm. I wish.",),
    0.3:("You're just saying that.",
         "I know you're full of it.",),
    0.4:("You're lying.",
         "You're a liar.",
         "That's just ridiculous.",),
    0.5:("You liar!",
         "Yea, right. Come on, {tof}.",
         "I wish...",),
    0.6:("Stop it! I wish that were true.",),
    0.7:("Not that I don't think you're being sincere, but I just can't see it that way.",),
    0.8:("That's really nice of you to say, but... I can't believe you. It's not you, it's me...",),
    },
}

# flirtation -- making a pass, complimenting in a romantic or sexual way, suggestive language (flirting) #

FLIRTATION_SUCCESS={
"generic" : {
    0  :("*laughs nervously*",
         "*smiles, avoids eye contact*",),
    0.2:("*starts checking you out*",
         "*looks away*",
         "*glancing over you*",),
    0.4:("*giggles*",
         "*smiles, glances down*",),
    0.5:("*glances suggestively*",),
    0.6:("Hey... *smiles*",
         "*laughs, leans forward*",),
    0.7:("Hey, {flirt}.",
         "*bites lip*",),
    0.8:("Hey there, {flirt}. Are you free this Friday?",
         "You're not too bad, yourself.",
         "*flutters eyes*",),
    0.9:("*suggestive smile*",
         "*opens mouth in horniness*",),
    1.0:("*looks suggestively at your lips*",
         "*shows tounge*",),
    },
"outgoing" : {
    0.8:("*goes in for a kiss*",),
    },
"bubbly" : {
    0.4:("*blows kiss*",),
    },
}

FLIRTATION_FAILURE={
"generic" : {
    0  :("I'm extremely uncomfortable right now.",
         "*disgusted expression*",),
    0.1:("Oh -- sorry, I can't.",
         "Not with you. No.",
         "Please, stop. You're making me so uncomfortable.",
         "Don't make me call the cops.",),
    0.2:("Oh, I'm actually seeing someone.",
         "It's too much. Too sudden.",
         "You're making me very uncomfortable...",
         "*no response*",),
    0.3:("You're making me uncomfortable.",
         "*smiles, glances away*",
         "*ignoring you*",),
    0.4:("*stares at you*",
         "*looks away*",),
    0.5:("*tries to look busy*",
         "*leans away*",),
    0.6:("*shuffles nervously*",
         "*grumbles uncomfortably*",),
    0.7:("I'm sorry, {pcn}. You've got the wrong idea.",),
    0.8:("Sorry... I can't.",),
    0.9:("I'm sorry, {pcn}. You're very nice, but I just don't think of you in that way.",),
    1.0:("Oh, {pcn}. You're too much. Really.",),
    },
"outgoing" : {
    0  :("You {slur}, you don't mean any of that!",),
    },
"bubbly" : {
    0  :("Help, help! I'm being raped!",),
    },
}

# anger -- brought near the point of violent outbreak #

ANGRY={
"generic" : {
    0  :("I'm going to kick your ass.",
         "You're such a {nc}.",
         "{Slur}.",
         "{Nc}.",
         "{Insult}.",
         "*no response*",),
    0.2:("Hey. Shut up.",),
    0.4:("Who would do something like that?",
         "What a {nc}.",
         "What a {slur} you are.",
         "You absolute {nc}.",),
    0.6:("You're being a real {nc}.",
         "Stop being such a {slur}.",
         "You {nc}!",
         "Are you trying to piss me off?",),
    0.8:("You {nc}! I hate you! I can't believe you would do this!",
         "You absolute {nc}! What are you thinking?",
         "What's gotten into you?",
         "Quit trying to piss me off, {pcn}.",
         "You complete {nc} of a {pcc}. I'm going to smash your face.",),
    },
"outgoing" : {
    0  :("Are you ready to fight, {slur}?",),
    },
"argumentative" : {
    0  :("I'm about to curb-stomp your ass.",
         "Fucking {nc}, {insult}.",
         "*laughs* Look at this fuckin' {nc}.",),
    0.2:("You've made me really fuckin' mad.",
         "I will bury you.",
         "I'm not scared, you {nc}. Come at me, {tof}.",
         "You made a mistake, kiddo.",),
    },
"bubbly" : {
    0.4:("You {nc}, I'll eat you for breakfast!",),
    },
"motivated" : {
    0  :("I will have you know I am a skilled practitioner of the art of fisticuffs.",),
    0.4:("That's one step too far, great {pcgp}. You'd best keep quiet.",),
    0.6:("Have you gone mad, {pcgg}?",),
    },
}

_={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}



'''

"proud" : {
    },
"low-self-esteem" : {
    },
"argumentative" : {
    },
"non-confrontational" : {
    },
"outgoing" : {
    },
"shy" : {
    },
"independent" : {
    },
"codependent" : {
    },
"bubbly" : {
    },
"low-energy" : {
    },
"motivated" : {
    },
"unmotivated" : {
    },
"relaxed" : {
    },
"uptight" : {
    },
"proactive" : {
    },
"apathetic" : {
    },
    '''













