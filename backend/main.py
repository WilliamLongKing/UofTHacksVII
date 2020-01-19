from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from common.connect import Database
from datetime import date

app = Flask(__name__)
AVERAGE = 0.5
ANGER_TEMPO_MIN = 88
ANGER_VALENCE_MAX = 0.4
ANGER_LOUDNESS_MIN = -6.26
ANGER_ENERGY_MIN = 0.5
NEUTRAL_MIN = 0.95
NEUTRAL_MAX = 1.05


def getMood(song):
    # do mood analysis math from spreadsheet here
    # title artist energy loudness valence tempo ranking date
    title = song[0]
    print(title)
    energy = song[2]
    loudness = song[3]
    valence = song[4]
    tempo = song[5]

    #print("Energy: " + str(energy))
    # print(loudness)
    #print("Valence: " + str(valence))
    # print(tempo)

    score = energy + valence
    #print("Score: " + str(score))
    mood = ""
    if tempo >= ANGER_TEMPO_MIN and valence <= ANGER_VALENCE_MAX and loudness > ANGER_LOUDNESS_MIN and energy > ANGER_ENERGY_MIN:
        mood = "angry"
        print(mood)
        return mood
    if score > NEUTRAL_MAX:  # happy or excited
        #print(abs(energy - AVERAGE))
        #print(abs(valence - AVERAGE))
        if(abs(energy - AVERAGE) > abs(valence - AVERAGE)):
            mood = "energetic"
            # print("energetic")
        else:
            mood = "happy"
            # print("happy")
    elif score < NEUTRAL_MIN:
        #print(abs(energy - AVERAGE))
        #print(abs(valence - AVERAGE))
        if(abs(energy - AVERAGE) > abs(valence - AVERAGE)):
            mood = "relaxed"
            # print("relaxed")
        else:
            mood = "sad"
            # print("sad")
    else:
        mood = "neutral"
        # print("neutral")
    # print(mood)
    return mood


def getMoodBreakdown(billboardChart, date):
    # do the calcs here, return json object
    happy = 0.0
    sad = 0.0
    angry = 0.0
    excited = 0.0
    relaxed = 0.0
    neutral = 0.0
    lengthChart = len(billboardChart)
    denominator = lengthChart*(lengthChart + 1)/2
    for i in range(lengthChart):
        emotion = getMood(billboardChart[i])
        if emotion == "happy":
            happy += (lengthChart - i)
        elif emotion == "sad":
            sad += (lengthChart - i)
        elif emotion == "angry":
            angry += (lengthChart - i)
        elif emotion == "energetic":
            excited += (lengthChart - i)
        elif emotion == "relaxed":
            relaxed += (lengthChart - i)
        elif emotion == "neutral":
            neutral += (lengthChart - i)
    # print("LENGTH CHART " + str(lengthChart))
    # print(happy)
    # print(sad)
    # print(angry)
    # print(excited)
    # print(relaxed)
    # print(neutral)
    # print("FINAL: " + str(happy + sad + excited + relaxed + neutral))
    breakdown = {
        "week": date.strftime("%Y-%m-%d"),
        "happy": happy/denominator*100,
        "sad": sad/denominator*100,
        "angry": angry/denominator*100,
        "excited": excited/denominator*100,
        "relaxed": relaxed/denominator*100,
        "neutral": neutral/denominator*100
    }
    return breakdown


@app.route('/yearly_chart_data', methods=['GET'])
def yearlyData():
    year = 2019  # request.args.get('year')
    Database.connect()
    data = Database.selectSongsInDateRange(
        str(year) + "-01-01", str(year) + "-12-31")
    lastWeek = date(year, 1, 1)
    billboardChart = []
    retval = []
    for event in data:
        currentWeek = event[7]
        if lastWeek == currentWeek:  # continue to add to array
            billboardChart.append(event[:])
        else:  # must ship out the array and start anew
            retval.append(getMoodBreakdown(billboardChart, currentWeek))
            billboardChart = []
            lastWeek = currentWeek
            billboardChart.append(event[:])
            # reset date
    print(retval)
    return jsonify(retval)


if __name__ == '__main__':
    app.run(debug=True, port=4999)
    #yearlyData()
