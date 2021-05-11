def translateIAndE(formula):
  if beginsWith("And(", formula):
    andArray = splitOnComma(formula)

    isTrue = translate(andArray[0][4:])
    for i in range(1, len(andArray)):
      isTrue = isTrue and translate(andArray[i])
    return isTrue

  elif beginsWith("Or(", formula):
    orArray = splitOnComma(formula)

    isTrue = translate(orArray[0][3:])
    for i in range(1, len(orArray)):
      isTrue = isTrue and translate(orArray[i])
    return isTrue

  elif beginsWith("Not(", formula):
    return not translate(formula[4:])

  elif beginsWith("Impl(", formula):
    [left, right] = splitOnComma(formula)
    return not translate(left[5:]) or translate(right[:-1])

  elif beginsWith("BiImpl(", formula):
    [left, right] = splitOnComma(formula)
    return translate("Impl(" + left[7:] + "," + right[:-1] + ")")  and translate("Impl(" + right[:-1] + "," + left[7:] +")")
  
  elif beginsWith("TOP", formula):
    return True
  
  elif beginsWith("BOT", formula):
    return False

  else:
    return boolean(formula)

def eliminateImpl(formula):
  if beginsWith("And(", formula):
    andArray = splitOnComma(formula[3:])

    return "And(" + eliminateImpl(andArray[0]) + "," + eliminateImpl(andArray[1]) + ")"

  elif beginsWith("Or(", formula):

    orArray = splitOnComma(formula[2:])

    return "Or(" + eliminateImpl(orArray[0]) + "," + eliminateImpl(orArray[1]) + ")"

  elif beginsWith("Not(", formula):
    return "Not(" + eliminateImpl(formula[4:-1]) + ")"

  elif beginsWith("Impl(", formula):
    [left, right] = splitOnComma(formula[4:])
    # print("Or(Not("+ (left) + ")," + (right) + ")")
    return "Or(Not("+ eliminateImpl(left) + ")," + eliminateImpl(right) + ")"

  elif beginsWith("BiImpl(", formula):
    [left, right] = splitOnComma(formula[6:])
    # print("And(" + "Impl(" + left + "," + right + ")"  + "," + "Impl(" + right + "," + left +")" + ")")
    return "And(" + eliminateImpl("Impl(" + left + "," + right + ")")  + "," + eliminateImpl("Impl(" + right + "," + left +")") + ")"

  elif beginsWith("TOP", formula):
    return "TOP"
  
  elif beginsWith("BOT", formula):
    return "BOT"
  else:
    return formula

def eliminateNot(formula):
  if beginsWith("And(", formula):
    andArray = splitOnComma(formula[3:])
    

    return "And(" + eliminateNot(andArray[0]) + "," + eliminateNot(andArray[1]) + ")"

  elif beginsWith("Or(", formula):

    orArray = splitOnComma(formula[2:])

    return "Or(" + eliminateNot(orArray[0]) + "," + eliminateNot(orArray[1]) + ")"

  elif beginsWith("Not(", formula):
    return changeNotOrAnd(formula[4:-1])

  elif beginsWith("TOP", formula):
    return "TOP"
  
  elif beginsWith("BOT", formula):
    return "BOT"
  else:
    return formula

def boolean(formula):
  return bool(int(formula[0]))

def changeNotOrAnd(text):
  if beginsWith("And(", text):
    andArray = splitOnComma(text[3:])
    return "Or(Not(" + eliminateNot(andArray[0]) + "),Not(" + eliminateNot(andArray[1]) + "))"

  elif beginsWith("Or(", text):

    orArray = splitOnComma(text[2:])
    return "And(Not(" + eliminateNot(orArray[0]) + "),Not(" + eliminateNot(orArray[1]) + "))"

  return text

def splitOnComma(formula):
  counter = 0

  for i in range(len((formula))):
    
    if formula[i] == "(":
      counter += 1

    if formula[i] == ")":
      counter -=1

    if counter == 1 and formula[i+1] == ",":
      return [formula[1:i+1], formula[i+2:-1]]

  return False

def beginsWith(word, text):
  if len(word) > len(text):
    return False
  
  for i in range(len(word)):
    if text[i] != word[i]:
      return False

  return True

def eliminateIAndE(text):
  return eliminateImpl(text)


def convertToCNF(text):
  text = eliminateIAndE(text)
  #print(text)
  text = eliminateNot(text)
  #print(text)
  return text

# if beginsWith("And(", formula):

#   andArray = splitOnComma(formula)

#   andString = translate(andArray[0])
#   for i in range(1, len(andArray)):
#     andString = andString + "," + translate(andArray[i])
#   return andString

# elif beginsWith("Or(", formula):

#   orArray = splitOnComma(formula)

#   orString = translate(orArray[0])
#   for i in range(1, len(orArray)):
#     orString = orString + "," + translate(orArray[i])

#   return orString



# def splitOnComma(formula):
#   counter = 0
#   numberOfItems = 1
#   firstBracketEncountered = False
#   returnArray = []
#   lastIWhenComma = -1

#   for i in range(len((formula))):
  
#     if formula[i] == "(":
#       firstBracketEncountered = True
#       counter += 1

#     if formula[i] == ")":
#       counter -=1

#     if counter == 1 and formula[i+1] == ",":
#       returnArray.append(formula[lastIWhenComma+1:i+1])
#       lastIWhenComma = i+1
#       numberOfItems += 1

#   returnArray.append(formula[lastIWhenComma+1:])
#   return returnArray