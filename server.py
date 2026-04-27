from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "zodiac_hw10"

QUIZ_LENGTH = 5

userData = {
    "name": "",
    "birthday": "",
    "zodiacSign": "",
    "startTime": None,
    "learnVisits": {},
    "quizAnswers": {},
    "quizQuestions": [],
}

data = {
    "constellations": [
        {
            "id": 1,
            "name": "Aries",
            "sign": "aries",
            "symbol": "Aries (Ram)",
            "dates": "Mar 21 - Apr 19",
            "image": "https://www.star-registration.com/cdn/shop/articles/83_Widder.jpg?v=1682353402&width=600",
            "description": (
                "Aries is one of the fainter zodiac constellations, but it has a lot of "
                "historical importance. For a long time it marked the vernal equinox, "
                "which is the point where the Sun crosses the celestial equator each spring. "
                "The brightest star is Hamal, an orange giant about 66 light-years away. "
                "To find it, look for a short arc of three stars sitting between Taurus "
                "and Pisces."
            ),
            "keyStars": [
                {"name": "Hamal (alpha)", "magnitude": "2.0",
                 "note": "Orange giant, the brightest star in Aries"},
                {"name": "Sheratan (beta)", "magnitude": "2.6",
                 "note": "A blue-white binary star system"},
                {"name": "Mesarthim (gamma)", "magnitude": "3.9",
                 "note": "One of the first double stars found with a telescope"},
            ],
            "howToFind": (
                "Look for a short arc of three stars in a fairly empty patch of sky "
                "between Taurus and Pisces. Hamal has a warm orange tint that helps it "
                "stand out. Best time to look is November through December in the evening."
            ),
            "funFact": (
                "Even though it is called the First Point of Aries, the vernal equinox "
                "has actually drifted into Pisces over the past 2,000 years because of "
                "a wobble in Earth's axis. The name just stuck around."
            ),
        },
        {
            "id": 2,
            "name": "Taurus",
            "sign": "taurus",
            "symbol": "Taurus (Bull)",
            "dates": "Apr 20 - May 20",
            "image": "https://www.star-registration.com/cdn/shop/articles/71_Stier_42f5f1e3-52f3-410e-af94-d8e14dd98337.jpg?v=1748064751&width=600",
            "description": (
                "Taurus is one of the easiest winter constellations to pick out. "
                "The bright orange-red star Aldebaran marks the bull's eye, and it sits "
                "right in the middle of the V-shaped Hyades cluster that forms the bull's "
                "face. To the northwest you can also spot the Pleiades, also known as "
                "the Seven Sisters, as a tight fuzzy group of stars. Taurus also contains "
                "the Crab Nebula, the leftover cloud from a supernova that Chinese "
                "astronomers recorded back in 1054 AD."
            ),
            "keyStars": [
                {"name": "Aldebaran (alpha)", "magnitude": "0.9",
                 "note": "A brilliant orange giant marking the bull's eye"},
                {"name": "Elnath (beta)", "magnitude": "1.7",
                 "note": "Blue-white star at the tip of the northern horn"},
                {"name": "Alcyone", "magnitude": "2.9",
                 "note": "The brightest star in the Pleiades cluster"},
            ],
            "howToFind": (
                "Find the V-shaped Hyades cluster first. Aldebaran sits right in the "
                "middle of it with a noticeable orange color. Then look northwest for "
                "the Pleiades, which look like a small fuzzy smudge or a tiny dipper. "
                "Best viewed November through January."
            ),
            "funFact": (
                "Aldebaran looks like it is part of the Hyades cluster, but it is "
                "actually much closer to us at only 65 light-years away. The Hyades "
                "are about 150 light-years out. It is a nice depth illusion in the sky."
            ),
        },
        {
            "id": 3,
            "name": "Gemini",
            "sign": "gemini",
            "symbol": "Gemini (Twins)",
            "dates": "May 21 - Jun 20",
            "image": "https://www.star-registration.com/cdn/shop/articles/88_Zwillinge_b10e8f56-b3f6-4627-878b-08b23320f88d.jpg?v=1748064094&width=600",
            "description": (
                "Gemini represents the twin brothers Castor and Pollux from Greek mythology. "
                "The two stars are right next to each other at the top, which is what makes "
                "this constellation so recognizable. From there, two parallel chains of stars "
                "extend southward, tracing the bodies of the twins. Every December the "
                "Geminid meteor shower radiates from this constellation, making it one "
                "of the best meteor showers of the year."
            ),
            "keyStars": [
                {"name": "Pollux (beta)", "magnitude": "1.2",
                 "note": "An orange giant that hosts a confirmed exoplanet"},
                {"name": "Castor (alpha)", "magnitude": "1.6",
                 "note": "Looks like one star but is actually a system of six stars"},
                {"name": "Alhena (gamma)", "magnitude": "1.9",
                 "note": "A blue-white star at the feet of the twins"},
            ],
            "howToFind": (
                "Find the two bright stars side by side near the top: Castor is "
                "blue-white and Pollux is slightly brighter and more orange. "
                "Gemini is located east of Orion, so use Orion's belt as a "
                "pointer to guide you east. Best visible December through March."
            ),
            "funFact": (
                "Castor looks like a single star to the naked eye, but it is "
                "actually six stars total: three pairs of binary stars all "
                "orbiting each other in one big gravitational dance."
            ),
        },
        {
            "id": 4,
            "name": "Cancer",
            "sign": "cancer",
            "symbol": "Cancer (Crab)",
            "dates": "Jun 21 - Jul 22",
            "image": "https://www.star-registration.com/cdn/shop/articles/40_Krebs.jpg?v=1681456204&width=600",
            "description": (
                "Cancer is the faintest of all the zodiac constellations. None of its "
                "stars get brighter than magnitude 3.5, which means you really do need "
                "a dark sky to see it well. The main reason to seek it out is the "
                "Beehive Cluster, also called M44 or Praesepe, which is a large open "
                "cluster of over a thousand stars. On a clear dark night it looks like "
                "a fuzzy patch with the naked eye."
            ),
            "keyStars": [
                {"name": "Altarf (beta)", "magnitude": "3.5",
                 "note": "The brightest star in Cancer, an orange giant"},
                {"name": "Asellus Australis (delta)", "magnitude": "3.9",
                 "note": "The southern donkey star, flanking the Beehive"},
                {"name": "Asellus Borealis (gamma)", "magnitude": "4.7",
                 "note": "The northern donkey star, also flanking the Beehive"},
            ],
            "howToFind": (
                "Find Cancer between bright Gemini to the west and Leo to the east "
                "along the ecliptic. The Beehive Cluster (M44) is your best target "
                "since the stars of Cancer itself are quite faint. You really need "
                "to be away from city lights. Best seen February through April."
            ),
            "funFact": (
                "The two Asellus stars (which mean donkeys in Latin) were imagined "
                "by ancient astronomers as donkeys feeding from the Beehive manger "
                "between them. The cluster has over 1,000 stars at about 577 light-years away."
            ),
        },
        {
            "id": 5,
            "name": "Leo",
            "sign": "leo",
            "symbol": "Leo (Lion)",
            "dates": "Jul 23 - Aug 22",
            "image": "https://www.star-registration.com/cdn/shop/articles/43_Loewe_ae6af638-f980-4d30-b667-dbf4fb7d3479.jpg?v=1748064192&width=600",
            "description": (
                "Leo is one of the few constellations that actually looks like what it "
                "is supposed to be. The Sickle, which is a backwards question mark "
                "shape, traces the lion's mane and head, ending at the bright "
                "blue-white star Regulus. To the east, a small triangle of stars forms "
                "the lion's hindquarters and tail. Leo is also home to a trio of "
                "galaxies called the Leo Triplet that you can spot through a small telescope."
            ),
            "keyStars": [
                {"name": "Regulus (alpha)", "magnitude": "1.4",
                 "note": "A bright blue-white star at the base of the Sickle"},
                {"name": "Denebola (beta)", "magnitude": "2.1",
                 "note": "Marks the tail of the lion"},
                {"name": "Algieba (gamma)", "magnitude": "2.0",
                 "note": "A nice double star in the lion's mane"},
            ],
            "howToFind": (
                "Look for the Sickle, which is a backwards question mark shape. "
                "Regulus sits at the base of it and is the brightest star in the "
                "area. Then trace east to the triangle of stars that forms the "
                "lion's back half. Best visible March through May."
            ),
            "funFact": (
                "Regulus spins incredibly fast, about 96 percent of the theoretical "
                "speed at which it would break apart. Because of this, it bulges "
                "out at the equator and is about 32 percent wider there than at its poles."
            ),
        },
        {
            "id": 6,
            "name": "Virgo",
            "sign": "virgo",
            "symbol": "Virgo (Maiden)",
            "dates": "Aug 23 - Sep 22",
            "image": "https://www.star-registration.com/cdn/shop/articles/31_Jungfrau_58000cd9-338c-4315-9d4b-9b1355a4fb60.jpg?v=1748064975&width=600",
            "description": (
                "Virgo is the largest of the zodiac constellations, covering roughly "
                "1,294 square degrees of sky. That makes it the second largest "
                "constellation overall. Its brightest star Spica is a brilliant "
                "blue-white beacon that is pretty hard to miss. The region of sky "
                "near Virgo also contains the Virgo Galaxy Cluster, which has over "
                "1,300 galaxies in it and is a popular target for telescopes."
            ),
            "keyStars": [
                {"name": "Spica (alpha)", "magnitude": "1.0",
                 "note": "A brilliant blue-white binary, the 15th brightest star in the sky"},
                {"name": "Porrima (gamma)", "magnitude": "2.7",
                 "note": "A beautiful pair of equal-brightness stars"},
                {"name": "Vindemiatrix (epsilon)", "magnitude": "2.8",
                 "note": "An orange giant whose name means grape harvester"},
            ],
            "howToFind": (
                "There is a classic trick called 'Arc to Arcturus, Speed on to Spica.' "
                "Start at the handle of the Big Dipper, follow the arc of its curve "
                "and keep going in the same direction and you hit Spica. Best visible May through June."
            ),
            "funFact": (
                "Spica is actually two stars orbiting so close together that they "
                "are both stretched into egg shapes by each other's gravity. They "
                "complete one orbit every four days."
            ),
        },
        {
            "id": 7,
            "name": "Libra",
            "sign": "libra",
            "symbol": "Libra (Scales)",
            "dates": "Sep 23 - Oct 22",
            "image": "https://www.star-registration.com/cdn/shop/articles/79_Waage_6674c693-791a-4c73-af1d-7fb5d0604ba3.jpg?v=1748064266&width=600",
            "description": (
                "Libra is the only zodiac constellation that represents an object "
                "rather than a person or animal. Historically its stars were seen "
                "as the claws of the neighboring Scorpion. The Arabic names of its "
                "two main stars still reflect that: Zubenelgenubi means southern claw "
                "and Zubeneschamali means northern claw. Today it represents the "
                "scales of justice."
            ),
            "keyStars": [
                {"name": "Zubeneschamali (beta)", "magnitude": "2.6",
                 "note": "Possibly the only star that looks faintly greenish to the naked eye"},
                {"name": "Zubenelgenubi (alpha)", "magnitude": "2.8",
                 "note": "A wide double star you can split with binoculars"},
                {"name": "Brachium (sigma)", "magnitude": "3.3",
                 "note": "An orange giant on the western side of the constellation"},
            ],
            "howToFind": (
                "Look for a rough quadrilateral of medium-brightness stars between "
                "Virgo and Scorpius. Zubenelgenubi is especially interesting because "
                "binoculars will show it as two separate stars. Best visible May through June."
            ),
            "funFact": (
                "Zubeneschamali is one of the very few stars that observers have "
                "described as looking slightly green. Most stars appear white or "
                "blue-white at the faint end, so this is pretty unusual."
            ),
        },
        {
            "id": 8,
            "name": "Scorpius",
            "sign": "scorpius",
            "symbol": "Scorpius (Scorpion)",
            "dates": "Oct 23 - Nov 21",
            "image": "https://www.star-registration.com/cdn/shop/articles/69_Skorpion_bf8cb997-5b99-426d-96c5-019832ad47fe.jpg?v=1748064689&width=600",
            "description": (
                "Scorpius is one of the most impressive constellations in the whole sky. "
                "The giant red star Antares sits at its heart, and its name literally "
                "means rival to Mars because they look so similar in color. The rest "
                "of the constellation curves in a long sweeping S shape through the "
                "southern summer sky, ending at a bright star called Shaula that marks "
                "the scorpion's stinger."
            ),
            "keyStars": [
                {"name": "Antares (alpha)", "magnitude": "1.1",
                 "note": "A red supergiant whose name means rival to Mars"},
                {"name": "Shaula (lambda)", "magnitude": "1.6",
                 "note": "Blue-white star at the tip of the stinger"},
                {"name": "Sargas (theta)", "magnitude": "1.9",
                 "note": "A yellow-white supergiant in the tail"},
            ],
            "howToFind": (
                "Antares is really hard to miss once you know what you are looking for. "
                "It has a blazing orange-red color in the summer sky. The S-shaped "
                "curving tail sweeps through the Milky Way and is one of the most "
                "recognizable shapes in the sky. Look south during June through August."
            ),
            "funFact": (
                "Antares is enormous. If you swapped it in for our Sun, it would "
                "swallow up Mercury, Venus, Earth, and Mars completely. Astronomers "
                "expect it to explode as a supernova at some point in the next "
                "100,000 years or so."
            ),
        },
        {
            "id": 9,
            "name": "Sagittarius",
            "sign": "sagittarius",
            "symbol": "Sagittarius (Archer)",
            "dates": "Nov 22 - Dec 21",
            "image": "https://www.star-registration.com/cdn/shop/articles/64_Schuetze_9742c5c4-0c46-4b36-80de-fd827a2b7372.jpg?v=1748064611&width=600",
            "description": (
                "Sagittarius is the constellation that points its arrow straight toward "
                "the center of our Milky Way galaxy. Most people find it easiest to "
                "spot by looking for the Teapot, which is an asterism made from eight "
                "of its brightest stars. The area around the Teapot's spout is "
                "absolutely packed with nebulae and star clusters because you are "
                "looking toward the galactic core."
            ),
            "keyStars": [
                {"name": "Kaus Australis (epsilon)", "magnitude": "1.8",
                 "note": "The brightest star in Sagittarius, forming the base of the Teapot"},
                {"name": "Nunki (sigma)", "magnitude": "2.1",
                 "note": "A blue-white star on the handle of the Teapot"},
                {"name": "Ascella (zeta)", "magnitude": "2.6",
                 "note": "A binary star at the bottom of the Teapot"},
            ],
            "howToFind": (
                "Look for the Teapot shape: the spout is on the lower left pointing "
                "toward Scorpius and the handle is on the right. The Milky Way looks "
                "like steam rising from the spout. This region is richest in "
                "binocular targets of any area in the sky. Best July through August."
            ),
            "funFact": (
                "The supermassive black hole at the center of our galaxy, called "
                "Sagittarius A*, sits in the direction of the Teapot's spout. It "
                "has a mass of about 4 million suns packed into a tiny region of space."
            ),
        },
        {
            "id": 10,
            "name": "Capricornus",
            "sign": "capricornus",
            "symbol": "Capricornus (Sea-Goat)",
            "dates": "Dec 22 - Jan 19",
            "image": "https://www.star-registration.com/cdn/shop/articles/70_Steinbock.jpg?v=1681998386&width=600",
            "description": (
                "Capricornus is one of the oldest constellations on record, with "
                "Babylonian records going back over 3,000 years. It represents a "
                "mythological creature that is half goat and half fish. The "
                "constellation itself forms a triangular shape that can look a "
                "bit like a bicorne hat. It sits between Sagittarius and Aquarius "
                "and is fairly faint overall."
            ),
            "keyStars": [
                {"name": "Deneb Algedi (delta)", "magnitude": "2.8",
                 "note": "The brightest star in Capricornus, an eclipsing binary"},
                {"name": "Dabih (beta)", "magnitude": "3.1",
                 "note": "A complex multiple star system"},
                {"name": "Algedi (alpha)", "magnitude": "3.6",
                 "note": "Looks like a double star but the two are not actually related"},
            ],
            "howToFind": (
                "Look for the triangular shape between Sagittarius and Aquarius. "
                "Deneb Algedi is your brightest anchor star. Algedi is interesting "
                "to check out because it appears to be a double star but the two "
                "are just lined up by coincidence. Best August through September."
            ),
            "funFact": (
                "The Tropic of Capricorn is named after this constellation. It marks "
                "the latitude where the Sun is directly overhead at the December "
                "solstice. Because of precession the Sun is now actually in Sagittarius "
                "at that moment, but the geographic name never changed."
            ),
        },
        {
            "id": 11,
            "name": "Aquarius",
            "sign": "aquarius",
            "symbol": "Aquarius (Water-Bearer)",
            "dates": "Jan 20 - Feb 18",
            "image": "https://www.star-registration.com/cdn/shop/articles/81_Wassermann.jpg?v=1682346733&width=600",
            "description": (
                "Aquarius depicts a person pouring water from a jar, with the stream "
                "of water flowing down as a zigzag chain of faint stars. The small "
                "Y-shaped Water Jar asterism near the center is the most recognizable "
                "feature. Aquarius also happens to contain the Helix Nebula, which is "
                "the closest planetary nebula to Earth and looks like a giant eye "
                "staring back at you through a telescope."
            ),
            "keyStars": [
                {"name": "Sadalsuud (beta)", "magnitude": "2.9",
                 "note": "Its Arabic name means luckiest of the lucky"},
                {"name": "Sadalmelik (alpha)", "magnitude": "3.0",
                 "note": "A yellow supergiant about 520 light-years away"},
                {"name": "Skat (delta)", "magnitude": "3.3",
                 "note": "A blue-white star marking the leg of the Water-Bearer"},
            ],
            "howToFind": (
                "Look for the small Y-shaped Water Jar near the center of the "
                "constellation. Sadalsuud is your brightest anchor star. The water "
                "stream zigzags southward from the jar in a chain of fainter stars. "
                "Best visible September through October."
            ),
            "funFact": (
                "The Helix Nebula in Aquarius is the closest planetary nebula to "
                "Earth at about 650 light-years away, and it spans about half the "
                "width of the full Moon in the sky."
            ),
        },
        {
            "id": 12,
            "name": "Pisces",
            "sign": "pisces",
            "symbol": "Pisces (Fish)",
            "dates": "Feb 19 - Mar 20",
            "image": "https://www.star-registration.com/cdn/shop/articles/16_Fische_885f87a6-2b35-45c5-88e5-c1047a842dc6.jpg?v=1748064889&width=600",
            "description": (
                "Pisces represents two fish swimming in opposite directions, tied "
                "together by a long cord with the knot at the star Al Rischa. The "
                "whole constellation is quite faint, but the Circlet of Pisces, which "
                "is a small ring of six stars forming the western fish's head, is a "
                "decent target. Pisces is also notable because the vernal equinox "
                "currently sits here (having drifted over from Aries over the past "
                "couple thousand years due to axial precession)."
            ),
            "keyStars": [
                {"name": "Eta Piscium", "magnitude": "3.6",
                 "note": "The brightest star in Pisces, a yellow giant"},
                {"name": "Al Rischa (alpha)", "magnitude": "3.8",
                 "note": "The knot tying the two fish together, a binary star"},
                {"name": "Gamma Piscium", "magnitude": "3.7",
                 "note": "A yellow giant in the body of the western fish"},
            ],
            "howToFind": (
                "Start by finding the Circlet of Pisces, which is a small ring of "
                "about six faint stars. The full constellation is large and spread "
                "out, so it helps to have a star chart. Look near the Great Square "
                "of Pegasus. Best visible October through December."
            ),
            "funFact": (
                "Because of Earth's axial precession, the vernal equinox is slowly "
                "creeping west through Pisces. Astronomers calculate it will move "
                "into Aquarius around the year 2597 which would technically mark "
                "the start of the Age of Aquarius."
            ),
        },
    ],

    "quiz": [
        {
            "id": 1,
            "question": (
                "According to the Leo lesson, what is the name of the "
                "backwards question mark shape that traces the lion's mane?"
            ),
            "imageConstellationId": 5,
            "answers": ["The Sickle", "The Scythe", "The Crook", "The Hook"],
            "correct": 0,
            "explanations": [
                "Correct! The Leo lesson says the backwards question mark shape is called the Sickle. Regulus sits at the base of it.",
                "Incorrect. The lesson calls it the Sickle, not the Scythe.",
                "Incorrect. The correct term from the lesson is the Sickle.",
                "Incorrect. The correct term from the lesson is the Sickle.",
            ],
        },
        {
            "id": 2,
            "question": (
                "The Virgo lesson describes a classic sky trick to find Spica. "
                "Which mnemonic does it mention?"
            ),
            "imageConstellationId": None,
            "answers": [
                "Arc to Arcturus, Speed on to Spica",
                "Follow the Pointer Stars to Spica",
                "Trace Orion's Belt to Spica",
                "Hop from Polaris down to Spica",
            ],
            "correct": 0,
            "explanations": [
                "Correct! The Virgo lesson says to arc from the Big Dipper handle to Arcturus, then keep going to reach Spica.",
                "Incorrect. The pointer stars trick is used to find Polaris, not Spica.",
                "Incorrect. Orion's belt points toward Sirius and Aldebaran, not Spica.",
                "Incorrect. Polaris is the North Star and is not used to find Spica.",
            ],
        },
        {
            "id": 3,
            "question": (
                "The Sagittarius lesson says its brightest stars form a recognizable "
                "asterism. What shape is it?"
            ),
            "imageConstellationId": 9,
            "answers": ["A Teapot", "A Bow and Arrow", "A Ladle", "A Triangle"],
            "correct": 0,
            "explanations": [
                "Correct! The Sagittarius lesson explains that eight of its brightest stars form a Teapot, with the spout pointing toward the galactic center.",
                "Incorrect. Even though Sagittarius is an archer, the asterism you look for is a Teapot, not a bow.",
                "Incorrect. The asterism is a Teapot. Ladle shapes belong to the Dipper constellations.",
                "Incorrect. The Sagittarius lesson specifically describes a Teapot shape.",
            ],
        },
        {
            "id": 4,
            "question": (
                "According to the Scorpius lesson, what does the name Antares mean?"
            ),
            "imageConstellationId": 8,
            "answers": [
                "Rival to Mars",
                "Heart of the Scorpion",
                "Red Fire Star",
                "Southern Beacon",
            ],
            "correct": 0,
            "explanations": [
                "Correct! The Scorpius lesson states that Antares means rival to Mars because the two look similar in color.",
                "Incorrect. Antares means rival to Mars. It does mark the heart, but that is not what the name means.",
                "Incorrect. The lesson says the name means rival to Mars, not red fire star.",
                "Incorrect. The Scorpius lesson is clear that Antares means rival to Mars.",
            ],
        },
        {
            "id": 5,
            "question": (
                "The Taurus fun fact explains why Aldebaran looks like part of "
                "the Hyades cluster but actually is not. What is the reason?"
            ),
            "imageConstellationId": 2,
            "answers": [
                "Aldebaran is only 65 light-years away while the Hyades are 150 light-years out",
                "Aldebaran is actually 300 light-years behind the Hyades",
                "The Hyades are in a completely different part of the sky",
                "Aldebaran orbits around the Hyades cluster",
            ],
            "correct": 0,
            "explanations": [
                "Correct! The Taurus lesson explains that Aldebaran is only 65 light-years away while the Hyades are about 150 light-years out. They just happen to line up from our perspective.",
                "Incorrect. The lesson says Aldebaran is closer to us than the Hyades, not farther.",
                "Incorrect. Both are in Taurus. The point is the distance difference, not their sky position.",
                "Incorrect. Aldebaran does not orbit the Hyades. It just happens to be lined up in the same direction.",
            ],
        },
        {
            "id": 6,
            "question": (
                "According to the Aries lesson, what color and type of star is "
                "Hamal, the brightest star in Aries?"
            ),
            "imageConstellationId": 1,
            "answers": [
                "An orange giant",
                "A blue-white supergiant",
                "A red dwarf",
                "A yellow main-sequence star",
            ],
            "correct": 0,
            "explanations": [
                "Correct! The Aries lesson describes Hamal as an orange giant about 66 light-years away, with a warm orange tint that helps it stand out.",
                "Incorrect. The lesson describes Hamal as an orange giant, not a blue-white supergiant.",
                "Incorrect. Hamal is an orange giant, not a red dwarf.",
                "Incorrect. The Aries lesson specifically calls Hamal an orange giant.",
            ],
        },
        {
            "id": 7,
            "question": (
                "The Cancer lesson highlights one famous deep-sky object as the main "
                "reason to seek the constellation out. What is it?"
            ),
            "imageConstellationId": 4,
            "answers": [
                "The Beehive Cluster (M44)",
                "The Pleiades",
                "The Crab Nebula",
                "The Helix Nebula",
            ],
            "correct": 0,
            "explanations": [
                "Correct! The Cancer lesson points to the Beehive Cluster (M44, also called Praesepe) as the main reason to look at Cancer.",
                "Incorrect. The Pleiades belong to Taurus, not Cancer.",
                "Incorrect. The Crab Nebula is in Taurus. The Cancer highlight is the Beehive Cluster.",
                "Incorrect. The Helix Nebula sits in Aquarius. Cancer's highlight is the Beehive Cluster.",
            ],
        },
        {
            "id": 8,
            "question": (
                "The Gemini fun fact reveals something surprising about Castor. "
                "What is it?"
            ),
            "imageConstellationId": 3,
            "answers": [
                "It is actually six stars: three pairs of binaries orbiting each other",
                "It is the closest star to Earth besides the Sun",
                "It hosts a confirmed exoplanet larger than Jupiter",
                "It is a hidden black hole disguised as a single star",
            ],
            "correct": 0,
            "explanations": [
                "Correct! The Gemini fun fact says Castor looks like one star but is actually six stars total — three binary pairs all orbiting each other.",
                "Incorrect. Castor is roughly 50 light-years away. The Gemini fun fact is about its six-star system.",
                "Incorrect. The lesson notes Pollux (not Castor) hosts a confirmed exoplanet. The Castor fun fact is its six-star system.",
                "Incorrect. Castor is a six-star system, not a black hole.",
            ],
        },
        {
            "id": 9,
            "question": (
                "According to the Aquarius lesson, what makes the Helix Nebula notable?"
            ),
            "imageConstellationId": 11,
            "answers": [
                "It is the closest planetary nebula to Earth",
                "It is the largest emission nebula in the night sky",
                "It is the brightest nebula visible without any optical aid",
                "It is the youngest nebula ever discovered",
            ],
            "correct": 0,
            "explanations": [
                "Correct! The Aquarius lesson states the Helix Nebula is the closest planetary nebula to Earth, about 650 light-years away.",
                "Incorrect. The lesson does not call it the largest emission nebula. It calls it the closest planetary nebula.",
                "Incorrect. The lesson highlights its proximity, not naked-eye brightness.",
                "Incorrect. The lesson says it is the closest planetary nebula, not the youngest.",
            ],
        },
        {
            "id": 10,
            "question": (
                "In the Pisces lesson, what is the name of the star that marks the "
                "knot tying the two fish together?"
            ),
            "imageConstellationId": 12,
            "answers": [
                "Al Rischa",
                "Eta Piscium",
                "Gamma Piscium",
                "Spica",
            ],
            "correct": 0,
            "explanations": [
                "Correct! The Pisces lesson identifies Al Rischa as the knot tying the two fish together. It is also a binary star.",
                "Incorrect. Eta Piscium is the brightest star in Pisces, not the knot. The knot is Al Rischa.",
                "Incorrect. Gamma Piscium sits in the body of the western fish, not at the knot.",
                "Incorrect. Spica is in Virgo, not Pisces.",
            ],
        },
    ],
}

