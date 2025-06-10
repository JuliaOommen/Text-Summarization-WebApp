import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


text = """On March 15, 2023, at exactly 7:45 a.m., residents of the coastal town of Clearwater were jolted awake by a 5.6 magnitude earthquake that lasted approximately 45 seconds. According to the National Seismological Center, the epicenter was located 12 kilometers southwest of the town, at a depth of 10 kilometers. Emergency services were immediately dispatched, and local authorities activated disaster response protocols within 10 minutes of the tremor.
        Witnesses described scenes of chaos as buildings shook, power lines snapped, and car alarms blared across neighborhoods. "I was making coffee when everything started shaking," said Helen Ramirez, a resident of downtown Clearwater. "The cups flew off the shelves—it was terrifying."
        By 9:30 a.m., the Clearwater General Hospital reported treating at least 32 people for minor injuries, including cuts, bruises, and stress-related symptoms. Fortunately, no fatalities were reported. Public schools were closed for the day, and structural engineers began assessing damage to bridges, roads, and historical landmarks such as the St. Agnes Cathedral, which sustained minor cracks in its bell tower.
        In a press conference held at 1:00 p.m., Mayor Thomas Ellery assured citizens that the situation was under control. "We urge everyone to remain calm, stay updated via official channels, and report any gas leaks or structural hazards," he said.
        By evening, power was restored to 85% of affected areas, and temporary shelters were set up in community centers for those whose homes were deemed unsafe. The Red Cross began distributing food, water, and blankets at 5:00 p.m., while volunteers assisted with cleanup efforts throughout the night."""


def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)

    nlp = spacy.load("en_core_web_sm")
    doc=nlp(rawdocs)
    #print(doc)

    tokens=[token.text for token in doc]
    #print(tokens)

    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1

    #print(word_freq)

    sent_tokens=[sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text.lower()]
                else:
                    sent_scores[sent]+=word_freq[word.text.lower()]

    #print(sent_scores)

    select_len=int(len(sent_tokens)*0.3)
    #print(select_len)

    summary=nlargest(select_len, sent_scores, key=sent_scores.get)
    print(summary)

    final_summary=[word.text for word in summary]
    summary=" ".join(final_summary)
    # print(text)
    # print(summary)
    # print("Length of original text: ",len(text.split(" ")))
    # print("Length of summary: ",len(summary.split(" ")))

    return summary, doc, len(rawdocs.split(" ")), len(summary.split(" "))

