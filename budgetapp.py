class Category:

  def __init__(self,cat):
    self.total_cash = 0
    self.ledger = []
    self.cat = cat

  def __str__(self):
    top = self.cat.center(30, "*") + '\n'
    things = ''
    for item in self.ledger:
      info = item['description'][0:23]
      # add 2 decimals to the amount
      amt = "{:.2f}".format(item['amount'])
      things += info
      things += str(amt).rjust(30 - len(info),' ') + '\n'
      
    total = "{:.2f}".format(self.total_cash)
    return top + things + 'Total: ' + str(total)
  
  def deposit(self,amount,description=''):
    self.ledger.append({"amount": amount, "description": description})
    self.total_cash += amount

  def withdraw(self,deduction,description=''):
    if self.check_funds(deduction):
      self.total_cash -= deduction
      self.ledger.append({"amount": -deduction, "description": description})
      return True
    else:
      return False

  def get_balance(self):
    return self.total_cash

  def transfer(self,amount,cat):
    if self.check_funds(amount):
      self.withdraw(amount,'Transfer to ' + cat.cat)
      cat.deposit(amount,'Transfer from ' + self.cat)
      return True
    else:
      return False

  def check_funds(self,amount):
    if self.total_cash >= amount:
      return True
    else:
      return False

def create_spend_chart(categories):
  marks = ['  0| ',' 10| ',' 20| ',' 30| ',' 40| ',' 50| ',' 60| ',' 70| ',' 80| ',' 90| ','100| ']
  dashes = '    ' + '-' * (len(categories) * 3)
  names = list() # category names
  amounts = [0] # withdrawals from each category; saves percentages later
  index = 0
  total = 0 # total from the amounts to calculate percentages
  result = 'Percentage spent by category\n'

  # get withdrawals from every ledger of every category
  for item in categories:
    names.append(item.cat) # save category name for later
    for movement in item.ledger:
      if movement['amount'] < 0:
        # retrieve positive value using abs()
        amounts[index] += abs(movement['amount'])
    
    total += amounts[index]
    # avoid going out of range
    amounts.append(0)
    index += 1
  # remove last element so it doesnt have +1 categories
  amounts.pop()

  # convert the amounts to express percentages instead
  index -= 1 # index = categories count
  while index >= 0:
    if (amounts[index] / total * 100) <= 10:
      amounts[index] = int(round(amounts[index] / total * 100,-2))
    else:
      # divide by total, multiply by 100 to get a percentage, -1 to round to nearest multiple of 10
      amounts[index] = int(round(amounts[index] / total * 100,-1))
    index -= 1

  # fill chart
  for item in amounts:
    index = 0
    while index <= 10:
      if (index * 10) <= item:
          marks[index] += 'o  '
      else:
          marks[index] += '   '
      index += 1
    
  for item in reversed(marks):
    result += item.ljust(1,' ') + '\n'

  x_axis = '' 
  maxi = max(names, key=len)
  for x in range(len(maxi)):
    nameString = '     '
    for name in names:
        if x >= len(name):
            nameString += '   '
        else:
            nameString += name[x] + '  '
    if (x != len(maxi) - 1):
        nameString += '\n'
    x_axis += nameString

  return result + dashes + '\n' + x_axis

food = Category('Food')
entertainment = Category('Entertainment')
business = Category('Business')
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
actual = create_spend_chart([business, food, entertainment])
print(actual)
