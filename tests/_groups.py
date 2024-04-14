import random

# from builtins import __builtin__

Set = frozenset # Data will be frozensets, so they can't be mutated.

def words(text):
    "All space-separated words in text."
    return Set(text.split())

def phrases(text, sep='/'):
    "All sep-separated phrases in text, uppercased and stripped."
    return Set(p.upper().strip() for p in text.split(sep))


winners = words('''washington adams jefferson jefferson madison madison monroe
    monroe adams jackson jackson van-buren harrison polk taylor pierce buchanan
    lincoln lincoln grant grant hayes garfield cleveland harrison cleveland mckinley
    mckinley roosevelt taft wilson wilson harding coolidge hoover roosevelt
    roosevelt roosevelt roosevelt truman eisenhower eisenhower kennedy johnson nixon
    nixon carter reagan reagan bush clinton clinton bush bush obama obama''')
losers = words('''clinton jefferson adams pinckney pinckney clinton king adams
    jackson adams clay van-buren van-buren clay cass scott fremont breckinridge
    mcclellan seymour greeley tilden hancock blaine cleveland harrison bryan bryan
    parker bryan roosevelt hughes cox davis smith hoover landon wilkie dewey dewey
    stevenson stevenson nixon goldwater humphrey mcgovern ford carter mondale
    dukakis bush dole gore kerry mccain romney''') - winners

boys = words('jacob mason ethan noah william liam jayden michael alexander aiden')
girls = words('sophia emma isabella olivia ava emily abigail mia madison elizabeth')

pharma = words('lipitor nexium plavix advair ablify seroquel singulair crestor actos epogen')
cities = words('paris trinidad capetown riga zurich shanghai vancouver chicago adelaide auckland')

foo = words('''afoot catfoot dogfoot fanfoot foody foolery foolish fooster footage foothot footle footpad footway
    hotfoot jawfoot mafoo nonfood padfoot prefool sfoot unfool''')
bar = words('''Atlas Aymoro Iberic Mahran Ormazd Silipan altared chandoo crenel crooked fardo folksy forest
    hebamic idgah manlike marly palazzi sixfold tarrock unfold''')

nouns = words('''time year people way day man thing woman life child world school
    state family student group country problem hand part place case week company
    system program question work government number night point home water room
    mother area money story fact month lot right study book eye job word business
    issue side kind head house service friend father power hour game line end member
    law car city community name president team minute idea kid body information
    back parent face others level office door health person art war history party result
    change morning reason research girl guy moment air teacher force education''')
adverbs = words('''all particularly just less indeed over soon course still yet before
    certainly how actually better to finally pretty then around very early nearly now
    always either where right often hard back home best out even away enough probably
    ever recently never however here quite alone both about ok ahead of usually already
    suddenly down simply long directly little fast there only least quickly much forward
    today more on exactly else up sometimes eventually almost thus tonight as in close
    clearly again no perhaps that when also instead really most why ago off
    especially maybe later well together rather so far once''') - nouns
verbs = words('''ask believe borrow break bring buy can be able cancel change clean
    comb complain cough count cut dance draw drink drive eat explain fall
    fill find finish fit fix fly forget give go have hear hurt know learn
    leave listen live look lose make do need open close shut organise pay
    play put rain read reply run say see sell send sign sing sit sleep
    smoke speak spell spend stand start begin study succeed swim take talk
    teach tell think translate travel try turn off turn on type understand
    use wait wake up want watch work worry write''') - nouns

# randoms = Set(vars(random))
# print(randoms)
# builtins = Set(vars(__builtin__)) - randoms

starwars = phrases('''The Phantom Menace / Attack of the Clones / Revenge of the Sith /
    A New Hope / The Empire Strikes Back / Return of the Jedi''')
startrek = phrases('''The Wrath of Khan / The Search for Spock / The Voyage Home /
    The Final Frontier / The Undiscovered Country / Generations / First Contact /
    Insurrection / Nemesis''')

