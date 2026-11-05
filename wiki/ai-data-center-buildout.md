# AI Data Center Build-out

**Summary**: The public companies building and letting AI compute capacity, split by business model — pure-play neoclouds, infrastructure and HPC hosts, hyperscalers and colocation REITs — with each one's footprint, site counts by stage, power and cooling arrangements, and the KPIs that actually move. 60 sites are pinned on the [Data Centers map](../map.html), which shades US states by the November 3, 2026 Senate result.

**Sources**: Company site lists, SEC filings and press releases as cited line by line below; the US state shading is the 2026 Senate map (Nov 3, 2026) and, as an alternative layer, the 2024 presidential certificates published by the National Archives (source: archives.gov/electoral-college/2024). Figures that exist only in third-party trackers are labelled as such.

**Last updated**: 2026-11-04

---

## Four business models, and why the distinction matters

The companies on this page do not compete with each other in the way a sector screen implies.
They sit at different points of the same stack, and the same megawatt can be counted by three of
them at once.

| Model | What it sells | Who it is here |
|---|---|---|
| **Pure-play neocloud** | GPU compute by the hour or by contract; usually leases the buildings | CoreWeave, Nebius, IREN |
| **Infrastructure / HPC host** | Powered shell, or powered land, on a long lease; the tenant brings the chips | Applied Digital, Core Scientific, Cipher, TeraWulf, Galaxy, Hut 8, Riot |
| **Hyperscaler** | Its own cloud, and its own models; builds for itself | Microsoft, Alphabet, Meta, Amazon, Oracle |
| **Colocation REIT** | Space, power and interconnection, mostly to enterprises | Equinix, Digital Realty |

**The double-count is the thing to watch.** CoreWeave's 4.2 GW of contracted power is largely
*other people's* buildings: Applied Digital's Ellendale campus, Core Scientific's Denton and
Muskogee sites, Galaxy's Helios. Each of those landlords reports the same campus as its own
contracted capacity. Add the group's announced megawatts together and you will count the same
concrete two or three times.

**A second layer of the same problem**: Fluidstack, a private company, is the named tenant at
TeraWulf's Lake Mariner, TeraWulf's Abernathy, Cipher's Barber Lake and Hut 8's River Bend —
and Google backs a large part of those lease obligations rather than signing them itself. The
credit behind several "diversified" tenant rosters is one balance sheet.

## The map

[map.html](../map.html) draws every site below that a company, a filing or a named report
places in a specific city or county. Markers are sized by megawatts and coloured by stage;
the table under the map carries the source link for every row.

- **Pins are city or county centroids, not parcels.** Several campuses are deliberately sited
  away from the named town.
- **Hyperscaler entries are the named AI-era campuses only**, not every data center those
  companies own. Google publishes **69 locations, 44 of them in the US**
  (source: datacenters.google/locations); three are pinned here. Microsoft operates in more
  than 60 Azure regions; two are pinned. Pinning the rest would bury the build-out this page
  is about, because most of that estate predates it.

