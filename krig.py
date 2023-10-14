import random
from dataclasses import dataclass

from rich.console import Console
console = Console()


@dataclass
class Kort:
	tegn: str
	tall: int

	def __repr__(self):
		# See https://en.wikipedia.org/wiki/Playing_cards_in_Unicode
		return {
			'hjerte': '[red]\u2665[/]',
			'kløver': '[white]\u2663[/]',
			'spar': '[white]\u2660[/]',
			'ruter': '[red]\u2666[/]'
		}[self.tegn] + ' ' + {
			2: '2',
			3: '3',
			4: '4',
			5: '5',
			6: '6',
			7: '7',
			8: '8',
			9: '9',
			10: '10',
			11: 'J',
			12: 'Q',
			13: 'K',
			14: 'A'
		}[self.tall]


@dataclass
class Kortstokk:
	kort: list[Kort]

	def __init__(self, kort=None):
		if kort:
			self.kort = kort
			return

		self.kort = []
		for tegn in ['hjerte', 'kløver', 'spar', 'ruter']:
			for tall in range(2, 15):
				kort = Kort(tegn, tall)
				self.kort.append(kort)

	def stokk(self):
		random.shuffle(self.kort)

	def trekk(self):
		return self.kort.pop(0)

	def tell(self):
		return len(self.kort)

	def er_tom(self):
		return  self.tell() == 0

	def legg_til(self, kort):
		self.kort.extend(kort)


def main():
	navn1 = console.input('Skriv navnet på spiller nr 1: ')
	navn2 = console.input('Skriv navnet på spiller nr 2: ')

	kortstokk = Kortstokk()
	kortstokk.stokk()

	hånd1 = Kortstokk([kortstokk.trekk() for _ in range(26)])
	console.print(f'Kortene til {navn1} er {hånd1.kort}')

	hånd2 = Kortstokk([kortstokk.trekk() for _ in range(26)])
	console.print(f'Kortene til {navn2} er {hånd2.kort}')

	pott = []
	runde = 1
	while not hånd1.er_tom() and not hånd2.er_tom():
		console.rule(f'Runde nr {runde}')
		console.print(f'{navn1} har {len(hånd1.kort)} kort', end=', ')
		kort1 = hånd1.trekk()
		console.print(f'og legger {kort1} i potten')

		console.print(f'{navn2} har {len(hånd2.kort)} kort', end=', ')
		kort2 = hånd2.trekk()
		console.print(f'og legger {kort2} i potten')

		pott += [kort1, kort2]
		console.print(f'Potten er nå {pott}')
		if kort1.tall > kort2.tall:
			console.print(f'{navn1} vant potten på {len(pott)} kort!')
			hånd1.legg_til(pott)
			pott.clear()
			hånd1.stokk()
		elif kort1.tall < kort2.tall:
			console.print(f'{navn2} vant potten på {len(pott)} kort!')
			hånd2.legg_til(pott)
			pott.clear()
			hånd2.stokk()
		else:
			console.print('Det blir KRIG!')
			fjernes = min([4, hånd1.tell(), hånd2.tell()]) -1
			if fjernes < 3:
				console.print(f'{navn1} har {hånd1.tell()} kort igjen')
				console.print(f'{navn2} har {hånd2.tell()} kort igjen')
			if fjernes > -1:  # Ellers har en spiller allerede tapt
				console.print(f'Fjerner {fjernes} kort fra hver og legger i potten')
			else:
				console.print(f'Spillet kan ikke fortsette!')

			pott += [hånd1.trekk() for _ in range(fjernes)]
			pott += [hånd2.trekk() for _ in range(fjernes)]

		## console.input('Fortsette?')
		runde = runde +1

	console.rule(f'Spillet er over')
	if hånd1.er_tom():
		console.print(f'{navn2} vant fordi {navn1} ikke har flere kort!')
	else:
		console.print(f'{navn1} vant fordi {navn2} ikke har flere kort!')


if __name__ == '__main__':
	main()
