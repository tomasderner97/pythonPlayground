def d_hondt(votes, seats, quorum, absolute_quorum=False, verbose=False, modified=False):
    """
    Calculates the seat distribution between parties with D'Hondt method.

    Parameters
    ----------
    votes : dictionary
        Dictionary of parties and their votes gained, in format {"party": vote_number}
    seats : int
        Number of seats to be allocated
    quorum : float
        Percentage of all votes a party needs to be part of distribution process
        if absolute_quorum, this is treated as absolute count of votes needed

    Returns
    -------
    allocated_seats : dictionary
        Dictionary of parties with number of seats they gained
    """

    if modified:
        raise NotImplementedError()

    sum_of_votes = sum(votes.values())
    if absolute_quorum:
        min_votes_for_quorum = quorum
    else:
        min_votes_for_quorum = int(sum_of_votes * quorum / 100)
    votes_after_quorum = {k: v for k, v in votes.items() if v > min_votes_for_quorum}

    allocated_seats = {party: 0 for party in votes.keys()}

    for seat in range(seats):
        score = {k: votes_after_quorum[k] / (allocated_seats[k] + 1)
                 for k in votes_after_quorum.keys()}
        round_winner = max(score.keys(),
                           key=lambda k: score[k])
        allocated_seats[round_winner] += 1

    return allocated_seats