def getZodiacSign(birthdayStr):
    try:
        d = datetime.strptime(birthdayStr, "%Y-%m-%d")
        m, day = d.month, d.day
        if   (m == 3 and day >= 21) or (m == 4 and day <= 19): return "aries"
        elif (m == 4 and day >= 20) or (m == 5 and day <= 20): return "taurus"
        elif (m == 5 and day >= 21) or (m == 6 and day <= 20): return "gemini"
        elif (m == 6 and day >= 21) or (m == 7 and day <= 22): return "cancer"
        elif (m == 7 and day >= 23) or (m == 8 and day <= 22): return "leo"
        elif (m == 8 and day >= 23) or (m == 9 and day <= 22): return "virgo"
        elif (m == 9 and day >= 23) or (m == 10 and day <= 22): return "libra"
        elif (m == 10 and day >= 23) or (m == 11 and day <= 21): return "scorpius"
        elif (m == 11 and day >= 22) or (m == 12 and day <= 21): return "sagittarius"
        elif (m == 12 and day >= 22) or (m == 1 and day <= 19): return "capricornus"
        elif (m == 1 and day >= 20) or (m == 2 and day <= 18): return "aquarius"
        else: return "pisces"
    except Exception:
        return None

def getConstellationBySign(sign):
    for c in data["constellations"]:
        if c["sign"] == sign:
            return c
    return None