**Coverage, company by company.** Complete against the company's own site list: IREN (8 of 8),
Core Scientific (9 pins covering all 10 listed facilities — Dalton's two entries share a city),
TeraWulf (3 of 3), Galaxy (1 of 1). Partial: Applied Digital (3 of 5 campuses, two unlocated),
Cipher (3 of 5 named sites), Hut 8 (4 pins plus one unlocated, against about 15 sites under
management), Riot (its 2 AI campuses, not its mining estate), Nebius (7 of roughly 11 named
locations). Deliberately illustrative: every hyperscaler, and the two REITs, which carry one
pin each for roughly 280 and 300+ facilities. CoreWeave is a special case — it reports 51
active data centers and publishes no site list, so what is pinned is 2 of its own plus the 4
landlord campuses it leases, which appear under the landlord's ticker.
- **One site has no pin at all**: Hut 8's Beacon Point, its first gigawatt-scale campus, is not
  located in the November 4 release (source: Hut 8 8-K exhibit 99.1, Nov 4, 2026).

### Why the states are coloured

The default shading gives **every state a party**. Where a state voted on November 3, 2026 and
the race has been called, it takes the **2026 US Senate result** — 33 Class 2 seats plus the
Ohio and Florida specials. The states with no Senate race this cycle, and the two still
uncalled (Alaska and Mississippi), fall back to the last statewide result there, the **2024
presidential vote**. The hover says which of the two a state is coloured on, so a filled map
never implies a race that did not happen.

Two further layers are available: the 2026 Senate result *as called*, which leaves the
no-race states grey and the uncalled two pale, and the 2024 presidential result on its own.

This is not decoration. Data center siting is a state and local matter — interconnection
queues, tax abatements, water permits and, increasingly, moratorium bills. Three of the four
densest clusters on the map sit in states whose politics moved on November 3:

- **Texas** holds more of the pinned capacity than every other state combined, and elected a
  new governor and a Democratic senator on November 3 (source: CBS News and CNBC election
  coverage, Nov 3–4, 2026). ERCOT's large-load interconnection rules are set in Austin.
- **Louisiana**, which holds Meta's Hyperion, Applied Digital's Delta Forge 1 and Hut 8's
  River Bend, returned a Republican senator.
- **North Dakota** — Applied Digital's two Polaris Forge campuses and Core Scientific's Grand
  Forks site — had no Senate race this cycle.

The map states what it shades and does not editorialise beyond it. Election outcomes are not a
forecast of any company's permits.

## The group at a glance

| Ticker | Company | Model | Pinned sites | Headline capacity claim |
|---|---|---|---|---|
| CRWV | CoreWeave | Neocloud | 2 own, many leased | 51 active data centers, >1.5 GW active, ~4.2 GW contracted |
| NBIS | Nebius Group | Neocloud | 7 | target of >3 GW contracted by end-2026 |
| IREN | IREN | Neocloud | 8 | ~2,750 MW announced in Texas alone |
| APLD | Applied Digital | Host | 3 | 600 MW leased across two North Dakota campuses |
| CORZ | Core Scientific | Host | 9 | 1,300+ MW of current power capacity |
| CIFR | Cipher Mining | Host | 3 | 300 MW to Fluidstack, 300 MW to AWS |
| WULF | TeraWulf | Host | 3 | 522 critical IT MW across two campuses |
| GLXY | Galaxy Digital | Host | 1 | 1.63 GW approved at one campus |
| HUT | Hut 8 | Host | 4 (+1 unlocated) | 7,859 MW development pipeline |
| RIOT | Riot Platforms | Host | 2 | 910 MW IT leased at Corsicana, 191 MW at Rockdale |
| MSFT | Microsoft | Hyperscaler | 2 | Fairwater WI + Atlanta as one "AI superfactory" |
| GOOG | Alphabet | Hyperscaler | 3 | $4bn Arkansas, reported $9bn Oklahoma |
| META | Meta Platforms | Hyperscaler | 3 | Hyperion to 2 GW by 2030, scaling to 5 GW |
| AMZN | Amazon (AWS) | Hyperscaler | 1 | Project Rainier live, dedicated to Anthropic |
| ORCL | Oracle / Stargate | Hyperscaler | 3 (+4 partner sites) | 4.5 GW of additional leasing for OpenAI |
| EQIX | Equinix | REIT | platform | ~280 data centers, 77 markets, 36 countries |
| DLR | Digital Realty | REIT | platform | 300+ facilities across 50+ metros |

---

## CoreWeave (CRWV)

| | |
|---|---|
| **Ticker and model** | CRWV. Pure-play neocloud. It sells GPU hours; it leases most of the buildings those GPUs sit in, which is why its name appears as the *tenant* on four other companies' sites in this page. |
| **Footprint** | 51 active data centers across North America and Europe as of June 30, 2026, eight of them added during 2026 (source: coreweave.com newsroom). Named international capacity: Copenhagen (atNorth DEN01), Navi Mumbai via AdaniConneX, and three Indonesian facilities. |
| **Sites by stage** | **Operational**: 51 company-wide, individually undisclosed; Copenhagen's 22.5 MW is largely online. **In progress**: Ellendale ND (Applied Digital), Denton TX and Muskogee OK (Core Scientific), Helios TX (Galaxy) — all leased in, all under build. **Planned**: 240 MW at Navi Mumbai with an option to 480 MW, first capacity mid-2028; 360 MW across three Indonesian sites, all due 2028. |
| **Power and infrastructure** | Almost entirely landlord-supplied. Most of the leased US capacity is ERCOT (Texas) or MISO (North Dakota); the Copenhagen site is Nordic grid. CoreWeave also built its own AI backbone network linking the sites rather than relying on transit. |
| **KPIs to watch** | Contracted power (4.2 GW) **against** active power (1.5 GW) — the gap is future revenue and future capex at the same time. Revenue backlog and its weighted life. Interest expense: [[coreweave-q2-fy26]] shows a $49M operating loss turning into a $626M net loss almost entirely on financing cost, which is the structural risk of leasing capacity with debt. |

## Nebius Group (NBIS)

| | |
|---|---|
| **Ticker and model** | NBIS. Pure-play neocloud with a European centre of gravity, and the only one here that both builds and leases at scale. |
| **Footprint** | **US**: New Jersey (Vineland), Missouri (Kansas City colocation, plus a planned Independence campus). **Europe**: Finland (Mäntsälä, Lappeenranta), France (Béthune), Estonia, UK (London, Harlow, and capacity at a Vantage campus in Wales). **Israel**: leased space from Mega Or. |
| **Sites by stage** | **Operational**: Vineland (phased, up to 300 MW), Kansas City, Mäntsälä (75 MW). **In progress**: Lappeenranta 310 MW (operations from 2027), Harlow. **Planned**: Independence MO, gigawatt-scale with a first 200 MW; Béthune 240 MW. |
| **Power and infrastructure** | Mäntsälä recovers waste heat into the municipal district heating system — a genuinely different cooling economics from the Texas sites. Béthune draws on a French grid that is predominantly nuclear. Independence requires new generation, which is the gating item there, not the building. |
| **KPIs to watch** | ARR and the contracted-power target of more than 3 GW by end-2026. Capex against revenue: [[nebius-q2-fy26]] records capex running at roughly eight times revenue, and a $190.4M net loss that is almost all depreciation and interest. That ratio, not the growth rate, is the thing that decides whether the build is financeable. |

## IREN (IREN)

| | |
|---|---|
| **Ticker and model** | IREN. Neocloud that owns its sites — the opposite structure to CoreWeave, and the reason its balance sheet carries the land and the substations. |
| **Footprint** | **US**: Texas (Childress, Sweetwater 1 and 2), Oklahoma (state named, site not). **Canada**: British Columbia (Prince George, Mackenzie, Canal Flats). **International**: Bundey, South Australia; Badajoz, Spain. |
| **Sites by stage** | **Operational**: the three BC sites (160 MW combined). **In progress**: Childress, 750 MW planned, with Horizon 1 (50 MW IT) accepted by Microsoft in August 2026 and three more 50 MW buildings due; Sweetwater, 2,000 MW planned across two sites, substation energized at SW1 and 300 MW of gross capacity targeted for Q4 2027. **Planned**: Oklahoma 1,600 MW, Bundey 800 MW, Badajoz 300 MW. |
| **Power and infrastructure** | The BC sites run on BC Hydro — actual hydroelectric power, not a renewable energy certificate. Texas is ERCOT. Childress is direct-to-chip liquid cooled, built to Microsoft's specification. IREN describes the portfolio as grid-connected and 100% renewable (source: iren.com/data-centers). |
| **KPIs to watch** | MW delivered and accepted, not MW announced — the gap between 2,750 MW of announced Texas capacity and the 50 MW accepted so far is the whole investment case. AI Cloud revenue against Bitcoin Mining revenue: [[iren-fq4-fy26]] marks the first quarter AI Cloud passed mining. Watch the gross margin basis too — IREN reports cost of revenue *exclusive of D&A*, which turns a 76% margin into a gross loss once depreciation is above the line. |

## Applied Digital (APLD)

| | |
|---|---|
| **Ticker and model** | APLD. Infrastructure host: it builds the campus and leases it whole, on 15-year terms, to a single investment-grade tenant. No compute of its own. |
| **Footprint** | **North Dakota**: Polaris Forge 1 (Ellendale), Polaris Forge 2 (Harwood). **Louisiana**: Delta Forge 1 (Boyce, Rapides Parish). Polaris Forge 3 and Delta Forge 2 are announced but their locations are not in the cited releases. A Finnish option of up to 1 GW has also been reported. |
| **Sites by stage** | **Operational**: Polaris Forge 1, 250 MW ready for service as of October 2026 after Building 2 completed; fully leased to CoreWeave, 400 MW of critical IT at full build. **In progress**: Polaris Forge 2, 1 GW across 900 acres, with a 200 MW critical-IT lease worth about $5bn over an estimated 15 years to an unnamed investment-grade hyperscaler; Delta Forge 1, 300 MW of critical IT on about 430 MW of utility power, a ~$3.6bn campus. **Planned**: Polaris Forge 3 (300 MW IT on ~430 MW utility) and Delta Forge 2 (210 MW), both unlocated here. |
| **Power and infrastructure** | North Dakota's MISO grid is wind-heavy and cold, which is the whole siting logic: free cooling for much of the year and cheap interconnection. Louisiana is Entergy. The campuses are purpose-built for liquid-cooled high-density racks rather than converted mining sheds. |
| **KPIs to watch** | Leased MW against delivered MW; contracted revenue backlog and its average term; tenant concentration (CoreWeave is one campus entirely). The June 2026 memorandum that would let a CoreWeave subsidiary assume the Building 3 lease *if it reaches an investment-grade rating* is a credit trigger worth tracking by name. |

## Core Scientific (CORZ)

| | |
|---|---|
| **Ticker and model** | CORZ. Infrastructure host, converting a bitcoin-mining estate to AI/HPC hosting. Still a standalone Nasdaq registrant: CoreWeave's 2025 all-stock bid did not produce a merged filer, and Core Scientific was still filing under its own CIK on November 4, 2026 (source: data.sec.gov submissions, CIK 0001839341). |
| **Footprint** | Ten sites across seven states: Auburn AL, Dalton GA (three buildings), Calvert City KY (three), Marble NC, Grand Forks ND, Muskogee OK, Austin TX, Denton TX, Pecos TX (Cottonwood 1–2). |
| **Sites by stage** | **Operational**: all ten, as mining or hosting capacity. **In progress**: six "AI factories" under development company-wide; Denton is the largest, with 394 MW of total power on the company's own page and roughly 260 MW billing to CoreWeave by mid-2026; Muskogee broke ground as a 100 MW facility delivering about 70 MW of critical IT. **Planned**: the Denton upgrade has been reported at up to $6.1bn with a 2027 launch. |
| **Power and infrastructure** | 1,300+ MW of current power capacity company-wide, racks offered at 50–200+ kW, which is the density band that requires liquid cooling (source: corescientific.com). Mixed grids: ERCOT in Texas, SPP in Oklahoma, TVA-adjacent in Kentucky and Georgia. |
| **KPIs to watch** | Critical IT load contracted and revenue-generating (around 500 MW to CoreWeave) against total power capacity. Conversion cost per MW. Residual bitcoin exposure, which is now the smaller business but still sets the comparison quarters. |

## Cipher Mining (CIFR)

| | |
|---|---|
| **Ticker and model** | CIFR. Infrastructure host, Texas-only, mid-pivot from self-mining to AI hosting. Trackers report a rebrand toward Cipher Digital; the SEC registrant name should be checked before quoting it. |
| **Footprint** | All in Texas: Odessa (operating), Black Pearl, Barber Lake (Colorado City), Stingray and Reveille. Only the first and Barber Lake are confidently located here; the others are pinned to the state or omitted. |
| **Sites by stage** | **Operational**: Odessa, self-mining. **In progress**: Barber Lake, 300 MW of critical IT leased in full to Fluidstack — a deal that began as 168 MW over 10 years for about $3bn and was then extended; bitcoin mining at Black Pearl is being wound down to free power for AI tenants. **Planned**: a 15-year, ~$5.5bn, 300 MW arrangement with Amazon Web Services; Reveille (~70 MW, 2027) and Stingray (~100 MW, timing disputed between sources). |
| **Power and infrastructure** | ERCOT throughout, with the West Texas siting logic: cheap interconnection, curtailable load, and an existing mining estate already energized. |
| **KPIs to watch** | Contracted revenue against energized MW. Counterparty mix — AWS is investment grade, Fluidstack is a private company whose obligations are backed by Google at other operators. The pace at which mining load is converted rather than simply switched off. |

## TeraWulf (WULF)

| | |
|---|---|
| **Ticker and model** | WULF. Infrastructure host built on retired power-plant sites in New York, plus a Texas joint venture. |
| **Footprint** | **New York**: Lake Mariner (Barker, Niagara County), Cayuga (Lansing). **Texas**: Abernathy, via a JV with Fluidstack. |
| **Sites by stage** | **Operational**: Lake Mariner, where 380 critical IT MW are leased to Fluidstack with Google credit enhancement and 60 MW were energized and generating revenue as of March 31, 2026. **In progress**: Abernathy, 168 critical IT MW on a 25-year lease, with Google backing about $1.3bn of the tenant's obligations, delivery targeted Q4 2026. **Planned**: Cayuga, up to 320 critical IT MW, on an 80-year site lease with HPC deployment from 2027. |
| **Power and infrastructure** | Lake Mariner sits on a former coal site in NYISO Zone A, next to the Niagara hydro complex — the cleanest grid position of any site on this page. Cayuga is also a former coal plant, which is why the interconnection already exists. |
| **KPIs to watch** | Energized critical IT MW against leased MW: 60 of 380 at the last disclosure is the single most important ratio on this name. Lease commencement dates, because revenue starts at delivery, not at signature. Whether the Google credit enhancement is ever actually drawn on. |

## Galaxy Digital (GLXY)

| | |
|---|---|
| **Ticker and model** | GLXY. A digital-asset financial firm that happens to own one of the largest single data center campuses in Texas; the hosting business is a distinct segment from the trading and asset-management one. |
| **Footprint** | One campus: Helios, Dickens County, Texas. |
| **Sites by stage** | **Operational**: Phase I, completed July 2026, delivering about 200 MW of gross power — 133 MW of critical IT — to CoreWeave, with rent commencing in Q2 2026. **In progress**: Helios 2, 3 and 4, permitted, about $3.5bn, taking CoreWeave's total commitment to 526 MW of critical IT (800 MW gross) on a 15-year lease expected to produce over $1bn of average annual revenue. **Planned**: ERCOT approved roughly 1.63 GW at the site in January 2026, with a stated potential of 3.6 GW. |
| **Power and infrastructure** | ERCOT, on a site whose approved load is now more than double what is leased. The approval, not the construction, is the scarce asset — ERCOT's large-load queue is the binding constraint in Texas. |
| **KPIs to watch** | MW delivered per phase and the rent-commencement date of each. Approved power against leased power — the 1.63 GW approval is the option value. Note that Galaxy's reported earnings mix trading and asset management with hosting, so hosting revenue has to be read out of the segment note. |

## Hut 8 (HUT)

| | |
|---|---|
| **Ticker and model** | HUT. Infrastructure host and bitcoin miner, now describing itself as an energy-and-compute business. |
| **Footprint** | **Louisiana**: River Bend (West Feliciana Parish). **Texas**: Vega (Panhandle), Salt Creek (Orla), plus two energized West Texas sites under agreement to acquire with up to 230 MW of utility capacity. **Undisclosed**: Beacon Point, its first gigawatt-scale campus. |
| **Sites by stage** | **Operational**: Vega (205 MW) and Salt Creek (63 MW), mining; 710 MW of energy capacity under management in total. **In progress**: 1,330 MW of utility capacity under construction — 330 MW at River Bend and 1,000 MW at Beacon Point, with first data halls targeted Q2 2027 (River Bend), Q3 2027 (Beacon Point Phase 1) and Q2 2028 (Phase 2). **Planned**: a 7,859 MW pipeline, comprising 3,300 MW under diligence, 3,180 MW under exclusivity and 49 MW under development (source: Hut 8 8-K exhibit 99.1, Nov 4, 2026). |
| **Power and infrastructure** | Entergy Louisiana at River Bend; ERCOT in the Panhandle and Permian. The Phase 2 lease at Beacon Point is take-or-pay, which moves the risk from occupancy to the tenant's credit. |
| **KPIs to watch** | Energy Capacity Under Management, Under Construction, Under Exclusivity and Under Diligence — Hut 8 publishes all four and they are not interchangeable; only the first two are committed. Base-term contract value (about $9.8bn on Beacon Point Phase 2 alone). And read the income statement carefully: [[hut-8-q3-fy26]] shows $189.5M of net income that is a $413.8M digital-asset mark sitting *inside* operating expenses. |

## Riot Platforms (RIOT)

| | |
|---|---|
| **Ticker and model** | RIOT. Infrastructure host on a powered-land model — the tenant procures and operates its own compute on Riot's pads, so Riot funds less of the fit-out and earns rent rather than hosting fees. |
| **Footprint** | Texas: Rockdale (Milam County) and Corsicana (Navarro County). |
| **Sites by stage** | **Operational**: Rockdale, 700 MW of grid interconnection with dedicated water and fiber; AMD's initial 25 MW was delivered in May 2026, and a 191 MW critical-IT lease to a frontier AI lab runs 20 years to June 2048 for about $9.1bn. **In progress**: Corsicana, 1 GW of approved utility power, leased in its entirety on November 4, 2026 to a frontier AI lab — 910 MW of critical IT on a 15-year triple-net powered land lease, with roughly $38bn of expected data center revenue (source: Riot 8-K exhibit 99.1, Nov 4, 2026). |
| **Power and infrastructure** | ERCOT, with Rockdale's interconnection inherited from an aluminium smelter. Riot's own release notes that tenant reimbursements are expected to be funded with non-recourse project debt sized to contracted rent. |
| **KPIs to watch** | Contracted rent against the project debt raised to deliver it — the non-recourse structure is the point. Critical IT MW delivered. The 756 MW of critical IT Riot previously described at Corsicana against the 910 MW now leased: the releases do not reconcile the two figures, which is worth resolving before using either. |

## Microsoft (MSFT)

| | |
|---|---|
| **Ticker and model** | MSFT. Hyperscaler: builds for its own Azure estate and for OpenAI, and *also* rents capacity from this page's hosts — Microsoft is the named tenant at IREN's Childress campus. |
| **Footprint** | More than 60 Azure regions globally. The named AI-era builds here are Mount Pleasant, Wisconsin and Atlanta, Georgia. |
| **Sites by stage** | **Operational**: Fairwater at Mount Pleasant, first building completed June 2026 on 315 acres, with approval to expand by a further 1,000 acres; Fairwater 2 in Atlanta, about 1M sq ft on 85 acres. **In progress**: a second Mount Pleasant facility due 2028. **Leased in**: Childress, where IREN delivered the first 50 MW IT building in August 2026 with three more due. |
| **Power and infrastructure** | Fairwater puts more than 90% of servers on closed-loop liquid cooling with a water-cooled chiller plant — closed-loop matters because water consumption is the live local objection in most of these counties. Microsoft links Atlanta and Wisconsin over a dedicated network into what it calls an AI superfactory, which is a training-topology claim, not a marketing one. |
| **KPIs to watch** | Azure growth and, specifically, the capacity-constrained language in the quarterly commentary: [[microsoft-fq1-fy27]] has Azure at +48% and 36% of the company. Capex and finance-lease additions. How much capacity is leased from third parties rather than owned — that is the line that connects MSFT to IREN and CRWV. |

## Alphabet / Google (GOOG)

| | |
|---|---|
| **Ticker and model** | GOOG. Hyperscaler with its own silicon (TPUs), which changes the economics: it is not bidding for the same GPUs as everyone else on this page. It is also, indirectly, a large credit backer of other operators' tenants. |
| **Footprint** | The 2026 announcements cluster in the mid-South and plains: West Memphis AR, Pryor/Stillwater/Muskogee OK, a Tulsa-area campus, Armstrong County TX, and a reported Kansas site. |
| **Sites by stage** | **Operational**: Pryor (MidAmerica), long-established. **In progress**: West Memphis, $4bn through 2027 on about 1,100 acres, Google's first data center in Arkansas; Armstrong County, developed by Crusoe. **Planned/reported**: a $9bn Oklahoma programme spanning Stillwater and Muskogee, a Tulsa campus confirmed in August 2026, and a reported $1bn Port of Little Rock site. |
| **Power and infrastructure** | Entergy Arkansas is building roughly $600M of new generation and transmission for West Memphis, with Google covering the cost — the clearest example on this page of a tenant paying for grid build rather than queueing for it. Armstrong County pairs with 531 MW of adjacent West Texas wind. |
| **KPIs to watch** | Cloud revenue and backlog: [[alphabet-q3-fy26]] has Cloud more than doubling while free cash flow went negative on capex. Capex guidance, which is the number that moves the whole supply chain. And the off-balance-sheet exposure: Google credit-enhances Fluidstack's leases at TeraWulf and Cipher, so some of Google's capacity shows up on other companies' sites. |

## Meta Platforms (META)

| | |
|---|---|
| **Ticker and model** | META. Hyperscaler building only for itself — no external cloud to sell, which means every megawatt is a cost line, not a revenue line, until the models earn it back. |
| **Footprint** | The named multi-gigawatt builds: Prometheus (New Albany, Ohio), Hyperion (Richland Parish, Louisiana), and El Paso, Texas. Meta operates many more US campuses; these are the AI-era ones. |
| **Sites by stage** | **In progress**: Prometheus, described by Zuckerberg as a ~1 GW cluster coming online in 2026; Hyperion, targeting 2 GW by 2030 and scaling toward 5 GW; El Paso, scalable to about 1 GW with $1.5bn committed to the current phase and completion expected 2028. |
| **Power and infrastructure** | Prometheus is reported to use on-site gas turbines, and Hyperion is supported by new Entergy gas generation plus solar. This is the part of the build-out where the power source is new fossil generation rather than an existing grid position — a different regulatory exposure from the hydro and nuclear-adjacent sites. |
| **KPIs to watch** | Capex guidance and the depreciation that follows it; Meta has already lengthened useful lives once. Reality Labs is no longer the capex story. Watch the gap between announced gigawatts and energized ones, which for Meta is almost the entire figure. |

## Amazon / AWS (AMZN)

| | |
|---|---|
| **Ticker and model** | AMZN. Hyperscaler with its own accelerators (Trainium), and a landlord relationship running the other way: AWS is the *tenant* on Cipher's 300 MW lease. |
| **Footprint** | The named AI build is Project Rainier at New Carlisle, Indiana, plus a further $15bn announced across northwest Indiana. AWS's general region footprint is global and not pinned here. |
| **Sites by stage** | **Operational**: Project Rainier, live since October 2025, roughly $11bn in its first phase, dedicated to a single customer — Anthropic — for training and serving Claude. **In progress**: further buildings at New Carlisle, with full campus build-out projected no earlier than late 2027. |
| **Power and infrastructure** | AEP Indiana Michigan Power. Reported IT power of about 910 MW rising toward 1,925 MW is a press estimate rather than an AWS figure, and should be quoted as such. The site drew an Indiana environmental halt order over wetland impacts earlier in 2026. |
| **KPIs to watch** | AWS growth rate and backlog: [[amazon-q3-fy26]] has AWS at +39% and accelerating for a fifth quarter. Capex against operating cash flow. Single-tenant concentration at Rainier is an unusual structure for AWS and worth watching as a template. |

## Oracle, and the Stargate sites (ORCL)

| | |
|---|---|
| **Ticker and model** | ORCL. Hyperscaler by balance sheet, landlord by behaviour: Oracle leases capacity from developers and subleases compute to OpenAI. The Stargate sites below are developed by several different parties — Crusoe, Vantage, SB Energy, Related — so the ticker exposure differs site by site. |
| **Footprint** | Abilene TX, Shackelford County TX, Doña Ana County NM (Project Jupiter), plus partner-developed sites at Milam County TX, Lordstown OH, Port Washington WI and Saline Township MI. Michigan, Texas, Wisconsin and Wyoming have all been named as candidate states for more. |
| **Sites by stage** | **Operational**: Abilene, where Oracle said two of eight buildings were operational in March 2026 and an independent tracker estimated four by April, projecting about 1.2 GW by Q4 2026. **In progress**: Shackelford (~2 GW, completion projected Q4 2028), Project Jupiter (~2.2 GW, two lawsuits filed against it), Port Washington (~1.3 GW, Vantage-developed), Milam County (1.2 GW leased, SB Energy), Saline Township (~$16bn financed April 2026). **Planned**: Lordstown, whose status is reported inconsistently. |
| **Power and infrastructure** | Abilene runs on ERCOT with on-site gas turbines. Milam County pairs with SB Energy solar and storage. Oracle says it has completed leasing arrangements for an additional 4.5 GW to support its OpenAI commitments; Bloomberg reported an Abilene expansion had been scrapped and Oracle called that coverage incorrect — the contradiction is unresolved and is noted rather than settled here. |
| **KPIs to watch** | RPO (remaining performance obligations) and how much of it is one counterparty. Capex against operating cash flow — S&P has flagged the spending pace as straining cash flow. The gap between leasing arrangements "completed" and capacity energized. |

## Equinix (EQIX) and Digital Realty (DLR)

| | |
|---|---|
| **Ticker and model** | EQIX and DLR. Colocation REITs. They are the incumbent landlords of the internet, selling space, power and interconnection — a retail business with an AI-facing hyperscale line bolted on (Equinix's xScale, Digital Realty's hyperscale joint ventures). |
| **Footprint** | Equinix: approximately 280 data centers across 77 markets in 36 countries. Digital Realty: 300+ facilities across 50+ metros on its PlatformDIGITAL description. Both are pinned once on the map, at their headquarters, because pinning 580 facilities would make the AI build-out invisible. |
| **Sites by stage** | Equinix: 58 major projects under way including 12 xScale builds; about 700 MW under construction against roughly 3 GW of developable capacity on land under control; xScale itself is 23 operational facilities across 13 metros with 430+ MW leased against a ~2 GW build-out target. Digital Realty's current pipeline is not verified here against a filing. |
| **Power and infrastructure** | Grid power market by market, with the retail colocation density band (5–15 kW/rack) far below the AI band — which is exactly why both have separate hyperscale vehicles rather than retrofitting the retail estate. |
| **KPIs to watch** | Bookings mix: Equinix reported about 60% of one recent quarter's bookings from AI workloads. MW leased and MW under construction. Interconnection count, which is the moat the neoclouds do not have. Cost of capital — these are REITs, so the equity story is spread over the development yield, not growth. |

## Private companies that matter here, and have no ticker

Four of the most important operators in this build-out cannot be charted and will not get a
Financials card, under the same gate [[sankey-income-statement]] applies to any private
company: no filings exist, and a run-rate or a valuation is not an income statement.

- **Fluidstack** — tenant at TeraWulf (Lake Mariner and Abernathy), Cipher (Barber Lake) and
  Hut 8 (River Bend). Google credit-enhances several of those obligations.
- **Crusoe** — developer of the Abilene Stargate campus and of Google's Armstrong County site.
- **Vantage Data Centers** — developer at Port Washington and a Nebius landlord in Wales.
- **SB Energy** (SoftBank) — Milam County.

Their absence from the tables is a gap in the public market, not a gap in this page.

## What to watch across the whole group

1. **Energized MW, not announced MW.** Every company on this page quotes a bigger number than
   it is running. TeraWulf: 60 of 380. IREN: 50 of 2,750 in Texas. The ratio is the build.
2. **Who holds the lease, and who holds the credit.** Take-or-pay leases to an unnamed
   "investment-grade hyperscaler" are not the same asset as a lease to a private startup whose
   obligations a third party guarantees in part.
3. **Interest expense.** It is already the largest recurring charge on several of these
   statements — $105.5M in one quarter at Hut 8, against $8.6M a year earlier.
4. **The basis of the gross margin.** Several of these filers report cost of revenue
   *exclusive of depreciation and amortization*. On a business whose asset *is* the
   depreciation, that margin describes very little; see [[iren-fq4-fy26]] and
   [[hut-8-q3-fy26]].
5. **Power approval, not construction.** ERCOT large-load approval, an Entergy generation
   build, a state interconnection queue — these set the schedule. Concrete does not.
6. **State and local politics**, which is why the map is shaded. Moratorium bills, water
   permits and abatement clawbacks are decided in the states where the pins cluster.

## What this page does not carry

- **No per-site megawatts for CoreWeave's 51 data centers.** The company publishes the total
  and not the list; third-party trackers disagree with each other on the individual sites, so
  none of their figures are used here.
- **No legacy hyperscaler estate.** Google's other 66 locations, Meta's other US campuses,
  AWS's 38 regions and Microsoft's 60-plus are all real and all absent. They would be a second
  layer on the map, not an extension of this one.
- **No Digital Realty site list.** Its platform figures are the company's own description and
  were not verified against a filing in this pass.
- **No Beacon Point pin.** Hut 8 has not disclosed the location.
- **No Polaris Forge 3 or Delta Forge 2 pins**, for the same reason.
- **No investment view.** Everything above is sourcing and structure. [[favorites-financials]]
  is the index of what is actually charted.

## Related pages
- [[coreweave-q2-fy26]]
- [[nebius-q2-fy26]]
- [[iren-fq4-fy26]]
- [[hut-8-q3-fy26]]
- [[microsoft-fq1-fy27]]
- [[alphabet-q3-fy26]]
- [[amazon-q3-fy26]]
- [[vertiv-q3-fy26]]
- [[ge-vernova-q3-fy26]]
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[index]]
