"""
Sport pages — one entry per sport. build.py turns each entry into
sport-<slug>.html and also builds the sport grid on sport-kultuur.html.

To add a sport: copy an entry, give it a new slug, and run `python _src/build.py`.

Fields
  slug       file name part  -> sport-<slug>.html
  icon       key in SPORT_ICONS below (or any icon in build.ICONS)
  name       (Afrikaans, English)
  season     (Afrikaans, English)
  kind       (Afrikaans, English) — team sport, individual, mind sport …
  photos     list of (file in assets/img/, alt AF, alt EN) — first one is the page banner
  intro      list of (AF paragraph, EN paragraph)
  highlights list of (title AF, title EN, text AF, text EN)
  kit        list of (AF, EN) — from the school's uniform policy; leave [] if none
  news       English news category to show related articles (see news-data.js), or ""
  coach      optional (AF, EN) text, e.g. ("Afrigter: mnr. X", "Coach: Mr X") — shown when filled in
"""

# Extra line icons (24×24, stroke) for sports that Lucide doesn't cover.
SPORT_ICONS = {
    "footprints": '<path d="M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.68V16a2 2 0 1 1-4 0Z"/><path d="M20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.68V20a2 2 0 1 0 4 0Z"/><path d="M16 17h4"/><path d="M4 13h4"/>',
    "mountain": '<path d="m8 3 4 8 5-5 5 15H2L8 3z"/>',
    "rugby": '<ellipse cx="12" cy="12" rx="10" ry="5.5" transform="rotate(-45 12 12)"/><path d="m8.5 15.5 7-7"/><path d="m10 12 2 2"/><path d="m12 10 2 2"/>',
    "netball": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20"/><path d="M12 2a15 15 0 0 0 0 20"/>',
    "hockey": '<path d="M17 2 9.2 17.6A3 3 0 0 1 6.5 19.3H3"/><circle cx="18" cy="18.5" r="2.5"/>',
    "cricket": '<path d="m20.5 3.5-6 6"/><path d="m15.5 8.5-9.8 9.8a1.5 1.5 0 0 1-2.1 0l-.1-.1a1.5 1.5 0 0 1 0-2.1l9.8-9.8z"/><circle cx="18" cy="18" r="2.5"/>',
    "bike": '<circle cx="18.5" cy="17.5" r="3.5"/><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="15" cy="5" r="1"/><path d="M12 17.5V14l-3-3 4-3 2 3h2"/>',
    "fish": '<path d="M6.5 12c.94-3.46 4.94-6 8.5-6 3.56 0 6.06 2.54 7 6-.94 3.47-3.44 6-7 6s-7.56-2.53-8.5-6Z"/><path d="M18 12v.5"/><path d="M7 10.67C7 8 5.58 5.97 2.73 5.5c-1 1.5-1 5 .23 6.5-1.24 1.5-1.24 5-.23 6.5C5.58 18.03 7 16 7 13.33"/>',
    "tennis": '<circle cx="12" cy="12" r="10"/><path d="M6 4.6a10 10 0 0 1 0 14.8"/><path d="M18 4.6a10 10 0 0 0 0 14.8"/>',
    "horseshoe": '<path d="M7 21H4c-1.6-4.6-1.8-9.3.4-12.6A8.9 8.9 0 0 1 12 3a8.9 8.9 0 0 1 7.6 5.4c2.2 3.3 2 8-.4 12.6h-3"/><path d="M8 21c-1-3.8-1-7 .6-9.4A4 4 0 0 1 12 9.5a4 4 0 0 1 3.4 2.1C17 14 17 17.2 16 21"/><path d="M5 12h.01"/><path d="M19 12h.01"/><path d="M6.5 7.5h.01"/><path d="M17.5 7.5h.01"/>',
    "crown": '<path d="M11.56 3.27a.5.5 0 0 1 .88 0l2.95 5.6a1 1 0 0 0 1.52.3l4.27-3.67a.5.5 0 0 1 .8.52l-2.83 10.25a1 1 0 0 1-.96.73H5.81a1 1 0 0 1-.96-.73L2.02 6.02a.5.5 0 0 1 .8-.52l4.27 3.67a1 1 0 0 0 1.52-.3z"/><path d="M5 21h14"/>',
    "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
}