def getConstellationById(cid):
    for c in data["constellations"]:
        if c["id"] == cid:
            return c
    return None

def pickQuizQuestions():
    bank = data["quiz"]
    k = min(QUIZ_LENGTH, len(bank))
    userData["quizQuestions"] = random.sample(bank, k)
    userData["quizAnswers"] = {}

def formatBirthday(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%b %d, %Y")
    except Exception:
        return s

@app.context_processor
def injectUser():
    return {
        "userBirthday": formatBirthday(userData["birthday"]),
    }

@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        userData["name"]        = request.form.get("name", "").strip()
        userData["birthday"]    = request.form.get("birthday", "")
        userData["zodiacSign"]  = getZodiacSign(userData["birthday"])
        userData["startTime"]   = datetime.now().isoformat()
        userData["learnVisits"] = {}
        userData["quizAnswers"] = {}
        userData["quizQuestions"] = []
        return redirect(url_for("home"))
    if userData["name"]:
        return redirect(url_for("home"))
    return render_template("start.html")

@app.route("/switch", methods=["POST", "GET"])
def switchProfile():
    userData["name"]          = ""
    userData["birthday"]      = ""
    userData["zodiacSign"]    = ""
    userData["startTime"]     = None
    userData["learnVisits"]   = {}
    userData["quizAnswers"]   = {}
    userData["quizQuestions"] = []
    return redirect(url_for("start"))

@app.route("/home")
def home():
    if not userData["name"]:
        return redirect(url_for("start"))
    userSignC = getConstellationBySign(userData["zodiacSign"])
    return render_template(
        "home.html",
        constellations=data["constellations"],
        userName=userData["name"],
        userSignConstellation=userSignC,
    )

@app.route("/learn/<int:n>")
def learn(n):
    if not userData["name"]:
        return redirect(url_for("start"))
    total = len(data["constellations"])
    if n < 1 or n > total:
        return redirect(url_for("home"))
    userData["learnVisits"][str(n)] = datetime.now().isoformat()
    constellation = data["constellations"][n - 1]
    userSignC = getConstellationBySign(userData["zodiacSign"])
    isUserSign = bool(userSignC and userSignC["id"] == constellation["id"])
    return render_template(
        "learn.html",
        n=n,
        total=total,
        constellation=constellation,
        userName=userData["name"],
        isUserSign=isUserSign,
        prev=n - 1 if n > 1 else None,
        nextN=n + 1 if n < total else None,
    )

@app.route("/quiz/<int:n>")
def quiz(n):
    if not userData["name"]:
        return redirect(url_for("start"))

    quizSet = userData.get("quizQuestions") or []
    if not quizSet:
        pickQuizQuestions()
        quizSet = userData["quizQuestions"]
    elif n == 1 and len(userData["quizAnswers"]) >= len(quizSet):
        pickQuizQuestions()
        quizSet = userData["quizQuestions"]

    total = len(quizSet)
    if n < 1 or n > total:
        return redirect(url_for("result"))
    q = quizSet[n - 1]
    imgC = getConstellationById(q["imageConstellationId"]) if q["imageConstellationId"] else None
    return render_template(
        "quiz.html",
        n=n,
        total=total,
        question=q,
        imgConstellation=imgC,
        userName=userData["name"],
        prevAnswer=userData["quizAnswers"].get(str(n)),
    )

@app.route("/quiz/<int:n>/answer", methods=["POST"])
def quizAnswer(n):
    chosen = request.form.get("answer")
    if chosen is not None:
        userData["quizAnswers"][str(n)] = int(chosen)
    if n < len(userData.get("quizQuestions") or []):
        return redirect(url_for("quiz", n=n + 1))
    return redirect(url_for("result"))

@app.route("/result")
def result():
    if not userData["name"]:
        return redirect(url_for("start"))
    quizSet = userData.get("quizQuestions") or []
    score = 0
    results = []
    for i, q in enumerate(quizSet):
        ans = userData["quizAnswers"].get(str(i + 1))
        correct = (ans is not None and ans == q["correct"])
        if correct:
            score += 1
        results.append({
            "question":   q["question"],
            "chosen":     ans,
            "correctIdx": q["correct"],
            "answers":    q["answers"],
            "explanation": q["explanations"][ans] if ans is not None else "No answer recorded.",
            "isCorrect":  correct,
        })
    userSignC = getConstellationBySign(userData["zodiacSign"])
    return render_template(
        "result.html",
        score=score,
        total=len(quizSet),
        results=results,
        userName=userData["name"],
        userSignConstellation=userSignC,
    )

if __name__ == "__main__":
    app.run(debug=True)