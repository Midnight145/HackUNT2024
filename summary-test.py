import llm

text = """
I had a coworker who had their headphones when I worked at Dominos. I never asked her about them since I'd end up shitting on them and I didn't want to be a dick
I know some who bought them because they couldn't afford airpods and it was the only other name they knew. Mostly teenagers
My friend swears by them. I've never seen an ad. I had the opportunity to try them and I passed on them for no real reason.
Someone at my school owns a pair of over ears by them. I asked to try them and they were the dirtiest bass dispensers I've ever heard. Not good.
terrible tws by all accounts but I'm glad they give Tim and Internetcommentiquette money
Bought them and they were just boomy, even moreso than consumer stuff. I currently use Soundcore Liberty Air2's the few times i use TWS. They're still really bassy but even so, far more listenable than Raycons. Pretty much any other TWS would probably be a better buy.
Haven't tried RayCon, but if you want to buy wireless IEMs/earbuds, https://scarbir.com for someone who has bought and reviewed hundreds of them independently.\n\nRayCon products look like just about everyone else's who have rebranded some Chinese OEM's thing. These OEMs make excellent earphones for the most part, but they don't usually get marked up as high as RayCon does it. I bet they are actually good based on the consumer reviews, but you're paying a good amount for their marketing costs.
Nope, they suck ass.\nOn a low budget you might want to consider some KZ wireless iems. The Moondrop Sparks are good too. Above $100 it'll be more worth it to get a good wired iems and bluetooth receivers for them.
They aren't. Get the Moondrop Sparks if you want to go TWS. Or cheap USB-C dongle like HiDizs sonata HD and Blon BL03 IEMs.
They hella shit. If you don't mind wires, get the Moondrop Arias. If you need wireless, Airpod Pros or those Galaxy Buds Pros are good options
No, I've heard from non-sponsored reviews that they're pretty bad. I'd recommend galaxy buds plus, galaxy buds 2 or galaxy buds pro, airpods pro, wf-1000xm4. If you don't have the budget for any of these, check out other people's recommendations here, such as moondrop sparks. Remember you can always get better sound quality by going with wired iems, but afromentioned tws earbuds are great as well
They aren't, my sister ordered me some and the left one didn't work. Costumer service is terrible.
"""

thing = llm.get_model('Llama-3')
resp = thing.prompt(text, "Use these reviews to create a summarized concise review of Raycon Earbuds.")
print(resp.text())
