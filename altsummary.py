# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "english"
SENTENCES_COUNT = 5
text="""NEW DELHI: The government, after verbally backing the concept of net neutrality for some months, is all set to put it in writing. It is likely to make public this week the telecom department's report on the subject, which sources say will back the Centre's stance that the internet should be completely free with equitable access and without any obstruction or prioritization.

The Department of Telecom report - prepared by a team of six officials - is currently with the Prime Minister's Office (PMO), and will form framework for the government policy on 'net neutrality' along with recommendations of the telecom regulator, which are yet to be submitted to DoT. The principle of net neutrality guarantees consumers equal and non-discriminatory access to all data, apps and services on internet, with no discrimination on the basis of tariffs or speed.

"A panel has the taken the views of all the stakeholders before submitting it to the telecom minister. There were a few critical points of debate such as allowing zero rating plans or not. The report will back the government's stand unequivocally," a person familiar with the matter said.
While the government has made its stand in favour of neutrality of the internet amply clear, industry experts and civil society groups say that the fine print of the policy will be critical for implementation.

"A policy supporting net neutrality in the Indian context must block any preferential treatment to any content. This is so because India is a country where all connectivity is slow. Hence, speed matters less than cost in a price sensitive country like ours," Nikhil Pahwa, the founder of online news portal Medianama and one of the prime movers behind the campaign for net neutrality.

Last week, US telecom regulator, the Federal Communications Commission, slapped a $100-million fine on AT&T alleging the telecom giant was intentionally slowing down internet speeds to its unlimited data subscribers after they consumed a certain amount of data. This the commission said amounted to a lack of transparency on the company's part. Earlier this year, the FCC, prodded by US president Barack Obama, embraced net neutrality.

Some say the government should either clearly bar a telecom operator from creating or owning content or it must put regulations in place which strictly forbid the telecom operator from throttling or slowing down the content of other providers.

"There could be a blanket ban. Or, instead of just a blanket ban on operators owning content, the government should ensure no content is throttled. The purpose will be defeated even if telecom service providers enter into agreements with other content providers and give certain content preference over the rest," Prasanth Sugathan, Counsel at Software Freedom Law Center, told ET.

The DoT report will be made public even as the Telecom Regulatory Authority of India (Trai), after finishing a consultation process, is preparing its own report. The consultation, and launch of Airtel's Airtel Zero plan — under which certain apps can be accessed by users free of charge, with the app makers paying telco for users' access — caused a furore, especially on social media.

Bharti Airtel's plan is what is known as zero rating plan when the content provider pays the telco for providing free access to users. Critics say such a plan gives a clear advantage to bigger content providers who can afford to pay, against those who cannot.

"In case a Flipkart app or browsing becomes free whereas a small startup is unavailable to make its app or website free because it cannot pay the telecom operator like a Flipkart. It will kill the small person's business," explained Pahwa. "Hence prevention of a 'carriage fee' in internet access which could be charged for zero rating or increasing or lowering speeds is a critical issue."

Trai and Airtel's plan faced a severe backlash from netizens who overwhelmingly expressed support for maintaining neutrality of internet. The regulator in fact received over 10 lakh responses supporting a free internet in a month, the highest ever it has received on any consultation paper.

Meanwhile, telecom department officials say the government could disallow the controversial 'zero rating' plans in its final policy on net neutrality. However, it could make an exemption for delivery of essential government services such as education and health on a preferential basis.

Telecom operators such as Bharti Airtel, Vodafone and Idea complain growth of apps, especially the ones providing communication services such as Whatsapp and Skype, have been eating into their messaging revenues and now have the potential to hurt their voice revenues, which makes up over 80% of their business.

Most telcos said that since the apps offer the same voice services as they do, they must be brought under similar rules, which involve payment of licence fees and meet roll out obligations.

Jio, the 4G mobile service from the Mukesh Ambani-run Reliance due to launched later this year, has on its part called for a regulatory framework for voice and messaging apps which will ensure that the likes of WhatsApp comply with all security guidelines that mobile phone operators need to follow, while supporting key proposals of rivals like Airtel, Vodafone and Idea.

Supporters of net neutrality though say any move to regulate content providers will stifle innovation. They add that the security rules proposal indirectly seeks to burden innovative application providers by increasing cost of providing services.

"Do you really want the government to decide which app should be allowed to offer services in the country? Do you think Whatsapp could have grown in this country if it had to take permission from the Indian government?" Pahwa asks."""


def summary(text):

    stemmer = Stemmer(LANGUAGE)
    parser = PlaintextParser(text, Tokenizer(LANGUAGE))
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    short = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        short = short + ">" + "* " + str(sentence).decode('utf-8') + "\n\n"
        #print(sentence)
    return short

if __name__ == '__main__':
    summary(text)