dogs = phrases(''''Labrador Retrievers / German Shepherd Dogs / Golden Retrievers / Beagles / Bulldogs /
    Yorkshire Terriers / Boxers / Poodles / Rottweilers / Dachshunds / Shih Tzu / Doberman Pinschers /
    Miniature Schnauzers / French Bulldogs / German Shorthaired Pointers / Siberian Huskies / Great Danes /
    Chihuahuas / Pomeranians / Cavalier King Charles Spaniels / Shetland Sheepdogs / Australian Shepherds /
    Boston Terriers / Pembroke Welsh Corgis / Maltese / Mastiffs / Cocker Spaniels / Havanese /
    English Springer Spaniels / Pugs / Brittanys / Weimaraners / Bernese Mountain Dogs / Vizslas / Collies /
    West Highland White Terriers / Papillons / Bichons Frises / Bullmastiffs / Basset Hounds /
    Rhodesian Ridgebacks / Newfoundlands / Russell Terriers / Border Collies / Akitas /
    Chesapeake Bay Retrievers / Miniature Pinschers / Bloodhounds / St. Bernards / Shiba Inu / Bull Terriers /
    Chinese Shar-Pei / Soft Coated Wheaten Terriers / Airedale Terriers / Portuguese Water Dogs / Whippets /
    Alaskan Malamutes / Scottish Terriers / Australian Cattle Dogs / Cane Corso / Lhasa Apsos /
    Chinese Crested / Cairn Terriers / English Cocker Spaniels / Dalmatians / Italian Greyhounds /
    Dogues de Bordeaux / Samoyeds / Chow Chows / German Wirehaired Pointers / Belgian Malinois /
    Great Pyrenees / Pekingese / Irish Setters / Cardigan Welsh Corgis / Staffordshire Bull Terriers /
    Irish Wolfhounds / Old English Sheepdogs / American Staffordshire Terriers / Bouviers des Flandres /
    Greater Swiss Mountain Dogs / Japanese Chin / Tibetan Terriers / Brussels Griffons /
    Wirehaired Pointing Griffons / Border Terriers / English Setters / Basenjis / Standard Schnauzers /
    Silky Terriers / Flat-Coated Retrievers / Norwich Terriers / Afghan Hounds / Giant Schnauzers / Borzois /
    Wire Fox Terriers / Parson Russell Terriers / Schipperkes / Gordon Setters / Treeing Walker Coonhounds''')
cats = phrases('''Abyssinian / Aegean cat / Australian Mist / American Curl / American Bobtail /
    American Polydactyl / American Shorthair / American Wirehair / Arabian Mau / Asian / Asian Semi-longhair /
    Balinese / Bambino / Bengal / Birman / Bombay / Brazilian Shorthair / British Shorthair / British Longhair /
    Burmese / Burmilla / California Spangled Cat / Chantilly/Tiffany / Chartreux / Chausie / Cheetoh /
    Colorpoint Shorthair / Cornish Rex / Cymric / Cyprus cat / Devon Rex / Donskoy or Don Sphynx / Dragon Li /
    Dwelf / Egyptian Mau / European Shorthair / Exotic Shorthair / German Rex / Havana Brown / Highlander /
    Himalayan-Colorpoint Persian / Japanese Bobtail / Javanese / Khao Manee / Korat / Korn Ja /
    Kurilian Bobtail / LaPerm / Maine Coon / Manx / Mekong bobtail / Minskin / Munchkin / Nebelung / Napoleon /
    Norwegian Forest Cat / Ocicat / Ojos Azules / Oregon Rex / Oriental Bicolor / Oriental Shorthair /
    Oriental Longhair / Persian / Peterbald / Pixie-bob / Ragamuffin / Ragdoll / Russian Blue / Russian Black /
    Sam Sawet / Savannah / Scottish Fold / Selkirk Rex / Serengeti cat / Serrade petit / Siamese / Siberian /
    Singapura / Snowshoe / Sokoke / Somali / Sphynx / Swedish forest cat / Thai / Tonkinese / Toyger /
    Turkish Angora / Turkish Van / Ukrainian Levkoy / York Chocolate Cat''')

movies = phrases('''Citizen Kane / The Godfather / Vertigo / 2001: A Space Odyssey / The Searchers / Sunrise /
    Singin’ in the Rain / Psycho / Casablanca / The Godfather Part II / The Magnificent Ambersons / Chinatown /
    North by Northwest / Nashville / The Best Years of Our Lives / McCabe & Mrs Miller / The Gold Rush /
    City Lights / Taxi Driver / Goodfellas / Mulholland Drive / Greed / Annie Hall / The Apartment /
    Do the Right Thing / Killer of Sheep / Barry Lyndon / Pulp Fiction / Raging Bull / Some Like It Hot /
    A Woman Under the Influence / The Lady Eve / The Conversation / The Wizard of Oz / Double Indemnity /
    Star Wars / Imitation of Life / Jaws / The Birth of a Nation / Meshes of the Afternoon / Rio Bravo /
    Dr Strangelove / Letter from an Unknown Woman / Sherlock Jr / The Man Who Shot Liberty Valance /
    It’s a Wonderful Life / Marnie / A Place in the Sun / Days of Heaven / His Girl Friday / Touch of Evil /
    The Wild Bunch / Grey Gardens / Sunset Boulevard / The Graduate / Back to the Future / Crimes and Misdemeanors /
    The Shop Around the Corner / One Flew Over the Cuckoo’s Nest / Blue Velvet / Eyes Wide Shut / The Shining /
    Love Streams / Johnny Guitar / The Right Stuff / Red River / Modern Times / Notorious / Koyaanisqatsi /
    The Band Wagon / Groundhog Day / The Shanghai Gesture / Network / Forrest Gump /
    Close Encounters of the Third Kind / The Empire Strikes Back / Stagecoach / Schindler’s List /
    The Tree of Life / Meet Me in St Louis / Thelma & Louise / Raiders of the Lost Ark / Bringing Up Baby /
    Deliverance / Night of the Living Dead / The Lion King / Eternal Sunshine of the Spotless Mind /
    West Side Story / In a Lonely Place / Apocalypse Now / ET: The Extra-Terrestrial / The Night of the Hunter /
    Mean Streets / 25th Hour / Duck Soup / The Dark Knight / Gone With the Wind / Heaven’s Gate / 12 Years a Slave /
    Ace in the Hole''')
