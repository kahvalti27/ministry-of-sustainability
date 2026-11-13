# Ministry of Sustainability

A short, satirical choice game. You are the Minister of Sustainability of a small Mediterranean
country that lives on tourism, agriculture and fashion. Every season a problem lands on your desk,
every answer costs something, and some answers come back a few seasons later.

Work in progress: all 26 planned events are written as drafts and the numbers are balanced. Still to do: the
owner's rewrite of the drafts, a playtest, and the final look.

## Run it

The game is plain HTML, CSS and JavaScript with no build step. It loads its events from a file, so
it needs a web server:

```bash
python3 -m http.server 8123
```

Then open http://localhost:8123.

## How it is built

- `events.json` holds every event, option, effect and report line. Adding an event needs no code.
- `engine.js` is the rules: meters, event selection, flags, scheduled follow-ups, sector crises, the
  final report and its titles. It has no screen attached.
- `game.js` draws a term in the browser.
- `tools/balance.mjs` plays thousands of terms with simple strategies and reports how they end
  (`node tools/balance.mjs`). It is how the numbers were tuned.
- `TASARIM.md` is the design document (rules, event list, build order).
- `art/deneme/portreler.py` draws the 64×64 character portraits.

## True story notes: sources

The game's world is invented, but most events are built on something that happened. In the game a
small "True story" stamp gives only a year and what happened. The sources are here.

| Event | Note in the game | Source |
|---|---|---|
| Special Delivery | 2024: farmers dumped manure outside government buildings in several countries. | To be added |
| The Olive Plague | 2013: a bacterium began killing one region's olive trees. Millions are gone. | [NPR, 2020](https://www.npr.org/2020/05/03/849551027/southern-europe-could-lose-22-billion-fighting-deadly-olive-tree-disease) |
| Where Did the Bees Go? | 2018: three pesticides were banned from outdoor use across a continent to protect bees. | [Euronews, 2018](https://www.euronews.com/2018/04/27/eu-nations-back-ban-on-insecticides-to-protect-bees) |
| The Hazelnut Empire | today: one country grows most of the world's hazelnuts, and one company is its biggest buyer. | [FreshPlaza](https://www.freshplaza.com/europe/article/9792232/turkish-hazelnut-production-drops-sending-prices-soaring/), [T-Vine](https://t-vine.com/ferrero-single-biggest-buyer-of-turkish-hazelnuts-while-germany-biggest-market-in-2017) |
| Who Picks the Tomatoes? | 2016: a law against gang-masters was passed after a farm worker died in the fields. | [Avvenire](https://www.avvenire.it/opinioni/pagine/ricordare-paola-attuare-la-legge-contro-il-caporalato) |
| Ban the Meme | 2025: a government blocked 26 social media platforms. Within days its prime minister had resigned. | [Kathmandu Post, 2025](https://kathmandupost.com/money/2025/09/10/nepal-lifts-social-media-ban-in-wake-of-deadly-crackdown-that-killed-19-protesters) |
| The Floating City | 2021: a lagoon city banned large cruise ships from its historic centre. | [Lonely Planet](https://www.lonelyplanet.com/articles/venice-italy-cruise-ships) |
| Nobody Lives Here Anymore | 2023: a historic city banned new short-term holiday lets in its old centre. | [Skift, 2023](https://skift.com/2023/10/04/florence-bans-new-short-term-rentals-in-historic-center/) |
| The Secret Beach | 2018: a famous beach was closed to visitors after the crowds wrecked its coral. | [Travel Noire](https://travelnoire.com/thailands-maya-bay-reopens-after-much-needed-rejuvenation) |
| The Secret Beach (cups option) | 2019: "biodegradable" bags could still carry shopping after three years in soil and sea. | [Dezeen, 2019](https://www.dezeen.com/2019/04/30/biodegradable-plastic-bags-research-university-plymouth/amp/) |
| Umbrella Wars | today: in one country, beach concessions were renewed for decades without ever being put up for competition. | [Euronews, 2023](https://www.euronews.com/my-europe/2023/04/20/italian-beach-space-must-be-open-to-competition-ecj-ruling) |
| Pay to Enter | 2024: a city began charging day visitors a fee to enter. | [NPR, 2024](https://www.npr.org/2024/04/25/1247162570/venice-entry-fee-day-trippers-tourists) |
| All Inclusive, Nothing Local (towel option) | 1986: the word "greenwashing" was invented to describe hotel towel cards. | [NRDC](https://www.nrdc.org/stories/what-greenwashing) |
| The Documentary | today: campaigners ask tourists to boycott a group of islands over a traditional hunt. | To be added |
| Wool-Free Wool | today: washing synthetic clothes is one of the main sources of microplastics in the sea. | To be added |
| The Green Gala | 2021: a study found that six in ten green claims by big fashion brands were misleading. | [Eco-Business](https://www.eco-business.com/zh-hans/news/almost-60-per-cent-of-sustainability-claims-by-fashion-giants-are-greenwash/) |
| The River Is Blue Today | today: near some textile towns, the river changes colour with whatever dye was used that week. | [The Daily Star](https://www.thedailystar.net/backpage/news/louhajang-river-palette-pollution-1738819) |
| Mount Textile | 2021: a dump of unsold clothes in a desert was reported to be growing by 39,000 tonnes a year. | [Al Jazeera, 2021](https://www.aljazeera.com/gallery/2021/11/8/chiles-desert-dumping-ground-for-fast-fashion-leftovers) |
| Behind the Workshop Door | 2024: a court heard that a handbag sold for 2,600 euros had cost 53 euros to make in a subcontracted workshop. | [The Fashion Law](https://www.thefashionlaw.com/cheap-bags-labor-abuses-made-in-italy-continues-to-face-scrutiny/) |
| The Water War | 2024: in a record drought, one region cut farm irrigation by 80% while hotels paid for their own desalination plant. | [Catalan News](https://www.catalannews.com/drought/item/catalonia-declares-drought-emergency---what-it-means) |
| A Slight Scrape | 2019: a cruise ship lost control in a lagoon city and hit a quay and a tour boat. | [NPR, 2019](https://www.npr.org/2019/06/02/729075426/massive-cruise-ship-crashes-into-port-in-venice-injuring-at-least-5) |
| One Bad Frost | 2025: one spring frost cut the world's biggest hazelnut harvest by about a third. | [FreshPlaza](https://www.freshplaza.com/europe/article/9757019/turkey-frost-cuts-hazelnuts-hitting-nutella-and-ferrero) |
| Poll Panic (paper straws option) | 2023: most paper straws tested had forever chemicals in them. | [NBC News, 2023](https://www.nbcnews.com/health/health-news/paper-bamboo-straws-contain-pfas-forever-chemicals-rcna101614) |
| The Green Gala (tote option) | 2018: a study found a cotton tote must be used thousands of times to match a plastic bag. | [FashionUnited, 2021](https://fashionunited.uk/news/fashion/why-cotton-tote-bags-are-killing-the-planet-too/2021082657379) |
| The Neighbours' Green Fund (credits option) | 2023: an investigation found most of one big certifier's rainforest credits saved no carbon. | [EcoWatch, 2023](https://www.ecowatch.com/phantom-credits-verra.html) |
