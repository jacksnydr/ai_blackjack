import random
class Deck:
	def shuffle( self ):
		self.cards= []
		self.negated = []
		for suit in self.suits:
			for value in self.values:
				self.cards.append( value+"-"+suit )
		self.tempCards = [ ]
		for i in range(len(self.cards)):
			element = random.choice( self.cards )
			self.tempCards.append( element )
			self.cards.remove( element )
		self.cards = self.tempCards

	def __init__( self ):
		self.cards = []
		self.negated = []
		self.suits = [ "c", "s", "d", "h" ]
		self.values = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13" ]
		self.shuffle()

	def cardinality( self ):
		return len( self.cards )

	def checkDeck( self ):
		for card in self.cards:
			print( card )
		print( len( self.cards ) )

    # return all the cards that were removed
	def negation( self ):
		final = []
		for i in range( 52 ):
			final.append( 0 )
		for card in self.negated:
			value = int( card.split('-')[0] )
			index = 4 * ( value - 1 )
			if final[ index ] == 0:
				final[ index ] = 1
			elif final[ index+1 ] == 0:
				final[ index+1 ] = 1
			elif final[ index+2 ] == 0:
				final[ index+2 ] = 1
			else:
				final[ index+3 ] = 1
		return final

	def deal( self ):
		element = random.choice( self.cards )
		self.cards.remove( element )
		self.negated.append( element )
		return element