tv = phrases('''The Abbott and Costello Show / ABC’s Wide World of Sports / Alfred Hitchcock Presents /
    All in the Family / An American Family / American Idol / Arrested Development / Battlestar Galactica /
    The Beavis and Butt-Head Show / The Bob Newhart Show / Brideshead Revisited / Buffalo Bill /
    Buffy the Vampire Slayer / The Carol Burnett Show / The CBS Evening News with Walter Cronkite /
    A Charlie Brown Christmas / Cheers / The Cosby Show / The Daily Show / Dallas / The Day After /
    Deadwood / The Dick Van Dyke Show / Dragnet / The Ed Sullivan Show / The Ernie Kovacs Show /
    Felicity / Freaks and Geeks / The French Chef / Friends / General Hospital /
    The George Burns and Gracie Allen Show / Gilmore Girls / Gunsmoke / Hill Street Blues /
    Homicide: Life on the Street / The Honeymooners / I, Claudius / I Love Lucy / King of the Hill /
    The Larry Sanders Show / Late Night with David Letterman / Leave It to Beaver / Lost /
    Married with Children / Mary Hartman, Mary Hartman / The Mary Tyler Moore Show / MASH / The Monkees /
    Monty Python’s Flying Circus / Moonlighting / My So-Called Life / Mystery Science Theater 3000 /
    The Odd Couple / The Office / The Oprah Winfrey Show / Pee Wee’s Playhouse / Playhouse 90 /
    The Price Is Right / Prime Suspect / The Prisoner / The Real World / Rocky and His Friends / Roots /
    Roseanne / Sanford and Son / Saturday Night Live / Second City Television / See It Now / Seinfeld /
    Sesame Street / Sex and the City / The Shield / The Simpsons / The Singing Detective / Six Feet Under /
    60 Minutes / Soap / The Sopranos / South Park / SpongeBob SquarePants / SportsCenter / Star Trek /
    St Elsewhere / The Super Bowl / Survivor / Taxi /The Tonight Show Starring Johnny Carson /
    24 / The Twilight Zone / Twin Peaks / The West Wing / What’s My Line / WKRP in Cincinnati /
    The Wire / Wiseguy / The X-Files''')

stars = phrases('''Humphrey Bogart / Cary Grant / James Stewart / Marlon Brando / Fred Astaire / Henry Fonda /
    Clark Gable / James Cagney / Spencer Tracy / Charlie Chaplin / Gary Cooper / Gregory Peck / John Wayne /
    Laurence Olivier / Gene Kelly / Orson Welles / Kirk Douglas / James Dean / Burt Lancaster / Marx Brothers /
    Buster Keaton / Sidney Poitier / Robert Mitchum / Edward G. Robinson / William Holden / Katharine Hepburn /
    Bette Davis / Audrey Hepburn / Ingrid Bergman / Greta Garbo / Marilyn Monroe / Elizabeth Taylor / Judy Garland /
    Marlene Dietrich / Joan Crawford / Barbara Stanwyck / Claudette Colbert / Grace Kelly / Ginger Rogers /
    Mae West / Vivien Leigh / Lillian Gish / Shirley Temple / Rita Hayworth / Lauren Bacall / Sophia Loren /
    Jean Harlow / Carole Lombard / Mary Pickford / Ava Gardner''')
scientists = phrases('''Alain Aspect / Martin Karplus / David Baltimore / Donald Knuth / Allen Bard /
    Robert Marks II / Timothy Berners-Lee / Craig Mello / John Tyler Bonner / Luc Montagnier / Dennis Bray /
    Gordon Moore / Sydney Brenner / Kary Mullis / Pierre Chambon / C Nüsslein-Volhard / Simon Conway Morris /
    Seiji Ogawa / Mildred Dresselhaus / Jeremiah Ostriker / Gerald M Edelman / Roger Penrose / Ronald Evans /
    Stanley Prusiner / Anthony Fauci / Henry F Schaefer III / Anthony Fire / Thomas Südhof / Jean Frechet /
    Jack Szostak / Margaret Geller / James Tour / Jane Goodall / Charles Townes / Alan Guth / Harold Varmus /
    Lene Vestergaard Hau / Craig Venter / Stephen Hawking / James Watson / Peter Higgs / Steven Weinberg /
    Leroy Hood / George Whitesides / Eric Kandel / Edward Wilson / Andrew Knoll / Edward Witten / Charles Kao /
    Shinya Yamanaka''')


_winners = (winners, boys, pharma, foo, nouns, starwars, dogs, movies, stars)
_losers = (losers, girls, cities, bar, adverbs, startrek, cats, tv, scientists)
