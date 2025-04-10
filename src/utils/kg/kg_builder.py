import networkx as nx # type: ignore

from src.utils.logging.logging import setup_logger
logger = setup_logger()


def build_baseball_kg():
    G = nx.DiGraph()

    triples = [
        ("Shortstop", "covers", "Second Base"),
        ("Runner on 1st", "isPartOf", "GameState_2outs_Runner1"),
        ("2 Outs", "isPartOf", "GameState_2outs_Runner1"),
        ("GameState_2outs_Runner1", "triggers", "Grounder to SS"),
        ("Grounder to SS", "suggests", "Throw to 2nd"),
        ("Throw to 2nd", "requiresUnderstandingOf", "Force Out"),
        ("Force Out", "requires", "Runner behind Batter"),
        ("Throw to 2nd", "leadsTo", "Out at 2nd"),
        ("Shortstop", "hasResponsibilityIn", "GameState_2outs_Runner1"),
    ]

    # Runner on 2nd, 1 out, grounder to 3B
    triples += [
        ("Third Base", "hasResponsibilityIn", "GameState_1out_Runner2"),
        ("Runner on 2nd", "isPartOf", "GameState_1out_Runner2"),
        ("1 Out", "isPartOf", "GameState_1out_Runner2"),
        ("GameState_1out_Runner2", "triggers", "Grounder to 3B"),
        ("Grounder to 3B", "suggests", "Throw to 1st"),
        ("Throw to 1st", "leadsTo", "Out at 1st"),
        ("Throw to 3rd", "requiresUnderstandingOf", "Runner Speed Judgment"),
        ("Throw to 3rd", "leadsTo", "Risky Out at 3rd"),
    ]

    # Runner on 1st and 2nd, 0 outs, grounder to SS
    triples += [
        ("Shortstop", "hasResponsibilityIn", "GameState_0outs_Runners12"),
        ("Second Baseman", "hasResponsibilityIn", "GameState_0outs_Runners12"),
        ("Runners on 1st and 2nd", "isPartOf", "GameState_0outs_Runners12"),
        ("0 Outs", "isPartOf", "GameState_0outs_Runners12"),
        ("GameState_0outs_Runners12", "triggers", "Grounder to SS"),
        ("Grounder to SS", "suggests", "Throw to 2nd"),
        ("Throw to 2nd", "leadsTo", "Out at 2nd"),
        ("Throw to 1st", "leadsTo", "Double Play"),
        ("Double Play", "requires", "Clean Fielding"),
        ("Double Play", "requiresUnderstandingOf", "Force Out at Multiple Bases"),
    ]

    # Runner on 3rd, 2 outs, grounder to 1B
    triples += [
        ("First Baseman", "hasResponsibilityIn", "GameState_2outs_Runner3"),
        ("Runner on 3rd", "isPartOf", "GameState_2outs_Runner3"),
        ("2 Outs", "isPartOf", "GameState_2outs_Runner3"),
        ("GameState_2outs_Runner3", "triggers", "Grounder to 1B"),
        ("Grounder to 1B", "suggests", "Step on 1st"),
        ("Step on 1st", "leadsTo", "End of Inning"),
        ("Throw Home", "isNotRecommended", "GameState_2outs_Runner3"),
        ("Throw Home", "failsToResultIn", "Force Out"),
    ]
    
    logger.info("Building baseball knowledge graph with triples")
    logger.info(f"Total triples in the graph: {len(triples)}")

    for subj, pred, obj in triples:
        G.add_edge(subj, obj, predicate=pred)

    logger.info("Baseball knowledge graph built successfully")
    
    return G
