import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Define a few auxiliary functions
    def prob_no_parents(person, num_genes, has_trait):
        # This is the simplest cases for persons w/o parent information
        gene_cnt = num_genes[person]
        return PROBS["gene"][gene_cnt] * PROBS["trait"][gene_cnt][has_trait]

    def prob_has_parents(person, people, num_genes, has_trait):
        mother_genes = num_genes[people[person]["mother"]]
        father_genes = num_genes[people[person]["father"]]

        prob_mother_pass = mother_genes / 2
        prob_father_pass = father_genes / 2

        prob_mother_pass_nomutate = prob_mother_pass * (1 - PROBS["mutation"])
        prob_mother_pass_mutate = prob_mother_pass * PROBS["mutation"]
        prob_mother_nopass_nomutate = (1 - prob_mother_pass) * (1 - PROBS["mutation"])
        prob_mother_nopass_mutate = (1 - prob_mother_pass) * PROBS["mutation"]

        prob_father_pass_nomutate = prob_father_pass * (1 - PROBS["mutation"])
        prob_father_pass_mutate = prob_father_pass * PROBS["mutation"]
        prob_father_nopass_nomutate = (1 - prob_father_pass) * (1 - PROBS["mutation"])
        prob_father_nopass_mutate = (1 - prob_father_pass) * PROBS["mutation"]

        child_genes = num_genes[person]
        if child_genes == 0:
            # Child has zero genes - 4 cases:
            #     #  Mother (pass/mutation) | Father (pass/mutation)
            #     ==================================================
            #     1.         Y/Y            |         Y/Y
            #     2.         Y/Y            |         N/N
            #     3.         N/N            |         Y/Y
            #     4.         N/N            |         N/N
            prob = prob_mother_pass_mutate * prob_father_pass_mutate + \
                prob_mother_pass_mutate * prob_father_nopass_nomutate + \
                prob_mother_nopass_nomutate * prob_father_pass_mutate + \
                prob_mother_nopass_nomutate * prob_father_nopass_nomutate
        elif child_genes == 1:
            # Child has one genes - 8 cases:
            #     #  Source | Mother (pass/mutation) | Father (pass/mutation)
            #     ===========================================================
            #     1. Mother |         Y/N            |         Y/Y
            #     2. Mother |         Y/N            |         N/N
            #     3. Mother |         N/Y            |         Y/Y
            #     4. Mother |         N/Y            |         N/N
            #     5. Father |         Y/Y            |         Y/N
            #     6. Father |         N/N            |         Y/N
            #     7. Father |         Y/Y            |         N/Y
            #     8. Father |         N/N            |         N/Y
            prob = prob_mother_pass_nomutate * prob_father_pass_mutate + \
                prob_mother_pass_nomutate * prob_father_nopass_nomutate + \
                prob_mother_nopass_mutate * prob_father_pass_mutate + \
                prob_mother_nopass_mutate * prob_father_nopass_nomutate + \
                prob_mother_pass_mutate * prob_father_pass_nomutate + \
                prob_mother_nopass_nomutate * prob_father_pass_nomutate + \
                prob_mother_pass_mutate * prob_father_nopass_mutate + \
                prob_mother_nopass_nomutate * prob_father_nopass_mutate
        else:
            # Child has two genes - 4 cases:
            #     #  Mother (pass/mutation) | Father (pass/mutation)
            #     ==================================================
            #     1.         Y/N            |         Y/N
            #     2.         Y/N            |         N/Y
            #     3.         N/Y            |         Y/N
            #     4.         N/Y            |         N/Y
            prob = prob_mother_pass_nomutate * prob_father_pass_nomutate + \
                prob_mother_pass_nomutate * prob_father_nopass_mutate + \
                prob_mother_nopass_mutate * prob_father_pass_nomutate + \
                prob_mother_nopass_mutate * prob_father_nopass_mutate

        return prob * PROBS["trait"][child_genes][has_trait]

    num_genes = {}  # Dictionary with person mapping to number of genes
    for person in people:
        if person in one_gene:
            num_genes[person] = 1
        elif person in two_genes:
            num_genes[person] = 2
        else:
            num_genes[person] = 0

    joint_prob = 1
    for person in people:
        if person in have_trait:
            has_trait = True
        else:
            has_trait = False

        if people[person]["mother"] == None:  # No parents case
            joint_prob *= prob_no_parents(person, num_genes, has_trait)
        else:  # Known parent case
            joint_prob *= prob_has_parents(person, people, num_genes, has_trait)

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_factor = 1.0/sum(probabilities[person]['gene'].values())
        trait_factor = 1.0 / sum(probabilities[person]['trait'].values())
        for g in probabilities[person]['gene']:
            probabilities[person]['gene'][g] *= gene_factor
        for t in probabilities[person]['trait']:
            probabilities[person]['trait'][t] *= trait_factor


if __name__ == "__main__":
    main()
