Q|Cards⟩ is a card game which uses quantum computers to resolve the winner.

Created during Quantum Wheel, fifth quantum game jam: https://itch.io/jam/quantum-wheel

Instructions, calculation software and printable cards are provided in this repository.

To use the API of the game run

    pip install -r requirements.txt

To use the frontend application run

    pip install -r requirements-game.txt

Example use of the API:

```python
# Example
import QuantumEngine as qe

# An example game string
game_string = ('H1X2Y3')

# Check if the string represents a valid game
qe.is_valid_game(game_string, num_players=3)
```

    True

```python
# Run the circuit on the simulator
qe.get_scores(game_string, num_players=3)
```

    [502, 1024, 1024, 0, 0]

```python
# Run the circuit on the simulator with a noise model (requires setting up a free IBM Q account)
# See https://github.com/Qiskit/qiskit-ibmq-provider#setting-up-the-ibmq-provider for instructions
qe.get_scores(game_string, 3, noisy=True)
```

    [515, 995, 991, 0, 0]
