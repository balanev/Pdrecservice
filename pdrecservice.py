#!flask/bin/python
from pybrain.tools.customxml.networkreader import NetworkReader
from flask import Flask, jsonify
from flask import request
import re

app = Flask(__name__)
    
players=['Cooperator', 'Defector', 'TitForTat', 'WinStayLoseShift', 'Prober', 'Grudger']
net10=NetworkReader.readFrom(filename='n2_10_14_32.xml')
net11=NetworkReader.readFrom(filename='n2_11_14_32.xml')
net12=NetworkReader.readFrom(filename='n2_12_14_32.xml')
net13=NetworkReader.readFrom(filename='n2_13_14_32.xml')
net14=NetworkReader.readFrom(filename='n2_14_14_32.xml')
net15=NetworkReader.readFrom(filename='n2_15_14_32.xml')
net16=NetworkReader.readFrom(filename='n2_16_14_32.xml')
net17=NetworkReader.readFrom(filename='n2_17_14_32.xml')
net18=NetworkReader.readFrom(filename='n2_18_14_32.xml')
net19=NetworkReader.readFrom(filename='n2_19_14_32.xml')
net20=NetworkReader.readFrom(filename='n2_20_14_32.xml')
net21=NetworkReader.readFrom(filename='n2_21_14_32.xml')
net22=NetworkReader.readFrom(filename='n2_22_14_32.xml')
net23=NetworkReader.readFrom(filename='n2_23_14_32.xml')
net24=NetworkReader.readFrom(filename='n2_24_14_32.xml')
net25=NetworkReader.readFrom(filename='n2_25_14_32.xml')
net26=NetworkReader.readFrom(filename='n2_26_14_32.xml')
net27=NetworkReader.readFrom(filename='n2_27_14_32.xml')
net28=NetworkReader.readFrom(filename='n2_28_14_32.xml')
net29=NetworkReader.readFrom(filename='n2_29_14_32.xml')
net30=NetworkReader.readFrom(filename='n2_30_14_32.xml')

def convertToCode(str = 'RRRRRRRRRR'):
    res = []
    for i in (range(0, len(str))):
        if str[i] == 'R': res.append(1), res.append(1)  # CC R 1
        if str[i] == 'P': res.append(-1), res.append(-1)  # DD P 4
        if str[i] == 'T': res.append(-1), res.append(1)  # DC T 2
        if str[i] == 'S': res.append(1), res.append(-1)  # CD S 3
    return res

def fnd(string = "RSTP"):
    str = string.upper()
    str = re.sub('R', '', str)
    str = re.sub('S', '', str)
    str = re.sub('T', '', str)
    str = re.sub('P', '', str)
    return str

def strategy(str = "RRRRRRRRRR"):
    lg = len(str)
    dat = convertToCode(str)
    if lg == 10: res = net10.activate(dat)
    if lg == 11: res = net11.activate(dat)
    if lg == 12: res = net12.activate(dat)
    if lg == 13: res = net13.activate(dat)
    if lg == 14: res = net14.activate(dat)
    if lg == 15: res = net15.activate(dat)
    if lg == 16: res = net16.activate(dat)
    if lg == 17: res = net17.activate(dat)
    if lg == 18: res = net18.activate(dat)
    if lg == 19: res = net19.activate(dat)
    if lg == 20: res = net20.activate(dat)
    if lg == 21: res = net21.activate(dat)
    if lg == 22: res = net22.activate(dat)
    if lg == 23: res = net23.activate(dat)
    if lg == 24: res = net24.activate(dat)
    if lg == 25: res = net25.activate(dat)
    if lg == 26: res = net26.activate(dat)
    if lg == 27: res = net27.activate(dat)
    if lg == 28: res = net28.activate(dat)
    if lg == 29: res = net29.activate(dat)
    if lg == 30: res = net30.activate(dat)
    return res

@app.route('/strategy/api/v1.0/', methods=['GET'])
def get_tasks():
       req = []
       if 'str' in request.args:
          dta = request.args['str']
          if fnd(dta) != '':
              result = u"Bad Data - only RSTP legend"
              comment = u"R - cc; S - cd; T - dc; P - dd"
              req.append({'2_Comment': comment, '1_Strategy': result})
              return jsonify({'result': req})
          if len(dta)<10:
              result =  u"Error: Length of Data < 10"
              comment = u"A string of at least 10 characters and no more than 30 characters"
              req.append({'2_Comment': comment, '1_Strategy': result})
              return jsonify({'result': req})
          if len(dta)>30:
              result = u"Error: Length of Data > 30"
              comment = u"A string of at least 10 characters and no more than 30 characters"
              req.append({'2_Comment': comment, '1_Strategy': result})
              return jsonify({'result': req})
          res = strategy(dta)
          iresult = res.argmax()
          result = players[res.argmax()]
          if iresult == 0: comment = u"Always Co-operate"; #Cooperator
          if iresult == 1: comment = u"Always Defect"; #Defector
          if iresult == 2: comment = u"Tit For Tat - Repeat opponent's last choice"; #TitForTat
          if iresult == 3: comment = u"Win-stay, lose-shift repeats the previous move if the resulting payoff has met its aspiration level and changes otherwise"; #WinStayLoseShift
          if iresult == 4: comment = u"The 'Prober' strategy offers the following sequence of actions: 'D', 'C' and 'C' moves initially, with defects forever if the opponent cooperated in moves 2 and 3, otherwise TFT moves"; #Prober
          if iresult == 5: comment = u"(Co-operate, but only be a sucker once) - Co-operate until the opponent defects. Then always defect unforgivingly"; #Grudger
          req.append({'2_Comment': comment, '1_Strategy': result})
          return jsonify({'result': req})
       else:
          result = u"Data not found!"
          comment = u"The end of the line should be: ?str=RSTPSSSSSSSSS"
          req.append({'2_Comment': comment, '1_Strategy': result})
          return jsonify({'result': req})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
