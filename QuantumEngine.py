"""Module with functions to check if the Q|cards> game is valid and to run it
on a simulator or on a real quantum computer"""

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, IBMQ, execute
from qiskit.providers.aer import noise
from qiskit.providers.aer.noise import NoiseModel
from random import shuffle

_IBMQ_ACCOUNT_LOADED = False

def get_scores(game_str, num_players, simulate=True, noisy=False):
    """
    Get the scores for the game by running the corresponding quantum circuit
    either on the simulator (with or without noise) or in the quantum computer.

    Args:
        game_str: string representing the game
        num_players: number of players in the range [1-5]
        simulate: True (default) uses the simulator, False uses the quantum computer
        noisy: if True, use the noisy simulation (default to False)

    Returns:
        A list of the counts of ones (i.e. winnings) for each player.
    """

    score = [0]*5
    #Check whether it's valid game
    if not game_str or not is_valid_game(game_str, num_players):
        return score

    #Initialisation
    q = QuantumRegister(num_players)
    c = ClassicalRegister(num_players)
    qc = QuantumCircuit(q, c)

    #Shuffle players' qubits
    qbts = [i for i in range(0, num_players)]
    shuffle(qbts)
    pq = {}
    for p in range(0, num_players):
        pq[p] = qbts[p]

    #Parse game string and construct quantum circuit
    i = 0
    while i < len(game_str):
        g = game_str[i].upper()
        if g == "H":
            p = pq[int(game_str[i+1])-1]
            qc.h(q[p])
            i += 2
        elif g == "I":
            p = pq[int(game_str[i+1])-1]
            qc.id(q[p])
            i += 2
        elif g == "X":
            p = pq[int(game_str[i+1])-1]
            qc.x(q[p])
            i += 2
        elif g == "Y":
            p = pq[int(game_str[i+1])-1]
            qc.y(q[p])
            i += 2
        elif g == "Z":
            p = pq[int(game_str[i+1])-1]
            qc.z(q[p])
            i += 2
        elif g == "C":
            p1 = pq[int(game_str[i+1])-1]
            p2 = pq[int(game_str[i+2])-1]
            qc.cx(q[p1], q[p2])
            i += 3
        elif g == "S":
            p1 = pq[int(game_str[i+1])-1]
            p2 = pq[int(game_str[i+2])-1]
            qc.swap(q[p1], q[p2])
            i += 3
        else:
            print("Error",g)

    #Measurement
    qc.measure(q, c)
    if simulate:
        if noisy:
            device = get_ibmq_device()
            noise_model = noise.device.basic_device_noise_model(device.properties())
            backend = Aer.get_backend('qasm_simulator')
            job_sim = execute(qc, backend, noise_model=noise_model)
        else:
            backend = Aer.get_backend('qasm_simulator')
            job_sim = execute(qc, backend, noise_model=None)
    else:
            backend = get_ibmq_device()
            job_sim = execute(qc, backend)

    sim_result = job_sim.result()
    counts = sim_result.get_counts(qc)

    #Compute players' scores
    score = [0]*5
    for result in counts:
        c = counts[result]
        for p in range(0, num_players):
            if result[num_players-1-pq[p]] == "1":
                score[p] += c

    return score

def is_valid_game(game_str, num_players):
    """ Check whether game_str represents a valid game

    Args:
        game_str: the string representing the game
        num_players: the number of players (between 1 and 5)

    Returns:
        True if the game is valid or False otherwise
    """


    gates = {"H": 1, "I": 1, "X": 1, "Y": 1, "Z": 1, "C": 2, "S": 2}
    valid = True
    i = 0
    while i < len(game_str):
        g = game_str[i].upper()
        if g not in gates:
            valid = False
            break
        else:
            if i + gates[g] >= len(game_str):
                valid = False
                break
            for j in range(0, gates[g]):
                n = game_str[i+j+1]
                if ord(n) not in range(ord("1"), ord("1")+num_players):
                    valid = False
                    break
            if gates[g] > 1 and game_str[i+1] == game_str[i+2]:
                valid = False
                break
        i += gates[g] + 1

    return valid

def get_ibmq_device():
    global _IBMQ_ACCOUNT_LOADED
    """ Get the IBMQ device for noise model or running the game"""
    #Load IBMQ credentials
    if not _IBMQ_ACCOUNT_LOADED:
        IBMQ.load_account()
        _IBMQ_ACCOUNT_LOADED = True
    provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
    device = provider.get_backend('ibmqx2')
    return device