SUMMER = ("Somer", "Summer")
WINTER = ("Winter", "Winter")
YEAR = ("Deur die jaar", "Year-round")
TEAM = ("Spansport", "Team sport")
SOLO = ("Individueel", "Individual")

SPORTS = [
    {
        "slug": "atletiek", "icon": "footprints", "name": ("Atletiek", "Athletics"),
        "season": SUMMER, "kind": SOLO, "photos": [], "news": "athletics",
        "intro": [
            ("Atletiek is die hartklop van die somerseisoen by Namies. Van die sprint en hekkies tot die spring- en gooi-items en langafstand — daar is 'n nommer vir elke leerder, ongeag hoe jy gebou is.",
             "Athletics is the heartbeat of the summer season at Namies. From sprints and hurdles to the jumping and throwing events and distance running — there is an event for every learner, whatever their build."),
            ("Atletiek leer leerders om doelwitte te stel, hard te oefen en hul eie grense te verskuif — waardes wat hulle ver buite die baan sal dra.",
             "Athletics teaches learners to set goals, train hard and push their own limits — values they carry far beyond the track."),
        ],
        "highlights": [
            ("Baanitems", "Track events", "Sprint, hekkies, middel- en langafstand en aflos.", "Sprints, hurdles, middle and long distance, and relays."),
            ("Veldnommers", "Field events", "Hoogspring, verspring, driesprong, gewigstoot, diskus en spiesgooi.", "High jump, long jump, triple jump, shot put, discus and javelin."),
            ("Byeenkomste", "Meetings", "Verteenwoordig Dinamika by atletiekbyeenkomste teen ander skole.", "Represent Dinamika at athletics meetings against other schools."),
        ],
        "kit": [
            ("Meisies: hemp — vollengte of “crop top” (navy &amp; wit met skoolwapen)", "Girls: top — full length or crop top (navy &amp; white with school crest)"),
            ("Meisies: knielengte- of middeldy-skibroek (navy), of jogger (navy)", "Girls: knee-length or mid-thigh ski pants (navy), or joggers (navy)"),
            ("Seuns: vollengte-hemp (navy &amp; wit met skoolwapen)", "Boys: full-length shirt (navy &amp; white with school crest)"),
            ("Seuns: knielengte-skibroek of jogger (navy)", "Boys: knee-length ski pants or joggers (navy)"),
            ("Skoolsweetpak en tekkies na byeenkomste", "School tracksuit and sneakers to meetings"),
        ],
    },
    {
        "slug": "landloop", "icon": "mountain", "name": ("Landloop", "Cross-country"),
        "season": WINTER, "kind": SOLO, "photos": [], "news": "cross-country",
        "intro": [
            ("Landloop neem atletiek van die baan af en oor gras, heuwels en paadjies. Dit is die perfekte sport vir leerders wat van uithouvermoë en 'n uitdaging hou.",
             "Cross-country takes running off the track and over grass, hills and trails. It is the perfect sport for learners who enjoy endurance and a challenge."),
            ("Landloop bou fiksheid, geestelike taaiheid en selfdissipline — en dit is 'n uitstekende manier vir atlete om in die winter fiks te bly.",
             "Cross-country builds fitness, mental toughness and self-discipline — and it is an excellent way for athletes to stay fit during winter."),
        ],
        "highlights": [
            ("Uithouvermoë", "Endurance", "Bou jou fiksheid stap vir stap, van kort tot langer roetes.", "Build your fitness step by step, from short to longer routes."),
            ("Vir alle vlakke", "For all levels", "Of jy vir die pret of vir 'n tyd hardloop — almal is welkom.", "Whether you run for fun or for a time — everyone is welcome."),
            ("Byeenkomste", "Meetings", "Hardloop vir Dinamika by landloopbyeenkomste in die winter.", "Run for Dinamika at cross-country meetings in winter."),
        ],
        "kit": [("Skoolsweetpak en tekkies na byeenkomste", "School tracksuit and sneakers to meetings")],
    },
    {
        "slug": "rugby", "icon": "rugby", "name": ("Rugby", "Rugby"),
        "season": WINTER, "kind": TEAM, "photos": [], "news": "rugby",
        "intro": [
            ("Rugby is 'n trotse tradisie in Suid-Afrikaanse skole, en by Namies is dit niks anders nie. Op die veld leer spelers moed, spanwerk en respek vir die spel, die skeidsregter en die opponent.",
             "Rugby is a proud tradition in South African schools, and Namies is no different. On the field players learn courage, teamwork and respect for the game, the referee and the opposition."),
            ("Wedstryddae bring die hele Namies-gemeenskap saam — leerders, ouers en oud-leerders wat langs die kantlyn staan en die spanne aanmoedig.",
             "Match days bring the whole Namies community together — learners, parents and old learners on the touchline cheering the teams on."),
        ],
        "highlights": [
            ("Spanwerk", "Teamwork", "Vyftien spelers wat as een eenheid werk.", "Fifteen players working as one unit."),
            ("Fiksheid &amp; krag", "Fitness &amp; strength", "Gestruktureerde oefeninge bou spoed, krag en vaardigheid.", "Structured training builds speed, strength and skill."),
            ("Skoolgees", "School spirit", "Wedstryde teen ander skole met die hele Namies-familie agter jou.", "Matches against other schools with the whole Namies family behind you."),
        ],
        "kit": [
            ("Skoolrugbybroek (navy)", "School rugby shorts (navy)"),
            ("Skoolrugbytrui", "School rugby jersey"),
            ("Skoolrugbykouse", "School rugby socks"),
        ],
    },
    {
        "slug": "netbal", "icon": "netball", "name": ("Netbal", "Netball"),
        "season": WINTER, "kind": TEAM, "news": "netball",
        "photos": [("netball.webp", "Dinamika-netbalspelers in aksie", "Dinamika netball players in action")],
        "intro": [
            ("Netbal is een van ons gewildste spansporte. Dit is vinnig, tegnies en vra presiese aangee, slim posisionering en uitstekende kommunikasie tussen spelers.",
             "Netball is one of our most popular team sports. It is fast, technical and demands precise passing, smart positioning and excellent communication between players."),
            ("Ons netbalspelers dra die skool se kenmerkende teal-drag met trots en kompeteer teen skole in die omgewing.",
             "Our netball players wear the school's distinctive teal kit with pride and compete against schools in the area."),
        ],
        "highlights": [
            ("Vaardighede", "Skills", "Aangee, vang, doelskiet en verdediging — oefen elke week.", "Passing, catching, shooting and defence — practised every week."),
            ("Spanne", "Teams", "Speel saam met jou maats in 'n span wat mekaar ondersteun.", "Play alongside your friends in a team that supports each other."),
            ("Wedstryde", "Matches", "Kompeteer teen ander skole tydens die winterseisoen.", "Compete against other schools during the winter season."),
        ],
        "kit": [
            ("Skoolnetbalromp", "School netball skirt"),
            ("Skoolnetbalhemp", "School netball shirt"),
            ("Skoolnetbalkouse", "School netball socks"),
        ],
    },
    {
        "slug": "hokkie", "icon": "hockey", "name": ("Hokkie", "Hockey"),
        "season": WINTER, "kind": ("Spansport — seuns &amp; dogters", "Team sport — boys &amp; girls"), "news": "hockey",
        "photos": [
            ("hockey-medals.jpg", "Die meisies-hokkiespan met hul medaljes", "The girls' hockey team with their medals"),
            ("hockey-team.jpg", "Die meisies-hokkiespan op die kunsgrasbaan", "The girls' hockey team on the astro turf"),
        ],
        "intro": [
            ("Hokkie by Dinamika word vir beide seuns en dogters aangebied. Dit is 'n vinnige, vaardige spel wat stokwerk, fiksheid en taktiese insig vereis.",
             "Hockey at Dinamika is offered for both boys and girls. It is a fast, skilful game that demands stick work, fitness and tactical insight."),
            ("Ons spanne speel op kunsgrasbane teen skole in die omgewing — en ons meisies het al met medaljes om die nek van die veld gestap.",
             "Our teams play on astro turf against schools in the area — and our girls have walked off the field with medals around their necks."),
        ],
        "highlights": [
            ("Seuns &amp; dogters", "Boys &amp; girls", "Spanne vir beide seuns en dogters.", "Teams for both boys and girls."),
            ("Stokwerk", "Stick work", "Oefen dribbel, aangee en doelskiet op die kunsgras.", "Practise dribbling, passing and shooting on the astro."),
            ("Toernooie", "Tournaments", "Wedstryde en toernooie teen ander skole.", "Matches and tournaments against other schools."),
        ],
        "kit": [
            ("Meisies: skoolhokkieromp", "Girls: school hockey skirt"),
            ("Seuns: skoolhokkiebroek", "Boys: school hockey shorts"),
            ("Skoolhokkiehemp", "School hockey shirt"),
            ("Skoolhokkiekouse", "School hockey socks"),
        ],
    },
    {
        "slug": "krieket", "icon": "cricket", "name": ("Krieket", "Cricket"),
        "season": SUMMER, "kind": TEAM, "news": "cricket",
        "photos": [
            ("cricket-team.jpg", "Die dogters-krieketspan by sonsondergang", "The girls' cricket team at sunset"),
            ("cricket-whites.jpg", "Die dogters-krieketspan in wit drag", "The girls' cricket team in whites"),
        ],
        "intro": [
            ("Krieket is die somer se groot spansport by Namies. Dit vra geduld, konsentrasie en vaardigheid — met die kolf, die bal en in die veld.",
             "Cricket is the big team sport of summer at Namies. It demands patience, concentration and skill — with the bat, the ball and in the field."),
            ("Krieket by Dinamika groei van krag tot krag, en ons dogters-krieketspan speel in die nuwe navy-en-teal-drag.",
             "Cricket at Dinamika keeps growing, and our girls' cricket team plays in the new navy-and-teal kit."),
        ],
        "highlights": [
            ("Kolf &amp; boul", "Batting &amp; bowling", "Ontwikkel jou tegniek in die nette en op die veld.", "Develop your technique in the nets and on the field."),
            ("Dogterskrieket", "Girls' cricket", "'n Groeiende dogters-krieketspan.", "A growing girls' cricket team."),
            ("Wedstryde", "Matches", "Speel teen ander skole in die somerseisoen.", "Play against other schools in the summer season."),
        ],
        "kit": [
            ("Wedstryde: kriekethemp (wit met skoolwapen)", "Games: cricket shirt (white with school badge)"),
            ("Wedstryde: krieketlangbroek (wit)", "Games: cricket longs (white)"),
            ("Wedstryde: krieketpet (wit)", "Games: cricket cap (white)"),
            ("Opwarm: hemp en kortbroek (navy &amp; wit met skoolwapen)", "Warm-ups: shirt and shorts (navy &amp; white with school badge)"),
        ],
    },
    {
        "slug": "bergfiets", "icon": "bike", "name": ("Bergfiets", "Mountain biking"),
        "season": YEAR, "kind": SOLO, "photos": [], "news": "mountain biking",
        "intro": [
            ("Bergfietsry kombineer fiksheid, tegniese vaardigheid en avontuur. Ryers pak paadjies, klimme en afdraandes aan en leer om hul fiets met selfvertroue te hanteer.",
             "Mountain biking combines fitness, technical skill and adventure. Riders tackle trails, climbs and descents and learn to handle their bike with confidence."),
            ("Dit is 'n sport waar jy teen die klok en teen jouself ry — en elke keer 'n bietjie beter word.",
             "It is a sport where you ride against the clock and against yourself — and get a little better every time."),
        ],
        "highlights": [
            ("Tegniek", "Technique", "Leer klim, daal en hindernisse veilig oorkom.", "Learn to climb, descend and clear obstacles safely."),
            ("Fiksheid", "Fitness", "Bou uithouvermoë en beenkrag.", "Build endurance and leg strength."),
            ("Wedrenne", "Races", "Ry vir Dinamika in skolewedrenne.", "Ride for Dinamika in school races."),
        ],
        "kit": [
            ("Fietsrybroek (swart)", "Cycling shorts (black)"),
            ("Skoolfietsrytrui", "School cycling jersey"),
            ("Spanfietsrykouse", "Team cycling socks"),
        ],
    },
    {
        "slug": "hengel", "icon": "fish", "name": ("Hengel", "Angling"),
        "season": YEAR, "kind": SOLO, "photos": [], "news": "angling",
        "intro": [
            ("Hengel is 'n sport van geduld, kennis en vaardigheid. Hengelaars leer oor aas, toerusting, waterkennis en die natuur — en om met respek vir die omgewing te hengel.",
             "Angling is a sport of patience, knowledge and skill. Anglers learn about bait, tackle, reading the water and nature — and to fish with respect for the environment."),
            ("Dit is 'n sport wat leerders buite in die natuur bring en vriendskappe bou wat 'n leeftyd hou.",
             "It is a sport that takes learners outdoors into nature and builds friendships that last a lifetime."),
        ],
        "highlights": [
            ("Vaardighede", "Skills", "Leer gooi, knope, aas en toerusting.", "Learn casting, knots, bait and tackle."),
            ("Natuur", "Nature", "Tyd buite, met respek vir die omgewing.", "Time outdoors, with respect for the environment."),
            ("Kompetisies", "Competitions", "Hengel vir Dinamika by skolekompetisies.", "Fish for Dinamika at school competitions."),
        ],
        "kit": [
            ("Skoolhengelhemp", "School angling shirt"),
            ("Kortbroek (navy)", "Shorts (navy)"),
        ],
    },
    {
        "slug": "tennis", "icon": "tennis", "name": ("Tennis", "Tennis"),
        "season": SUMMER, "kind": SOLO, "photos": [], "news": "tennis",
        "intro": [
            ("Tennis ontwikkel voetwerk, hand-oog-koördinasie en 'n sterk wedstrydbrein. Leerders speel enkelspel en dubbelspel en leer om onder druk kalm te bly.",
             "Tennis develops footwork, hand-eye coordination and a strong match mindset. Learners play singles and doubles and learn to stay calm under pressure."),
            ("Dit is 'n sport wat jy vir die res van jou lewe kan geniet.",
             "It is a sport you can enjoy for the rest of your life."),
        ],
        "highlights": [
            ("Enkel &amp; dubbel", "Singles &amp; doubles", "Speel alleen of saam met 'n maat.", "Play on your own or with a partner."),
            ("Tegniek", "Technique", "Afslaan, voorhand, handrug en vlughou.", "Serve, forehand, backhand and volley."),
            ("Liga", "League", "Speel wedstryde teen ander skole.", "Play matches against other schools."),
        ],
        "kit": [
            ("Meisies: skooltennisrok en wit kouse", "Girls: school tennis dress and white socks"),
            ("Seuns: skool-Vrydaghemp, skoolrugbybroek en wit kouse", "Boys: school Friday shirt, school rugby shorts and white socks"),
        ],
    },
    {
        "slug": "perdry", "icon": "horseshoe", "name": ("Perdry", "Equestrian"),
        "season": YEAR, "kind": SOLO, "photos": [], "news": "equestrian",
        "intro": [
            ("Ruiterkuns is vir leerders met 'n passie vir perde. Dit vra 'n spesiale vennootskap tussen ruiter en perd, gebou op vertroue, geduld en harde werk.",
             "Equestrian is for learners with a passion for horses. It requires a special partnership between rider and horse, built on trust, patience and hard work."),
            ("Ruiters verteenwoordig Dinamika in die navy skoolrybaadjie in dissiplines soos springry en dressuur.",
             "Riders represent Dinamika in the navy school riding jacket in disciplines such as show jumping and dressage."),
        ],
        "highlights": [
            ("Vennootskap", "Partnership", "Bou 'n band van vertroue met jou perd.", "Build a bond of trust with your horse."),
            ("Dissiplines", "Disciplines", "Soos springry en dressuur.", "Such as show jumping and dressage."),
            ("Kompetisies", "Competitions", "Ry vir Dinamika by skole-ruiterbyeenkomste.", "Ride for Dinamika at school equestrian events."),
        ],
        "kit": [
            ("Perdrybroek (wit)", "Riding breeches (white)"),
            ("Skoolrybaadjie (navy met embleem)", "School riding jacket (navy with logo)"),
        ],
    },
    {
        "slug": "skaak", "icon": "crown", "name": ("Skaak", "Chess"),
        "season": YEAR, "kind": ("Denksport", "Mind sport"), "photos": [], "news": "chess",
        "intro": [
            ("Skaak is sport vir die brein. Spelers leer om vooruit te dink, patrone raak te sien, geduldig te wees en beslissings onder druk te neem.",
             "Chess is sport for the brain. Players learn to think ahead, spot patterns, be patient and make decisions under pressure."),
            ("Die vaardighede wat jy op die skaakbord aanleer — konsentrasie en logiese denke — help ook in die klaskamer.",
             "The skills you learn at the chessboard — concentration and logical thinking — help in the classroom too."),
        ],
        "highlights": [
            ("Strategie", "Strategy", "Leer openings, taktiek en eindspel.", "Learn openings, tactics and endgames."),
            ("Vir almal", "For everyone", "Beginners en ervare spelers is welkom.", "Beginners and experienced players are welcome."),
            ("Toernooie", "Tournaments", "Speel vir Dinamika teen ander skole.", "Play for Dinamika against other schools."),
        ],
        "kit": [],
    },
    {
        "slug": "robotika", "icon": "bot", "name": ("Robotika", "Robotics"),
        "season": YEAR, "kind": ("Tegnologie", "Technology"), "photos": [], "news": "robotics",
        "intro": [
            ("Robotika bring wetenskap, tegnologie en kreatiwiteit saam. Leerders bou en programmeer robotte en los werklike probleme stap vir stap op.",
             "Robotics brings science, technology and creativity together. Learners build and program robots and solve real problems step by step."),
            ("Ons Digitale Tegnologie-sentrum word gebruik vir robotika, basiese kodering en rekenaarvaardighede — die perfekte plek om die ingenieurs en programmeerders van môre te vorm.",
             "Our Digital Technology centre is used for robotics, basic coding and computer skills — the perfect place to shape tomorrow's engineers and programmers."),
        ],
        "highlights": [
            ("Bou", "Build", "Ontwerp en bou jou eie robotte.", "Design and build your own robots."),
            ("Kodering", "Coding", "Leer die basiese beginsels van programmering.", "Learn the basics of programming."),
            ("Probleemoplossing", "Problem solving", "Werk in spanne om uitdagings op te los.", "Work in teams to solve challenges."),
        ],
        "kit": [],
    },
]
